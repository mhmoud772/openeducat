from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class OpenEduCatDashboard(models.AbstractModel):
    _name = 'openeducat.dashboard'
    _description = 'OpenEduCat School Dashboard'

    @api.model
    def _set_admin_home_action(self):
        admin = self.env.ref('base.user_admin')
        action = self.env.ref(
            'openeducat_dashboard.action_school_dashboard_client')
        admin.write({'action_id': action.id})

    @api.model
    def get_dashboard_data(self):
        if not self.env.user.has_group(
                'openeducat_core.group_op_back_office_admin'):
            raise AccessError(
                _("Only school administrators can open this dashboard."))

        today = fields.Date.context_today(self)
        return {
            'company_name': self.env.company.display_name,
            'today': fields.Date.to_string(today),
            'counts': {
                'students': self.env['op.student'].search_count([
                    ('active', '=', True),
                ]),
                'admissions': self.env['op.admission'].search_count([
                    ('active', '=', True),
                    ('state', 'in', ['submit', 'confirm', 'admission', 'pending']),
                ]),
                'attendance': self.env['op.attendance.sheet'].search_count([
                    ('active', '=', True),
                    ('attendance_date', '=', today),
                    ('state', 'in', ['start', 'done']),
                ]),
                'courses': self.env['op.course'].search_count([
                    ('active', '=', True),
                ]),
            },
            'actions': {
                'students': self.env.ref(
                    'openeducat_core.act_open_op_student_view').id,
                'admissions': self.env.ref(
                    'openeducat_admission.act_open_op_admission_view').id,
                'attendance': self.env.ref(
                    'openeducat_attendance.act_open_op_attendance_sheet_view').id,
                'courses': self.env.ref(
                    'openeducat_core.act_open_op_course_view').id,
            },
        }
