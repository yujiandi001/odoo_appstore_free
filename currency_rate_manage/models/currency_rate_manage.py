# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError


class CurrencyRateManage(models.Model):
    _name = "currency.rate.manage"

    name = fields.Char(string="说明")
    date = fields.Date(string="日期", default=lambda self: fields.Date.today())
    currency_id = fields.Many2one("res.currency", string="币种", ondelete="cascade")
    rate_f2c = fields.Float(string="外币 to 本币位", digits=0, default=1.0)
    rate_c2f = fields.Float(string="本币位 to 外币", digits=0, default=1.0)
    # domain = lambda self: [('id', 'in', self.env.user.company_ids.ids)]
    company_ids = fields.Many2many("res.company", string="公司", )
    currency_rate_ids = fields.Many2many("res.currency.rate", string="关联数据", copy=False)

    _sql_constraints = [
        ('currency_rate_check', 'CHECK (rate>0)', '货币汇率必须严格为正数'),
    ]

    @api.onchange('rate_f2c')
    def _onchange_rate_f2c(self):
        for currency_rate in self:
            currency_rate.rate_c2f = 1.0 / currency_rate.rate_f2c

    @api.onchange('rate_c2f')
    def _onchange_rate_c2f(self):
        for currency_rate in self:
            currency_rate.rate_f2c = 1.0 / currency_rate.rate_c2f

    def create_multi_currency_rate(self):
        self_sudo = self.sudo()
        # currency_rate_sudo = self.env["res.currency.rate"].sudo()
        currency_rate_ids_list = []
        for i in self.company_ids:
            c = {
                "name": self.date,
                "currency_id": self.currency_id.id,
                "company_id": i.id,
                "rate": self.rate_c2f,
            }
            # res = currency_rate_sudo.create(c)
            currency_rate_ids_list.append((0, 0, c))
        self_sudo.currency_rate_ids = currency_rate_ids_list

    def del_rate(self):
        self.sudo().currency_rate_ids.unlink()
        # self.sudo().currency_rate_ids = [(5, 0, 0)]

    def unlink(self):
        for rec in self:
            if rec.currency_rate_ids:
                raise ValidationError("请取消删除汇率后，再删除该记录")
        res = super(CurrencyRateManage, self).unlink()
        return res
