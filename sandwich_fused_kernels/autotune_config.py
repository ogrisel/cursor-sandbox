"""Autotune configuration cache and search-space helpers for sandwich kernels."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_CACHE_PATH = Path(__file__).resolve().parent / "artifacts" / "autotune_cache.json"


@dataclass(frozen=True)
class TuneParams:
    """Tile/chunk parameters for one kernel family."""

    block: int = 4
    n_chunks: int = 1
    jax_chunk: int = 4096
    xsimd_block: int = 4
    xsimd_chunk_factor: int = 4

    def to_dict(self) -> dict[str, int]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TuneParams:
        return cls(
            block=int(data.get("block", 4)),
            n_chunks=int(data.get("n_chunks", 1)),
            jax_chunk=int(data.get("jax_chunk", 4096)),
            xsimd_block=int(data.get("xsimd_block", 4)),
            xsimd_chunk_factor=int(data.get("xsimd_chunk_factor", 4)),
        )


@dataclass
class TuneResult:
    family: str
    problem: str
    threading: str
    num_threads: int
    params: TuneParams
    median_seconds: float
    vs_tabmat: float
    max_rel_error: float


@dataclass
class AutotuneCache:
    """Nested map: problem_key -> family -> TuneParams (as dict)."""

    entries: dict[str, dict[str, dict[str, int]]] = field(default_factory=dict)

    def problem_key(self, problem: str, threading: str, num_threads: int) -> str:
        return f"{problem}|{threading}|{num_threads}"

    def get(self, problem: str, threading: str, num_threads: int, family: str) -> TuneParams | None:
        key = self.problem_key(problem, threading, num_threads)
        raw = self.entries.get(key, {}).get(family)
        if raw is None:
            return None
        return TuneParams.from_dict(raw)

    def set(
        self,
        problem: str,
        threading: str,
        num_threads: int,
        family: str,
        params: TuneParams,
    ) -> None:
        key = self.problem_key(problem, threading, num_threads)
        self.entries.setdefault(key, {})[family] = params.to_dict()

    def save(self, path: Path = DEFAULT_CACHE_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.entries, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path = DEFAULT_CACHE_PATH) -> AutotuneCache:
        if not path.is_file():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(entries=data)


def block_candidates(n_cols: int) -> list[int]:
    vals = [4, 8, 16, 32, 64]
    return sorted({b for b in vals if b <= max(n_cols, 4)})


def chunk_count_candidates(n_rows: int, num_threads: int) -> list[int]:
    if num_threads <= 1:
        return [1]
    raw = {num_threads * m for m in (1, 2, 4, 8, 16, 32)}
    for div in (1, 2, 4, 8):
        if n_rows >= div:
            raw.add(max(div, min(n_rows // div, num_threads * 32)))
    raw.add(min(n_rows, num_threads))
    return sorted(k for k in raw if k >= 1)


def jax_chunk_candidates(n_rows: int, num_threads: int) -> list[int]:
    if num_threads <= 1:
        return [2048, 4096, 8192]
    target_chunks = chunk_count_candidates(n_rows, num_threads)
    rows_per_chunk = [max(256, (n_rows + nc - 1) // nc) for nc in target_chunks]
    explicit = [512, 1024, 2048, 4096, 8192, 16384]
    merged = sorted({r for r in rows_per_chunk + explicit if r <= n_rows})
    return merged or [4096]


def xsimd_block_candidates(n_cols: int) -> list[int]:
    return block_candidates(n_cols)


def xsimd_chunk_factor_candidates() -> list[int]:
    return [1, 2, 4, 8, 16, 32]
