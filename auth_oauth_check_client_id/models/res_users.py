from odoo import api, models
from odoo.exceptions import AccessDenied


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _auth_oauth_validate(self, provider, access_token):
        """Reject an OAuth response if its supplied client_id differs from ours.

        This extends Odoo's core OAuth validation. It only checks a client_id
        when the provider actually returns one, preserving legacy behavior.
        """
        validation = super()._auth_oauth_validate(provider, access_token)
        client_id = validation.get("client_id")
        if client_id:
            expected = self.env["auth.oauth.provider"].browse(provider).client_id
            if client_id != expected:
                raise AccessDenied(
                    self.env._("OAuth client ID does not match the configured provider.")
                )
        return validation
