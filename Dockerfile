FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade existing packages to resolve OS-level CVEs (e.g. CVE-2025-45582 in tar)
# and install required dependencies including Node.js for Tailwind CSS compilation
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY package*.json ./
RUN npm ci

COPY requirements.txt .

# Upgrade pip to latest version to resolve pip vulnerabilities (e.g. CVE-2025-8869, CVE-2026-6357, CVE-2026-3219)
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# Compile Tailwind CSS output.css
RUN npm run build

ENV PORT=2222
EXPOSE 2222

CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT} --workers 2 --threads 2 --timeout 60 --log-file -"]