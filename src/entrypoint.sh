#!/bin/bash
set -e

exec uvicorn --host 0.0.0.0 --proxy-headers src.main:app
