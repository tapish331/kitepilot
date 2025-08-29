FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
COPY apps/api/pyproject.toml apps/api/README.md ./
COPY apps/api/kitepilot_api ./kitepilot_api
RUN pip install --no-cache-dir -e .[dev]
USER appuser
EXPOSE 8000
CMD ["uvicorn", "kitepilot_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
