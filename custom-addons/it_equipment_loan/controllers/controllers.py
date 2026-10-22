# from odoo import http


# class ItEquipmentLoan(http.Controller):
#     @http.route('/it_equipment_loan/it_equipment_loan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/it_equipment_loan/it_equipment_loan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('it_equipment_loan.listing', {
#             'root': '/it_equipment_loan/it_equipment_loan',
#             'objects': http.request.env['it_equipment_loan.it_equipment_loan'].search([]),
#         })

#     @http.route('/it_equipment_loan/it_equipment_loan/objects/<model("it_equipment_loan.it_equipment_loan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('it_equipment_loan.object', {
#             'object': obj
#         })

