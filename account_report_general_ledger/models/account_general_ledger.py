# -*- coding: utf-8 -*-
from odoo import models, api, _, _lt, fields
from odoo.tools.misc import format_date
from datetime import timedelta

from collections import defaultdict

OFFSET = 1


class AccountGeneralLedgerReport(models.AbstractModel):
    _inherit = "account.general.ledger"

    @api.model
    def _get_columns_name(self, options):
        columns_names = [
            {'name': '科目'},
            {'name': _('Date'), 'class': 'date'},
            {'name': _('Communication')},
            {'name': _('Partner')},
            {'name': _('Debit'), 'class': 'number'},
            {'name': _('Credit'), 'class': 'number'},
            {'name': _('Balance'), 'class': 'number'}
        ]
        if self.user_has_groups('base.group_multi_currency'):
            columns_names.insert(4, {'name': _('币种'), 'class': 'number'})
            columns_names.insert(5, {'name': _('外币金额'), 'class': 'number'})

        return columns_names

    @api.model
    def _get_aml_line(self, options, account, aml, cumulated_balance):
        if aml['payment_id']:
            caret_type = 'account.payment'
        else:
            caret_type = 'account.move'

        if aml['ref'] and aml['name']:
            title = '%s - %s' % (aml['name'], aml['ref'])
        elif aml['ref']:
            title = aml['ref']
        elif aml['name']:
            title = aml['name']
        else:
            title = ''

        # if (aml['currency_id'] and aml['currency_id'] != account.company_id.currency_id.id) or account.currency_id:
        #     currency = self.env['res.currency'].browse(aml['currency_id'])
        # else:
        #     currency = False
        currency = self.env['res.currency'].browse(aml['currency_id'])

        columns = [
            {'name': format_date(self.env, aml['date']), 'class': 'date'},
            {'name': self._format_aml_name(aml['name'], aml['ref'], aml['move_name']), 'title': title,
             'class': 'whitespace_print o_account_report_line_ellipsis'},
            {'name': aml['partner_name'], 'title': aml['partner_name'], 'class': 'whitespace_print'},
            {'name': self.format_value(aml['debit'], blank_if_zero=True), 'class': 'number'},
            {'name': self.format_value(aml['credit'], blank_if_zero=True), 'class': 'number'},
            {'name': self.format_value(cumulated_balance), 'class': 'number'},
        ]
        if self.user_has_groups('base.group_multi_currency'):
            columns.insert(3, {'name': currency.name, 'title': currency.name, 'class': 'whitespace_print'})
            columns.insert(4, {'name': currency and aml['amount_currency'] and self.format_value(aml['amount_currency'],
                                                                                                 currency=currency,
                                                                                                 blank_if_zero=True) or '',
                               'class': 'number'})
        return {
            'id': aml['id'],
            'caret_options': caret_type,
            'class': 'top-vertical-align',
            'parent_id': 'account_%d' % aml['account_id'],
            'name': aml['move_name'],
            'columns': columns,
            'level': 2,
        }

    @api.model
    def _get_account_title_line(self, options, account, amount_currency, debit, credit, balance, has_lines):
        res = super(AccountGeneralLedgerReport, self)._get_account_title_line(options, account, amount_currency, debit,
                                                                              credit, balance, has_lines)
        res.update({'colspan': 4 + OFFSET})
        return res

    @api.model
    def _get_account_total_line(self, options, account, amount_currency, debit, credit, balance):
        res = super(AccountGeneralLedgerReport, self)._get_account_total_line(options, account, amount_currency, debit,
                                                                              credit, balance)
        res.update({'colspan': 4 + OFFSET})
        return res

    @api.model
    def _get_load_more_line(self, options, account, offset, remaining, progress):
        return {
            'id': 'loadmore_%s' % account.id,
            'offset': offset,
            'progress': progress,
            'remaining': remaining,
            'class': 'o_account_reports_load_more text-center',
            'parent_id': 'account_%s' % account.id,
            'name': _('Load more... (%s remaining)', remaining),
            'colspan': self.user_has_groups('base.group_multi_currency') and 7 + OFFSET or 6 + OFFSET,
            'columns': [{}],
        }

    @api.model
    def _get_total_line(self, options, debit, credit, balance):
        return {
            'id': 'general_ledger_total_%s' % self.env.company.id,
            'name': _('Total'),
            'class': 'total',
            'level': 1,
            'columns': [
                {'name': self.format_value(debit), 'class': 'number'},
                {'name': self.format_value(credit), 'class': 'number'},
                {'name': self.format_value(balance), 'class': 'number'},
            ],
            'colspan': self.user_has_groups('base.group_multi_currency') and 5 + OFFSET or 4 + OFFSET,
        }

    @api.model
    def _get_tax_declaration_lines(self, options, journal_type, taxes_results):
        lines = [{
            'id': 0,
            'name': _('Tax Declaration'),
            'columns': [{'name': ''}],
            'colspan': self.user_has_groups('base.group_multi_currency') and 7 + OFFSET or 6 + OFFSET,
            'level': 1,
            'unfoldable': False,
            'unfolded': False,
        }, {
            'id': 0,
            'name': _('Name'),
            'columns': [{'name': v} for v in ['', _('Base Amount'), _('Tax Amount'), '']],
            'colspan': self.user_has_groups('base.group_multi_currency') and 4 + OFFSET or 3 + OFFSET,
            'level': 2,
            'unfoldable': False,
            'unfolded': False,
        }]

        tax_report_date = options['date'].copy()
        tax_report_date['strict_range'] = True
        tax_report_options = self.env['account.generic.tax.report']._get_options()
        tax_report_options.update({
            'tax_grids': False,
            'date': tax_report_date,
            'journals': options['journals'],
            'all_entries': options['all_entries'],
        })
        journal = self.env['account.journal'].browse(self._get_options_journals(options)[0]['id'])
        tax_report_lines = self.env['account.generic.tax.report'].with_company(journal.company_id)._get_lines(
            tax_report_options)

        for tax_line in tax_report_lines:
            if tax_line['id'] not in ('sale', 'purchase'):  # We want to exclude title lines here
                tax_line['columns'].append({'name': ''})
                tax_line['colspan'] = self.user_has_groups('base.group_multi_currency') and 5 + OFFSET or 4 + OFFSET
                lines.append(tax_line)

        return lines
