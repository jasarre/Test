# -*- coding: utf-8 -*-

import jinja2
from odoo import models, fields, api, _

class ProductOptions(models.TransientModel):
	_name = 'product.options'
	_description = "Product Options"

	optional_prod_ids = fields.Many2many('product.product',)
	sale_line_id = fields.Many2one('sale.order.line')
	quantity = fields.Float('Quantity')
	optional_product_id = fields.Many2one('product.product', string="Optional Product")
	stock_details = fields.Html('',compute="_compute_stock_details")

	def _compute_stock_details(self):
		for record in self:
			product_body = """"""
			for optional_prod_id in record.optional_prod_ids:
				product_body += """
					 <h2 style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">{product_name}</h2>
				""".format(product_name = optional_prod_id.display_name)
				quant_ids = self.env['stock.quant'].sudo().search([('product_id','=',optional_prod_id.id),
						       ('location_id.usage','=','internal')])
				if quant_ids:
					
					for quant_id in quant_ids:
						unit_details = str(quant_id.available_quantity) +'  '+quant_id.product_uom_id.name
						product_body += """
							<div style="display: flex; align-items: center; margin-bottom: 10px;">
								<div style="font-weight: bold; width: 120px;">{location_name}</div>
								<div style="display: flex;">
									<div style="margin-right: 10px;"><strong>Stock:</strong></div>
									<div style="color: green;">{unit_details}</div>
								</div>
							</div>
						""".format(location_name=quant_id.location_id.display_name,unit_details=unit_details)
			body = """
				<div style="margin: 20px;">
    				<h1 style="text-align: center;">Product Stock Availability</h1>
				     <div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
      					<div style="width: 100%; background-color: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); padding: 20px; margin-bottom: 20px;">
					    	{{product_body}}
						</div>
					</div>
				</div>
			"""
			
			body = body.replace("\n", "")
			formatted = jinja2.Template(body).render(product_body=product_body)
			record.stock_details = formatted
	
	def action_submit(self):
		self.sale_line_id.update({
			'product_id':self.optional_product_id.id,
			'name':self.optional_product_id.display_name,
			'product_uom_qty':self.quantity
		})
