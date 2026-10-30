"""skrub DataOps for point-in-time features, censored labels and backtesting.

Two DataOps mirror how a payment platform is organised:

1. ``feature_store_dataop`` turns the raw public event log into point-in-time
   features. It runs on the *whole* log, like a streaming feature store: the
   features of a payment at ``t`` only depend on events before ``t`` and on
   labels that have arrived before ``t``, so they can be computed once.
   Running it inside each cross-validation split instead would wrongly erase
   the history that precedes the test window.
2. ``learner_dataop`` derives the training label *as known at the retraining
   cutoff* (a skrub variable), vectorises the features with skrub, and fits a
   ``HistGradientBoostingClassifier``. ``backtest`` evaluates it with
   ``skrub.cross_validate`` on calendar folds.

The target passed to the learner is a small dataframe: the model is fitted on
its ``y_train`` column, while scorers read the private ``is_fraud`` column of
the test rows. This is only possible because the data is simulated.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import skrub
from skrub import selectors as s
from sklearn.ensemble import HistGradientBoostingClassifier

from .backtest import BacktestConfig, fold_cutoffs, label_as_known_at
from .features import add_feedback_features, add_window_features

ROW_FEATURES = [
    "timestamp",
    "merchant_id",
    "merchant_category",
    "amount_eur",
    "device_age_days",
    "account_age_days",
    "ip_mismatch",
    "ip_non_eu",
    "legacy_score",
]
WINDOW_FEATURES = [
    "cust_n_1h",
    "cust_n_24h",
    "cust_amount_24h",
    "amount_to_cust_mean_30d",
    "cust_declined_24h",
    "cust_seconds_since_prev",
    "device_n_24h",
    "device_n_7d",
    "merchant_n_1h",
    "merchant_burst",
]
KNOWN_LABEL_FEATURES = ["known_merchant_fraud_rate_30d", "known_card_fraud_7d", "known_device_fraud_90d"]
LEAKY_LABEL_FEATURES = [c.replace("known_", "leaky_") for c in KNOWN_LABEL_FEATURES]

FEATURE_SETS = {
    "row": ROW_FEATURES,
    "row+window": ROW_FEATURES + WINDOW_FEATURES,
    "row+window+labels": ROW_FEATURES + WINDOW_FEATURES + KNOWN_LABEL_FEATURES,
    "row+window+leaky_labels": ROW_FEATURES + WINDOW_FEATURES + LEAKY_LABEL_FEATURES,
}
TARGET_COLUMNS = ["y_train", "is_fraud", "fraud_type", "amount_eur", "decision", *KNOWN_LABEL_FEATURES]


def feature_store_dataop() -> skrub.DataOp:
    log = skrub.var("log")
    return log.skb.apply_func(add_window_features).skb.apply_func(add_feedback_features)


def _targets(store: pd.DataFrame, cutoff: pd.Timestamp, labels: str, maturity_days: int) -> pd.DataFrame:
    if labels == "censored":
        y_train = label_as_known_at(store, cutoff, maturity_days)
    elif labels == "oracle":
        y_train = store["is_fraud"].astype(float).where(store["timestamp"] < cutoff)
    else:
        raise ValueError(labels)
    # Label-aggregate columns are optional: the scale run does not need them,
    # and scorers address every column by name.
    columns = [column for column in TARGET_COLUMNS[1:] if column in store.columns]
    return store[columns].assign(y_train=y_train)[["y_train", *columns]]


def learner_dataop(feature_set: str, labels: str, maturity_days: int = 45,
                   cardinality_threshold: int = 64, max_iter: int = 200) -> skrub.DataOp:
    store = skrub.var("feature_store")
    cutoff = skrub.var("cutoff")
    X = store[FEATURE_SETS[feature_set]].skb.mark_as_X()
    y = store.skb.apply_func(_targets, cutoff, labels, maturity_days).skb.mark_as_y()
    vectorizer = skrub.TableVectorizer(
        cardinality_threshold=cardinality_threshold,
        low_cardinality=skrub.ToCategorical(),
        datetime=skrub.DatetimeEncoder(resolution="hour", add_weekday=True, add_total_seconds=False,
                                       periodic_encoding="circular"),
    )
    # Six months of history: year, month and day-of-month would only let the
    # trees memorise the period. Time of day and day of week do generalise.
    calendar_drift = s.glob("timestamp_year") | s.glob("timestamp_month_*") | s.glob("timestamp_day_*")
    features = X.skb.apply(vectorizer).skb.apply(skrub.DropCols(calendar_drift))
    model = HistGradientBoostingClassifier(
        learning_rate=0.1, max_iter=max_iter, max_leaf_nodes=31, l2_regularization=1.0,
        categorical_features="from_dtype", early_stopping=True, random_state=0,
    )
    return features.skb.apply(model, y=y["y_train"])


def fold_splits(store: pd.DataFrame, cutoff: pd.Timestamp, test_days: int, y_train: pd.Series):
    test = (store["timestamp"] >= cutoff) & (store["timestamp"] < cutoff + pd.Timedelta(days=test_days))
    return [(np.flatnonzero(y_train.notna().to_numpy()), np.flatnonzero(test.to_numpy()))]


def backtest(store: pd.DataFrame, feature_set: str, labels: str, scoring: dict,
             cfg: BacktestConfig = BacktestConfig(), return_predictions: bool = False,
             cardinality_threshold: int = 64, max_iter: int = 200):
    """One ``skrub.cross_validate`` call per retraining cutoff.

    The label known at a cutoff depends on the cutoff itself (chargebacks keep
    arriving), so the target is re-derived for every fold through the
    ``cutoff`` variable instead of being fixed once for all folds.

    With ``return_predictions``, also return the test rows of every fold with
    the fitted learner's fraud probability in a ``p_fraud`` column.
    """
    learner = learner_dataop(
        feature_set, labels, cfg.maturity_days, cardinality_threshold, max_iter
    ).skb.make_learner()
    results, predictions = [], []
    for fold, cutoff in enumerate(fold_cutoffs(store, cfg)):
        y_train = _targets(store, cutoff, labels, cfg.maturity_days)["y_train"]
        env = {"feature_store": store, "cutoff": cutoff}
        cv = fold_splits(store, cutoff, cfg.test_days, y_train)
        scores = skrub.cross_validate(learner, env, cv=cv, scoring=scoring, return_learner=return_predictions)
        if return_predictions:
            test = store.iloc[cv[0][1]].reset_index(drop=True)
            fitted = scores.pop("learner").iloc[0]
            p = fitted.predict_proba({"feature_store": test, "cutoff": cutoff})[:, 1]
            predictions.append(test.assign(p_fraud=p, fold=fold))
        scores = scores.drop(columns=["fit_time", "score_time"]).rename(columns=lambda c: c.removeprefix("test_"))
        results.append(scores.assign(fold=fold, cutoff=cutoff, n_train=len(cv[0][0]),
                                     train_fraud_rate=y_train.mean()))
    results = pd.concat(results, ignore_index=True).assign(feature_set=feature_set, labels=labels)
    if return_predictions:
        return results, pd.concat(predictions, ignore_index=True)
    return results
