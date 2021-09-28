# -*- coding: utf-8 -*-
# from odoo import http


# class ExpPertenecias(http.Controller):
#     @http.route('/exp_pertenecias/exp_pertenecias/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exp_pertenecias/exp_pertenecias/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exp_pertenecias.listing', {
#             'root': '/exp_pertenecias/exp_pertenecias',
#             'objects': http.request.env['exp_pertenecias.exp_pertenecias'].search([]),
#         })

#     @http.route('/exp_pertenecias/exp_pertenecias/objects/<model("exp_pertenecias.exp_pertenecias"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exp_pertenecias.object', {
#             'object': obj
#         })
