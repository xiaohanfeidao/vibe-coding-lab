from __future__ import annotations

import os
from pathlib import Path

import pytest

from app.config.loader import deep_merge, load_config, _resolve_env_vars


CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def test_load_config_base():
    config = load_config()
    assert config["app"]["name"] == "tech-blazing-core-scaffold"
    assert config["app"]["version"] == "0.1.0"
    assert config["app"]["debug"] is False


def test_load_config_with_profile():
    config = load_config(profile="dev")
    assert config["app"]["debug"] is True
    assert config["logging"]["level"] == "DEBUG"
    assert config["logging"]["format"] == "text"


def test_load_config_server_settings():
    config = load_config()
    assert config["server"]["host"] == "0.0.0.0"
    assert config["server"]["port"] == 8000
    assert config["server"]["workers"] == 4


def test_load_config_auth_settings():
    config = load_config()
    assert config["auth"]["algorithm"] == "HS256"
    assert config["auth"]["access_token_expire_minutes"] == 30


def test_load_config_cors_settings():
    config = load_config()
    assert "http://localhost:5173" in config["cors"]["origins"]


def test_load_config_menus():
    config = load_config()
    assert "web" in config["menus"]
    assert "admin" in config["menus"]
    assert len(config["menus"]["web"]) > 0
    assert len(config["menus"]["admin"]) > 0


def test_deep_merge():
    base = {"a": 1, "b": {"c": 2, "d": 3}}
    override = {"b": {"c": 99, "e": 5}, "f": 6}
    result = deep_merge(base, override)
    assert result == {"a": 1, "b": {"c": 99, "d": 3, "e": 5}, "f": 6}


def test_resolve_env_vars_with_default():
    result = _resolve_env_vars("${NONEXISTENT_VAR:default_value}")
    assert result == "default_value"


def test_resolve_env_vars_from_env():
    os.environ["TEST_CONFIG_VAR"] = "from_env"
    try:
        result = _resolve_env_vars("${TEST_CONFIG_VAR:fallback}")
        assert result == "from_env"
    finally:
        del os.environ["TEST_CONFIG_VAR"]


def test_resolve_env_vars_in_config():
    os.environ["AUTH_SECRET_KEY"] = "my-secret"
    try:
        config = load_config()
        assert config["auth"]["secret_key"] == "my-secret"
    finally:
        del os.environ["AUTH_SECRET_KEY"]
