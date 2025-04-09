from odoo import http
from odoo.http import content_disposition, request
from werkzeug.datastructures import FileStorage
import base64
import io
import json
import xlsxwriter

class InvoiceExportController(http.Controller):

    @http.route('/invoice_analysis_excel/export_xlsx', type='http', auth='user')
    def export_xlsx(self, data, **kw):
        jdata = json.load(data) if isinstance(data, FileStorage) else json.loads(data)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Invoice Analysis')

        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'pattern': 1,
            'bg_color': '#80EF80',
            'border': 1,
            'border_color': '#2F528F',
            'align': 'center',
            'valign': 'vcenter'
        })
        
        number_format = workbook.add_format({'num_format': '#,##0.00'})

        domain = jdata.get('domain', [])
        context = jdata.get('context', {})
        domain.append(('move_type', 'in', ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']))
        
        invoice_obj = request.env['account.move'].with_context(**context)
        invoices = invoice_obj.search(domain)

        headers = [
            'Invoice Number', 
            'Partner', 
            'Untaxed Amount', 
            'Tax Amount',
            'Total Amount'
        ]
        
        # Write headers
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, len(header) + 5)
        
        # Write data
        row = 1
        for invoice in invoices:
            worksheet.write(row, 0, invoice.name or '')
            worksheet.write(row, 1, invoice.partner_id.name or '')
            worksheet.write(row, 2, invoice.amount_untaxed or 0.0, number_format)
            worksheet.write(row, 3, invoice.amount_tax or 0.0, number_format)
            worksheet.write(row, 4, invoice.amount_total or 0.0, number_format)
            row += 1
        
        workbook.close()
        xlsx_data = output.getvalue()
        
        filename = "invoice_analysis_detail_report"
        
        return request.make_response(
            xlsx_data,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', content_disposition(filename + '.xlsx'))
            ],
        )