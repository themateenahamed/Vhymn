# Use compatible Python version
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Run the app
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
