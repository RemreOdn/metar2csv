# Python bazlı Docker imajı
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli dosyaları kopyala
COPY . .

# Gerekli kütüphaneleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Ana komut
CMD ["python", "metar_parser.py"]
