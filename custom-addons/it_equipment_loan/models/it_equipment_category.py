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
    max_loan_days = fields.Integer(string='Durée maximale de prêt', default=14)
    requires_approval = fields.Boolean(string='Approbation requise', default=False)
    equipment_count = fields.Integer(string='Nombre d\'équipement', compute='_compute_equipment_count')

    @api.constrains("name")
    def _check_unique_name(self):
        for category in self:
            normalized_name = self._normalize_name(category.name)

            duplicate = self.search([
                ("id", "!=", category.id),
            ]).filtered(
                lambda c: self._normalize_name(c.name)
                == normalized_name
            )

            if duplicate:
                raise ValidationError(
                    "Une catégorie portant ce nom existe déjà."
                )

    def _normalize_name(self, field):
        # Ignore les différences de casse, d'accents et d'espacement.
        field = field.strip()
        field = re.sub(r"\s+", " ", field)
        field = unicodedata.normalize("NFKD", field)
        field = "".join(
            char for char in field
            if not unicodedata.combining(char)
        )
        return field.casefold()