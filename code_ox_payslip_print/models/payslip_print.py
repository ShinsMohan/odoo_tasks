from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def get_annual_leave_balance(self):
        annual_leave = self.env['hr.leave.type'].search([
            ('annual_leave', '=', True),
            ('company_id', 'in', [self.company_id.id, False])
        ], limit=1)

        if annual_leave:
            leave_allocations = self.env['hr.leave.allocation'].search([
                ('employee_id', '=', self.id),
                ('holiday_status_id', '=', annual_leave.id),
                ('state', '=', 'validate')
            ])
            total_allocated_days = sum(leave_allocations.mapped('number_of_days'))
            total_taken_days = sum(leave_allocations.mapped('leaves_taken'))
            return total_allocated_days - total_taken_days

        return 0