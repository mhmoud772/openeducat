# 📋 خطة تعديل مشروع OpenEduCat ERP

> خطة مرحلية لتحسين الواجهات والتعريب والتقارير

---

## 📊 الوضع الحالي

| البند | الحالة |
|---|---|
| **عدد الوحدات** | 14 وحدة |
| **ملفات الواجهات (Views)** | 72 ملف XML |
| **ملف RTL** | ✅ موجود (`rtl_arabic.scss` - 240 سطر) |
| **التعريب** | 90%+ مترجم، بعض الإدخالات ناقصة |
| **ملفات SCSS** | 4 ملفات (base, main, style, rtl_arabic) |

---

## 🚀 المراحل

### المرحلة 1: `openeducat_core` — الوحدة الأساسية ⭐

هذه أهم وحدة وتشمل أكبر عدد من الواجهات (19 ملف).

#### 1.1 تحسين نماذج الإدخال (Form Views)

| الملف | التحسينات المقترحة |
|---|---|
| [student_view.xml](file:///media/mahmood/64b0ff99-8470-4277-a10a-63bf21231e635/openeducat_erp-19.0/openeducat_core/views/student_view.xml) | ✅ تنظيم الحقول في tabs واضحة (بيانات شخصية، أكاديمية، عنوان) |
| [faculty_view.xml](file:///media/mahmood/64b0ff99-8470-4277-a10a-63bf21231e635/openeducat_erp-19.0/openeducat_core/views/faculty_view.xml) | ✅ إضافة tab للمواد + القسم |
| [course_view.xml](file:///media/mahmood/64b0ff99-8470-4277-a10a-63bf21231e635/openeducat_erp-19.0/openeducat_core/views/course_view.xml) | ✅ تحسين التخطيط |
| [batch_view.xml](file:///media/mahmood/64b0ff99-8470-4277-a10a-63bf21231e635/openeducat_erp-19.0/openeducat_core/views/batch_view.xml) | ✅ إضافة حقول اختيارية |
| [subject_view.xml](file:///media/mahmood/64b0ff99-8470-4277-a10a-63bf21231e635/openeducat_erp-19.0/openeducat_core/views/subject_view.xml) | ✅ تحسين التخطيط |

#### 1.2 تحسين القوائم (List/Tree Views)
- إضافة `optional="show/hide"` للحقول المهمة
- ترتيب الأعمدة بشكل منطقي
- إضافة ألوان شرطية (decoration) حيث يناسب

#### 1.3 تحسين فلاتر البحث (Search Views)
- إضافة فلاتر `gender` للطلاب والأساتذة
- إضافة فلاتر `course_id` للطلاب
- إضافة فلاتر بالتاريخ (تسجيل حديث، إلخ)
- إضافة `searchpanel` للتصفية الجانبية

#### 1.4 تحسين القوائم والمنيوهات
- ترتيب القوائم بشكل منطقي
- إضافة فواصل (separators) بين المجموعات

#### 1.5 دعم RTL المحسّن
- تحسين ملف `rtl_arabic.scss` الحالي
- إضافة دعم Notebook tabs
- تحسين عرض الـ Many2many tags
- تحسين SearchPanel بالاتجاه العربي

#### 1.6 التعريب الكامل
- ترجمة جميع الإدخالات الناقصة في `ar_001.po`
- مراجعة الترجمات الحالية وتحسينها
- ترجمة placeholders في XML

---

### المرحلة 2: `openeducat_admission` + `openeducat_fees`

#### التحسينات:
- تحسين نموذج القبول (Admission Form)
- تحسين قائمة الرسوم
- إضافة فلاتر حسب الحالة (Draft/Confirmed/Done)
- تحسين التقارير المالية

---

### المرحلة 3: `openeducat_exam` + `openeducat_attendance`

#### التحسينات:
- تحسين واجهة الامتحانات
- إضافة ألوان حسب حالة الامتحان
- تحسين جدول الحضور
- إضافة فلاتر حسب التاريخ والمادة

---

### المرحلة 4: `openeducat_library` + `openeducat_assignment`

#### التحسينات:
- تحسين واجهة المكتبة
- إضافة Kanban view للكتب
- تحسين واجهة الواجبات

---

### المرحلة 5: باقي الوحدات

- `openeducat_timetable` — الجداول
- `openeducat_parent` — أولياء الأمور
- `openeducat_activity` — الأنشطة
- `openeducat_classroom` — القاعات
- `openeducat_facility` — المرافق
- `openeducat_dashboard` — لوحة التحكم

---

### المرحلة 6: التقارير المطبوعة (PDF Reports)

- تحسين تقرير شهادة الطالب (Bonafide Certificate)
- تحسين بطاقة هوية الطالب (ID Card)
- إضافة دعم RTL للتقارير
- تحسين التنسيق والخطوط العربية

---

## 🎯 الأولوية المقترحة للبدء

> [!IMPORTANT]
> أقترح البدء بالمرحلة 1 (`openeducat_core`) لأنها:
> 1. الوحدة الأساسية التي تعتمد عليها كل الوحدات
> 2. تحتوي على أكبر عدد من الواجهات (19 ملف)
> 3. التحسينات فيها ستنعكس على كل النظام

---

*هل تريد البدء بالمرحلة 1؟ أم تفضل ترتيب مختلف؟*
