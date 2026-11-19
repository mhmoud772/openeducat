#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate PDF for OpenEduCat Official Getting Started & Allocating Assignments Guide
"""

import os
import re
import subprocess
import markdown

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MD_PATH = os.path.join(PROJECT_ROOT, "docs", "OPENEDUCAT_OFFICIAL_GUIDE.md")
HTML_PATH = os.path.join(PROJECT_ROOT, "docs", "OPENEDUCAT_OFFICIAL_GUIDE.html")
PDF_PATH = os.path.join(PROJECT_ROOT, "docs", "OPENEDUCAT_OFFICIAL_GUIDE.pdf")

def build_pdf():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 1. Remove top title line if covered by banner
    lines = md_text.split('\n')
    start_idx = 0
    for i, l in enumerate(lines):
        if l.strip().startswith('## 📌 الفهرس العام'):
            start_idx = i
            break
    cleaned_md = '\n'.join(lines[start_idx:])

    # 2. Extract TOC
    toc_match = re.search(r'(## 📌 الفهرس العام لمراحل التهيئة الرسمية.*?\n)(.*?)(\n---)', cleaned_md, re.DOTALL)
    if toc_match:
        toc_items = toc_match.group(2).strip()
        parsed_items = []
        for item in toc_items.split('\n'):
            item = item.strip()
            if not item:
                continue
            m = re.match(r'^\d+\.\s*\[(.*?)\]\((.*?)\)', item)
            if m:
                parsed_items.append(f'<li><a href="{m.group(2)}">{m.group(1)}</a></li>')
            else:
                parsed_items.append(f'<li>{item}</li>')
        
        toc_html = f'''
<div class="toc-wrapper">
    <div class="toc-title">📌 فهرس المراحل الـ 27 لدليل البدء السريع والواجبات المدرسية</div>
    <ol class="toc-grid">
        {''.join(parsed_items)}
    </ol>
</div>
'''
        cleaned_md = cleaned_md[:toc_match.start()] + toc_html + cleaned_md[toc_match.end():]

    # 3. Handle Mermaid
    mermaid_blocks = {}
    def save_mermaid(match):
        idx = len(mermaid_blocks)
        key = f"<!-- MERMAID_{idx} -->"
        code = match.group(1).strip()
        mermaid_blocks[key] = f'<div class="mermaid-container"><div class="mermaid">\n{code}\n</div></div>'
        return key

    cleaned_md = re.sub(r'```mermaid\n(.*?)```', save_mermaid, cleaned_md, flags=re.DOTALL)

    # 4. Markdown to HTML
    html_body = markdown.markdown(
        cleaned_md,
        extensions=['extra', 'tables', 'fenced_code', 'nl2br']
    )

    for k, v in mermaid_blocks.items():
        html_body = html_body.replace(f'<p>{k}</p>', v).replace(k, v)

    full_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>الدليل الرسمي - OpenEduCat 19.0 - البدء السريع وتوزيع الواجبات</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@300;400;500;700;900&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'base',
            themeVariables: {{
                fontFamily: 'Tajawal, sans-serif',
                fontSize: '12px',
                primaryColor: '#eff6ff',
                primaryTextColor: '#1e3a8a',
                primaryBorderColor: '#3b82f6',
                lineColor: '#2563eb',
                secondaryColor: '#f0fdf4',
                tertiaryColor: '#fef2f2',
                mainBkg: '#ffffff',
                nodeBorder: '#3b82f6',
                actorBkg: '#eff6ff',
                actorBorder: '#3b82f6',
                actorTextColor: '#1e3a8a',
                signalColor: '#2563eb',
                signalTextColor: '#1e293b'
            }}
        }});
    </script>
    <style>
        @page {{
            size: A4 portrait;
            margin: 18mm 15mm 18mm 15mm;
            @bottom-left {{
                content: "OpenEduCat 19.0 - Official Getting Started & Assignments Guide";
                font-family: 'Tajawal', sans-serif;
                font-size: 8.5pt;
                color: #64748b;
            }}
            @bottom-right {{
                content: "صفحة " counter(page) " من " counter(pages);
                font-family: 'Tajawal', sans-serif;
                font-size: 8.5pt;
                color: #1e40af;
                font-weight: 700;
            }}
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: 'Tajawal', 'Noto Sans Arabic', Tahoma, sans-serif;
            color: #1e293b;
            line-height: 1.7;
            font-size: 10.5pt;
            background: #ffffff;
            margin: 0;
            padding: 0;
        }}

        .cover-banner {{
            background: linear-gradient(135deg, #1e3a8a 0%, #0369a1 50%, #0d9488 100%);
            color: white;
            padding: 28px 24px;
            border-radius: 12px;
            margin-bottom: 22px;
            box-shadow: 0 4px 15px rgba(3, 105, 161, 0.15);
            text-align: center;
            page-break-after: avoid;
        }}

        .cover-banner h1 {{
            font-family: 'Cairo', sans-serif;
            font-size: 20pt;
            font-weight: 800;
            margin: 0 0 10px 0;
            color: #ffffff;
            border: none;
            padding: 0;
        }}

        .cover-banner .subtitle {{
            font-size: 11.5pt;
            font-weight: 500;
            color: #e0f2fe;
            margin-bottom: 16px;
        }}

        .cover-badges {{
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 8.5pt;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
            color: #ffffff;
        }}

        .toc-wrapper {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 24px;
            page-break-inside: avoid;
        }}

        .toc-title {{
            font-family: 'Cairo', sans-serif;
            font-size: 12pt;
            font-weight: 800;
            color: #1e3a8a;
            margin-bottom: 12px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 6px;
        }}

        .toc-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px 18px;
            margin: 0;
            padding-right: 20px;
            padding-left: 0;
            font-size: 9pt;
        }}

        .toc-grid li {{
            margin-bottom: 4px;
        }}

        .toc-grid a {{
            color: #0369a1;
            text-decoration: none;
            font-weight: 600;
        }}

        h1, h2, h3, h4 {{
            font-family: 'Cairo', sans-serif;
            color: #0f172a;
            page-break-after: avoid;
        }}

        h2 {{
            font-size: 13pt;
            color: #1e3a8a;
            background: #f0fdfa;
            border-right: 5px solid #0d9488;
            padding: 7px 14px;
            border-radius: 0 6px 6px 0;
            margin-top: 26px;
            margin-bottom: 14px;
        }}

        h3 {{
            font-size: 11pt;
            color: #0284c7;
            margin-top: 18px;
            margin-bottom: 8px;
            border-bottom: 1px dashed #cbd5e1;
            padding-bottom: 4px;
        }}

        p {{
            margin: 0 0 10px 0;
            text-align: justify;
        }}

        ul, ol {{
            margin: 0 0 12px 0;
            padding-right: 22px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0 18px 0;
            page-break-inside: avoid;
            font-size: 9.5pt;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
        }}

        th, td {{
            padding: 8px 11px;
            border: 1px solid #cbd5e1;
            text-align: right;
            vertical-align: middle;
        }}

        th {{
            background: #f1f5f9;
            color: #0f172a;
            font-family: 'Cairo', sans-serif;
            font-weight: 700;
            border-bottom: 2px solid #94a3b8;
        }}

        tr:nth-child(even) {{
            background: #f8fafc;
        }}

        code {{
            font-family: 'Fira Code', monospace;
            background: #f1f5f9;
            color: #b91c1c;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 9pt;
            direction: ltr;
            display: inline-block;
        }}

        .mermaid-container {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 16px 20px;
            margin: 16px 0;
            text-align: center;
            page-break-inside: avoid;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}

        .mermaid svg {{
            max-width: 100% !important;
            height: auto !important;
        }}

        .footer-note {{
            margin-top: 35px;
            padding-top: 15px;
            border-top: 2px dashed #cbd5e1;
            text-align: center;
            font-size: 9pt;
            color: #64748b;
            page-break-inside: avoid;
        }}
    </style>
</head>
<body>

    <div class="cover-banner">
        <h1>الدليل الرسمي لمنظومة OpenEduCat 19.0</h1>
        <div class="subtitle">دليل البدء السريع، دورة التهيئة الشاملة، وإدارة وتوزيع الواجبات المدرسية</div>
        <div class="cover-badges">
            <span class="badge">📖 التوثيق الرسمي: doc.openeducat.org/19.0</span>
            <span class="badge">📝 Allocating & Grading Assignments</span>
            <span class="badge">🎯 إصدار 19.0 الرسمي</span>
        </div>
    </div>

    {html_body}

    <div class="footer-note">
        <strong>OpenEduCat 19.0 Documentation Guide</strong> | مستخرج ومترجم ومحفوظ للمشروع محلياً وسحابياً © 2026
    </div>

</body>
</html>
"""
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Generated HTML at: {HTML_PATH}")

    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        f"--print-to-pdf={PDF_PATH}",
        HTML_PATH
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"Successfully generated PDF at: {PDF_PATH}")
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"PDF Size: {size_kb:.2f} KB")
        return True
    else:
        print(f"Error: {res.stderr}")
        return False

if __name__ == "__main__":
    build_pdf()
