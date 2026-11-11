FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY aigov ./aigov
COPY examples ./examples
RUN pip install --no-cache-dir ".[docs]"
ENV AIGOV_DB=/data/aigov.db
VOLUME /data
EXPOSE 8080
CMD ["aigov", "serve", "--host", "0.0.0.0", "--port", "8080"]
