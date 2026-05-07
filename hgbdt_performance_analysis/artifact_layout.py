#!/usr/bin/env python3
import os
import platform
import re
from pathlib import Path


_OS_MAP = {
    "darwin": "macos",
    "linux": "linux",
    "windows": "windows",
}

_ARCH_MAP = {
    "x86_64": "amd64",
    "amd64": "amd64",
    "aarch64": "arm64",
    "arm64": "arm64",
    "armv8": "arm64",
}


def _sanitize_segment(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9._-]+", "-", value.strip().lower())
    cleaned = cleaned.strip("-._")
    return cleaned or "unknown"


def detect_machine_tag() -> str:
    os_name = _OS_MAP.get(platform.system().strip().lower(), platform.system().strip().lower())
    arch_name = _ARCH_MAP.get(platform.machine().strip().lower(), platform.machine().strip().lower())
    return f"{_sanitize_segment(os_name)}-{_sanitize_segment(arch_name)}"


def resolve_machine_tag(machine_tag: str | None = None) -> str:
    if machine_tag:
        return _sanitize_segment(machine_tag)
    env_tag = os.getenv("HGBDT_MACHINE_TAG")
    if env_tag:
        return _sanitize_segment(env_tag)
    return detect_machine_tag()


def machine_artifacts_dir(
    base_dir: Path,
    artifacts_root: str | Path | None = None,
    machine_tag: str | None = None,
) -> Path:
    root = Path(artifacts_root) if artifacts_root is not None else (base_dir / "artifacts")
    return root / "machines" / resolve_machine_tag(machine_tag)
