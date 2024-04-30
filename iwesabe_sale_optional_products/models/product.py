# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	optional_prod_ids = fields.Many2many('product.product', 'optional_prod_rel', 'product_id', 'template_id',string='Optional Product(s)', check_company=True)
	
	def write(self,vals):
		old_optional_prod_ids = self.mapped('optional_prod_ids')
		result = super().write(vals)
		if vals.get('optional_prod_ids'):
			for record in self:
				for product in record.optional_prod_ids:
					if not product._context.get('manual_operation'):
						product.with_context(manual_operation=True)\
						.write({'optional_prod_ids':[(4,record.product_variant_id.id)]})
				if len(old_optional_prod_ids) > len(self.mapped('optional_prod_ids')):
					removed_optional_product_ids = old_optional_prod_ids - self.mapped('optional_prod_ids')
					for removed_optional_product_id in removed_optional_product_ids:
						removed_optional_product_id.with_context(manual_operation=True)\
						.write({'optional_prod_ids':[(3,record.product_variant_id.id)]})
		return result

class ProductProduct(models.Model):
	_inherit = 'product.product'

	def write(self,vals):
		old_optional_prod_ids = self.mapped('optional_prod_ids')
		result = super().write(vals)
		if vals.get('optional_prod_ids'):
			for record in self:
				for product in record.optional_prod_ids:
					if not product._context.get('manual_operation'):
						product.with_context(manual_operation=True)\
						.write({'optional_prod_ids':[(4,record.id)]})
				if len(old_optional_prod_ids) > len(self.mapped('optional_prod_ids')):
					removed_optional_product_ids = old_optional_prod_ids - self.mapped('optional_prod_ids')
					for removed_optional_product_id in removed_optional_product_ids:
						removed_optional_product_id.with_context(manual_operation=True)\
						.write({'optional_prod_ids':[(3,record.id)]})
		return result