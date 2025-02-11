from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_print_header = fields.Binary(string="Invoice print header")
    invoice_print_footer = fields.Binary(string="Invoice print footer")