#!/bin/bash
# ========================================================
# سمارت إديو (SmartEdu) - سكربت استعادة النسخة الاحتياطية
# ========================================================

set -e

if [ -z "$1" ]; then
    echo "الاستخدام: $0 <مسار_ملف_النسخة_الاحتياطية.tar.gz>"
    echo "مثال: $0 /var/backups/smartedu/smartedu_backup_20261107_120000.tar.gz"
    exit 1
fi

ARCHIVE_PATH="$1"
if [ ! -f "$ARCHIVE_PATH" ]; then
    echo "خطأ: الملف غير موجود: $ARCHIVE_PATH"
    exit 1
fi

TEMP_RESTORE_DIR="/tmp/smartedu_restore_$$"
mkdir -p "$TEMP_RESTORE_DIR"

echo "[1/4] فك ضغط الأرشيف..."
tar -xzf "$ARCHIVE_PATH" -C "$TEMP_RESTORE_DIR"
BACKUP_FOLDER=$(ls "$TEMP_RESTORE_DIR")

echo "[2/4] استعادة قاعدة البيانات..."
docker exec openeducat_db dropdb -U odoo --if-exists openeducat
docker exec openeducat_db createdb -U odoo openeducat
docker cp "$TEMP_RESTORE_DIR/$BACKUP_FOLDER/db.dump" openeducat_db:/tmp/restore.dump
docker exec openeducat_db pg_restore -U odoo -d openeducat -v /tmp/restore.dump || true
docker exec openeducat_db rm -f /tmp/restore.dump

echo "[3/4] استعادة مجلد الملفات (Filestore)..."
if [ -d "$TEMP_RESTORE_DIR/$BACKUP_FOLDER/filestore" ]; then
    docker cp "$TEMP_RESTORE_DIR/$BACKUP_FOLDER/filestore" openeducat_web:/var/lib/odoo/filestore/openeducat
fi

echo "[4/4] تنظيف الملفات المؤقتة وإعادة تشغيل الخادم..."
rm -rf "$TEMP_RESTORE_DIR"
docker restart openeducat_web

echo "========================================================"
echo "تمت استعادة النظام بنجاح من: $ARCHIVE_PATH"
echo "========================================================"
