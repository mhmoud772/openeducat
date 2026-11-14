# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class StudentCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'student_courses_count' in counters:
            student = request.env['op.student'].sudo().search([
                ('user_id', '=', request.env.user.id)
            ], limit=1)
            if not student:
                student = request.env['op.student'].sudo().search([
                    ('partner_id', '=', request.env.user.partner_id.id)
                ], limit=1)
            count = len(student.course_detail_ids) if student else 0
            values['student_courses_count'] = count
        return values

    @http.route(['/my/academic'], type='http', auth='user', website=True)
    def portal_my_academic(self, **kw):
        user = request.env.user
        student = request.env['op.student'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        if not student:
            student = request.env['op.student'].sudo().search([
                ('partner_id', '=', user.partner_id.id)
            ], limit=1)

        attendance_summary = {
            'present': 0,
            'absent': 0,
            'late': 0,
            'excused': 0,
            'total': 0,
        }
        recent_attendance = []
        if student:
            lines = request.env['op.attendance.line'].sudo().search([
                ('student_id', '=', student.id)
            ], order='attendance_date desc', limit=20)
            attendance_summary = {
                'present': sum(1 for line in lines if line.present),
                'absent': sum(1 for line in lines if line.absent),
                'late': sum(1 for line in lines if line.late),
                'excused': sum(1 for line in lines if line.excused),
                'total': len(lines),
            }
            recent_attendance = lines

        values = {
            'page_name': 'my_academic',
            'student': student,
            'attendance_summary': attendance_summary,
            'recent_attendance': recent_attendance,
        }
        return request.render(
            'openeducat_core.portal_my_student_academic', values
        )
