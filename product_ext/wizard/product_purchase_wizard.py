from odoo import models, fields, api


class ProductPurchaseWizard(models.TransientModel):
    _name = 'product.purchase.wizard'
    _description = 'Product Purchase Wizard'

    product_id = fields.Many2one('product.product', string='Product')
    vendor_id = fields.Many2one('res.partner', string='Vendor')

    @api.model
    def default_get(self, fields):
        res = super(ProductPurchaseWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            product = self.env['product.product'].browse(active_id)
            res.update({
                'product_id': product.id,
            })
        return res

    def create_purchase_order(self):
        self.ensure_one()
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.vendor_id.id,
            'order_line': [(0, 0, {
                'product_id': self.product_id.id,
                'price_unit': self.product_id.lst_price,
            })],
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'target': 'current',
        }
