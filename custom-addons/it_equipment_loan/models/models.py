# from odoo import models, fields, api


# class it_equipment_loan(models.Model):
#     _name = 'it_equipment_loan.it_equipment_loan'
#     _description = 'it_equipment_loan.it_equipment_loan'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

