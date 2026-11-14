# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class ParentCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'children_count' in counters:
            parent = request.env['op.parent'].sudo().search([
                ('user_id', '=', request.env.user.id)
            ], limit=1)
            if not parent:
                parent = request.env['op.parent'].sudo().search([
                    ('name', '=', request.env.user.partner_id.id)
                ], limit=1)
            values['children_count'] = len(parent.student_ids) if parent else 0
        return values

    @http.route(
        ['/my/child', '/my/children'],
        type='http',
        auth='user',
        website=True
    )
    def portal_my_children(self, student_id=None, **kw):
        user = request.env.user
        parent = request.env['op.parent'].sudo().search([
            ('user_id', '=', user.id)
        ], limit=1)
        if not parent:
            parent = request.env['op.parent'].sudo().search([
                ('name', '=', user.partner_id.id)
            ], limit=1)

        students = parent.student_ids if parent else request.env['op.student']

        selected_student = None
        if student_id:
            matched = students.filtered(lambda s: s.id == int(student_id))
            if matched:
                selected_student = matched[0]
        if not selected_student and students:
            selected_student = students[0]

        attendance_summary = {
            'present': 0,
            'absent': 0,
            'late': 0,
            'excused': 0,
            'total': 0,
        }
        recent_attendance = []
        if selected_student:
            lines = request.env['op.attendance.line'].sudo().search([
                ('student_id', '=', selected_student.id)
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
            'page_name': 'my_children',
            'parent': parent,
            'students': students,
            'selected_student': selected_student,
            'attendance_summary': attendance_summary,
            'recent_attendance': recent_attendance,
        }
        return request.render('openeducat_parent.portal_my_children', values)
