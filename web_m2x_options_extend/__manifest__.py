# Copyright 2015 0k.io
# Copyright 2016 ACSONE SA/NV
# Copyright 2017 Tecnativa
# Copyright 2020 initOS GmbH.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "web_m2x_options_extend",
    "version": "14.0.1.0.0",
    'description': """
    改自web_m2x_options
        系统参数新增
    	web_m2x_options.create:False
    	web_m2x_options.create_edit:False
    	web_m2x_options.m2o_dialog:False
    	web_m2x_options.create_false_effect:product.template,res.partner,product.product  新增，设置时，不能创建只对值内模型生效
    	web_m2x_options.can_open_no_write:product.product                                 新增，设置时，打开这些模型时不能编辑
    	
    
""",
    "category": "Web",
    "author":
        "zero,"
        "initOS GmbH,"
        "ACSONE SA/NV, "
        "0k.io, "
        "Tecnativa, "
        "Odoo Community Association (OCA)",
    "website": "",
    "license": "AGPL-3",
    "depends": ["web"],
    "data": ["views/view.xml"],
    "qweb": ["static/src/xml/base.xml"],
    "installable": True,
}
