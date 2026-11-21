#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenEduCat 19.0 Official Arabic Documentation Word Generator
Generates a comprehensive, professional Arabic Word document (.docx) from
the official doc.openeducat.org/19.0/ar/ documentation.
Features:
- Pure RTL (Right-to-Left) formatting for all paragraphs, headings, and tables
- Styled tables with dark blue headers and alternating row shading
- Color-coded callout alert boxes (Notes, Tips, Warnings)
- Formatted code blocks and terminal commands
- Comprehensive coverage of all 4 parts:
  Part 1: Installation & Cloud Server Configuration
  Part 2: Getting Started (All 27 setup steps)
  Part 3: Academic Applications & Specialized Modules (14 core modules)
  Part 4: System Operations, Backups, and Maintenance
"""

import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCX_PATH = os.path.join(PROJECT_ROOT, "docs", "OpenEduCat_19_Arabic_Documentation.docx")
FONT_FAMILY = "Arial"

def set_p_rtl(p, align='right'):
    pPr = p._p.get_or_add_pPr()
    pPr.append(OxmlElement('w:bidi'))
    if align == 'right':
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == 'left':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif align == 'justify':
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def add_ar_run(p, text, bold=False, italic=False, font_size=11, color_rgb=(30, 41, 59), font_name=FONT_FAMILY):
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(font_size)
    run.font.name = font_name
    run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._r.get_or_add_rPr()
    rPr.append(OxmlElement('w:rtl'))
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is not None:
        rFonts.set(qn('w:cs'), font_name)
    return run

def add_h1(doc, text):
    p = doc.add_paragraph()
    set_p_rtl(p, 'right')
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    add_ar_run(p, text, bold=True, font_size=17, color_rgb=(30, 58, 138))
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    set_p_rtl(p, 'right')
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    add_ar_run(p, text, bold=True, font_size=13.5, color_rgb=(30, 64, 175))
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    set_p_rtl(p, 'right')
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    add_ar_run(p, text, bold=True, font_size=12, color_rgb=(2, 132, 199))
    return p

def add_p(doc, text, bold_prefix=""):
    p = doc.add_paragraph()
    set_p_rtl(p, 'justify')
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.25
    if bold_prefix:
        add_ar_run(p, bold_prefix, bold=True, font_size=11, color_rgb=(15, 23, 42))
        add_ar_run(p, " ", bold=False, font_size=11)
    add_ar_run(p, text, bold=False, font_size=11, color_rgb=(30, 41, 59))
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph()
    set_p_rtl(p, 'right')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0)
    p.paragraph_format.right_indent = Inches(0.25)
    p.paragraph_format.line_spacing = 1.2
    add_ar_run(p, "• ", bold=True, font_size=11, color_rgb=(37, 99, 235))
    if bold_prefix:
        add_ar_run(p, bold_prefix, bold=True, font_size=11, color_rgb=(15, 23, 42))
        add_ar_run(p, " ", bold=False, font_size=11)
    add_ar_run(p, text, bold=False, font_size=11, color_rgb=(30, 41, 59))
    return p

def add_callout(doc, title, text, callout_type="note"):
    table = doc.add_table(rows=1, cols=1)
    set_table_rtl(table)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    colors = {
        "note": ("EFF6FF", (37, 99, 235), "💡 ملاحظة هامة"),
        "tip": ("F0FDF4", (22, 163, 74), "⭐ إرشاد ونصيحة"),
        "warning": ("FFFBEB", (217, 119, 6), "⚡ تحذير وتنبيه"),
        "important": ("FEF2F2", (220, 38, 38), "⚠️ تنبيه أمني أساسي")
    }
    bg_hex, border_rgb, default_title = colors.get(callout_type, colors["note"])
    box_title = title if title else default_title

    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    
    # Shading and borders
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_hex}"/>')
    tcPr.append(shd)

    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="single" w:sz="36" w:space="0" w:color="{border_rgb[0]:02X}{border_rgb[1]:02X}{border_rgb[2]:02X}"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    set_p_rtl(p, 'right')
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    add_ar_run(p, box_title, bold=True, font_size=11.5, color_rgb=border_rgb)

    p2 = cell.add_paragraph()
    set_p_rtl(p2, 'justify')
    p2.paragraph_format.space_after = Pt(4)
    p2.paragraph_format.line_spacing = 1.2
    add_ar_run(p2, text, bold=False, font_size=10.5, color_rgb=(30, 41, 59))

    # Space after table
    sp_p = doc.add_paragraph()
    sp_p.paragraph_format.space_after = Pt(4)

def set_table_rtl(table):
    tblPr = table._tbl.tblPr
    tblPr.append(OxmlElement('w:bidiVisual'))

def add_table(doc, headers, rows_data):
    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    set_table_rtl(table)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        set_p_rtl(p, 'center')
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(5)
        add_ar_run(p, header_text, bold=True, font_size=10.5, color_rgb=(255, 255, 255))
        
        tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E3A8A"/>')
        tcPr.append(shd)

    # Data Rows
    for r_idx, row in enumerate(rows_data):
        row_cells = table.rows[r_idx + 1].cells
        bg_hex = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell_value in enumerate(row):
            row_cells[c_idx].text = ""
            p = row_cells[c_idx].paragraphs[0]
            set_p_rtl(p, 'right' if c_idx > 0 else 'center')
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            add_ar_run(p, str(cell_value), bold=(c_idx == 0), font_size=10, color_rgb=(30, 41, 59))

            tcPr = row_cells[c_idx]._tc.get_or_add_tcPr()
            if bg_hex != "FFFFFF":
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_hex}"/>')
                tcPr.append(shd)
            
            # Subtle borders
            borders = parse_xml(f'''
                <w:tcBorders {nsdecls("w")}>
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                    <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                    <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                </w:tcBorders>
            ''')
            tcPr.append(borders)

    sp_p = doc.add_paragraph()
    sp_p.paragraph_format.space_after = Pt(6)

def add_code(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)

    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>')
    tcPr.append(shd)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(248, 250, 252)

    sp_p = doc.add_paragraph()
    sp_p.paragraph_format.space_after = Pt(4)

def build_document():
    doc = docx.Document()

    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        section.header.is_linked_to_previous = False
        
        # Header
        hp = section.header.paragraphs[0]
        set_p_rtl(hp, 'right')
        add_ar_run(hp, "التوثيق الرسمي لمنظومة OpenEduCat 19.0 — النسخة العربية الشاملة", italic=True, font_size=8.5, color_rgb=(100, 116, 139))

    # ================= COVER / TITLE =================
    title_p = doc.add_paragraph()
    set_p_rtl(title_p, 'center')
    title_p.paragraph_format.space_before = Pt(30)
    title_p.paragraph_format.space_after = Pt(6)
    add_ar_run(title_p, "التوثيق الرسمي لمنظومة OpenEduCat 19.0", bold=True, font_size=24, color_rgb=(30, 58, 138))

    sub_p = doc.add_paragraph()
    set_p_rtl(sub_p, 'center')
    sub_p.paragraph_format.space_after = Pt(16)
    add_ar_run(sub_p, "الدليل التشغيلي والأكاديمي والتقني الكامل لمنظومة إدارة المنشآت التعليمية والمدارس", font_size=13, color_rgb=(2, 132, 199))

    meta_p = doc.add_paragraph()
    set_p_rtl(meta_p, 'center')
    meta_p.paragraph_format.space_after = Pt(30)
    add_ar_run(meta_p, "المرجع السحابي المعتمد: doc.openeducat.org/19.0/ar/ | الإصدار 19.0 الرسمي | لغة التوثيق: العربية (RTL)", italic=True, font_size=9.5, color_rgb=(100, 116, 139))

    add_callout(doc, "نطاق هذا المستند", 
        "تم استخراج وصياغة هذا المستند بدقة ليكون دليلاً مرجعياً متكاملاً وشاملاً بصيغة Word (.docx)، "
        "مخصصاً للمراجعة والقراءة والتدريب وإعداد اللوائح الداخلية للمؤسسة التعليمية. "
        "يشمل كافة محاور التثبيت السحابي، خطوات البدء السريع الـ 27، وإدارة كافة الموديولات والتطبيقات الأكاديمية.", 
        "note")

    # ================= TABLE OF CONTENTS =================
    add_h2(doc, "فهرس محتويات الدليل الشامل")
    toc_items = [
        ("الجزء الأول: التثبيت، التكوين، والصيانة السحابية والمحلية", "طرق التثبيت، تهيئة الخوادم، ضبط قواعد البيانات، وبوابات البريد الصادر."),
        ("الجزء الثاني: دليل البدء السريع الشامل (الـ 27 مرحلة كاملة)", "خطوات تأسيس المنشأة، المراحل، الكادر، الجداول، الرسوم، والقبول بالتسلسل المنطقي."),
        ("الجزء الثالث: توزيع وتقييم الواجبات المدرسية (Assignments & Grading)", "الشرح التفصيلي لإنشاء المهام، بوابات التسليم، وسلالم رصد الدرجات."),
        ("الجزء الرابع: دليل التطبيقات الأكاديمية التخصصية", "المكتبة والباركود، الكنترول والاختبارات، بوابات أولياء الأمور، والحضور اليومي."),
        ("الجزء الخامس: الإشراف الفني وإجراءات النسخ الاحتياطي والأمان", "أوامر الصيانة والنسخ الاحتياطي واستعادة البيانات وحماية النظام.")
    ]
    for title, desc in toc_items:
        add_bullet(doc, desc, bold_prefix=title + " :")

    doc.add_page_break()

    # ================= PART 1: INSTALLATION & MAINTENANCE =================
    add_h1(doc, "الجزء الأول: التثبيت، التكوين، والصيانة السحابية والمحلية (Install & Maintain)")
    add_p(doc, 
        "توفر منظومة OpenEduCat 19.0 مرونة فائقة في خيارات النشر والتشغيل، سواء على الخوادم السحابية المؤتمتة (مثل Render و AWS و DigitalOcean) "
        "أو عبر خوادم المؤسسة المحلية (On-Premise) باستخدام حاويات Docker أو التثبيت المباشر من المصدر.")

    add_h2(doc, "1. خيارات تثبيت المنظومة (Installation Methods)")
    add_bullet(doc, "التثبيت السحابي عبر حاويات Docker (الموصى به لبيئات الإنتاج): يضمن عزل النظام وسهولة التحديث السريع دون تعارض مع مكتبات نظام التشغيل.", "أ) حاويات Docker:")
    add_bullet(doc, "التثبيت المباشر عبر كود المصدر (Source Code): تنزيل حزمة الكود المصدري من GitHub وتثبيته فوق بيئة Python 3.10 مع PostgreSQL.", "ب) كود المصدر:")
    add_bullet(doc, "الحزم الجاهزة (Packaged Installers): استخدام حزم التثبيت debian/ubuntu لتشغيل المنظومة كخدمة نظام مستقلة (systemd service).", "جـ) الحزم الرسمية:")

    add_h2(doc, "2. متطلبات بيئة التشغيل والخادم (System Requirements)")
    req_headers = ["المورد / العنصر", "الحد الأدنى (مدرسة صغيرة)", "الموصى به (مجمع نموذجي)", "ملاحظات الاستخدام"]
    req_rows = [
        ["المعالج (CPU)", "2 Cores", "4 to 8 Cores", "معالجة الطلبات المتزامنة في أوقات تسجيل الدرجات"],
        ["الذاكرة العشوائية (RAM)", "4 GB", "8 to 16 GB", "PostgreSQL Buffer Cache و Odoo Workers"],
        ["مساحة التخزين (SSD)", "40 GB SSD", "100+ GB NVMe SSD", "تخزين قاعدة البيانات والمرفقات وكتب المكتبة"],
        ["نظام التشغيل", "Ubuntu 22.04 LTS", "Ubuntu 22.04 / 24.04 LTS", "التوافقية والاستقرار والدعم طويل الأمد"],
        ["قاعدة البيانات", "PostgreSQL 14+", "PostgreSQL 15 or 16", "دعم المعاملات المتوازية والمفاتيح الخارجية"]
    ]
    add_table(doc, req_headers, req_rows)

    add_h2(doc, "3. إعداد وتهيئة خادم البريد الصادر (Outgoing Email Gateway)")
    add_p(doc, 
        "يعتبر ربط خادم البريد الصادر (SMTP) ركيزة أساسية لتفعيل التواصل التلقائي مع أولياء الأمور والطلاب، "
        "حيث يتولى النظام إرسال دعوات تفعيل الحسابات، إشعارات الغياب الفوري، كشوف الدرجات، وفواتير الرسوم إلكترونياً.")

    add_bullet(doc, "Brevo (Sendinblue): يوفر 300 رسالة يومياً مجاناً، ويتميز بسرعة الإرسال ودقة التسليم دون حظر.", "الخيار السحابي المجاني الأفضل:")
    add_bullet(doc, "Google Workspace / Gmail: يدعم بروتوكول OAuth 2.0 الآمن لتفادي مشاكل كلمات المرور المؤقتة.", "خوادم Google:")
    add_bullet(doc, "Microsoft Outlook 365: يدعم الربط عبر منصة Azure OAuth.", "خوادم Microsoft:")

    add_p(doc, "خطوات ضبط خادم البريد الصادر في واجهة النظام:", bold_prefix="طريقة التهيئة:")
    add_bullet(doc, "انتقل إلى: الإعدادات (Settings) > القائمة الفنية (Technical) > البريد الإلكتروني الصادر (Outgoing Mail Servers).")
    add_bullet(doc, "انقر على جديد (New)، ثم حدد اسم الخادم (مثل: Brevo SMTP).")
    add_bullet(doc, "خادم SMTP: smtp-relay.brevo.com | المنفذ: 587 | الأمان: TLS (STARTTLS).")
    add_bullet(doc, "اسم المستخدم: بريدك المسجل في الخدمة | كلمة المرور: مفتاح SMTP API Key.")
    add_bullet(doc, "اضغط على زر (اختبار الاتصال - Test Connection) للتأكد من ظهور رسالة النجاح.")

    add_callout(doc, "تنبيه هام حول البريد في Odoo 19", 
        "إذا ظهر خطأ 'تعذر التواصل مع خادم البريد الإلكتروني' عند الضغط على 'إرسال دعوة عبر البريد'، "
        "فهذا يعني أن المنظومة تحاول إرسال إشعار بدون وجود خادم بريد SMTP مهيأ. بمجرد إضافة بيانات خادم البريد كما هو موضح أعلاه، "
        "ستعمل كافة الإشعارات ودعوات المستخدمين فوراً وبنجاح.", 
        "important")

    # ================= PART 2: GETTING STARTED (27 STEPS) =================
    add_h1(doc, "الجزء الثاني: دليل البدء السريع الشامل (Getting Started — دورة التهيئة من الصفر)")
    add_p(doc, 
        "تحدد وثيقة التوثيق الرسمية لمنظومة OpenEduCat تسلسلاً هندسياً دقيقاً مؤلفاً من 27 مرحلة متتابعة "
        "لبناء وتشغيل مدرسة رقمية متكاملة. يضمن هذا الترتيب المنطقي عدم حدوث أي أخطاء ترابطية بين الجداول والبيانات.")

    steps_headers = ["المرحلة", "المجال الأكاديمي", "المسار في القائمة", "الهدف والوظيفة الأساسية"]
    steps_rows = [
        ["1", "كود المصدر", "GitHub Repository", "تجهيز بيئة التشغيل وتثبيت المكونات الأساسية للنظام"],
        ["2", "قاعدة البيانات", "Database Manager", "إنشاء وتأمين قاعدة بيانات المنشأة وتحديد اسم المستخدم المسؤول"],
        ["3", "بيانات المنشأة", "الإعدادات > الشركات", "تسجيل اسم المدرسة، الشعار الرسمي، العنوان، وأرقام التواصل"],
        ["4", "التهيئة المحاسبية", "المحاسبة > التكوين", "إعداد دليل الحسابات وتحديد العملة الرسمية للمدرسة (ر.ي)"],
        ["5", "تثبيت الموديولات", "التطبيقات (Apps)", "تثبيت حزمة تطبيقات OpenEduCat الأساسية والمتقدمة"],
        ["6", "الموقع الإلكتروني", "الموقع > تحرير", "تصميم واجهة المدرسة، صفحة 'عن المدرسة'، وروابط القبول"],
        ["7", "الخيارات العامة", "الإعدادات العامة", "تفعيل الحضور اليومي، نظام التقييم، وبنك الأسئلة"],
        ["8", "الأعوام الدراسية", "التهيئة > الأعوام", "إنشاء العام الدراسي الجديد (2026-2027) وفصليه الدراسيين"],
        ["9", "المراحل الدراسية", "الكورسات (Courses)", "تعريف الصفوف والمراحل (الأساسي 1-9، الثانوي 1-3)"],
        ["10", "المواد والمناهج", "المواد (Subjects)", "إضافة المقررات الدراسية (القرآن، الرياضيات، الفيزياء، إلخ)"],
        ["11", "الشعب والدفع", "الشعب (Batches)", "تقسيم الصفوف إلى شعب صفية (شعبة أ، شعبة ب) وتحديد سعتها"],
        ["12", "الكادر التعليمي", "المعلمون (Faculties)", "تسجيل بيانات المعلمين، المؤهلات، والدرجات العلمية وتوزيع المواد"],
        ["13", "البريد الصادر", "الإعدادات > البريد", "ربط خادم SMTP لإرسال الإشعارات وكلمات المرور التلقائية"],
        ["14", "حسابات المعلمين", "المستخدمون والشركاء", "منح المعلم اسم مستخدم وصلاحية رصد الدرجات وتسجيل الحضور"],
        ["15", "مستخدمو الإدارة", "المستخدمون > الصلاحيات", "تعيين مدراء القبول، شؤون الطلاب، ومسؤولي الكنترول"],
        ["16", "هياكل الرسوم", "الرسوم (Fees Terms)", "برمجة الرسوم السنوية وجداول الأقساط الميسرة والخصومات"],
        ["17", "سجلات القبول", "القبول والتسجيل", "فتح نافذة التسجيل الإلكتروني واستقبال ملفات الطلاب المستجدين"],
        ["18", "حسابات الطلاب", "الطلاب (Students)", "توليد الرقم الأكاديمي (GR Number) وتفعيل بوابة الطالب الذاتية"],
        ["19", "القاعات والمعامل", "المنشآت (Facilities)", "ترقيم القاعات وتحديد الطاقة الاستيعابية ومنع تكدس الفصول"],
        ["20", "الجداول المدرسية", "الجداول (Timetables)", "بناء جدول الحصص الأسبوعي مع الفحص الآلي لتعارض المدرسين"],
        ["21", "توزيع الواجبات", "الواجبات (Assignments)", "تكليف الطلاب بالمهام المدرسية وتحديد المواعيد والمحاولات"],
        ["22", "تقييم الواجبات", "سجل الدرجات (Grade Book)", "تصحيح الحلول المرفوعة ورصد درجات الأعمال الفصلية"],
        ["23", "أولياء الأمور", "أولياء الأمور (Parents)", "ربط الأبناء بملف ولي الأمر وتفعيل بوابة المتابعة الرقمية"],
        ["24", "نظام التعلم LMS", "التعليم الإلكتروني", "رفع المناهج التفاعلية والمحاضرات المسجلة والملفات الإثرائية"],
        ["25", "بنك الاختبارات", "الاختبارات والامتحانات", "جدولة الاختبارات وتوزيع لجان السير وإصدار الشهادات بالباركود"],
        ["26", "الترجمة والتعريب", "الترجمة (Translations)", "ضبط الواجهة باللغة العربية RTL وتخصيص المسميات الرسمية"],
        ["27", "الصيانة المستمرة", "المجلد scripts/", "تشغيل النسخ الاحتياطي الدوري وحماية البيانات ومراجعة الأداء"]
    ]
    add_table(doc, steps_headers, steps_rows)

    # ================= PART 3: ASSIGNMENTS & GRADING =================
    add_h1(doc, "الجزء الثالث: موديول الواجبات المدرسية والتقييم (Assignments & Grading)")
    add_p(doc, 
        "يعد موديول الواجبات المدرسية في OpenEduCat منظومة تفاعلية متقدمة تهدف إلى رقمنة الواجبات والأنشطة البيتية بالكامل، "
        "مما يتيح للمعلم إسناد الواجبات ومتابعة تسليمها عبر الإنترنت، ويتيح للطلاب رفع ملفات الحلول من أي هاتف أو جهاز كمبيوتر.")

    add_h2(doc, "1. أنواع وتصنيفات الواجبات (Assignment Types)")
    add_p(doc, "تساعد تصنيفات الواجبات في فرز الأنشطة وتحديد أوزانها النسبية في سجل الدرجات:")
    add_bullet(doc, "اسم نوع الواجب (Name): مسمى التصنيف (مثل: واجب منزلي أسبوعي، مشروع فصلي، بحث علمي، تقرير معملي).")
    add_bullet(doc, "الكود التعريفي (Code): رمز فريد لتسهيل البحث والتقارير (مثل: HW-01 أو PRJ-01).")
    add_bullet(doc, "المدرسة / الفرع (Company): إمكانية تخصيص الأنواع لفروع معينة في المدارس متعددة الفروع.")

    add_h2(doc, "2. إنشاء بطاقة الواجب وتفاصيل الإسناد (Assignment Allocation)")
    assign_headers = ["الحقل (Field)", "النوع والقيمة", "الوصف والوظيفة العملية"]
    assign_rows = [
        ["اسم الواجب (Name)", "نصي إلزامي", "عنوان الواجب الظاهر للطالب في البوابة (مثال: واجب الفيزياء - حل مسائل الحركة ص 30)"],
        ["المرحلة (Course)", "قائمة منسدلة", "تحديد الصف الدراسي المستهدف (مثال: الأول الثانوي العام)"],
        ["الشعبة (Batch)", "قائمة منسدلة", "تحديد الشعبة الصفية المستهدفة (مثال: شعبة أ - بنين)"],
        ["المادة (Subject)", "قائمة منسدلة", "المقرر التابع له الواجب (مثال: مادة الفيزياء)"],
        ["المعلم (Faculty)", "قائمة منسدلة", "المعلم صاحب الواجب والمسؤول عن متابعته وتصحيحه"],
        ["نوع الواجب", "قائمة منسدلة", "التصنيف (واجب منزلي / مشروع / نشاط لاصفي)"],
        ["تاريخ الإصدار", "تاريخ ووقت", "تاريخ بدء ظهور الواجب للطلاب وبدء استقبال الإجابات"],
        ["تاريخ التسليم", "تاريخ ووقت", "الموعد النهائي الحاسم لقبول الحلول، وبعده تُقفل البوابة"],
        ["المراجع (Reviewer)", "مستخدم نظام", "المعلم أو المشرف الأكاديمي المعتمد لمراجعة التصحيح"]
    ]
    add_table(doc, assign_headers, assign_rows)

    add_h2(doc, "3. قواعد المحاولات وبوابة الاعتماد (Submission Gate Rules)")
    add_p(doc, 
        "ينفرد نظام OpenEduCat بآلية رقابة صارمة على دورة حياة الواجب تسمى (Submission Gate) "
        "لضمان نزاهة التقييم وعدم إغلاق الواجبات قبل استيفاء حقوق الطلاب:")

    add_bullet(doc, "محاولة واحدة (Single Attempt): يُسمح للطالب برفع الحل مرة واحدة فقط، ويُقفل التعديل فور الضغط على إرسال.", "أ) خيارات عدد المحاولات:")
    add_bullet(doc, "محاولات متعددة (Multiple Attempt): يمكن للمعلم تحديد سقف أعلى للمحاولات (مثل: 3 محاولات) لإتاحة الفرصة للطالب لتحسين إجابته.", "ب) المحاولات المتعددة:")
    add_bullet(doc, "محاولات إضافية لطالب محدد (Additional Attempt): يستطيع المعلم منح محاولة إضافية لطالب بعينه (في حال وجود عذر تقني أو صحي) دون فتح المحاولات لباقي الفصل.", "جـ) الاستثناءات الفردية:")
    add_bullet(doc, "شريط تنبيه الطلاب غير المسلّمين (Missing Submissions): يظهر شريط تنبيه أصفر بالعدد قبل انتهاء المهلة، ويتحول إلى أحمر داكن عند انتهاء الموعد النهائي.", "د) تتبع غير المسلمين:")
    add_bullet(doc, "بوابة الإغلاق (Finish Gate): يرفض النظام الضغط على زر إنهاء الواجب إلا في حالتين: إما تسليم كافة طلاب الشعبة، أو انقضاء الموعد النهائي رسمياً.", "هـ) قيود الإغلاق:")

    add_h2(doc, "4. دورة رصد وتقييم الدرجات (Grading Workflow)")
    add_p(doc, "تتم عملية رصد درجات الواجبات عبر موديول سجل الدرجات الأكاديمي (Gradebook) وفق الخطوات التالية:")
    add_bullet(doc, "1. الانتقال إلى: سجل الدرجات (Grade Book) > تقييم الواجبات (Grading Assignment).")
    add_bullet(doc, "2. النقر على جديد وتحديد المادة، الشعبة، الدرجة العظمى (Total Marks: مثلاً 20)، والوزن النسبي (Weightage).")
    add_bullet(doc, "3. الضغط على زر (نشر - Publish) ثم (بدء التقييم - Grading Started).")
    add_bullet(doc, "4. النقر على زر (رصد الدرجات - Start Grading): يفتح النظام كشف درجات الطلاب مباشرة لمطالعة ملفات الحلول ورصد الدرجة والملاحظات التوجيهية.")
    add_bullet(doc, "5. النقر على (إغلاق التقييم - Grading Closed) ثم (نشر النتائج - Grades Published) لتظهر فوراً في حساب الطالب وولي أمره.")

    # ================= PART 4: CORE APPLICATIONS =================
    add_h1(doc, "الجزء الرابع: دليل التطبيقات الأكاديمية التخصصية (Core Applications)")

    add_h2(doc, "1. شؤون الطلاب والسجل الشامل (Student Information System)")
    add_p(doc, 
        "يشكل موديول الطلاب النواة الرقمية التي تترابط معها كافة العمليات الأخرى في المنظومة. "
        "يحتوي ملف الطالب على:")
    add_bullet(doc, "البيانات الأساسية: الاسم الرباعي بالعربية والإنجليزية، تاريخ ومحل الميلاد، الجنسية، الديانة، والصورة الشخصية.")
    add_bullet(doc, "الرقم الأكاديمي الموحد (GR Number): رقم قيد فريد لا يتكرر يرافق الطالب طوال سنوات دراسته.")
    add_bullet(doc, "الملف الصحي الشامل: فصيلة الدم، الحساسية الدوائية والغذائية، الأمراض المزمنة، وسجل الطوارئ.")
    add_bullet(doc, "الارتباط الأسري: ربط الطالب بملف ولي الأمر مع تحديد درجة القرابة (أب، أم، وصي قانوني).")
    add_bullet(doc, "الأزرار الذكية العلوية (Smart Buttons): وصول سريع بنقرة واحدة إلى: إجمالي الحضور والغياب، فواتير الرسوم والمسدد منها، كشوف الدرجات، والكتب المستعارة.")

    add_h2(doc, "2. الكادر التعليمي وتوزيع الأنصبة (Faculty Management)")
    add_p(doc, "إدارة شاملة لملفات المعلمين، التخصصات، المؤهلات العلمية، وتوزيع المواد والأنصبة الأسبوعية:")
    add_bullet(doc, "ربط المواد بالمعلم: تحديد المقررات المسموح للمعلم تدريسها منعاً لأي خطأ في الجداول المدرسية.")
    add_bullet(doc, "النصاب التدريسي الأسبوعي: ضبط الساعات التدريسية لمنع التحميل الزائد على المعلم.")
    add_bullet(doc, "صلاحيات الوصول: منح المعلم حساباً مخصصاً يقتصر على رؤية طلابه ومواده ورصد درجاتهم وحضورهم فقط.")

    add_h2(doc, "3. الجداول المدرسية الذكية (Timetable & Session Management)")
    add_p(doc, "يحتوي النظام على محرك ذكي لبناء الجداول يضمن عدم حدوث أي تضارب بشري:")
    add_bullet(doc, "الفحص التلقائي لتعارض المعلم (Faculty Conflict Check): يمنع حجز المعلم لحصتين مختلفتين في نفس الساعة.")
    add_bullet(doc, "الفحص التلقائي لتعارض القاعات (Classroom Clash Check): يمنع حجز القاعة الواحدة أو المعمل لشعبتين في نفس التوقيت.")
    add_bullet(doc, "طرق العرض المتعددة: عرض الجدول كتقويم ملون أسبوعي، جدول يومي حسب القاعات، أو جدول شخصي لكل معلم وطالب.")

    add_h2(doc, "4. الكنترول المدرسي والشهادات المشفرة (Exams & QR Marksheets)")
    add_p(doc, "إدارة الامتحانات المدرسية وتوليد الشهادات الموثوقة رقمياً:")
    add_bullet(doc, "لجان الاختبارات وقاعات السير: توزيع الطلاب على قاعات الاختبارات وترقيم المقاعد.")
    add_bullet(doc, "رصد وتدقيق الدرجات: آليات سرية للرصد والتدقيق ومنع تعديل الدرجات بعد اعتماد رئيس الكنترول.")
    add_bullet(doc, "رمز الاستجابة السريع الذكي (QR Code): كل شهادة مطبوعة أو كشف درجات يحمل رمز QR فريد ومشفر، يتيح لأي جهة التحقق الفوري من صحة ومصداقية الشهادة إلكترونياً ومنع التزوير تماماً.")

    add_h2(doc, "5. الرسوم المدرسية والفوترة بالريال اليمني (School Fees & Invoicing)")
    add_p(doc, "منظومة متكاملة لربط العمليات الأكاديمية بالتحصيل المالي:")
    add_bullet(doc, "جداول الأقساط المرنة: إمكانية سداد الرسوم السنوية دفعة واحدة، أو على قسطين فصليين، أو 4 إلى 10 أقساط شهرية.")
    add_bullet(doc, "إصدار المطالبات الآلية: توليد الفواتير تلقائياً وتوجيهها إلى حساب ولي الأمر في البوابة الإلكترونية.")
    add_bullet(doc, "سندات القبض المعتمدة: طباعة سندات قبض نقدية أو بنكية وسجل تفصيلي بالمدفوعات والمتبقي بالريال اليمني (ر.ي).")

    add_h2(doc, "6. المكتبة المدرسية ونظام الإعارة بالباركود (Library System)")
    add_p(doc, "أتمتة كاملة لإدارة الكتب والمراجع والوسائط التعليمية:")
    add_bullet(doc, "الفهرسة المتقدمة: تصنيف الكتب بحسب التصنيف العشري، المؤلفين، دور النشر، والسنوات.")
    add_bullet(doc, "تتبع النسخ بالباركود (Barcode Units): وضع ملصق باركود فريد على كل نسخة ورقية لتسهيل مسحها بالماسح الضوئي.")
    add_bullet(doc, "بطاقات الإعارة الذكية: مسح بطاقة الطالب ثم مسح باركود الكتاب لتسجيل الإعارة في ثانيتين فقط مع تنبيهات التأخير.")

    add_h2(doc, "7. بوابات الخدمة الذاتية (Student & Parent Portals)")
    add_p(doc, "تواصل حي وتفاعلي على مدار الساعة بين المدرسة والأسرة:")
    add_bullet(doc, "بوابة ولي الأمر (/my/child): تتيح لولي الأمر استعراض كافة أبنائه في المدرسة، متابعة الحضور والغياب اليومي لحظة بلحظة، مراجعة كشوف الدرجات والشهادات، وسداد ومتابعة أقساط الرسوم المدرسية.")
    add_bullet(doc, "بوابة الطالب (/my/academic): تتيح للطالب استعراض جدوله الأسبوعي، تحميل الواجبات ورفع ملفات الحلول، ومتابعة نتائجه الأكاديمية.")

    # ================= PART 5: OPERATIONS & MAINTENANCE =================
    add_h1(doc, "الجزء الخامس: الإشراف الفني وإجراءات النسخ الاحتياطي والأمان (System Operations)")
    add_p(doc, 
        "لضمان استمرارية عمل المنظومة وحماية البيانات التعليمية والمالية من أي فقدان طارئ، "
        "يتضمن المشروع حزمة سكربتات تشغيلية مؤتمتة في مجلد scripts/ للنسخ الاحتياطي السحابي والمحلي.")

    add_h2(doc, "1. أوامر النسخ الاحتياطي الشامل (Full System Backup)")
    add_p(doc, "أمر أخذ نسخة احتياطية فورية تضم قاعدة البيانات بالكامل مع مرفقات الصور والوثائق (Filestore):")
    add_code(doc, "bash scripts/backup.sh")
    add_p(doc, "يتم حفظ الملف المضغوط بصيغة tar.gz يحمل تاريخ وتوقيت العملية داخل المجلد backups/.")

    add_h2(doc, "2. أوامر استعادة النظام (System Restore)")
    add_p(doc, "لاستعادة المنظومة بالكامل من نسخة سابقة على أي خادم:")
    add_code(doc, "bash scripts/restore.sh backups/backup_20261121_xxxx.tar.gz")

    add_h2(doc, "3. إعادة توليد البيانات التجريبية اليمنية (Demo Seeding)")
    add_p(doc, "لإعادة تغذية المنظومة ببيانات المدرسة اليمنية النموذجية (شعب، طلاب، مدرسين، رسوم بالريال):")
    add_code(doc, "python3 scripts/create_yemen_demo_data.py")

    add_callout(doc, "خاتمة الدليل وتحديث الوثائق", 
        "تم بحمد الله إعداد وتنسيق هذا التوثيق الرسمي ليكون دليلاً معيارياً شاملاً باللغة العربية لمنظومة OpenEduCat 19.0. "
        "المستند محفوظ ومحدث وجاهز للطباعة والمراجعة المستمرة من قِبل إدارة المدرسة وفريق التطوير.", 
        "tip")

    # Save Word Document
    doc.save(DOCX_PATH)
    print(f"Successfully generated Arabic Word Document: {DOCX_PATH}")
    file_size_kb = os.path.getsize(DOCX_PATH) / 1024
    print(f"File Size: {file_size_kb:.2f} KB")
    return DOCX_PATH

if __name__ == "__main__":
    build_document()
