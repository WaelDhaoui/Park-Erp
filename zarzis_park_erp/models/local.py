import base64
import os
import datetime

from odoo import api, fields, models, _, tools
from odoo.modules.module import get_module_resource


class Local(models.Model):
    _name = "zarzis.park.erp.local"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Zarzis Park Erp Local"
    _rec_name = "reference"
    _order = 'create_date desc'

    reference = fields.Char(string="Reference", required=True, copy=False, readonly=True,
                            default=lambda self: _("New"))

    @api.model
    def _default_image(self):
        image_path = get_module_resource('zarzis_park_erp', 'static/img/local/office', '01.jpg')
        return base64.b64encode(open(image_path, 'rb').read())

    def _default_attachments(self):
        default_attachments_folder = get_module_resource('zarzis_park_erp', 'static/img/local/office')
        attachment_ids = []

        if os.path.exists(default_attachments_folder):
            for filename in os.listdir(default_attachments_folder):
                filepath = os.path.join(default_attachments_folder, filename)
                with open(filepath, 'rb') as f:
                    data = f.read()
                    attachment = self.env['ir.attachment'].create({
                        'name': filename,
                        'datas': base64.b64encode(data),
                    })
                    attachment_ids.append(attachment.id)
                    if len(attachment_ids) > 3:
                        break

        return [(6, 0, attachment_ids)]

    name = fields.Char(string='Name', required=True)
    area_size = fields.Integer(string="Area (in Sq m): ", required=True)
    price_per_metre = fields.Monetary(string="Price per metre²:", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    total_price = fields.Monetary(string="Total Price:", compute="_compute_total_price")

    image = fields.Binary(string="Image", default=_default_image, attachment=True)
    img_att = fields.Many2one('ir.attachment', compute="_compute_image_attachment")

    @api.depends('image')
    def _compute_image_attachment(self):
        context = self.env.context or {}
        attachment_obj = self.env['ir.attachment']
        for wiz in self:
            if wiz.image:
                field_name = context.get('field_name', 'logo')
                values = {'name': wiz.name,
                          'res_id': wiz.id,
                          'res_model': 'zarzis.park.erp.local',
                          'public':True,
                          'datas': wiz.image}
                attachment = attachment_obj.create(values)
                for record in self:
                    record.img_att = attachment

    attachment_ids = fields.Many2many('ir.attachment', string='Images',
                                      default=lambda self: self._default_attachments())

    is_published = fields.Boolean(string='Ready for rental', default=False)

    state = fields.Selection([
        ('not_reserved', 'Not Reserved'),
        ('reserved', 'Reserved'),
    ], string='State', default="not_reserved", tracking=True)

    type_local = fields.Selection([
        ('land', 'Land'),
        ('premises', 'Premises'),
        ('office', 'Office'),
    ], string='Type', required=True)

    @api.depends('attachment_ids')
    def _compute_attachments(self):
        attachment_obj = self.env['ir.attachment']
        for attachment in self.env['ir.attachment'].sudo().browse(self._ids):
            if attachment.type == 'binary':
                self.attachment_ids = [(4, attachment.id, 0)]
            else:
                attachment_vals = {
                    'name': attachment.filename,
                    'type': 'binary',
                    'datas': attachment.datas,
                    'datas_fname': attachment.filename,
                    'public': True,
                }
                new_attachment = attachment_obj.create(attachment_vals)
                self.attachment_ids = [(4, new_attachment.id, 0)]
        return True

    @api.depends('area_size', 'price_per_metre')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.area_size * record.price_per_metre

    def set_to_not_reserved(self):
        if self.state == 'reserved':
            self.state = 'not_reserved'

    def setToReserved(self):
        if self.state == 'not_reserved':
            self.state = 'reserved'

    def active_request_form(self):
        submission_id = self.env['rental.submission'].search([("locale_id.id", '=', self.id)])
        return {
            'name': _("Active Request"),
            'type': 'ir.actions.act_window',
            'res_model': "rental.submission",
            'view_mode': 'tree,form',
            'domain': [('id', '=', submission_id.ids)],
            'target': 'self',
        }

    request = fields.Integer(string="Requests", compute="_num_requests", readonly=True)

    def _num_requests(self):
        allRequests = self.env['rental.submission'].search([("locale_id.id", '=', self.id)])
        self.request = len(allRequests)

    # Sequence
    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            vals['reference'] = 'New'
            if vals['type_local'] == "land":
                vals['reference'] = self.env['ir.sequence'].next_by_code('zarzis.park.erp.land') or _('New')
            elif vals['type_local'] == "premises":
                vals['reference'] = self.env['ir.sequence'].next_by_code('zarzis.park.erp.premises') or _('New')
            elif vals['type_local'] == "office":
                vals['reference'] = self.env['ir.sequence'].next_by_code('zarzis.park.erp.office') or _('New')
        res = super(Local, self).create(vals)
        return res

    def website_publish_button(self):
        for rec in self:
            if rec.is_published:
                rec.is_published = False
            else:
                rec.is_published = True
