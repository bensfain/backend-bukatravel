# Gunakan image resmi Python
FROM python:3.10

# Set working directory
WORKDIR /app

# Salin file proyek
COPY . /app/

# Install dependensi
# RUN pip install --upgrade pip
RUN pip install --no-cache-dir --no-binary django-suit -r requirements.txt

# Jalankan Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
