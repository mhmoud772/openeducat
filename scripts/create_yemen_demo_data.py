#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive, realistic, fully-interconnected demo data
for Yemeni educational system (مدارس النهضة النموذجية الأهلية - اليمن).
"""
import odoo
from odoo.modules.registry import Registry
from datetime import datetime, date, timedelta
import random

odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'openeducat'])
registry = Registry('openeducat')

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    print("=" * 60)
    print("🚀 بدء إنشاء البيانات التجريبية الشاملة - المدارس الأهلية في اليمن")
    print("=" * 60)

    # 1. Update Company to Yemen School Profile
    company = env['res.company'].browse(1)
    company.write({
        'name': 'مدارس النهضة النموذجية الأهلية الحديثة',
        'email': 'info@alnahda-yemen.edu.ye',
        'phone': '+967 1 445566',
        'website': 'https://alnahda-yemen.edu.ye',
    })
    c_partner = company.partner_id
    c_partner.write({
        'name': 'مدارس النهضة النموذجية الأهلية الحديثة',
        'city': 'صنعاء',
        'street': 'شارع الستين الغربي - جوار جولة مذبح',
        'country_id': 245, # Yemen
        'phone': '+967 1 445566',
    })
    print("✅ 1. تم تحديث بيانات المنشأة والمدرسة (صنعاء، اليمن)")

    # 2. Academic Year & Semesters
    year = env['op.academic.year'].search([], limit=1)
    if not year:
        year = env['op.academic.year'].create({
            'name': 'العام الدراسي 2026-2027 م',
            'code': 'AY-2026-27',
            'start_date': date(2026, 8, 25),
            'end_date': date(2027, 6, 15),
        })
    else:
        year.write({
            'name': 'العام الدراسي 2026-2027 م',
            'start_date': date(2026, 8, 25),
            'end_date': date(2027, 6, 15),
        })

    # Terms
    t1 = env['op.academic.term'].search([('name', 'like', 'الأول')], limit=1)
    if not t1:
        t1 = env['op.academic.term'].create({
            'name': 'الفصل الدراسي الأول',
            'academic_year_id': year.id,
            'term_start_date': date(2026, 8, 25),
            'term_end_date': date(2027, 1, 15),
        })
    else:
        t1.write({
            'term_start_date': date(2026, 8, 25),
            'term_end_date': date(2027, 1, 15),
            'academic_year_id': year.id,
        })

    t2 = env['op.academic.term'].search([('name', 'like', 'الثاني')], limit=1)
    if not t2:
        t2 = env['op.academic.term'].create({
            'name': 'الفصل الدراسي الثاني',
            'academic_year_id': year.id,
            'term_start_date': date(2027, 1, 25),
            'term_end_date': date(2027, 6, 10),
        })
    else:
        t2.write({
            'term_start_date': date(2027, 1, 25),
            'term_end_date': date(2027, 6, 10),
            'academic_year_id': year.id,
        })
    print(f"✅ 2. العام الدراسي والفصلين: {year.name} ({t1.name} و {t2.name})")

    # 3. Classrooms
    classrooms = {}
    cr_data = [
        ('قاعة الخوارزمي (الثالث الثانوي علمي)', 'CR-SEC-01', 35),
        ('قاعة القدس (معمل الحاسوب الرئيسي)', 'LAB-COMP', 40),
        ('قاعة ابن سينا (معمل العلوم والكيمياء)', 'LAB-SCI', 35),
        ('قاعة المتنبي (الصف التاسع الأساسي)', 'CR-BAS-09', 35),
        ('قاعة بلقيس (الصف الأول الأساسي)', 'CR-PRI-01', 30),
    ]
    for c_name, c_code, c_cap in cr_data:
        cr_rec = env['op.classroom'].search([('name', '=', c_name)], limit=1)
        if not cr_rec:
            cr_rec = env['op.classroom'].create({
                'name': c_name,
                'code': c_code,
                'capacity': c_cap,
            })
        classrooms[c_code] = cr_rec
    print(f"✅ 3. القاعات والمعامل الدراسية ({len(classrooms)} قاعات)")

    # 4. Courses and Batches
    # Get courses
    c_pri1 = env['op.course'].search([('code', '=', 'PRI-G01')], limit=1)
    c_bas9 = env['op.course'].search([('code', '=', 'BAS-G09')], limit=1)
    c_sec3_sci = env['op.course'].search([('code', '=', 'SEC-G03-SCI')], limit=1)
    c_sec3_lit = env['op.course'].search([('code', '=', 'SEC-G03-LIT')], limit=1)

    batches = {}
    batch_data = [
        ('شعبة (أ) - الصف الأول الأساسي', 'B-PRI-01-A', c_pri1.id if c_pri1 else False),
        ('شعبة (أ) - الصف التاسع الأساسي', 'B-BAS-09-A', c_bas9.id if c_bas9 else False),
        ('شعبة (ب) - الصف التاسع الأساسي', 'B-BAS-09-B', c_bas9.id if c_bas9 else False),
        ('شعبة (أ) - الثالث الثانوي (علمي)', 'B-SEC-03-A', c_sec3_sci.id if c_sec3_sci else False),
        ('شعبة (أ) - الثالث الثانوي (أدبي)', 'B-SEC-03-LIT', c_sec3_lit.id if c_sec3_lit else False),
    ]
    for b_name, b_code, b_course in batch_data:
        if not b_course:
            continue
        b_rec = env['op.batch'].search([('code', '=', b_code)], limit=1)
        if not b_rec:
            b_rec = env['op.batch'].create({
                'name': b_name,
                'code': b_code,
                'course_id': b_course,
                'start_date': date(2026, 8, 25),
                'end_date': date(2027, 6, 15),
            })
        batches[b_code] = b_rec
    print(f"✅ 4. الشعب الدراسية ({len(batches)} شعب)")

    # 5. Faculty Members (Yemeni Names)
    faculty_data = [
        ('صادق', 'محمد', 'علي', 'الحكيمي', 'أ. صادق محمد الحكيمي', 'sadeq.hakeemi@alnahda-yemen.edu.ye', '771122334', 'male'),
        ('فؤاد', 'عبدالله', 'سالم', 'باوزير', 'أ. فؤاد عبدالله باوزير', 'fouad.bawazir@alnahda-yemen.edu.ye', '772233445', 'male'),
        ('نبيل', 'أحمد', 'قاسم', 'الشميري', 'أ. نبيل أحمد الشميري', 'nabil.shumairi@alnahda-yemen.edu.ye', '773344556', 'male'),
        ('طارق', 'علي', 'حسن', 'الأكوع', 'أ. طارق علي الأكوع', 'tariq.akwa@alnahda-yemen.edu.ye', '774455667', 'male'),
        ('مروان', 'قائد', 'سعيد', 'الصبري', 'أ. مروان قائد الصبري', 'marwan.sabri@alnahda-yemen.edu.ye', '775566778', 'male'),
        ('بشرى', 'يحيى', 'عبدالله', 'المتوكل', 'أ. بشرى يحيى المتوكل', 'bushra.mutawakil@alnahda-yemen.edu.ye', '776677889', 'female'),
    ]
    faculties = {}
    for fn, mn, tn, ln, full_name, email, phone, gender in faculty_data:
        f_rec = env['op.faculty'].search([('first_name', '=', fn), ('last_name', '=', ln)], limit=1)
        if not f_rec:
            partner = env['res.partner'].create({
                'name': full_name,
                'email': email,
                'phone': phone,
                'is_company': False,
                'country_id': 245,
            })
            f_rec = env['op.faculty'].create({
                'partner_id': partner.id,
                'first_name': fn,
                'middle_name': mn,
                'third_name': tn,
                'last_name': ln,
                'gender': gender,
                'blood_group': 'O+',
                'birth_date': date(1985, 5, 10),
                'nationality': 245,
            })
        faculties[ln] = f_rec
    print(f"✅ 5. الكادر التعليمي والإداري ({len(faculties)} معلمين)")

    # 6. Parents (Yemeni Guardians)
    parents_info = [
        ('م. صادق محمد الحكيمي', 'sadeq.guardian@gmail.com', '771234567', 'مهندس برمجيات ونظم'),
        ('د. عبدالرحمن سالم باعباد', 'baabad.doc@gmail.com', '777654321', 'أستاذ جامعي'),
        ('أ. مروان قائد الصبري', 'marwan.parent@gmail.com', '733112233', 'رئيس قسم تقنية المعلومات'),
        ('أ. طارق علي الأكوع', 'tariq.parent@gmail.com', '711445566', 'مهندس كيميائي'),
    ]
    parents = {}
    for p_name, p_email, p_mobile, job in parents_info:
        p_partner = env['res.partner'].search([('name', '=', p_name)], limit=1)
        if not p_partner:
            p_partner = env['res.partner'].create({
                'name': p_name,
                'email': p_email,
                'phone': p_mobile,
                'function': job,
                'country_id': 245,
            })
        parent_rec = env['op.parent'].search([('name', '=', p_partner.id)], limit=1)
        if not parent_rec:
            parent_rec = env['op.parent'].create({
                'name': p_partner.id,
                'mobile': p_mobile,
                'relationship_id': 1,
            })
        parents[p_name] = parent_rec
    print(f"✅ 6. أولياء الأمور ({len(parents)} أولياء أمور)")

    # 7. Students (Linked to Batches and Parents)
    student_specs = [
        # Secondary 3 (Scientific)
        ('أسامة', 'صادق', 'محمد', 'الحكيمي', 'YEM-2026-101', 'm', date(2008, 4, 15), c_sec3_sci.id, batches.get('B-SEC-03-A').id, parents.get('م. صادق محمد الحكيمي'), '1'),
        ('هشام', 'عبدالرحمن', 'سالم', 'باعباد', 'YEM-2026-102', 'm', date(2008, 6, 20), c_sec3_sci.id, batches.get('B-SEC-03-A').id, parents.get('د. عبدالرحمن سالم باعباد'), '2'),
        # Basic 9 (9th Grade - Basic Certificate)
        ('حمزة', 'نبيل', 'أحمد', 'الشميري', 'YEM-2026-201', 'm', date(2011, 2, 10), c_bas9.id, batches.get('B-BAS-09-A').id, None, '1'),
        ('آية', 'مروان', 'قائد', 'الصبري', 'YEM-2026-202', 'f', date(2011, 8, 5), c_bas9.id, batches.get('B-BAS-09-A').id, parents.get('أ. مروان قائد الصبري'), '2'),
        # Basic 1 (Elementary 1)
        ('عبدالله', 'طارق', 'علي', 'الأكوع', 'YEM-2026-301', 'm', date(2019, 5, 12), c_pri1.id, batches.get('B-PRI-01-A').id, parents.get('أ. طارق علي الأكوع'), '1'),
        ('مريم', 'صادق', 'محمد', 'الحكيمي', 'YEM-2026-302', 'f', date(2019, 9, 18), c_pri1.id, batches.get('B-PRI-01-A').id, parents.get('م. صادق محمد الحكيمي'), '2'),
    ]

    students = []
    for fn, mn, tn, ln, gr, gdr, bdate, crs_id, btc_id, parent_obj, roll in student_specs:
        std = env['op.student'].search([('gr_no', '=', gr)], limit=1)
        full_n = f"{fn} {mn} {tn} {ln}"
        if not std:
            spartner = env['res.partner'].create({
                'name': full_n,
                'email': f"{gr.lower()}@student.alnahda-yemen.edu.ye",
                'country_id': 245,
            })
            std = env['op.student'].create({
                'partner_id': spartner.id,
                'first_name': fn,
                'middle_name': mn,
                'third_name': tn,
                'last_name': ln,
                'gr_no': gr,
                'gender': gdr,
                'birth_date': bdate,
                'blood_group': 'O+',
                'nationality': 245,
                'id_type': 'national_id',
                'id_number': f"0101{random.randint(100000, 999999)}",
            })
        
        # Course Detail
        cd = env['op.student.course'].search([('student_id', '=', std.id), ('batch_id', '=', btc_id)], limit=1)
        if not cd:
            env['op.student.course'].create({
                'student_id': std.id,
                'course_id': crs_id,
                'batch_id': btc_id,
                'academic_years_id': year.id,
                'academic_term_id': t1.id,
                'roll_number': roll,
                'state': 'running',
            })
        
        # Link to Parent
        if parent_obj and std not in parent_obj.student_ids:
            parent_obj.write({'student_ids': [(4, std.id)]})

        students.append(std)
    print(f"✅ 7. ملفات وسجلات الطلاب ({len(students)} طلاب مسجلين ومنتظمين)")

    # 8. Weekly Timetable / Sessions
    subj_mth = env['op.subject'].search([('code', '=', 'MTH-101')], limit=1)
    subj_phy = env['op.subject'].search([('code', '=', 'PHY-201')], limit=1)
    subj_isl = env['op.subject'].search([('code', '=', 'ISL-101')], limit=1)
    subj_arb = env['op.subject'].search([('code', '=', 'ARB-101')], limit=1)
    subj_eng = env['op.subject'].search([('code', '=', 'ENG-101')], limit=1)
    subj_dig = env['op.subject'].search([('code', '=', 'DIG-101')], limit=1)

    batch_sec3 = batches.get('B-SEC-03-A')
    f_hakeemi = faculties.get('الحكيمي')
    f_bawazir = faculties.get('باوزير')
    f_shumairi = faculties.get('الشميري')

    # Create sessions for this week
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    session_count = 0
    if batch_sec3 and f_hakeemi:
        for day_offset in range(5): # Sunday to Thursday in Yemen
            session_date = start_week + timedelta(days=day_offset)
            s_time = datetime.combine(session_date, datetime.min.time()) + timedelta(hours=8)
            e_time = s_time + timedelta(minutes=45)
            
            sess = env['op.session'].search([
                ('batch_id', '=', batch_sec3.id),
                ('start_datetime', '=', s_time)
            ], limit=1)
            if not sess:
                env['op.session'].create({
                    'name': f"حصة الرياضيات - {batch_sec3.name}",
                    'course_id': c_sec3_sci.id,
                    'batch_id': batch_sec3.id,
                    'subject_id': subj_mth.id,
                    'faculty_id': f_hakeemi.id,
                    'classroom_id': classrooms.get('CR-SEC-01').id,
                    'start_datetime': s_time,
                    'end_datetime': e_time,
                    'type': 'theory',
                })
                session_count += 1
    print(f"✅ 8. الجدول المدرسي والحصص المجدولة ({session_count} حصص لهذا الأسبوع)")

    # 9. Attendance Sheets & Records
    att_reg = env['op.attendance.register'].search([('name', 'like', 'الثالث الثانوي')], limit=1)
    if not att_reg and batch_sec3:
        att_reg = env['op.attendance.register'].create({
            'name': 'كشف حضور - الثالث الثانوي (علمي)',
            'code': 'REG-SEC3-SCI',
            'course_id': c_sec3_sci.id,
            'batch_id': batch_sec3.id,
        })

    att_lines_count = 0
    if att_reg:
        # Create attendance sheets for past 5 days
        for d_i in range(5):
            att_d = today - timedelta(days=d_i + 1)
            sheet = env['op.attendance.sheet'].search([
                ('register_id', '=', att_reg.id),
                ('attendance_date', '=', att_d)
            ], limit=1)
            if not sheet:
                sheet = env['op.attendance.sheet'].create({
                    'register_id': att_reg.id,
                    'attendance_date': att_d,
                    'state': 'done',
                })
                # Lines for students in Sec 3
                for s in students[:2]:
                    # Most are present, 1 late occasionally
                    is_late = (d_i == 2 and s.first_name == 'هشام')
                    env['op.attendance.line'].create({
                        'attendance_id': sheet.id,
                        'student_id': s.id,
                        'attendance_date': att_d,
                        'present': not is_late,
                        'absent': False,
                        'late': is_late,
                        'excused': False,
                        'remark': 'تأخر 10 دقائق بسبب المواصلات' if is_late else 'حاضر ومنضبط',
                    })
                    att_lines_count += 1
    print(f"✅ 9. دفاتر الحضور وسجلات الغياب اليومية ({att_lines_count} سجل حضور مرصود)")

    # 10. Exams & Marksheets (Yemeni Control)
    ex_session = env['op.exam.session'].search([('name', 'like', 'نصف العام')], limit=1)
    if not ex_session:
        ex_session = env['op.exam.session'].create({
            'name': 'اختبارات نصف العام 2026-2027 م',
            'course_id': c_sec3_sci.id,
            'batch_id': batch_sec3.id,
            'exam_type': 5,
            'evaluation_type': 'normal',
            'exam_code': 'EX-MID-2026',
            'start_date': date(2027, 1, 5),
            'end_date': date(2027, 1, 15),
        })

    # Exam for Math
    ex_math = env['op.exam'].search([('session_id', '=', ex_session.id), ('subject_id', '=', subj_mth.id)], limit=1)
    if not ex_math:
        ex_math = env['op.exam'].create({
            'session_id': ex_session.id,
            'name': 'اختبار الرياضيات - نصف العام',
            'exam_code': 'EX-MTH-MID',
            'subject_id': subj_mth.id,
            'total_marks': 100.0,
            'min_marks': 50.0,
            'start_time': datetime(2027, 1, 6, 8, 0),
            'end_time': datetime(2027, 1, 6, 10, 0),
        })
        # Attendees
        env['op.exam.attendees'].create({
            'exam_id': ex_math.id,
            'student_id': students[0].id,
            'marks': 96.0,
            'status': 'present',
        })
        env['op.exam.attendees'].create({
            'exam_id': ex_math.id,
            'student_id': students[1].id,
            'marks': 91.0,
            'status': 'present',
        })
    print("✅ 10. بنك الاختبارات ودرجات الكنترول المدرسي (رياضيات 96% و 91%)")

    # 11. Library Books & Movements
    media_type = env['op.media.type'].search([('code', '=', 'BOOK')], limit=1)
    if not media_type:
        media_type = env['op.media.type'].create({
            'name': 'كتب ومراجع دراسية',
            'code': 'BOOK',
        })

    author_yam = env['op.author'].search([('name', 'like', 'الهمداني')], limit=1)
    if not author_yam:
        author_yam = env['op.author'].create({'name': 'أبو محمد الحسن الهمداني'})

    book_data = [
        ('كتاب الإكليل (تاريخ اليمن وأنساب حمير)', 'BK-YEM-01', '978-999-101', author_yam.id),
        ('الفيزياء الحديثة للمرحلة الثانوية والجامعية', 'BK-PHY-02', '978-999-102', False),
        ('قواعد النحو العربي التطبيقي وتيسير الإعراب', 'BK-ARB-03', '978-999-103', False),
        ('أساسيات البرمجة بلغة بايثون والذكاء الاصطناعي', 'BK-CS-04', '978-999-104', False),
    ]
    media_count = 0
    for b_title, b_code, b_isbn, a_id in book_data:
        m_rec = env['op.media'].search([('isbn', '=', b_isbn)], limit=1)
        if not m_rec:
            m_rec = env['op.media'].create({
                'name': b_title,
                'isbn': b_isbn,
                'author_ids': [(4, a_id)] if a_id else [],
                'internal_code': b_code,
                'media_type_id': media_type.id,
            })
            # Create unit
            env['op.media.unit'].create({
                'name': f"{b_title} - النسخة الأصلية 1",
                'media_id': m_rec.id,
                'media_type_id': media_type.id,
                'barcode': b_code,
                'state': 'available',
            })
            media_count += 1
    print(f"✅ 11. المكتبة والكتب والمراجع المدرسية ({media_count} عناوين مع وحدات الباركود)")

    # 12. School Fees in YER
    fee_product = env['product.product'].search([('name', '=', 'الرسوم المدرسية والأقساط السنوية')], limit=1)
    if not fee_product:
        fee_product = env['product.product'].create({
            'name': 'الرسوم المدرسية والأقساط السنوية',
            'type': 'service',
            'list_price': 350000.0, # 350,000 YER
            'property_account_income_id': 157,
        })

    # Invoices in YER for parents
    journal = env['account.journal'].search([('type', '=', 'sale')], limit=1)
    invoices_created = 0
    for p_name, parent_rec in list(parents.items())[:2]:
        p_partner = parent_rec.name
        # Check existing invoice
        inv = env['account.move'].search([
            ('partner_id', '=', p_partner.id),
            ('move_type', '=', 'out_invoice')
        ], limit=1)
        if not inv and journal:
            inv = env['account.move'].create({
                'partner_id': p_partner.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_date': date(2026, 9, 1),
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': fee_product.id,
                        'account_id': 157,
                        'name': f"القسط المدرسي الأول (2026-2027) - لولي الأمر {p_partner.name}",
                        'quantity': 1,
                        'price_unit': 350000.0, # 350,000 YER
                    })
                ]
            })
            try:
                inv.action_post()
            except Exception as e:
                print(f"تنبيه عند اعتماد الفاتورة: {e}")
            invoices_created += 1
    print(f"✅ 12. الفواتير والرسوم المدرسية المعتمدة بالريال اليمني ({invoices_created} فواتير بمبلغ 350,000 ر.ي)")

    # 13. School Activities
    act_type = env['op.activity.type'].search([], limit=1)
    if not act_type:
        act_type = env['op.activity.type'].create({'name': 'أنشطة لا منهجية وثقافية'})

    act1 = env['op.activity'].search([('student_id', '=', students[0].id)], limit=1)
    if not act1:
        env['op.activity'].create({
            'type_id': act_type.id,
            'date': date(2026, 10, 20),
            'student_id': students[0].id,
            'faculty_id': faculties.get('باوزير').id,
            'description': 'المسابقة السنوية الكبرى لحفظ وتلاوة القرآن الكريم - فاز الطالب أسامة الحكيمي بالمركز الأول في فئة حفظ 15 جزءاً برواية حفص عن عاصم.',
        })
    print("✅ 13. الأنشطة المدرسية والمسابقات الثقافية والقرآنية")

    print("=" * 60)
    print("🎉 تم اكتمال إنشاء البيانات التجريبية الشاملة والمترابطة 100% بنجاح!")
    print("=" * 60)
    cr.commit()
