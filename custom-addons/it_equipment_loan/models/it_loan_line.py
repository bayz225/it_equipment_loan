from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ItLoanLine(models.Model):
    _name = 'it.loan.line'
    _description = 'Ligne de prêt'

    loan_id = fields.Many2one(
        comodel_name='it.loan',
        string='Prêt',
        ondelete='cascade',
        required=True
    )
    equipment_id = fields.Many2one(
        comodel_name='it.equipment',
        string='Équipement',
        domain=[('state', '=', 'available')],
        required=True
    )
    condition_out = fields.Selection(
        selection=[
            ('new', 'Neuf'),
            ('good', 'Bon état'),
            ('worn', 'Usagé (Fatigué)')
        ],
        string='État à la sortie',
        required=True,
        default='good'
    )
    condition_return = fields.Selection(
        selection=[
            ('good', 'Bon état'),
            ('damaged', 'Endommagé'),
            ('lost', 'Perdu')
        ],
        string='État au retour'
    )
    return_notes = fields.Text(
        string='Notes de retour'
    )