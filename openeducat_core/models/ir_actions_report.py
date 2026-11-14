# -*- coding: utf-8 -*-
import base64
from odoo import models, api
from odoo.tools.image import image_data_uri


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def get_barcode_data_uri(self, barcode_type, value, width=600, height=100, **kwargs):
        if not value:
            return ''
        try:
            barcode_bytes = self.barcode(barcode_type, str(value), width=width, height=height, **kwargs)
            return image_data_uri(base64.b64encode(barcode_bytes))
        except Exception:
            return ''
