from odoo import models, fields


class MailComposeMessageInherit(models.TransientModel):
    _inherit = 'mail.compose.message'
    _description = 'Zarzis Park Erp Refuse'

    form_ref = fields.Char(string='Form', readonly='1')
    reason = fields.Text(string='Reason')

    def _action_send_mail(self, auto_commit=False):
        records = self.env['rental.submission'].browse(self.env.context.get('active_ids'))
        records.is_unlocked = False
        for rec in records:
            rec.write({'state': 'refused'})
            rec.write({'reason_refuse': self.reason})
        template = self.env.ref('zarzis_park_erp.refuse_rental_request_email_template')
        template.send_mail(records.id)
        local = self.env['zarzis.park.erp.local'].search([('id', '=', records.locale_id.id)])
        local.write({
            'state': 'not_reserved',
        })
        return super(MailComposeMessageInherit, self)._action_send_mail(auto_commit=auto_commit)

