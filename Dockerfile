FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set working directory
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \ 
    # Try connecting to host db on port 3306. If it fails, try again every second.
 && rm -rf /var/lib/apt/lists/*


# Install Python dependencies



COPY requirements.txt /app/


# 1️⃣ Cập nhật pip mới nhất.
# 2️⃣ Cài toàn bộ thư viện mà Django project cần.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
