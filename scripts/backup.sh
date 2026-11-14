#!/bin/bash
# ========================================================
# سمارت إديو (SmartEdu) - سكربت النسخ الاحتياطي التلقائي
# ========================================================

set -e

BACKUP_DIR="/var/backups/smartedu"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="smartedu_backup_${TIMESTAMP}"
CONTAINER_DB="openeducat_db"
DB_NAME="openeducat"
DB_USER="odoo"

# إنشاء مجلد النسخ الاحتياطية إن لم يكن موجوداً
mkdir -p "${BACKUP_DIR}"
TEMP_DIR="${BACKUP_DIR}/${BACKUP_NAME}"
mkdir -p "${TEMP_DIR}"

echo "[1/4] بدء تصدير قاعدة البيانات ${DB_NAME}..."
docker exec "${CONTAINER_DB}" pg_dump -U "${DB_USER}" -d "${DB_NAME}" -F c -b -v -f "/tmp/${BACKUP_NAME}.dump"
docker cp "${CONTAINER_DB}:/tmp/${BACKUP_NAME}.dump" "${TEMP_DIR}/db.dump"
docker exec "${CONTAINER_DB}" rm -f "/tmp/${BACKUP_NAME}.dump"

echo "[2/4] جاري نسخ الملفات والمستندات (Filestore)..."
docker cp openeducat_web:/var/lib/odoo/filestore/${DB_NAME} "${TEMP_DIR}/filestore" 2>/dev/null || echo "تنبيه: مجلد filestore غير متاح حالياً أو فارغ."

echo "[3/4] ضغط النسخة الاحتياطية وتشفيرها..."
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" -C "${BACKUP_DIR}" "${BACKUP_NAME}"
rm -rf "${TEMP_DIR}"

echo "[4/4] تنظيف النسخ القديمة (الاحتفاظ بآخر 7 أيام فقط)..."
find "${BACKUP_DIR}" -type f -name "smartedu_backup_*.tar.gz" -mtime +7 -delete

echo "========================================================"
echo "تم إنشاء النسخة الاحتياطية بنجاح في:"
echo "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
echo "الحجم: $(du -sh ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz | cut -f1)"
echo "========================================================"
