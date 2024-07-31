from odoo import models, fields, api


class MultipleProductWizardLine(models.TransientModel):
    _name = 'multiple.product.wizard.line'
    _description = 'Product Quantities per Warehouse'

    wizard_id = fields.Many2one('multiple.product.wizard.dir', string='Wizard')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', readonly=True)
    qty_on_hand = fields.Float(string='On Hand Quantity', readonly=True)
    qty_available = fields.Float(string='Available Quantity', readonly=True)


class MultipleProductWizard(models.TransientModel):
    _name = 'multiple.product.wizard.dir'
    _description = 'Select Products'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    line_ids = fields.One2many('multiple.product.wizard.line', 'wizard_id')

    @api.model
    def default_get(self, fields):
        res = super(MultipleProductWizard, self).default_get(fields)
        product_id = self.env.context.get('active_id')
        res['product_id'] = product_id
        return res

    @api.model
    def create(self, vals):
        res = super(MultipleProductWizard, self).create(vals)
        res._compute_product_quantities()
        return res

    @api.onchange('product_id')
    def _compute_product_quantities(self):
        if self.product_id:
            warehouses = self.env['stock.warehouse'].search([])
            lines = []
            for warehouse in warehouses:
                qty_on_hand = self.product_id.with_context(warehouse=warehouse.id).qty_available
                qty_available = self.product_id.with_context(warehouse=warehouse.id).virtual_available
                lines.append((0, 0, {
                    'warehouse_id': warehouse.id,
                    'qty_on_hand': qty_on_hand,
                    'qty_available': qty_available,
                }))
            self.line_ids = lines
        else:
            self.line_ids = [(5, 0, 0)]
