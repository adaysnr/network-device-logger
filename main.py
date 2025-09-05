#!/usr/bin/env python3

"""
Created May 2025
"""

import os
import subprocess
import re
from datetime import datetime
import logging

# Dosya dizin yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "log_devices.txt")
KNOWN_FILE = os.path.join(BASE_DIR, "known_devices.txt")

# Terminalde "which arp-scan" komutuyla dizini bulup, buraya yaz
ARP_SCAN = ""

logging.basicConfig(
	filename=LOG_FILE,
	level=logging.INFO,
	format='%(message)s'
)

# Ağı tara ve bağlı cihazları tespit et
def scan_network():
	try:
		result = subprocess.run([ARP_SCAN, "-l"], capture_output=True, text=True)
		output = result.stdout

		if result.returncode != 0:
			print("Hata oluştu:", result.stderr)
			return ""

		return output

	except FileNotFoundError:
		print("İlgili araç bulunamadı!")
	except Exception as e:
		print("Bir hata oluştu:", e)

# Bilinen cihazları farklı dosyaya kaydet
def known_devices():
	known = set()

	if os.path.exists(KNOWN_FILE):
		with open(KNOWN_FILE, "r") as f:
			for line in f:
				if line.startswith("IP:") and "MAC:" in line:
					parts = line.strip().split("|")
					if len(parts) >= 2:
						mac = parts[1].strip().replace("MAC: ", "").lower()
						known.add(mac)
	
	return known


def check_new_devices(output):
	pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f:]{17})\s+(.*)"
	matches = re.findall(pattern, output)

	known = set()

	if os.path.exists(KNOWN_FILE):
		with open(KNOWN_FILE, "r") as f:
			for line in f:
				parts = line.strip().split("|")
				if len(parts) >= 2:
					mac = parts[1].strip().replace("MAC: ", "").lower()
					known.add(mac)
	
	new_lines = []
	log_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	logging.info(f"--Zaman: {log_time} --\n")

	for ip, mac, name in matches:
		mac = mac.lower()
		is_new = False

		if mac not in known:
			is_new = True
			known.add(mac)
			new_line = f"IP: {ip} | MAC: {mac} | {name}\n"
			new_lines.append(new_line)

		mark = " XX Yeni Cihaz! XX" if is_new else ""
		logging.info(f"IP: {ip} | MAC: {mac} | {name}{mark}")
	
	logging.info("\n-------------------------\n")

	if new_lines:
		with open(KNOWN_FILE, "a") as known_file:
			known_file.write(f"\n-------------------------\n")
			known_file.write(f"\n-- Son güncelleme: {log_time} --\n\n")
			known_file.writelines(new_lines)

	return known


if __name__ == "__main__":
	print("""
Network Scanner

*** *** *** ***
  *** *** ***
    *** ***
      ***
       *
""")
	print("Ağ taraması başlatılıyor!..\n")
	output = scan_network()

	if output:
		known_macs = check_new_devices(output)
		scan_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		print(f"""Tarama Zamanı: {scan_time}
Tarama sonuçları log_devices.txt dosyasına kaydedildi.
Bilinen cihazları known_devices.txt dosyasından kontrol ediniz.
""")
	else:
		print("Ağ taramasında sonuç alınamadı.")

	print("Ağ taraması başarıyla tamamlandı!")
