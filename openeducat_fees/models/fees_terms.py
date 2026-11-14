##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
##############################################################################

from odoo import _, api, exceptions, fields, models


class OpFeesTermsLine(models.Model):
    _name = "op.fees.terms.line"
    _rec_name = "due_days"
    _description = "بند قسط دراسي"

    due_days = fields.Integer('أيام الاستحقاق')
    due_date = fields.Date('تاريخ الاستحقاق')
    value = fields.Float('نسبة القسط (%)')
    fees_element_line = fields.One2many("op.fees.element",
                                        "fees_terms_line_id", "بنود الرسوم")
    fees_id = fields.Many2one('op.fees.terms', 'خطة الرسوم')


class OpFeesTerms(models.Model):
    _name = "op.fees.terms"
    _inherit = "mail.thread"
    _description = "خطة الرسوم والأقساط الدراسية"

    name = fields.Char('مسمى خطة الرسوم', required=True)
    active = fields.Boolean('نشط', default=True)
    fees_terms = fields.Selection([('fixed_days', 'أقساط دورية (بالأيام)'),
                                   ('fixed_date', 'أقساط بتواريخ محددة')],
                                  string='نوع خطة السداد', default='fixed_days')
    code = fields.Char('رمز الخطة', required=True)
    note = fields.Text('الوصف والشروط')
    company_id = fields.Many2one('res.company', 'المدرسة', required=True,
                                 default=lambda s: s.env.user.company_id)
    no_days = fields.Integer('عدد الأيام')
    day_type = fields.Selection([('before', 'قبل'), ('after', 'بعد')],
                                'النوع')
    line_ids = fields.One2many('op.fees.terms.line', 'fees_id', 'جدول الأقساط')
    discount = fields.Float(string='نسبة الخصم المسموح بها (%)',
                            digits='Discount', default=0.0)

    @api.constrains("line_ids")
    def terms_validation(self):
        if not self.line_ids:
            raise exceptions.AccessError(_("جدول أقساط الرسوم إلزامي لحفظ الخطة!"))
        total = 0.0
        for line in self.line_ids:
            if line.value:
                total += line.value
        if abs(total - 100.0) > 0.01:
            raise exceptions.AccessError(
                _("يجب أن يكون مجموع نسب الأقساط مساوياً 100% تماماً! (المجموع الحالي: %s%%)") % total)


class OpStudentCourseInherit(models.Model):
    _inherit = "op.student.course"

    fees_term_id = fields.Many2one('op.fees.terms', 'خطة الرسوم المدرسية')
    fees_start_date = fields.Date('تاريخ استحقاق القسط الأول')
