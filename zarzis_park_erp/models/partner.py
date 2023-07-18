import base64

from odoo import api, fields, models, _


class Partner(models.Model):
    _name = "zarzis.park.erp.partner"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Zarzis Park Erp Partner"
    _rec_name = "reference"
    _order = 'create_date desc'

    reference = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: _("New"))
    partner_id = fields.Many2one('res.partner', string='Name', tracking=True)
    desc = fields.Char(string="Description", required=True)
    logo = fields.Binary(string="Logo")

    @api.onchange('logo')
    def button_add_attachments(self):
        u"""Add attachment to any object."""
        context = self.env.context or {}
        attachment_obj = self.env['ir.attachment']
        for wiz in self:
            if wiz.logo:
                field_name = context.get('field_name', 'logo')
                print("field_name",field_name)

                values = {'name': wiz.partner_id.name,
                          'res_id': wiz.id,
                          'res_model': 'zarzis.park.erp.partner',
                          'description': wiz.desc,
                          'public':True,
                          'datas': wiz.logo}
                attachment = attachment_obj.create(values)
    # Sequence
    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            vals['reference'] = 'New Partner'
            vals['reference'] = self.env['ir.sequence'].next_by_code('zarzis.park.erp.partner') or _('New')
        res = super(Partner, self).create(vals)
        return res


