import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('SERVER_PORT', '8000')}"
workers = int(os.getenv("WORKERS", str(multiprocessing.cpu_count() * 2 + 1)))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 5000
max_requests_jitter = 500
preload_app = True
