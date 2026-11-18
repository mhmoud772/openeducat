#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartEdu User Manual Markdown to PDF Generator
Generates a professional, print-ready Arabic RTL PDF from docs/USER_MANUAL_AR.md
"""

import os
import re
import subprocess
import markdown

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MD_PATH = os.path.join(PROJECT_ROOT, "docs", "USER_MANUAL_AR.md")
HTML_PATH = os.path.join(PROJECT_ROOT, "docs", "USER_MANUAL_AR.html")
PDF_PATH = os.path.join(PROJECT_ROOT, "docs", "USER_MANUAL_AR.pdf")

def format_alert_content(lines):
    cleaned = []
    for line in lines:
        l = line.strip()
        if l.startswith('>'):
            l = l[1:].strip()
        cleaned.append(l)
    raw_text = "\n".join(cleaned)
    # Convert markdown within alert
    html = markdown.markdown(raw_text, extensions=['extra'])
    return html

def parse_alerts(text):
    pattern = r'(?m)^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n((?:>.*(?:\n|$))*)'
    def replace_alert(match):
        alert_type = match.group(1).upper()
        content_lines = match.group(2).split('\n')
        inner_html = format_alert_content(content_lines)
        
        type_labels = {
            'NOTE': ('💡 ملاحظة هامة', 'alert-note', '#2563eb'),
            'TIP': ('⭐ نصيحة وإرشاد', 'alert-tip', '#16a34a'),
            'IMPORTANT': ('⚠️ تنبيه أساسي', 'alert-important', '#dc2626'),
            'WARNING': ('⚡ تحذير هام', 'alert-warning', '#d97706'),
            'CAUTION': ('🛡️ تنبيه أمان', 'alert-caution', '#7c3aed')
        }
        title, css_class, color = type_labels.get(alert_type, ('💡 تنبيه', 'alert-note', '#2563eb'))
        return f'\n<div class="callout {css_class}"><div class="callout-title" style="color: {color};">{title}</div><div class="callout-body">{inner_html}</div></div>\n\n'

    return re.sub(pattern, replace_alert, text)

def build_html():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 1. Normalize indented code fences inside lists (unindent them so markdown fences work properly)
    md_text = re.sub(r'(?m)^ {1,4}```', '```', md_text)

    # 2. Remove redundant first H1 and blockquote
    lines = md_text.split('\n')
    start_idx = 0
    for i, l in enumerate(lines):
        if l.strip() == '## 📌 فهرس الدليل':
            start_idx = i
            break
    
    cleaned_md = '\n'.join(lines[start_idx:])

    # 3. Extract and wrap the Table of Contents in a 2-column container
    toc_match = re.search(r'(## 📌 فهرس الدليل\s*\n)(.*?)(\n---)', cleaned_md, re.DOTALL)
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
    <div class="toc-title">📌 فهرس محتويات الدليل الشامل</div>
    <ol class="toc-grid">
        {''.join(parsed_items)}
    </ol>
</div>
'''
        cleaned_md = cleaned_md[:toc_match.start()] + toc_html + cleaned_md[toc_match.end():]

    # 4. Handle Mermaid blocks
    mermaid_blocks = {}
    def save_mermaid(match):
        idx = len(mermaid_blocks)
        key = f"<!-- MERMAID_PLACEHOLDER_{idx} -->"
        code = match.group(1).strip()
        mermaid_blocks[key] = f'<div class="mermaid-container"><div class="mermaid">\n{code}\n</div></div>'
        return key

    cleaned_md = re.sub(r'```mermaid\n(.*?)```', save_mermaid, cleaned_md, flags=re.DOTALL)

    # 5. Parse GitHub-style alerts
    cleaned_md = parse_alerts(cleaned_md)

    # 6. Convert Markdown to HTML
    html_body = markdown.markdown(
        cleaned_md,
        extensions=['extra', 'tables', 'fenced_code', 'nl2br']
    )

    # 7. Restore Mermaid blocks
    for key, val in mermaid_blocks.items():
        html_body = html_body.replace(f'<p>{key}</p>', val).replace(key, val)

    full_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>دليل المستخدم الشامل - منظومة سمارت إديو (SmartEdu)</title>
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
                content: "منظومة سمارت إديو (SmartEdu ERP) - دليل المستخدم";
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

        /* Header Banner */
        .cover-banner {{
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0284c7 100%);
            color: white;
            padding: 28px 24px;
            border-radius: 12px;
            margin-bottom: 22px;
            box-shadow: 0 4px 15px rgba(30, 58, 138, 0.15);
            text-align: center;
            page-break-after: avoid;
        }}

        .cover-banner h1 {{
            font-family: 'Cairo', 'Noto Kufi Arabic', sans-serif;
            font-size: 21pt;
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
            background: rgba(255, 255, 255, 0.18);
            border: 1px solid rgba(255, 255, 255, 0.35);
            color: #ffffff;
        }}

        /* Table of Contents Wrapper */
        .toc-wrapper {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 24px;
            page-break-inside: avoid;
            break-inside: avoid;
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
            font-size: 9.5pt;
        }}

        .toc-grid li {{
            margin-bottom: 4px;
        }}

        .toc-grid a {{
            color: #0369a1;
            text-decoration: none;
            font-weight: 600;
        }}

        /* Headings */
        h1, h2, h3, h4 {{
            font-family: 'Cairo', 'Noto Kufi Arabic', sans-serif;
            color: #0f172a;
            page-break-after: avoid;
            break-after: avoid;
        }}

        h2 {{
            font-size: 13pt;
            color: #1e3a8a;
            background: #eff6ff;
            border-right: 5px solid #2563eb;
            padding: 7px 14px;
            border-radius: 0 6px 6px 0;
            margin-top: 26px;
            margin-bottom: 14px;
        }}

        h3 {{
            font-size: 11pt;
            color: #0369a1;
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
            padding-left: 0;
        }}

        li {{
            margin-bottom: 5px;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0 18px 0;
            page-break-inside: avoid;
            break-inside: avoid;
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
            font-size: 9.5pt;
            border-bottom: 2px solid #94a3b8;
        }}

        tr:nth-child(even) {{
            background: #f8fafc;
        }}

        /* Code & Pre */
        code {{
            font-family: 'Fira Code', 'DejaVu Sans Mono', Consolas, monospace;
            background: #f1f5f9;
            color: #b91c1c;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 9pt;
            direction: ltr;
            display: inline-block;
            border: 1px solid #e2e8f0;
        }}

        pre {{
            background: #0f172a;
            border-radius: 8px;
            padding: 12px 14px;
            margin: 12px 0;
            overflow-x: auto;
            direction: ltr;
            text-align: left;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        pre code {{
            background: transparent;
            color: #f8fafc;
            border: none;
            padding: 0;
            font-size: 8.5pt;
            line-height: 1.5;
            display: block;
        }}

        /* Mermaid Box */
        .mermaid-container {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 16px 20px;
            margin: 16px 0;
            text-align: center;
            page-break-inside: avoid;
            break-inside: avoid;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}

        .mermaid {{
            background: transparent !important;
            margin: 0 auto;
        }}

        .mermaid svg {{
            max-width: 100% !important;
            height: auto !important;
        }}

        /* Callouts / Alerts */
        .callout {{
            border-right: 4.5px solid #2563eb;
            background: #f0f9ff;
            padding: 10px 14px;
            border-radius: 0 6px 6px 0;
            margin: 14px 0;
            page-break-inside: avoid;
            break-inside: avoid;
            font-size: 9.5pt;
        }}

        .callout-title {{
            font-family: 'Cairo', sans-serif;
            font-weight: 700;
            margin-bottom: 4px;
            font-size: 10pt;
        }}

        .callout-body p {{
            margin: 0 0 6px 0;
        }}

        .callout-body p:last-child {{
            margin: 0;
        }}

        .alert-note {{
            border-right-color: #2563eb;
            background: #eff6ff;
        }}

        .alert-tip {{
            border-right-color: #16a34a;
            background: #f0fdf4;
        }}

        .alert-important {{
            border-right-color: #dc2626;
            background: #fef2f2;
        }}

        .alert-warning {{
            border-right-color: #d97706;
            background: #fffbeb;
        }}

        hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 22px 0;
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
        <h1>منظومة سمارت إديو (SmartEdu ERP)</h1>
        <div class="subtitle">الدليل التعليمي والإرشادي الشامل للمدارس والمجمعات التعليمية الحديثة</div>
        <div class="cover-badges">
            <span class="badge">🚀 OpenEduCat 19.0 Core</span>
            <span class="badge">🇾🇪 مهيأ للمنهج والسلم التعليمي اليمني</span>
            <span class="badge">🌐 السحابة: openeducat.onrender.com</span>
            <span class="badge">📅 إصدار 2026</span>
        </div>
    </div>

    {html_body}

    <div class="footer-note">
        <strong>سمارت إديو - SmartEdu ERP 19.0</strong> | كافة الحقوق محفوظة © 2026 | مخصص للمدارس النموذجية والأهلية بالجمهورية اليمنية
    </div>

</body>
</html>
"""
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Generated HTML at: {HTML_PATH}")
    return HTML_PATH

def convert_html_to_pdf(html_path):
    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        f"--print-to-pdf={PDF_PATH}",
        html_path
    ]
    print(f"Running Chrome to generate PDF...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"Successfully generated PDF at: {PDF_PATH}")
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"PDF Size: {size_kb:.2f} KB")
        return True
    else:
        print(f"Error generating PDF: {res.stderr}")
        return False

if __name__ == "__main__":
    html_file = build_html()
    convert_html_to_pdf(html_file)
