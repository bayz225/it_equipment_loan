from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import unicodedata

class ItEquipment(models.Model):
    _name = "it.equipment"
    _description = "Équipement"
    
    _it_equipments_serial_number_unique = models.Constraint(
        "Unique(serial_number)",
        "Le numéro de serie de l'équipement doit être unique."
    )

    name = fields.Char(string="Name", required=True)
    reference = fields.Char(
        string="Référence",
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: "Nouveau"
    )
    category_id = fields.Many2one(
        comodel_name='it.equipment.category',
        string='Catégorie',
        required=True,
    )
    serial_number = fields.Char(string='Numéro de serie', required=True)
    purchase_date = fields.Date(string='Date d\'achat')
    state = fields.Selection(
        selection=[
            ("new", "Nouveau"),
            ("available", "Disponible"),
            ("loaned", "Prêter"),
            ("maintenance", "En maintenance"),
            ("retired", "Rétirer")
        ],
        string="État",
        default="new",
        group_expand=True,
    )
    image = fields.Image(string="Image", max_width=1024, max_height=1024)
    notes = fields.Html(
        string='Notes'
    )
    active = fields.Boolean(string="Active", default=True)
    
    @api.constrains("serial_number")
    def _check_unique_name(self):
        for equipment in self:
            normalized_name = self._normalize_name(equipment.name)

            duplicate = self.search([
                ("id", "!=", equipment.id),
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