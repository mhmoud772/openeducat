# 📊 تحليل مشروع OpenEduCat ERP

> **نظام إدارة مؤسسات تعليمية مبني على Odoo 19.0**  
> مفتوح المصدر | رخصة LGPL-3 | Python + XML + JavaScript

---

## 🗂️ نظرة عامة على المشروع

**OpenEduCat** هو نظام ERP تعليمي متكامل مبني فوق منصة **Odoo 19.0**. يُغطي إدارة الطلاب، الأعضاء الأكاديميين، المقررات، الامتحانات، الرسوم الدراسية، الحضور والمكتبة — كل ذلك ضمن وحدات (Modules) منفصلة وقابلة للتركيب بشكل مستقل.

---

## 🏗️ هيكل المشروع — الوحدات (Modules)

```
openeducat_erp-19.0/
├── openeducat_core           ← الوحدة الأساسية (الجذر)
├── openeducat_erp            ← وحدة التجميع (Meta-module)
├── openeducat_admission      ← إدارة القبول والتسجيل
├── openeducat_fees           ← إدارة الرسوم المالية
├── openeducat_exam           ← إدارة الامتحانات والنتائج
├── openeducat_attendance     ← إدارة الحضور والغياب
├── openeducat_assignment     ← إدارة الواجبات
├── openeducat_library        ← إدارة المكتبة
├── openeducat_timetable      ← إدارة الجداول الدراسية
├── openeducat_parent         ← بوابة أولياء الأمور
├── openeducat_activity       ← الأنشطة اللاصفية
├── openeducat_classroom      ← إدارة القاعات الدراسية
├── openeducat_facility       ← إدارة المرافق
└── theme_web_openeducat      ← قالب الموقع الإلكتروني
```

---

## 🔗 شجرة الاعتمادية بين الوحدات

```
openeducat_core (الجذر)
    ├── openeducat_fees
    │   └── openeducat_admission ──────────────────┐
    ├── openeducat_exam                             │
    ├── openeducat_attendance                       ├──► openeducat_erp
    ├── openeducat_assignment                       │    (Meta-module)
    ├── openeducat_library                          │
    ├── openeducat_parent ─────────────────────────┘
    ├── openeducat_timetable
    ├── openeducat_classroom
    └── openeducat_facility
```

> ⚠️ **openeducat_core** هو الوحدة الأم — لا يمكن تشغيل أي وحدة أخرى بدونها.

---

## 📋 تفصيل كل وحدة

### 1. `openeducat_core` — الوحدة الأساسية
**يعتمد على:** `board`, `hr`, `web`, `website`, `contacts`

| النموذج | الغرض |
|---|---|
| `op.student` | بيانات الطالب (اسم، تاريخ ميلاد، جنس، رقم تسجيل) |
| `op.student.course` | ربط الطالب بالمقرر والدفعة والرقم الدراسي |
| `op.faculty` | بيانات عضو هيئة التدريس |
| `op.course` | المقررات الدراسية وأنواع التقييم |
| `op.batch` | الدفعات الدراسية |
| `op.subject` | المواد الدراسية |
| `op.department` | الأقسام الأكاديمية |
| `op.academic.year` | السنة الأكاديمية وهيكل الفصول |
| `op.academic.term` | الفصول الدراسية |
| `op.program` | البرامج الأكاديمية |
| `op.category` | تصنيفات الطلاب |
| `op.subject.registration` | تسجيل المواد |

**مميزات خاصة:**
- إنشاء مستخدم Odoo (Portal) مباشرة من سجل الطالب
- إنشاء موظف HR من سجل عضو هيئة التدريس
- ربط كامل بين `res.partner` ↔ `op.student` / `op.faculty`
- تقرير شهادة الطالب (Bonafide Certificate)
- بطاقة هوية الطالب (ID Card Report)
- دعم استيراد Excel للطلاب والأعضاء الأكاديميين

---

### 2. `openeducat_fees` — الرسوم الدراسية
**يعتمد على:** `openeducat_core`, `account`

| النموذج | الغرض |
|---|---|
| `op.student.fees.details` | تفاصيل رسوم الطالب |
| `op.fees.terms` | شروط الدفع |
| `op.fees.terms.line` | بنود الدفع مع التواريخ |
| `op.fees.element` | عناصر الرسوم |

**مميزات خاصة:**
- إنشاء فاتورة Odoo تلقائياً من سجل الرسوم
- دعم الخصومات (Discount %)
- ربط مباشر بـ `account.move` (نظام المحاسبة)
- حساب تلقائي للمبلغ بعد الخصم

---

### 3. `openeducat_admission` — القبول والتسجيل
**يعتمد على:** `openeducat_core`, `openeducat_fees`

**مميزات:**
- سجل القبول (Admission Register)
- إجراءات قبول الطالب الجديد
- تقارير تحليل القبول
- تسلسل تلقائي لأرقام القبول
- تحويل المتقدم إلى طالب مسجل

---

### 4. `openeducat_exam` — الامتحانات
**يعتمد على:** `openeducat_core`

| النموذج | الغرض |
|---|---|
| `op.exam` | الامتحان (مادة، وقت، درجات) |
| `op.exam.session` | جلسة الامتحانات |
| `op.exam.attendees` | حضور الطلاب للامتحان ودرجاتهم |
| `op.exam.room` | قاعات الامتحان |
| `op.exam.type` | أنواع الامتحانات |
| `op.grade.configuration` | تكوين التقديرات |
| `op.marksheet.register` | كشف الدرجات |
| `op.result.template` | قالب النتائج |

**دورة حياة الامتحان:**
```
Draft → Scheduled → Held → Result Updated → Done
                         ↘ Cancel
```

**مميزات خاصة:**
- منع تداخل أوقات الامتحانات لنفس المادة
- التحقق من أن درجة النجاح لا تتجاوز الدرجة الكلية
- إلغاء الامتحان يحذف تلقائياً قوائم الحضور

---

### 5. `openeducat_attendance` — الحضور والغياب
**يعتمد على:** `openeducat_core`

| النموذج | الغرض |
|---|---|
| `op.attendance.register` | سجل الحضور |
| `op.attendance.session` | جلسة حضور |
| `op.attendance.line` | سطر حضور لكل طالب |
| `op.attendance.sheet` | ورقة الحضور |
| `op.attendance.type` | أنواع الحضور |

---

### 6. `openeducat_library` — المكتبة
**يعتمد على:** `openeducat_core`

| النموذج | الغرض |
|---|---|
| `op.library` | بيانات المكتبة |
| `op.media` | الوسائط (كتب، مجلات...) |
| `op.media.unit` | نسخ الوسائط |
| `op.media.movement` | استعارة وإرجاع |
| `op.media.purchase` | شراء الوسائط |
| `op.media.queue` | قائمة انتظار الاستعارة |
| `op.author` | المؤلفون |
| `op.publisher` | دور النشر |
| `op.media.type` | أنواع الوسائط |
| `op.tag` | الوسوم |

---

### 7. الوحدات الأخرى

| الوحدة | الوظيفة |
|---|---|
| `openeducat_timetable` | إنشاء وإدارة الجداول الدراسية |
| `openeducat_assignment` | الواجبات والتسليمات |
| `openeducat_parent` | بوابة أولياء الأمور لمتابعة أبنائهم |
| `openeducat_activity` | الأنشطة الطلابية |
| `openeducat_classroom` | إدارة القاعات الدراسية |
| `openeducat_facility` | إدارة المرافق والبنية التحتية |
| `theme_web_openeducat` | قالب الموقع الرسمي للمؤسسة |

---

## 🔐 نظام الصلاحيات

يعتمد النظام على **3 مستويات صلاحيات**:

| المجموعة | المعرف التقني | الصلاحيات |
|---|---|---|
| **Admin** | `group_op_back_office_admin` | إدارة كاملة + عرض جميع السجلات |
| **User (Faculty)** | `group_op_faculty` | عرض الطلاب + بياناتهم الخاصة |
| **Student (Portal)** | `base.group_portal` | بوابة الطالب فقط |

**قواعد متعددة الشركات:** يدعم النظام العمل بأكثر من شركة/مؤسسة ضمن نفس قاعدة البيانات.

---

## 🌍 اللغات المدعومة

| اللغة | الملف |
|---|---|
| العربية ✅ | `ar_001.po` |
| الألمانية | `de.po` |
| الإسبانية | `es.po` |
| الفرنسية | `fr.po` |
| الروسية | `ru.po` |
| الصينية المبسطة | `zh_CN.po` |
| الفارسية | `fa.po` |
| الدنماركية | `da_DK.po` |
| الإيطالية | `it.po` |
| الهولندية | `nl.po` |
| البرتغالية | `pt.po` |
| الفيتنامية | `vi_VN.po` |
| التايلاندية | `th.po` |

> ✅ **اللغة العربية مدعومة بالكامل** في جميع الوحدات.

---

## ⚡ التقنيات المستخدمة

| التقنية | الاستخدام |
|---|---|
| **Python 3** | نماذج البيانات والمنطق (Backend) |
| **Odoo ORM** | قاعدة البيانات والعلاقات |
| **XML** | تعريف الواجهات والقوائم والتقارير |
| **QWeb** | محرك القوالب للتقارير PDF والموقع |
| **JavaScript / OWL** | مكونات الواجهة التفاعلية |
| **SCSS** | تنسيق الواجهات |
| **PostgreSQL** | قاعدة البيانات |
| **Bootstrap** | إطار CSS للواجهة |

---

## 🐛 مشاكل مكتشفة في الكود

### 1. ~~دالة مكررة في `faculty.py`~~ ✅ **تم الإصلاح**

```diff
  @api.constrains('email')
  def _check_email_unique(self):   # ← النسخة الأولى (محفوظة)
      for record in self:
          ...

- @api.constrains('email')
- def _check_email_unique(self):   # ← النسخة المكررة (محذوفة)
-     for record in self:
-         ...
```

> في Python عند تعريف دالتين بنفس الاسم داخل نفس الكلاس، تُلغي الثانية الأولى — مما يجعل `@api.constrains` الأول لا يُفعَّل أبداً. الإصلاح: **حذف النسخة المكررة** من السطر 94.

### 2. استخدام `res.groups.privilege`
- في ملف `op_security.xml` يستخدم `res.groups.privilege` وهو نموذج جديد في Odoo 19 — يحتاج اختباراً للتأكد من التوافق مع إصدارك.

---

## 💡 نقاط القوة للبيع

| النقطة | التفاصيل |
|---|---|
| 🏗️ **بنية معيارية** | يمكن تثبيت كل وحدة منفصلة حسب احتياج العميل |
| 🌍 **متعدد اللغات** | 13+ لغة مدعومة بما فيها العربية |
| 🏢 **متعدد الشركات** | وحدة واحدة تخدم عدة مؤسسات |
| 🔗 **تكامل كامل مع Odoo** | محاسبة، HR، البريد، الموقع الإلكتروني |
| 📄 **تقارير PDF جاهزة** | بطاقة الطالب، شهادة البونافيد، كشف الدرجات |
| 🔒 **صلاحيات دقيقة** | 3 مستويات صلاحيات بقواعد record-level |
| 📱 **بوابة طلاب وأولياء** | وصول مباشر عبر الإنترنت |
| ⚡ **Odoo 19** | أحدث إصدار من Odoo (2025) |

---

## 🚀 مقترحات التخصيص للبيع

1. **إصلاح الأخطاء المكتشفة** — الدالة المكررة في `faculty.py`
2. **إضافة لوحة تحكم** (Dashboard) بمؤشرات KPI رئيسية
3. **إضافة تقارير Excel/PDF** إضافية (إحصاءات القبول، الأداء الأكاديمي)
4. **بوابة SMS/إشعارات** للطلاب وأولياء الأمور
5. **تخصيص الثيم** بشعار ولون العميل
6. **تعريب كامل** لجميع الواجهات إذا كان السوق المستهدف عربياً
7. **وثيقة تقنية** (Technical Documentation) باللغة العربية

---

## 📁 الملفات المهمة للمطوّر

| الملف | الوصف |
|---|---|
| `openeducat_core/__manifest__.py` | تعريف الوحدة الأساسية |
| `openeducat_erp/__manifest__.py` | وحدة التجميع |
| `openeducat_core/models/student.py` | نموذج الطالب |
| `openeducat_core/models/faculty.py` | نموذج عضو هيئة التدريس |
| `openeducat_core/models/course.py` | نموذج المقررات |
| `openeducat_core/security/op_security.xml` | الصلاحيات والمجموعات |
| `openeducat_fees/models/student.py` | الرسوم الدراسية والفواتير |
| `openeducat_exam/models/exam.py` | نموذج الامتحان |

---

*تم إعداد هذا التقرير بتاريخ: 2026-10-29*
