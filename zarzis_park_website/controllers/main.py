import base64
import datetime
from odoo import http, registry, api
from odoo.http import request


class Main(http.Controller):

    # Route for the homepage
    @http.route('/', type='http', auth="public", website=True)
    def zarzis_park_footer(self, **kw):
        # Retrieve the company data
        company = request.env['res.company'].sodu().search([])
        return request.render('zarzis_park_website.my_footer', {"company": company})

    # Route for the local list page
    @http.route(['/local/list'], type='http', auth='public', website='True', csrf=False)
    def local_list(self, **post):
        # Update the home menu and contact menu
        home_menu = request.env['website.menu'].sudo().browse(5)
        home_menu.write({
            'name': 'Zarzis Business Park',
        })
        contact_menu = request.env['website.menu'].sudo().browse(6)
        contact_menu.write({
            'name': ' ',
        })

        # Retrieve all locals and filter them based on type
        all_Local = request.env['zarzis.park.erp.local'].sudo().search([('is_published', '=', True)])
        land_local = all_Local.filtered(lambda p: p.type_local == "land")
        premises_local = all_Local.filtered(lambda p: p.type_local == "premises")
        office_local = all_Local.filtered(lambda p: p.type_local == "office")


        # Prepare the container for the locals based on their status
        allLocals = self.prepare_list_container_status(all_Local)
        allLand = self.prepare_list_container_status(land_local)
        allPremises = self.prepare_list_container_status(premises_local)
        allOffice = self.prepare_list_container_status(office_local)

        # Retrieve all partners and company data
        allPartners = request.env['zarzis.park.erp.partner'].sudo().search([])
        partner_attachment = []

        for partner in allPartners:
            logo = request.env['ir.attachment'].sudo().search([
                    ('res_model', '=', 'zarzis.park.erp.partner'),
                    ('description', '=', partner.desc)
            ])
            partner_attachment.append(logo)

        company = request.env['res.company'].sudo().search([])

        # Prepare the values to be passed to the template
        values = {
            "allLocals": allLocals,
            "len_locals": len(all_Local),
            "allLand": allLand,
            "len_land": len(land_local),
            "allPremises": allPremises,
            "len_premises": len(premises_local),
            "allOffice": allOffice,
            "len_office": len(office_local),
            "company": company,
            "partner_attachment": partner_attachment
        }
        return request.render('zarzis_park_website.list_tmp', values)

    @staticmethod
    def prepare_list_container_status(filtered_status):
        # Prepare the container for locals based on their status
        allCards = []
        length_all_cards = 1 if len(filtered_status) == 12 else (len(filtered_status) // 12) + 1

        patient_index = 0
        for i in range(0, length_all_cards):
            allCards.append('')

        for i in range(0, length_all_cards):
            cards = []
            for j in range(0, 12):
                cards.append('')
            for j in range(0, 12):
                if patient_index < len(filtered_status):
                    cards[j] = filtered_status[patient_index]
                    patient_index = patient_index + 1
            allCards[i] = cards
        return allCards

    # Route for local details page
    @http.route('/local/list/<int:reference>', type='http', auth='public', website=True)
    def local_details(self, reference, **kw):
        # Redirect to the second web controller with the reference as a parameter
        local = request.env['zarzis.park.erp.local'].sudo().search([('id', '=', reference)])

        # Retrieve the attachments associated with the record
        attachments = local.attachment_ids

        for att in attachments:
            if not request.env['ir.attachment'].sudo().search([('id', '=', att.id), ('public', '=', True)]):
                att.public = True

        company_id = request.env['res.company'].sudo().search([])
        values = {
            'local': local,
            "company": company_id
        }
        return request.render('zarzis_park_website.local_details_template', values)

    @http.route(['/local/list/<int:id>/rental_form'], type='http', auth='user', website='True', csrf=False)
    def rental_form(self, id, **post):
        country_ids = request.env['res.country'].search([])
        currency_ids = request.env['res.currency'].search([])
        company_id = request.env['res.company'].search([])
        user_name = request.env.user.name
        user_email = request.env.user.email

        local_id = request.env['zarzis.park.erp.local'].search([('id', '=', id)])

        if post.get('promoter_name'):
            # Calculate the refuse date as 3 days from today's date
            first_refuse_date = datetime.date.today() + datetime.timedelta(days=3)

            # owner nationality
            owner_nationality_code = post.get('nationality_promoter')
            owner_nationality = http.request.env['res.country'].search([('name', '=', owner_nationality_code)])

            # owner nationality
            manager_nationality_code = post.get('nationality_manager')
            manager_nationality = http.request.env['res.country'].search([('name', '=', manager_nationality_code)])

            # company nationality
            company_currency_code = post.get('currency')
            company_currency = http.request.env['res.currency'].search([('name', '=', company_currency_code)])

            # local type
            export_destination_code = post.get('export_destination')
            export_destination = http.request.env['res.country'].search([('name', '=', export_destination_code)])

            record_id = http.request.env['rental.submission'].create({
                'state': 'being_processed',
                # Name of company to be created:
                'name': post.get('promoter_name'),
                'owner_national_id': owner_nationality.id,
                'address': post.get('address'),
                'phone': post.get('phone'),
                'email': post.get('email'),
                'submission_date': datetime.date.today(),
                'first_refuse_date': first_refuse_date,
                'locale_id': local_id.id,

                # Main shareholders(precise resident / non - resident)
                'first_proposal': post.get('1st_proposal'),
                'second_proposal': post.get('2nd_proposal'),
                'third_proposal': post.get('3rd_proposal'),
                'activity': post.get('activities'),
                'name_surname_manager': post.get('surname_manager'),
                'company_national_id': manager_nationality.id,
                'company_capital': post.get('capital_company'),
                'currency_id': company_currency.id,

                # Construction nature:
                'category': local_id.type_local,
                'area_size': post.get('construction_area'),

                # Number of national jobs to be created:
                'construction_nature': post.get('construction_nature'),
                'description': post.get('description'),

                # Investment & financing program (EURO / US $ / TND)
                'estimated_export_value': post.get('estimated'),
                'local_added_value': post.get('local_added_value'),
                'year_one': post.get('year_one'),
                'year_two': post.get('year_two'),
                'year_three': post.get('year_three'),
                'export_destination_id': export_destination.id,
                'origin_of_imported_goods': post.get('origin'),

                # INVESTMENT
                'construction_equipments': post.get('construction_equipments'),
                'imported_equipments': post.get('imported_equipments'),
                'local_equipments': post.get('local_equipments'),
                'means_of_transport': post.get('means_transport'),
                'other_costs': post.get('other_costs'),
                'working_capital': post.get('working_capital'),
                'total_investment': post.get('total_investment'),

                # FINANCING
                'capital': post.get('capital_finance'),
                'current_account_partners': post.get('current_partners'),
                'long_term_credit': post.get('long_credit'),
                'middle_term_credit': post.get('middle_credit'),
                'short_term_credit': post.get('short_credit'),
                'total_financing': post.get('total_financing'),
            })
            shareholders = request.httprequest.form.getlist('shareholders')
            if shareholders != []:
                num_shareholders = len(shareholders)
                shareholder_ids = []

                for i in range(0, num_shareholders, 3):
                    group = shareholders[i:i + 3]

                    if len(group) == 3:
                        shareholder = request.env['main.shareholders'].create({
                            'name_surname': group[0],
                            'nationality_shareholders': group[1],
                            'subscription_percentage': group[2]
                        })
                        shareholder_ids.append(shareholder.id)

                record_id.shareholders_ids = [(6, 0, shareholder_ids)]

            local_id.write({
                'state': 'reserved',
            })
            ref_url = record_id.reference + '/check'
            return request.redirect('/local/request/%s' % ref_url)

        values = {
            "country_ids": country_ids,
            "currency_ids": currency_ids,
            "company": company_id,
            "id": id,
            "local_id": local_id,
            "user_name": user_name,
            "user_email": user_email
        }
        return request.render('zarzis_park_website.rental_template', values)

    @http.route('/local/request', type='http', auth='user', website=True)
    def rental_request(self, **kw):
        list_rental = request.env['rental.submission'].search([])
        company_id = request.env['res.company'].search([])
        values = {
            'list_rental': list_rental,
            'company': company_id
        }
        return request.render('zarzis_park_website.request_template', values)

    @http.route(['/local/request/<string:reference>/check'], type='http', auth='user', website='True', csrf=False)
    def request_check(self, reference, **post):
        request_form = request.env['rental.submission'].search([('reference', '=', reference)])
        company_id = request.env['res.company'].search([])
        local_id = request.env['zarzis.park.erp.local'].search([('id', '=', request_form.locale_id.id)])
        values = {
            'reference': reference,
            'request_form': request_form,
            'company': company_id,
            'local_id': local_id,
            'request_id': request_form.id
        }
        return request.render('zarzis_park_website.check_template', values)

    @http.route('/local/request/<int:request_id>', type='http', auth="user", website=True, csrf=False)
    def print_request_report_test(self, request_id):
        pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf('zarzis_park_erp.application_rental_submission_report_print', [request_id])[0]
        pdfhttpheaders = [
            ('Content-Type', 'application/download'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', 'attachment; filename="Application Form.pdf"')]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route(['/local/request/<string:reference>/update'], type='http', auth='user', website='True', csrf=False)
    def request_update(self, reference, **post):
        request_form = request.env['rental.submission'].search([('reference', '=', reference)], limit=1)
        company_id = request.env['res.company'].search([])
        currency_ids = request.env['res.currency'].search([])
        country_ids = request.env['res.country'].search([])

        local_id = request.env['zarzis.park.erp.local'].search([('id', '=', request_form.locale_id.id)])

        if post.get('Promoter_Name'):
            # owner nationality
            owner_nationality_code = post.get('nationality_promoter')
            owner_nationality = http.request.env['res.country'].search([('name', '=', owner_nationality_code)])

            # owner nationality
            manager_nationality_code = post.get('nationality_manager')
            manager_nationality = http.request.env['res.country'].search([('name', '=', manager_nationality_code)])

            # company nationality
            company_currency_code = post.get('currency')
            company_currency = http.request.env['res.currency'].search([('name', '=', company_currency_code)])

            record_id = http.request.env['rental.submission'].search([('reference', '=', reference)]).write({
                # Name of company to be created:
                'name': post.get('Promoter_Name'),
                'owner_national_id': owner_nationality.id,
                'address': post.get('Address'),
                'phone': post.get('phone'),
                'email': post.get('email'),

                # Main shareholders(precise resident / non - resident)
                'first_proposal': post.get('1st_Proposal'),
                'second_proposal': post.get('2nd_Proposal'),
                'third_proposal': post.get('3rd_Proposal'),
                'activity': post.get('activities'),
                'name_surname_manager': post.get('surname_manager'),
                'company_national_id': manager_nationality.id,
                'currency_id': company_currency.id,
                'company_capital': post.get('capital_company'),
            })

            shareholders = request.httprequest.form.getlist('shareholders')

            if shareholders == []:
                http.request.env['rental.submission'].search([('reference', '=', reference)]).shareholders_ids.unlink()
            else:
                http.request.env['rental.submission'].search([('reference', '=', reference)]).shareholders_ids.unlink()
                num_shareholders = len(shareholders)
                shareholder_ids = []

                for i in range(0, num_shareholders, 3):
                    group = shareholders[i:i + 3]

                    if len(group) == 3:
                        shareholder = request.env['main.shareholders'].create({
                            'name_surname': group[0],
                            'nationality_shareholders': group[1],
                            'subscription_percentage': group[2]
                        })
                        shareholder_ids.append(shareholder.id)

                http.request.env['rental.submission'].search([('reference', '=', reference)]).shareholders_ids = [
                    (6, 0, shareholder_ids)]
            ref_url = reference + '/check'
            return request.redirect('/local/request/%s' % ref_url)

        values = {
            'reference': reference,
            'request_form': request_form,
            'company': company_id,
            'currency_ids': currency_ids,
            'local_id': local_id,
            'country_ids': country_ids
        }
        return request.render('zarzis_park_website.update_request_template', values)
