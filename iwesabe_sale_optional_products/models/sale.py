# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def fetch_optional_products(self):
        if not self.product_id.optional_prod_ids:
            raise UserError(_("Product option(s) are not available for this product!..."))
        action = self.env["ir.actions.actions"]._for_xml_id("iwesabe_sale_optional_products.action_product_options")
        optional_prod_ids = self.product_id.optional_prod_ids + self.product_id
        context = {
            'default_sale_line_id':self.id,
            'default_quantity':self.product_uom_qty,
            'default_optional_prod_ids':[(6,0,optional_prod_ids.ids)],
        }
        res_id = self.env['product.options'].create({
            'sale_line_id':self.id,
            'quantity':self.product_uom_qty,
            'optional_prod_ids':[(6,0,optional_prod_ids.ids)],
        })
        res_id._compute_stock_details()
        action['res_id'] = res_id.id
        action['context'] = context
        return action

