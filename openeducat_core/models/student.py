###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class OpStudentCourse(models.Model):
    _name = "op.student.course"
    _description = "تفاصيل المراحل والمقررات للطالب"
    _inherit = "mail.thread"
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', 'الطالب',
                                 ondelete="cascade", tracking=True)
    course_id = fields.Many2one('op.course', 'المرحلة / الصف', required=True, tracking=True)
    batch_id = fields.Many2one('op.batch', 'الشعبة / الفصل', tracking=True)
    roll_number = fields.Char('رقم الجلوس', tracking=True)
    subject_ids = fields.Many2many('op.subject', string='المواد الدراسية')
    academic_years_id = fields.Many2one('op.academic.year', 'العام الدراسي')
    academic_term_id = fields.Many2one('op.academic.term', 'الفصل الدراسي')
    state = fields.Selection([('running', 'منتظم / مستمر'),
                              ('finished', 'متخرج / منتهٍ')],
                             string="حالة القيد", default="running")

    _unique_name_roll_number_id = models.Constraint(
        'unique(roll_number,course_id,batch_id,student_id)',
        'يجب أن يكون رقم الجلوس والطالب فريداً لكل شعبة!')
    _unique_name_roll_number_course_id = models.Constraint(
        'unique(roll_number,course_id,batch_id)',
        'يجب أن يكون رقم الجلوس فريداً لكل شعبة!')
    _unique_name_roll_number_student_id = models.Constraint(
        'unique(student_id,course_id,batch_id)',
        'لا يمكن تكرار تسجيل الطالب في نفس الشعبة والمرحلة!')

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Student Course Details'),
            'template': '/openeducat_core/static/xls/op_student_course.xls'
        }]


class OpStudent(models.Model):
    _name = "op.student"
    _description = "Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}

    first_name = fields.Char('الاسم الأول', translate=True, tracking=True)
    middle_name = fields.Char('اسم الأب', translate=True, tracking=True)
    third_name = fields.Char('اسم الجد', translate=True, tracking=True)
    last_name = fields.Char('العائلة / القبيلة', translate=True, tracking=True)
    birth_date = fields.Date('تاريخ الميلاد', tracking=True)
    blood_group = fields.Selection([
        ('A+', 'A+ (موجب)'),
        ('B+', 'B+ (موجب)'),
        ('O+', 'O+ (موجب)'),
        ('AB+', 'AB+ (موجب)'),
        ('A-', 'A- (سالب)'),
        ('B-', 'B- (سالب)'),
        ('O-', 'O- (سالب)'),
        ('AB-', 'AB- (سالب)')
    ], string='فصيلة الدم', tracking=True)
    gender = fields.Selection([
        ('m', 'ذكر'),
        ('f', 'أنثى'),
        ('o', 'أخرى')
    ], 'الجنس', required=True, default='m', tracking=True)
    nationality = fields.Many2one('res.country', 'الجنسية', tracking=True)
    emergency_contact = fields.Many2one('res.partner', 'جهة الاتصال للطوارئ')
    visa_info = fields.Char('معلومات التأشيرة / الإقامة', size=64)
    id_type = fields.Selection([
        ('national_id', 'هوية وطنية'),
        ('iqama', 'إقامة نظامية'),
        ('passport', 'جواز سفر'),
        ('gcc_id', 'هوية خليجية'),
        ('other', 'أخرى'),
    ], string='نوع الوثيقة', default='national_id', tracking=True)
    id_number = fields.Char('رقم الهوية / الإقامة', size=32, tracking=True)
    id_issue_date = fields.Date('تاريخ إصدار الهوية')
    id_expiry_date = fields.Date('تاريخ انتهاء الهوية')
    id_issue_place = fields.Char('مكان الإصدار', size=64)
    partner_id = fields.Many2one('res.partner', 'الشريك',
                                 required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'حساب المستخدم', ondelete="cascade")
    gr_no = fields.Char("رقم القيد", size=20)
    category_id = fields.Many2one('op.category', 'فئة الطالب')
    course_detail_ids = fields.One2many('op.student.course', 'student_id',
                                        'تفاصيل المراحل والمقررات',
                                        tracking=True)
    active = fields.Boolean(default=True)
    certificate_number = fields.Char(
        string='رقم الشهادة / الإفادة',
        readonly=True,
        copy=False,)
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    email = fields.Char(related='partner_id.email', readonly=False)

    _unique_gr_no = models.Constraint('unique(gr_no)',
                                      'يجب أن يكون رقم القيد فريداً لكل طالب!')

    @api.onchange('first_name', 'middle_name', 'third_name', 'last_name')
    def _onchange_name(self):
        parts = [
            (self.first_name or "").strip(),
            (self.middle_name or "").strip(),
            (self.third_name or "").strip(),
            (self.last_name or "").strip(),
        ]
        non_empty = [p for p in parts if p]
        if non_empty:
            self.name = " ".join(non_empty)
        else:
            self.name = "New"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            fname = (vals.get('first_name') or "").strip()
            mname = (vals.get('middle_name') or "").strip()
            tname = (vals.get('third_name') or "").strip()
            lname = (vals.get('last_name') or "").strip()
            parts = [fname, mname, tname, lname]
            non_empty = [p for p in parts if p]
            if non_empty:
                vals['name'] = " ".join(non_empty)
            elif not vals.get('name') or vals.get('name') == 'New':
                vals['name'] = "New"
        return super(OpStudent, self).create(vals_list)

    def write(self, vals):
        res = super(OpStudent, self).write(vals)
        if any(f in vals for f in ('first_name', 'middle_name', 'third_name', 'last_name')):
            for record in self:
                parts = [
                    (record.first_name or "").strip(),
                    (record.middle_name or "").strip(),
                    (record.third_name or "").strip(),
                    (record.last_name or "").strip(),
                ]
                non_empty = [p for p in parts if p]
                if non_empty:
                    full = " ".join(non_empty)
                    if full != record.name:
                        record.name = full
        return res

    def copy(self, default=None):
        raise ValidationError(_('لا يمكن نسخ أو تكرار ملف الطالب.'))

    @api.constrains('id_number', 'id_type')
    def _check_id_number(self):
        for record in self:
            if not record.id_number:
                continue
            id_val = str(record.id_number).strip()

            # Ensure uniqueness among active students
            duplicate = self.search([
                ('id_number', '=', id_val),
                ('id', '!=', record.id),
                ('active', '=', True)
            ], limit=1)
            if duplicate:
                raise ValidationError(_(
                    "رقم الهوية / الإقامة '%(id)s' مسجل مسبقاً للطالب: %(name)s!"
                ) % {'id': id_val, 'name': duplicate.name})

            # Format validation for National ID / Iqama
            if record.id_type in ('national_id', 'iqama'):
                if not id_val.isdigit():
                    raise ValidationError(_(
                        "يجب أن يتكون رقم الهوية أو الإقامة من أرقام فقط!"
                    ))

                country_code = record.nationality.code if record.nationality else False
                if country_code == 'SA' or record.id_type == 'iqama':
                    if len(id_val) != 10:
                        raise ValidationError(_(
                            "رقم الهوية الوطنية أو الإقامة في السعودية يجب أن يتكون من 10 أرقام بالضبط (المدخل: %(len)d أرقام)!"
                        ) % {'len': len(id_val)})
                    if record.id_type == 'national_id' and not id_val.startswith('1'):
                        raise ValidationError(_(
                            "رقم الهوية الوطنية السعودية للمواطنين يجب أن يبدأ بالرقم 1!"
                        ))
                    if record.id_type == 'iqama' and not id_val.startswith('2'):
                        raise ValidationError(_(
                            "رقم الإقامة النظامية للمقيمين يجب أن يبدأ بالرقم 2!"
                        ))
                elif country_code == 'EG':
                    if len(id_val) != 14:
                        raise ValidationError(_(
                            "الرقم القومي لجمهورية مصر العربية يجب أن يتكون من 14 رقماً بالضبط!"
                        ))
                else:
                    if len(id_val) < 8 or len(id_val) > 16:
                        raise ValidationError(_(
                            "رقم الهوية / الإقامة غير صحيح. يجب أن يتراوح طول الرقم بين 8 و 16 رقماً!"
                        ))

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "تاريخ الميلاد لا يمكن أن يكون في المستقبل!"))

    @api.constrains('email')
    def _check_email_unique(self):
        for record in self:
            if record.email:
                duplicate = self.env['res.partner'].search([
                    ('email', '=', record.email),
                    ('id', '!=', record.partner_id.id)
                ], limit=1)
                if duplicate:
                    raise ValidationError(_('البريد الإلكتروني مسجل مسبقاً لمستخدم آخر!'))

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/openeducat_core/static/xls/op_student.xls'
        }]

    def create_student_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'group_ids': user_group,
                    'is_student': True,
                    'tz': self.env.context.get('tz'),
                })
                record.user_id = user_id

    def action_print_id_card(self):
        """طباعة بطاقة هوية الطالب (CR80)"""
        return self.env.ref('openeducat_core.action_report_student_idcard').report_action(self)

    def action_print_bonafide(self):
        """فتح معالج شهادة تعريف طالب (إثبات قيد)"""
        return {
            'name': _('شهادة تعريف طالب (إثبات قيد)'),
            'type': 'ir.actions.act_window',
            'res_model': 'bonafide.certificate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_student_ids': [(6, 0, self.ids)]},
        }

