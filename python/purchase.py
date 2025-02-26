
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _amount_in_words(self):
        for record in self:
            if record.amount_total:
                currency = record.vendor_id.property_purchase_currency_id or self.env.company.currency_id
                amount_in_word = currency.amount_to_text(number=record.amount_total, currency='Riyal Omani')
                amt_l = amount_in_word['left'].replace('Hundred ', 'Hundred and ').replace('and Zero', '')
                amt_r = amount_in_word['right'].replace('Hundred ', 'Hundred and ').replace('and Zero', '')
                amount_formated_l = amt_l
                amount_formated_r = amt_r
                if (record.amount_total <= 999) and (int(record.amount_total) % 100 == 0):
                    amount_formated_l = amt_l.replace('Hundred and', 'Hundred')
                total = '%.3f' % record.amount_total
                floating_point = str(total).split('.')[1]
                if int(floating_point) and (int(floating_point) <= 999) and (int(floating_point) % 100 == 0):
                    amount_formated_r = amt_r.replace('and Baisa', 'Baisa')
                if amount_formated_r == 'Zero':
                    record.amount_in_text = amount_formated_l
                else:
                    record.amount_in_text = amount_formated_l + ' and ' + amount_formated_r

    amount_in_text = fields.Char('Amount in Text', compute='_amount_in_words')
    contact_details = fields.Text('Our Contact Details', tracking=True)
    bu_cc = fields.Many2one('account.analytic.account', string='Project Code',
                            states={'draft': [('readonly', False)]}, tracking=True)
    delivery_contact = fields.Many2one("res.partner", string="Delivery Contact Person", readonly=True)

    sent_back_finance_bool = fields.Boolean(string='Sent Back From Finance Dept')
    sent_back_bool = fields.Boolean(string='Sent Back Notify')
    review_bool = fields.Boolean(string='RFQ under Review?')
    budget_amount_exceeded = fields.Boolean(string='Budget Amount Exceeded!')

    mrf_id = fields.Many2one('mr', 'Material Requisition')

    confirm_bool = fields.Boolean(default=False, compute='_set_confirm')

    cost_segment = fields.Many2one('project.boq.category')
    amount_utilized = fields.Float()

    @api.onchange('mrf_id')
    def onchange_mrf(self):
        """
        Update Vals according to the mrf lines
        """
        order_lines = []
        if self.order_line: order_lines = [(5, _, _)]
        if self.mrf_id:
            for line in self.mrf_id.mr_order_line_1:
                product_lang = line.product_id
                name = product_lang.display_name
                if product_lang.description_purchase:
                    name += '\n' + product_lang.description_purchase
                line_history = line.fetch_mr_history()
                product_qty = line.qty
                if line_history:
                    product_qty = line_history['initial_qty'] - line_history['ordered_qty']
                if product_qty <= 0:
                    continue
                vals = {
                    'product_id': line.product_id.id,
                    'name': name,
                    'product_qty': product_qty,
                    'product_uom': line.product_id.uom_po_id.id,
                    'account_analytic_id': line.mr.bu_cc.id,
                    'mr_line_id': line.id,
                    'product_origin': line.product_origin,
                }
                order_lines.append((0, 0, vals))
            self.order_line = order_lines
            self.delivery_contact = self.mrf_id.delivery_contact.id
            self.bu_cc = self.mrf_id.bu_cc.id
            for rec in self.order_line:
                rec._product_id_change()
                rec._onchange_quantity()

