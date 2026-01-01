FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md ./
RUN pip install --no-cache-dir uv
RUN uv pip install --system .

COPY subscription_intelligence_mcp ./subscription_intelligence_mcp

ENV DATA_DIR=/data
VOLUME ["/data"]

CMD ["python", "subscription_intelligence_mcp/subscription_operator.py"]
