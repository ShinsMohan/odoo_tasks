from odoo import models, fields, api

class DocumentRequest(models.Model):
    _name = 'document.request'
    _description = 'Document Request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Request Name', required=True, tracking=True)
    description = fields.Text('Description')
    user_id = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    def action_submit_for_approval(self):
        self.state = 'waiting_approval'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'
    
    def action_reset_to_draft(self):
        self.state = 'draft'

    attachment_ids = fields.Many2many(
        'ir.attachment', 
        string='Attachments',
        domain=[('res_model', '=', 'document.request')],
        context={'default_res_model': 'document.request'}
    )
    
    def _compute_access_url(self):
        super(DocumentRequest, self)._compute_access_url()
        for request in self:
            request.access_url = f'/my/document_requests/{request.id}'