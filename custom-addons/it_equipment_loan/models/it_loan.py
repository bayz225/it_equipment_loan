from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ItLoan(models.Model):
    _name = 'it.loan'
    _description = 'Prêt / Demande'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, date_start desc"
    
    _sql_constraints = [
        (
            'check_date_due',
            'CHECK(date_due >= date_start)',
            'La date de retour prévue doit être postérieure ou égale à la date de début du prêt.'
        ),
    ]
    
    name = fields.Char(
        string="Référence", 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: 'Nouveau'
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Demandeur',
        default=lambda self: self.env.user.employee_id,
        ondelete='restrict',
        required=True
    )
    department_id = fields.Many2one(
        string='Département',
        related='employee_id.department_id',
        store=True,
    )
    line_ids = fields.One2many(
        comodel_name='it.loan.line', 
        inverse_name='loan_id', 
        string="Équipements demandés",
    )
    
    date_request = fields.Date(string='Date de la demande', default=fields.Date.context_today)
    date_start = fields.Date(string='Date de début', required=True)
    date_due = fields.Date(string='Date de retour prévue', required=True)
    date_return = fields.Date(string='Retourné le')
    
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('submitted', 'Soumis'),
            ('approved', 'Approuvé'),
            ('in_progress', 'En cours'),
            ('returned', 'Retourné'),
            ('refused', 'Refusé'),
            ('cancel', 'Annulé'),
        ],
        string="Statut",
        default="draft",
        tracking=True,
    )
    approver_id = fields.Many2one(
        comodel_name='res.users', 
        string="Validé par", 
        readonly=True
    )
    reason = fields.Text(string="Motif de la demande")
    refusal_reason = fields.Text(string="Motif de refus")
    is_late = fields.Boolean(string="En retard", compute='_compute_is_late', store=True)
    late_days = fields.Integer(string="Jours de retard", compute='_compute_is_late')

    @api.constrains('date_start', 'date_return')
    def _check_return_date(self):
        """Vérifie que la date de retour effective est cohérente."""
        for loan in self:
            if loan.date_return and loan.date_start and loan.date_return < loan.date_start:
                raise ValidationError("La date de retour effective ne peut pas être antérieure à la date de début du prêt.")

    @api.constrains('state', 'refusal_reason')
    def _check_refusal_reason(self):
        """Rend le motif de refus obligatoire si la demande est refusée."""
        for loan in self:
            if loan.state == 'refused' and not loan.refusal_reason:
                raise ValidationError("Vous devez obligatoirement saisir un motif de refus avant de refuser cette demande.")
                
    @api.constrains('date_request', 'date_start')
    def _check_request_date(self):
        """Avertissement/Blocage si le prêt commence avant la demande."""
        for loan in self:
            if loan.date_start and loan.date_request and loan.date_start < loan.date_request:
                raise ValidationError("La date de début du prêt ne peut pas être antérieure à la date de la demande.")

    @api.depends('date_due', 'date_return', 'is_late', 'late_days')
    def _compute_is_late(self):
        for loan in self:
            loan.is_late = bool(
                loan.date_due
                and loan.date_return
                and loan.date_return > loan.date_due
            )
            
            if loan.is_late:
                delta = loan.date_return - loan.date_due
                loan.late_days = delta.days
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', "Nouveau") == "Nouveau":
                vals['reference'] = self.env['ir.sequence'].next_by_code('it.loan')
            
        return super().create(vals_list)
    