import csv
import re

def extract_metar_data(metar):
    # Regex ile istenen alanları çıkar
    metar_pattern = re.compile(
        r"(?P<report_time>\d{12})\s"  # Rapor zamanı (YYYYMMDDHHMM)
        r"(METAR|SPECI)(?:\sCOR)?"  # METAR veya SPECI, opsiyonel COR
        r"\s(?P<station>[A-Z]{4})\s"  # İstasyon kodu
        r"(?P<datetime>\d{6}Z)\s"  # Gözlem zamanı (UTC)
        r"(?:.*?\s)?"  # Arada kalan her şey
        r"(?P<weather>[-+A-Z]{2,6})?\s?"  # Hava durumu
        r"(?P<clouds>(?:FEW|SCT|BKN|OVC|NSC|CLR|VV)[0-9]{3}.*)?\s"  # Bulut durumu
        r"(?P<temperature>-?\d{2}/-?\d{2})\s"  # Sıcaklık ve çiy noktası
        r"Q(?P<pressure>\d{4})"  # Barometrik basınç
    )

    match = metar_pattern.match(metar)
    if match:
        data = match.groupdict()

        # Rapor zamanı tarih ve saat olarak ayır
        data["report_date"] = data["report_time"][:8]  # YYYYMMDD
        data["report_hour"] = data["report_time"][8:]  # HHMM
        del data["report_time"]  # Artık bu anahtar kullanılmayacak

        return {
            "Rapor Tarihi (YYYYMMDD)": data["report_date"],
            "Rapor Saati (HHMM)": data["report_hour"],
            "İstasyon Kodu": data["station"],
            "Gözlem Zamanı (UTC)": data["datetime"],
            "Hava Durumu": data.get("weather", ""),
            "Bulut Durumu": data.get("clouds", ""),
            "Sıcaklık ve Çiy Noktası (°C)": data["temperature"],
            "Barometrik Basınç (hPa)": data["pressure"]
        }
    else:
        raise ValueError(f"Geçersiz METAR formatı: {metar}")

def save_to_csv(data, filename="metar_data.csv"):
    # Açıklayıcı kolon başlıkları
    columns = [
        "Rapor Tarihi (YYYYMMDD)",
        "Rapor Saati (HHMM)",
        "İstasyon Kodu",
        "Gözlem Zamanı (UTC)",
        "Hava Durumu",
        "Bulut Durumu",
        "Sıcaklık ve Çiy Noktası (°C)",
        "Barometrik Basınç (hPa)"
    ]

    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    input_file = "metar_reports.txt"  # METAR raporlarının bulunduğu dosya
    extracted_data = []

    try:
        with open(input_file, "r") as file:
            metar_reports = file.readlines()

        for report in metar_reports:
            try:
                extracted_data.append(extract_metar_data(report.strip()))
            except ValueError as e:
                print(f"Hata: {e}")

        # CSV dosyasına kaydet
        save_to_csv(extracted_data)
        print("METAR verileri metar_data.csv dosyasına kaydedildi.")
    except FileNotFoundError:
        print(f"Hata: '{input_file}' dosyası bulunamadı!")
