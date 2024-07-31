# -*- coding: utf-8 -*-
from odoo import http


class ProductExt(http.Controller):
    @http.route('/product_ext/product_ext', auth='public')
    def index(self, **kw):
        return "Hello, world"

#     @http.route('/product_ext/product_ext/objects', auth='public')f
#     def list(self, **kw):
#         return http.request.render('product_ext.listing', {
#             'root': '/product_ext/product_ext',
#             'objects': http.request.env['product_ext.product_ext'].search([]),
#         })

#     @http.route('/product_ext/product_ext/objects/<model("product_ext.product_ext"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_ext.object', {
#             'object': obj
#         })

