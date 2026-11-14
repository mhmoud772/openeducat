###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
###############################################################################

import urllib.parse
from odoo import api, fields, models


class OpAttendanceLine(models.Model):
    _name = "op.attendance.line"
    _inherit = ["mail.thread"]
    _rec_name = "attendance_id"
    _description = "سجل حضور وغياب الطالب"
    _order = "attendance_date desc"

    attendance_id = fields.Many2one(
        'op.attendance.sheet', 'كشف الحضور', required=True,
        tracking=True, ondelete="cascade")
    student_id = fields.Many2one(
        'op.student', 'الطالب', required=True, tracking=True)
    present = fields.Boolean(
        'حاضر', tracking=True)
    excused = fields.Boolean(
        'غائب بعذر', tracking=True)
    absent = fields.Boolean('غائب بدون عذر', tracking=True)
    late = fields.Boolean('متأخر', tracking=True)
    course_id = fields.Many2one(
        'op.course', 'المرحلة / الصف',
        related='attendance_id.register_id.course_id', store=True,
        readonly=True)
    batch_id = fields.Many2one(
        'op.batch', 'الشعبة / الفصل',
        related='attendance_id.register_id.batch_id', store=True,
        readonly=True)
    remark = fields.Char('ملاحظات', size=256, tracking=True)
    attendance_date = fields.Date(
        'التاريخ', related='attendance_id.attendance_date', store=True,
        readonly=True, tracking=True)
    register_id = fields.Many2one(
        related='attendance_id.register_id', store=True)
    active = fields.Boolean(default=True)
    attendance_type_id = fields.Many2one(
        'op.attendance.type', 'حالة الحضور',
        required=False, tracking=True)
    state = fields.Selection(related="attendance_id.state")

    parent_mobile = fields.Char('جوال ولي الأمر', compute='_compute_parent_contact')
    parent_name = fields.Char('اسم ولي الأمر', compute='_compute_parent_contact')

    def _compute_parent_contact(self):
        for line in self:
            p_mobile = False
            p_name = False
            st = line.student_id
            if st:
                # 1. Search in op.parent
                if 'op.parent' in self.env:
                    parent_rec = self.env['op.parent'].search([('student_ids', 'in', st.id)], limit=1)
                    if parent_rec and parent_rec.mobile:
                        p_mobile = parent_rec.mobile
                        p_name = parent_rec.name
                # 2. Check emergency_contact
                if not p_mobile and st.emergency_contact:
                    p_mobile = st.emergency_contact.mobile or st.emergency_contact.phone
                    p_name = st.emergency_contact.name
                # 3. Check student mobile
                if not p_mobile:
                    p_mobile = st.mobile or st.phone
                    p_name = st.name
            line.parent_mobile = p_mobile
            line.parent_name = p_name

    def action_send_whatsapp_attendance(self):
        """Open WhatsApp Web / Desktop with pre-filled attendance alert for parents"""
        self.ensure_one()
        mobile = self.parent_mobile or ''
        clean_num = ''.join([c for c in str(mobile) if c.isdigit()])
        if clean_num.startswith('05'):
            clean_num = '966' + clean_num[1:]
        elif clean_num.startswith('5') and len(clean_num) == 9:
            clean_num = '966' + clean_num

        state_str = 'غائباً' if self.absent else ('متأخراً' if self.late else ('غائباً بعذر' if self.excused else 'حاضراً'))
        date_str = str(self.attendance_date or fields.Date.today())
        student_name = self.student_id.name or 'ابنكم'
        school_name = self.env.user.company_id.name or 'إدارة المدارس'

        msg = (
            f"السلام عليكم ورحمة الله وبركاته،\n"
            f"المكرم ولي أمر الطالب/ـة: {student_name} المحترم،\n"
            f"نحيطكم علماً بأنه تم تسجيل الطالب ({state_str}) اليوم بتاريخ {date_str}.\n"
            f"نأمل منكم متابعة الطالب والتواصل مع المدرسة في حال وجود أي استفسار أو عذر رسمي.\n"
            f"مع تحيات: {school_name}."
        )
        encoded_msg = urllib.parse.quote(msg)
        whatsapp_url = f"https://api.whatsapp.com/send?phone={clean_num}&text={encoded_msg}"

        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new',
        }

    _unique_student = models.Constraint(
        'unique(student_id,attendance_id,attendance_date)',
        'Student must be unique per Attendance.')

    @api.onchange('attendance_type_id')
    def onchange_attendance_type(self):
        if self.attendance_type_id:
            self.present = self.attendance_type_id.present
            self.excused = self.attendance_type_id.excused
            self.absent = self.attendance_type_id.absent
            self.late = self.attendance_type_id.late

    @api.onchange('present')
    def onchange_present(self):
        if self.present:
            self.late = False
            self.excused = False
            self.absent = False

    @api.onchange('absent')
    def onchange_absent(self):
        if self.absent:
            self.present = False
            self.late = False
            self.excused = False

    @api.onchange('excused')
    def onchange_excused(self):
        if self.excused:
            self.present = False
            self.late = False
            self.absent = False

    @api.onchange('late')
    def onchange_late(self):
        if self.late:
            self.present = False
            self.excused = False
            self.absent = False
