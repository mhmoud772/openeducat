#!/bin/bash
# ========================================================
# سمارت إديو (SmartEdu) - سكربت النشر والتشغيل الميداني
# ========================================================

set -e

echo "========================================================"
echo "  مرحباً بك في معالج تشغيل سمارت إديو (SmartEdu Production)"
echo "========================================================"

# التحقق من تثبيت Docker و Docker Compose
if ! command -v docker &> /dev/null; then
    echo "خطأ: Docker غير مثبت. يرجى تثبيته أولاً."
    exit 1
fi

echo "[1/3] فحص ملفات التكوين والشبكة..."
mkdir -p nginx/ssl

echo "[2/3] تشغيل خدمات الإنتاج عبر Docker Compose..."
docker compose -f docker-compose.prod.yml up -d

echo "[3/3] التحقق من سلامة الحاويات..."
sleep 5
docker compose -f docker-compose.prod.yml ps

echo "========================================================"
echo " تم تشغيل نظام سمارت إديو بنجاح في بيئة الإنتاج!"
echo " المنفذ: http://localhost (أو عنوان IP / النطاق الخاص بك)"
echo " لوحة التحكم: Nginx Reverse Proxy + Odoo 19 (Multiprocessing)"
echo "========================================================"
