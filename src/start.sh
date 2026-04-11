#! /bin/bash
uvicorn --factory main.run:web_app --host 0.0.0.0 --port 8080 --log-level error --proxy-headers
