# دليل النشر والتشغيل الميداني الرسمي لنظام سمارت إديو (SmartEdu) 🚀

---

## 📋 المتطلبات الفنية للسيرفر (Server Prerequisites)

* **نظام التشغيل الموصى به**: Ubuntu Server 22.04 LTS أو 24.04 LTS.
* **المعالج (CPU)**: 4 نوى (Cores) أو أكثر لضمان سرعة المعالجة المتزامنة.
* **الذاكرة العشوائية (RAM)**: 8 جيجابايت كحد أدنى (16 جيجابايت موصى بها للمدارس الكبيرة).
* **التخزين (Storage)**: 60 جيجابايت SSD / NVMe على الأقل.
* **البرمجيات الأساسية**:
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y docker.io docker-compose-v2 curl git certbot
  sudo systemctl enable --now docker
  ```

---

## ⚡ خطوات النشر المباشر (1-Click Quick Deployment)

1. **نسخ المشروع إلى السيرفر**:
   ```bash
   cd /opt
   # انقل مجلد المشروع openeducat_erp-19.0 إلى هنا
   cd openeducat_erp-19.0
   ```

2. **ضبط كلمة سر المدير في ملف الإنتاج**:
   افتح ملف `odoo.prod.conf` وعدّل السطر التالي بكلمة مرور فائقة الصعوبة:
   ```ini
   admin_passwd = YourSuperSecretMasterPassword2026!
   ```

3. **تشغيل النظام فورياً بضغطة زر**:
   ```bash
   ./deploy.sh
   ```
   أو عبر الأمر المباشر:
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```

---

## 🔒 ربط النطاق وتفعيل شهادة الأمان (SSL / HTTPS)

1. وجّه سجل النطاق (`A Record`) الخاص بمدرستك إلى عنوان IP السيرفر (مثال: `school.smartedu.sa`).
2. استخرج شهادة مجانية معتمدة عبر Certbot:
   ```bash
   sudo certbot certonly --standalone -d school.smartedu.sa
   ```
3. انسخ الشهادات إلى مجلد Nginx:
   ```bash
   sudo cp /etc/letsencrypt/live/school.smartedu.sa/fullchain.pem nginx/ssl/cert.pem
   sudo cp /etc/letsencrypt/live/school.smartedu.sa/privkey.pem nginx/ssl/key.pem
   ```
4. أعد تشغيل Nginx لتفعيل الاتصال المشفر:
   ```bash
   docker compose -f docker-compose.prod.yml restart nginx
   ```

---

## 💾 جدول النسخ الاحتياطي التلقائي (Automated Backups)

تم تزويد النظام بسكربت ذكي يقوم بأخذ نسخة احتياطية يومية من قاعدة البيانات وملفات المرفقات ويحتفظ بآخر 7 أيام تلقائياً.

1. لجدولة النسخ اليومي الساعة 2:00 صباحاً عبر `crontab`:
   ```bash
   crontab -e
   ```
2. أضف السطر التالي:
   ```cron
   0 2 * * * /opt/openeducat_erp-19.0/scripts/backup.sh >> /var/log/smartedu_backup.log 2>&1
   ```

3. **طريقة استعادة أي نسخة احتياطية سابقة**:
   ```bash
   ./scripts/restore.sh /var/backups/smartedu/smartedu_backup_YYYYMMDD_HHMMSS.tar.gz
   ```

---

## 🛡️ إعدادات الحماية المطبقة في النظام افتراضياً

* **قفل واجهة مدراء القواعد (`list_db = False`)**: تم تعطيل صفحة إدارة وحذف قواعد البيانات عن زوار الموقع لمنع أي محاولات تلاعب أو تخمين كلمات السر.
* **تفعيل وضع المعالجة متعددة الأنوية (`workers = 4`)**: يدعم تصفح واستخدام مئات المستخدمين (إداريين، معلمين، أولياء أمور) في آن واحد بدون أي بطء.
* **دعم الويب سوكيت المستمر (`location /websocket`)**: منع انقطاع الاتصال الحي والإشعارات الفورية وشريط المهام.
* **الامتثال لمتطلبات الفاتورة الإلكترونية السعودية (ZATCA)**: دعم الباركود التشفيري، وضريبة القيمة المضافة 15%.

---
**نظام سمارت إديو (SmartEdu) • جاهز تماماً للتشغيل الميداني والتجاري المعتمد.**
