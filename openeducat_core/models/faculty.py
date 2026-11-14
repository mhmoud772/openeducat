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


class OpFaculty(models.Model):
    _name = "op.faculty"
    _description = "أعضاء هيئة التدريس والمعلمين"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    _parent_name = False

    partner_id = fields.Many2one('res.partner', 'الشريك / جهة الاتصال',
                                 required=True, ondelete="cascade")
    first_name = fields.Char('الاسم الأول', translate=True, required=True)
    middle_name = fields.Char('اسم الأب', size=128)
    third_name = fields.Char('اسم الجد', size=128)
    last_name = fields.Char('العائلة / القبيلة', size=128, required=True)
    birth_date = fields.Date('تاريخ الميلاد', required=True)
    blood_group = fields.Selection([
        ('A+', 'A+ (موجب)'),
        ('B+', 'B+ (موجب)'),
        ('O+', 'O+ (موجب)'),
        ('AB+', 'AB+ (موجب)'),
        ('A-', 'A- (سالب)'),
        ('B-', 'B- (سالب)'),
        ('O-', 'O- (سالب)'),
        ('AB-', 'AB- (سالب)')
    ], string='فصيلة الدم')
    gender = fields.Selection([
        ('male', 'ذكر'),
        ('female', 'أنثى')
    ], 'الجنس', required=True)
    nationality = fields.Many2one('res.country', 'الجنسية')
    emergency_contact = fields.Many2one(
        'res.partner', 'جهة الاتصال للطوارئ')
    visa_info = fields.Char('معلومات التأشيرة / الإقامة', size=64)
    id_type = fields.Selection([
        ('national_id', 'هوية وطنية'),
        ('iqama', 'إقامة نظامية'),
        ('passport', 'جواز سفر'),
        ('gcc_id', 'هوية خليجية'),
        ('other', 'أخرى'),
    ], string='نوع الوثيقة', default='national_id', tracking=True)
    id_number = fields.Char('رقم الهوية الوطنية / الإقامة', size=64, tracking=True)
    id_issue_date = fields.Date('تاريخ إصدار الهوية')
    id_expiry_date = fields.Date('تاريخ انتهاء الهوية')
    id_issue_place = fields.Char('مكان إصدار الهوية', size=64)
    login = fields.Char(
        'اسم المستخدم', related='partner_id.user_id.login', readonly=True)
    last_login = fields.Datetime('آخر تسجيل دخول', readonly=True,
                                 related='partner_id.user_id.login_date')
    faculty_subject_ids = fields.Many2many('op.subject', string='المواد والمقررات الدراسية',
                                           tracking=True)
    emp_id = fields.Many2one('hr.employee', 'ملف الموظف (HR)')
    main_department_id = fields.Many2one(
        'op.department', 'القسم الأكاديمي الأساسي',
        default=lambda self:
        self.env.user.dept_id and self.env.user.dept_id.id or False)
    allowed_department_ids = fields.Many2many(
        'op.department', string='الأقسام المصرح بها',
        default=lambda self:
        self.env.user.department_ids and self.env.user.department_ids.ids or False)
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    email = fields.Char(related='partner_id.email', readonly=False)
    active = fields.Boolean(default=True)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "تاريخ الميلاد لا يمكن أن يكون في المستقبل!"))

    @api.constrains('id_number', 'id_type')
    def _check_id_number(self):
        for record in self:
            if not record.id_number:
                continue
            id_val = str(record.id_number).strip()
            duplicate = self.search([
                ('id_number', '=', id_val),
                ('id', '!=', record.id),
                ('active', '=', True)
            ], limit=1)
            if duplicate:
                raise ValidationError(_(
                    "رقم الهوية / الإقامة '%(id)s' مسجل مسبقاً للمعلم: %(name)s!"
                ) % {'id': id_val, 'name': duplicate.name})

            if record.id_type in ('national_id', 'iqama'):
                if not id_val.isdigit():
                    raise ValidationError(_("يجب أن يتكون رقم الهوية أو الإقامة من أرقام فقط!"))
                country_code = record.nationality.code if record.nationality else False
                if country_code == 'SA' or record.id_type == 'iqama':
                    if len(id_val) != 10:
                        raise ValidationError(_(
                            "رقم الهوية الوطنية أو الإقامة في السعودية يجب أن يتكون من 10 أرقام بالضبط (المدخل: %(len)d أرقام)!"
                        ) % {'len': len(id_val)})
                    if record.id_type == 'national_id' and not id_val.startswith('1'):
                        raise ValidationError(_("رقم الهوية الوطنية السعودية للمواطنين يجب أن يبدأ بالرقم 1!"))
                    if record.id_type == 'iqama' and not id_val.startswith('2'):
                        raise ValidationError(_("رقم الإقامة النظامية للمقيمين يجب أن يبدأ بالرقم 2!"))

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

    def copy(self, default=None):
        raise ValidationError(_('لا يمكن نسخ أو تكرار سجل المعلم.'))

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
            if not vals.get('name') or vals.get('name') == 'New':
                fname = (vals.get('first_name') or "").strip()
                mname = (vals.get('middle_name') or "").strip()
                tname = (vals.get('third_name') or "").strip()
                lname = (vals.get('last_name') or "").strip()
                parts = [fname, mname, tname, lname]
                non_empty = [p for p in parts if p]
                if non_empty:
                    vals['name'] = " ".join(non_empty)
                else:
                    vals['name'] = "New"
        return super(OpFaculty, self).create(vals_list)

    def write(self, vals):
        res = super(OpFaculty, self).write(vals)
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

    def create_employee(self):
        for record in self:
            # If this faculty is already linked to an internal user
            # (via `res.users.partner_id = faculty.partner_id`), reuse
            # it on the new hr.employee instead of creating a fresh
            # employee with no user link. Without this, the "Create
            # User?" prompt on the employee form would appear even
            # though a user already exists, and picking "no" left
            # the employee with `user_id = False` — the whole
            # faculty↔employee↔user chain fell apart, breaking
            # anything downstream that walks `emp_id.user_id`
            # (Time Off manager assignments, appraisal owners, etc.).
            existing_user = self.env['res.users'].sudo().search(
                [('partner_id', '=', record.partner_id.id)], limit=1,
            )
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'sex': record.gender,
            }
            if existing_user:
                vals['user_id'] = existing_user.id
                # `work_contact_id` is hr.employee's canonical partner
                # link in Odoo 19 (replaced `address_home_id`). Point
                # it at the faculty's partner so the employee card
                # shows the same contact block instead of Odoo
                # auto-creating an empty duplicate partner.
                vals['work_contact_id'] = record.partner_id.id
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'partner_share': True, 'employee': True})

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Faculties'),
            'template': '/openeducat_core/static/xls/op_faculty.xls'
        }]


class PartnerTitle(models.Model):
    _name = 'res.partner.title'
    _order = 'name'
    _description = 'Partner Title'

    name = fields.Char(string='Title', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

    @api.depends('shortcut')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.shortcut}"


class ResPartner(models.Model):
    _inherit = "res.partner"

    title: PartnerTitle = fields.Many2one('res.partner.title')
