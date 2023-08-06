# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    @api.multi
    def _format_dob(self):
        self.ensure_one()
        date = 'No DoB'
        if self.dob:
            lang = self.env['res.lang'].search([('code', '=', self.lang)])
            date = fields.Datetime.from_string(self.dob).strftime(
                lang.date_format
            )
        return ' [%s]' % date

    @api.multi
    def name_get(self):
        res = []
        for rec_id in self:
            name = '%s%s' % (rec_id.name, rec_id._format_dob())
            res.append((rec_id.id, name))
        return res
