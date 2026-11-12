from odoo import models, exceptions

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def unlink(self):
        """Bloque la suppression/clôture de l'activité par une personne non autorisée."""
        for activity in self:
            # Si l'activité concerne notre module de prêt
            if activity.res_model == 'it.loan':
                # Si l'utilisateur connecté n'est pas celui à qui l'activité est assignée
                # (et qu'il n'est pas un administrateur système)
                if activity.user_id != self.env.user and not self.env.is_admin():
                    raise exceptions.UserError(
                        "Sécurité : Vous ne pouvez pas clôturer ou supprimer une tâche assignée à votre manager."
                    )
        return super().unlink()