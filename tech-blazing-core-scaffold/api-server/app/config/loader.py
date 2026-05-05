from __future__ import annotations

import os
import re
from pathlib import Path

import yaml


def deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


_ENV_VAR_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^}]*))?\}")


def _resolve_env_vars(value: str) -> str:
    def _replace(match: re.Match) -> str:
        env_var = match.group(1)
        default = match.group(2)
        return os.environ.get(env_var, default if default is not None else match.group(0))

    return _ENV_VAR_PATTERN.sub(_replace, value)


def _resolve_dict(d: dict) -> dict:
    result = {}
    for key, value in d.items():
        if isinstance(value, dict):
            result[key] = _resolve_dict(value)
        elif isinstance(value, list):
            result[key] = _resolve_list(value)
        elif isinstance(value, str):
            result[key] = _resolve_env_vars(value)
        else:
            result[key] = value
    return result


def _resolve_list(lst: list) -> list:
    result = []
    for item in lst:
        if isinstance(item, dict):
            result.append(_resolve_dict(item))
        elif isinstance(item, list):
            result.append(_resolve_list(item))
        elif isinstance(item, str):
            result.append(_resolve_env_vars(item))
        else:
            result.append(item)
    return result


def load_config(profile: str | None = None) -> dict:
    config_dir = Path(__file__).resolve().parent.parent.parent / "config"
    base_path = config_dir / "application.yml"
    if not base_path.exists():
        raise FileNotFoundError(f"Config file not found: {base_path}")

    base = yaml.safe_load(base_path.read_text(encoding="utf-8"))

    if profile:
        override_path = config_dir / f"application-{profile}.yml"
        if override_path.exists():
            override = yaml.safe_load(override_path.read_text(encoding="utf-8"))
            if override:
                base = deep_merge(base, override)

    return _resolve_dict(base)
