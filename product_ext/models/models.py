from odoo import models, fields, api


class ProductExt(models.Model):
    _inherit = 'product.product'

    qty_lhr = fields.Float(string='Branch 1', compute='_compute_qty_lhr', store=True, readonly=True)
    qty_karachi = fields.Float(string='Branch 2', readonly=True)
    qty_isb = fields.Float(string='Branch 3', readonly=True)

    @api.depends('qty_available')
    def _compute_qty_lhr(self):
        for product in self:
            lhr_location = self.env['stock.quant'].sudo().search(
                [('company_id.name', '=', 'lhr'), ('product_id', '=', product.id)], limit=1)
            product.qty_lhr = lhr_location.quantity
            khr_location = self.env['stock.quant'].sudo().search(
                [('company_id.name', '=', 'khr'), ('product_id', '=', product.id)], limit=1)
            product.qty_karachi = khr_location.quantity
            isb_location = self.env['stock.quant'].sudo().search(
                [('company_id.name', '=', 'isb'), ('product_id', '=', product.id)], limit=1)
            product.qty_isb = isb_location.quantity

    def create_purchase_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Purchase Wizard',
            'view_mode': 'form',
            'res_model': 'product.purchase.wizard',
            'view_id': self.env.ref('product_ext.view_product_purchase_wizard_form').id,
            'target': 'new',
            'context': {
                'active_id': self.id,
            },
        }


class SaleOrderExt(models.Model):
    _inherit = 'sale.order.line'

    def open_product_selection_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Stock Information',
            'view_mode': 'form',
            'res_model': 'multiple.product.wizard.dir',
            'target': 'new',
            'context': {
                'active_id': self.product_id.id,
            },
        }
