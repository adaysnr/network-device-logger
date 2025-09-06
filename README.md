# Network Scanner
Bu script, yerel ağdaki cihazları `arp-scan` aracı ile tespit eder. Her tarama log dosyasına işlenir ve ilk taramada oluşturulan bilinen cihazlar listesi yeni cihaz bulunduğunda güncellenir.

Bu script, Linux tabanlı sistemler için hazırlanmıştır.

### Gereksinimler
- Python3 (Kurulu değilse terminalde `sudo apt update && sudo apt install python3 -y` komutunu çalıştırın)
- `arp-scan` aracı (Kurulum için terminalde `sudo apt update && sudo apt install arp-scan -y` komutunu çalıştırın)
- Linux dağıtımı (Kali Linux ve Ubuntu üzerinde test edildi)

### Dosyalar
- `log_devices.txt` → Tüm tarama geçmişi zaman damgasıyla burada tutulur.
- `known_devices.txt` → Bilinen cihazların listesi. Yeni cihazlar tespit edildiğin bu listeye eklenir.

### Kullanım
1. Repoyu indirip sisteminizde script'in çalıştırılabilir şekilde olduğundan emin olun.
2. Terminalde `which arp-scan` komutu ile `arp-scan` aracının dizinini bulun. Script'i açıp `ARP_SCAN = ""` satırını düzenleyip dizini ekleyin.
3. Terminalde script'in olduğu dizine girip `sudo python3 main.py` komutu ile script'i çalıştırın.

Örnek çıktı - `log_devicex.txt` dosyası:
```
--Zaman: 14-07-2025 15:45:12 --
IP: 192.168.1.10 | MAC: aa:bb:cc:dd:ee:ff | Samsung Electronics
IP: 192.168.1.11 | MAC: ff:ee:dd:cc:bb:aa | Intel Corp XX Yeni Cihaz! XX
```

### `cron` ile Otomatik Çalıştırma
Script'in her 5 dakikada bir çalışması için `cron` kullanabilirsiniz.

**Kullanım:**
1. Terminalde `crantab`'ı düzenlemek için `sudo crontab -e` komutunu çalıştırın. Editör seçmeniz için liste verecek → nano'yu tercih edebilirsiniz.
```
no crontab for root - using an empty one
Select an editor. To change later, run select-editor again.
  1. /bin/nano       <----- easiest
  2. /usr/bin/vim.basic
  3. /usr/bin/vim.tiny
  4. /usr/bin/code

Choose 1-4 [1]:
```
2. Açılan dosyada `*/5 * * * * /python-dizin-yolu /script_dizin_yolu` satırını ekleyin.
<br/>(Python dizin yolu için terminalde `which python3` komutunu çalıştırıp öğrenebilirsiniz.)
<br/>`Ctrl+O` ve ardından `Enter` tuşlayarak dosyayı kaydedin, `Ctrl+X` ile çıkış yapın.

Bu ayarlama ile her 5 dakikada bir script otomatik çalışacak ve `log_devices.txt` ile `known_devices.txt` dosyası güncellenecektir.

**Dikkat edilmesi gereken noktalar:**
1. `arp-scan` genellikle root yetkisi ister. `cron` normal kullanıcı olarak çalıştırıldığında `Permission denied` veya hiç çıktı vermeme durumu oluşabilir.
    - `cron` satırına `sudo` eklenebilir: `*/5 * * * * sudo /python-dizin-yolu /script_dizin_yolu`
    - `root` kullanıcısının `crontab`ına ekleme yapılabilir. Yani `crontab-e` yerine `sudo crontab -e` komutu çalıştırılır.

3. `cron` ortam değişkenleri çok kısıtlıdır. `arp-scan` veya `python3` bulunamazsa hata oluşur. Dizinlerin doğru olduğundan emin olunmalıdır.
4. Script dosyasının çalıştırılabilir olduğundan emin olun. Terminalde `chmod +x /script-dosya-yolu` komutu ile script'e çalıştırılma yetkisi verin.

---
2025
