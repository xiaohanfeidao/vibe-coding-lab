from __future__ import annotations

import logging
import multiprocessing
import os
import platform
import sys


def main() -> None:
    profile = os.environ.get("APP_PROFILE", "dev")
    host = os.environ.get("SERVER_HOST", "127.0.0.1" if profile == "dev" else "0.0.0.0")
    port = os.environ.get("SERVER_PORT", "8000")
    is_windows = platform.system() == "Windows"

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("Tech Blazing Core Scaffold - API Server")
    logger.info("=" * 60)
    logger.info("OS:         %s", platform.system())
    logger.info("Python:     %s", platform.python_version())
    logger.info("Profile:    %s", profile)
    logger.info("Host:       %s", host)
    logger.info("Port:       %s", port)

    if is_windows or profile == "dev":
        logger.info("Mode:       uvicorn (single process)")
        logger.info("Reload:     %s", "enabled" if profile == "dev" else "disabled")
        logger.info("=" * 60)

        import uvicorn

        uvicorn.run(
            "app.main:app",
            host=host,
            port=int(port),
            reload=(profile == "dev"),
            log_level="debug" if profile == "dev" else "info",
        )
    else:
        workers = int(os.environ.get("WORKERS", str(multiprocessing.cpu_count() * 2 + 1)))
        logger.info("Mode:       gunicorn (multi process)")
        logger.info("Workers:    %s", workers)
        logger.info("=" * 60)

        from gunicorn.app.base import BaseApplication

        class StandaloneApplication(BaseApplication):
            def __init__(self, application, options=None):
                self.options = options or {}
                self.application = application
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    if key in self.cfg.settings and value is not None:
                        self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        from app.main import app

        options = {
            "bind": f"{host}:{port}",
            "workers": workers,
            "worker_class": "uvicorn.workers.UvicornWorker",
            "max_requests": 5000,
            "max_requests_jitter": 500,
            "preload_app": True,
            "timeout": 120,
            "keepalive": 5,
        }

        StandaloneApplication(app, options).run()


if __name__ == "__main__":
    main()
