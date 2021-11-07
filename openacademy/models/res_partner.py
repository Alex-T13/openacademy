from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(string="Is instructor", default=False)

    session_ids = fields.Many2many(
        comodel_name='openacademy.session',
        string='Sessions',
    )

    instructed_session_ids = fields.One2many(
        comodel_name='openacademy.session',
        inverse_name='instructor_id',
        string='Sessions',
    )
