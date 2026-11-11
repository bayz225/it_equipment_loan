from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import unicodedata

class ItEquipmentCategory(models.Model):
    _name = 'it.equipment.category'
    _description = 'Catégorie de matériel'

    _it_equipments_category_name_unique = models.Constraint(
        "Unique(name)",
        "Le nom de la catégorie doit être unique."
    )

    name = fields.Char(string='Nom', required=True)
    max_loan_days = fields.Integer(string='Durée du prêt (jour)', default=14,)
    requires_approval = fields.Boolean(string='Approbation requise', default=False)
    equipment_ids = fields.One2many(
        comodel_name='it.equipment', 
        inverse_name='category_id', 
        string='Équipements'
    )
    equipment_count = fields.Integer(
        string='Nombre d\'équipement', 
        compute='_compute_equipment_count',
        store=True
    )

    @api.constrains("name")
    def _check_unique_name(self):
        for category in self:
            normalized_name = self._normalize_field(category.name)

            duplicate = self.search([
                ("id", "!=", category.id),
            ]).filtered(
                lambda c: self._normalize_field(c.name)
                == normalized_name
            )

            if duplicate:
                raise ValidationError(
                    "Une catégorie portant ce nom existe déjà."
                )

    def _normalize_field(self, field):
        # Ignore les différences de casse, d'accents et d'espacement.
        field = field.strip()
        field = re.sub(r"\s+", " ", field)
        field = unicodedata.normalize("NFKD", field)
        field = "".join(
            char for char in field
            if not unicodedata.combining(char)
        )
        return field.casefold()

    @api.constrains("max_loan_days")
    def _check_max_loan_days(self):
        for category in self:
            if category.max_loan_days <= 0:
                raise ValidationError(
                    "La durée maximale du prêt doit être supérieure à 0."
                )
    
    @api.depends("equipment_ids")
    def _compute_equipment_count(self):
        for category in self:
            category.equipment_count = len(category.equipment_ids)
