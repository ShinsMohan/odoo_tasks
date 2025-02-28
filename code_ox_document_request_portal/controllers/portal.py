from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class PortalDocumentRequest(CustomerPortal):

    @http.route(['/my/document_requests'], type='http', auth="user", website=True)
    def portal_my_document_requests(self, **kwargs):
        values = self._prepare_portal_layout_values()
        
        documents = request.env['document.request'].search([('user_id', '=', request.env.user.id)])
        
        values.update({
            'document_requests': documents,
            'page_name': 'document_requests',
        })
        return request.render("code_ox_document_request_portal.portal_my_document_requests_template", values)

    @http.route(['/my/document_requests/new'], type='http', auth="user", website=True)
    def portal_new_document_request(self, **kwargs):
        values = self._prepare_portal_layout_values()
        values.update({
            'page_name': 'new_document_request',
        })
        return request.render("code_ox_document_request_portal.portal_new_document_request_form", values)

    @http.route(['/my/document_requests/submit'], type='http', auth="user", website=True, csrf=True)
    def portal_submit_document_request(self, **post):
        request.env['document.request'].sudo().create({
            'name': post.get('name'),
            'description': post.get('description'),
            'user_id': request.env.user.id,
            'state': 'pending',
        })
        return request.redirect('/my/document_requests')

    @http.route(['/my/document_requests/<int:document_id>'], type='http', auth="user", website=True)
    def portal_document_request_detail(self, document_id, **kwargs):
        values = self._prepare_portal_layout_values()
        document = request.env['document.request'].sudo().browse(document_id)
        if document.user_id.id != request.env.user.id:
            return request.redirect('/my')
        
        values.update({
            'document': document,
            'attachments': document.attachment_ids,
            'page_name': 'document_request_detail',
        })
        return request.render("code_ox_document_request_portal.portal_document_request_detail", values)