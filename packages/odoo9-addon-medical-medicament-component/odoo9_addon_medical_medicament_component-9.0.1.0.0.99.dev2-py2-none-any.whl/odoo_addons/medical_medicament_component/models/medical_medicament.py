# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models, fields


class MedicalMedicament(models.Model):
    _inherit = 'medical.medicament'
    component_ids = fields.Many2many(
        string='Components',
        comodel_name='medical.medicament.component',
    )
