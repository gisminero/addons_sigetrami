# -*- coding: utf-8 -*-

from odoo import models, fields, api

class departamento(models.Model):
    _name = 'departamento.departamento'
    name = fields.Char('Nombre', required=True)
    # description = fields.Char('Descripcion', required=False)
    state_id = fields.Many2one('res.country.state', string="Provincia")
    distritos = fields.One2many('exp_distrito', 'depart_id', string='Distritos Mineros',required=False)
    active = fields.Boolean('Activo', default=True)

    def name_get(self):
        result = []
        for record in self:
            if not record.name:
                nombre = "-"
            else:
                nombre = record.name
            if not record.state_id:
                prov = "(-)"
            else:
                prov = " (" + record.state_id.name + ")"
            record_name = nombre + prov
            result.append((record.id, record_name))
        return result


class exp_distrito(models.Model):
    _name = 'exp_distrito'
    name = fields.Char('Distrito Minero', required=True)
    # description = fields.Char('Descripcion', required=False)
    depart_id = fields.Many2one('departamento.departamento', string="Departamento")
    active = fields.Boolean('Activo', default=True)

# class departamento(models.Model):
#     _name = 'departamento.departamento'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100