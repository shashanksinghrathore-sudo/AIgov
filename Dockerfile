FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 AIGOV_DB=/data/aigov.db PORT=8080
WORKDIR /app
COPY pyproject.toml README.md ./
COPY aigov ./aigov
COPY examples ./examples
RUN pip install --no-cache-dir ".[docs]" && mkdir -p /data
VOLUME /data
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import os,urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ[\"PORT\"]}/health')"
# The server refuses to start without AIGOV_API_TOKEN (set it on the host).
CMD ["sh", "-c", "aigov serve --host 0.0.0.0 --port ${PORT}"]
