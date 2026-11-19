#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenEduCat Official Documentation Mirror & Offline Downloader
Downloads complete OpenEduCat 19.0 documentation (HTML, Arabic & English, Images, CSS, JS)
from https://doc.openeducat.org/19.0/ into docs/official_openeducat_docs/
"""

import os
import re
import json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEST_DIR = os.path.join(PROJECT_ROOT, "docs", "official_openeducat_docs")
BASE_URL = "https://doc.openeducat.org/19.0/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def download_file(url, local_path):
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return True, local_path, "cached"
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            with open(local_path, "wb") as f:
                f.write(content)
        return True, local_path, "downloaded"
    except Exception as e:
        return False, url, str(e)

def main():
    print(f"Starting OpenEduCat 19.0 Documentation Mirroring...")
    print(f"Target Directory: {DEST_DIR}")
    os.makedirs(DEST_DIR, exist_ok=True)

    # 1. Fetch Search Index to discover all documentation pages
    print("Fetching doc list from searchindex.js...")
    req = urllib.request.Request(BASE_URL + "searchindex.js", headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8')
            m = re.search(r'docnames:(\[.*?\])', content)
            docnames = json.loads(m.group(1)) if m else []
    except Exception as e:
        print(f"Error fetching searchindex: {e}")
        docnames = []

    # Extra root pages
    extra_pages = ["index", "genindex", "search", "applications", "administration", "getting-started/getting-started"]
    all_pages = sorted(list(set(docnames + extra_pages)))
    print(f"Total HTML pages discovered: {len(all_pages)}")

    # 2. Download all English and Arabic HTML pages
    tasks = []
    print("Downloading HTML documentation pages (English & Arabic)...")
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = {}
        for p in all_pages:
            # English version
            en_url = f"{BASE_URL}{p}.html"
            en_path = os.path.join(DEST_DIR, f"{p}.html")
            futures[executor.submit(download_file, en_url, en_path)] = ("en", p)
            
            # Arabic version
            ar_url = f"{BASE_URL}ar/{p}.html"
            ar_path = os.path.join(DEST_DIR, "ar", f"{p}.html")
            futures[executor.submit(download_file, ar_url, ar_path)] = ("ar", p)

        # Download searchindex.js
        futures[executor.submit(download_file, BASE_URL + "searchindex.js", os.path.join(DEST_DIR, "searchindex.js"))] = ("static", "searchindex.js")
        futures[executor.submit(download_file, BASE_URL + "ar/searchindex.js", os.path.join(DEST_DIR, "ar", "searchindex.js"))] = ("static", "ar/searchindex.js")

        success_count = 0
        for f in as_completed(futures):
            ok, target, status = f.result()
            if ok:
                success_count += 1
            if success_count % 50 == 0:
                print(f"  Processed {success_count} HTML files...")

    print(f"HTML pages download complete: {success_count} files.")

    # 3. Scan downloaded HTML files for all _images and _static references
    print("Scanning HTML pages for images, CSS, JS, and font assets...")
    image_names = set()
    static_paths = set()

    for root, _, files in os.walk(DEST_DIR):
        for file in files:
            if file.endswith(".html"):
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                    html = f.read()
                    for img in re.findall(r'(?:src|href)=["\']([^"\']+)["\']', html):
                        if "_images/" in img:
                            clean_img = img.split("_images/")[1].split("?")[0].split("#")[0]
                            image_names.add(clean_img)
                        elif "_static/" in img:
                            clean_stat = img.split("_static/")[1].split("?")[0].split("#")[0]
                            static_paths.add(clean_stat)

    print(f"Discovered {len(image_names)} images and {len(static_paths)} static assets.")

    # 4. Download all assets in parallel
    print("Downloading all images and static assets...")
    asset_futures = {}
    with ThreadPoolExecutor(max_workers=30) as executor:
        # Static files (for both root and ar)
        for s in static_paths:
            s_url = f"{BASE_URL}_static/{s}"
            s_path = os.path.join(DEST_DIR, "_static", s)
            asset_futures[executor.submit(download_file, s_url, s_path)] = s
            
            ar_s_url = f"{BASE_URL}ar/_static/{s}"
            ar_s_path = os.path.join(DEST_DIR, "ar", "_static", s)
            asset_futures[executor.submit(download_file, ar_s_url, ar_s_path)] = "ar_" + s

        # Images (for both root and ar)
        for img in image_names:
            img_url = f"{BASE_URL}_images/{urllib.parse.quote(img)}"
            img_path = os.path.join(DEST_DIR, "_images", img)
            asset_futures[executor.submit(download_file, img_url, img_path)] = img
            
            ar_img_url = f"{BASE_URL}ar/_images/{urllib.parse.quote(img)}"
            ar_img_path = os.path.join(DEST_DIR, "ar", "_images", img)
            asset_futures[executor.submit(download_file, ar_img_url, ar_img_path)] = "ar_" + img

        downloaded_assets = 0
        for f in as_completed(asset_futures):
            ok, target, status = f.result()
            if ok:
                downloaded_assets += 1
            if downloaded_assets % 100 == 0:
                print(f"  Processed {downloaded_assets} assets...")

    print(f"Assets download complete: {downloaded_assets} assets processed.")

    # 5. Create offline Portal Index file
    portal_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>دليل توثيق OpenEduCat 19.0 الرسمي - غير متصل (Offline Docs)</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Tajawal', Tahoma, sans-serif;
            background: #f1f5f9;
            color: #1e293b;
            margin: 0;
            padding: 40px 20px;
            direction: rtl;
        }
        .container {
            max-width: 950px;
            margin: 0 auto;
            background: white;
            padding: 35px 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.06);
            border: 1px solid #e2e8f0;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 25px;
            margin-bottom: 30px;
        }
        h1 {
            font-family: 'Cairo', sans-serif;
            color: #1e3a8a;
            font-size: 26px;
            margin: 0 0 10px 0;
        }
        p.subtitle {
            color: #64748b;
            font-size: 16px;
            margin: 0;
        }
        .badge {
            display: inline-block;
            background: #eff6ff;
            color: #2563eb;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            margin-top: 15px;
            border: 1px solid #bfdbfe;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }
        .card {
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 20px;
            background: #f8fafc;
            transition: all 0.2s ease;
        }
        .card:hover {
            border-color: #3b82f6;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
            transform: translateY(-2px);
        }
        .card h2 {
            font-family: 'Cairo', sans-serif;
            font-size: 18px;
            color: #1e40af;
            margin-top: 0;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card p {
            font-size: 14px;
            color: #475569;
            line-height: 1.6;
            margin: 0 0 15px 0;
        }
        .btn {
            display: inline-block;
            background: #2563eb;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
            transition: background 0.2s;
        }
        .btn:hover {
            background: #1d4ed8;
        }
        .btn-outline {
            background: transparent;
            color: #2563eb;
            border: 1px solid #2563eb;
            margin-right: 8px;
        }
        .btn-outline:hover {
            background: #eff6ff;
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 13px;
            color: #94a3b8;
            border-top: 1px dashed #cbd5e1;
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>توثيق OpenEduCat 19.0 الرسمي (نسخة غير متصلة بالإنترنت)</h1>
            <p class="subtitle">تم تنزيل وحفظ كامل التوثيق الرسمي ومكوناته للعمل دون اتصال بالإنترنت</p>
            <span class="badge">OpenEduCat 19.0 Community & Core Modules</span>
        </div>

        <div class="grid">
            <div class="card" style="border-right: 5px solid #2563eb;">
                <h2>🚀 البدء السريع وتوزيع الواجبات</h2>
                <p>دليل البدء السريع الرسمي، بما في ذلك إعداد المهام والواجبات المدرسية (Allocating Assignments)، الجداول، والقبول.</p>
                <a class="btn" href="getting-started/getting-started.html#allocating-assignments">النسخة الإنجليزية (EN)</a>
                <a class="btn btn-outline" href="ar/getting-started/getting-started.html">النسخة العربية (AR)</a>
            </div>

            <div class="card" style="border-right: 5px solid #16a34a;">
                <h2>📚 موديول الواجبات والتقييم (Assignments)</h2>
                <p>شرح تفصيلي لأنواع الواجبات (Assignment Types)، إدارة المهام، تصحيح إجابات الطلاب، وسلالم التقييم (Rubrics).</p>
                <a class="btn" href="applications/Assignments/assignment-type.html">فتح موديول الواجبات (EN)</a>
                <a class="btn btn-outline" href="ar/applications/Assignments/assignment-type.html">بالعربية (AR)</a>
            </div>

            <div class="card" style="border-right: 5px solid #d97706;">
                <h2>📖 الصفحة الرئيسية للتوثيق الكامل</h2>
                <p>استعراض كافة موديولات النظام الـ 350+ صفحة (القبول، الكادر، الجداول، الكنترول، المكتبة، والرسوم).</p>
                <a class="btn" href="index.html">الدليل الكامل (EN)</a>
                <a class="btn btn-outline" href="ar/index.html">الدليل الكامل (AR)</a>
            </div>

            <div class="card" style="border-right: 5px solid #7c3aed;">
                <h2>⚙️ التثبيت والصيانة السحابية</h2>
                <p>أدلة الإعداد المتقدم، بوابات البريد الإلكتروني، إدارة قواعد البيانات، واستضافة الخوادم.</p>
                <a class="btn" href="administration.html">دليل الصيانة (EN)</a>
                <a class="btn btn-outline" href="ar/administration.html">بالعربية (AR)</a>
            </div>
        </div>

        <div class="footer">
            تمت أرشفة وتنزيل التوثيق محلياً من <a href="https://doc.openeducat.org/19.0/" target="_blank" style="color: #2563eb;">doc.openeducat.org/19.0</a> لضمان توفرها الدائم للمشروع.
        </div>
    </div>
</body>
</html>
"""
    portal_path = os.path.join(DEST_DIR, "index_offline_portal.html")
    with open(portal_path, "w", encoding="utf-8") as f:
        f.write(portal_html)
    print(f"Created Offline Portal at: {portal_path}")
    print("ALL DONE SUCCESSFULLY!")

if __name__ == "__main__":
    main()
