# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions

class exp_pertenencias(models.Model):
    _name = 'exp_pertenencias'
    _description = "Cantidad de pertenencias por expediente"
    
    pertenencias = fields.Integer('Cantidad de pertenencias', readonly = 0,required = False, default = 0)
    exp_id = fields.Many2one('expediente.expediente','Pertenencias', required=1, ondelete='cascade')
    
    def save(self):
        return True



class expediente(models.Model):
    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Asociación con pertenencias"
    
    
    pertenencias_id = fields.One2many('exp_pertenencias', 'exp_id', string='Pertenencias', required=False, limit=3)


    def cambiar_pertenencias(self):
        
        if self.pertenencias_id:
            idPertenencias = self.pertenencias_id[0].id
        else:
            self.env['exp_pertenencias'].create({'exp_id': self.id})
            idPertenencias = self.pertenencias_id[0].id

        if True:
            return {
                'name': "Cambiar configuración de Canon",
                'view_mode': 'form',
                'res_id': idPertenencias,  # SOLO PARA FORM
                'res_model': 'exp_pertenencias',
                'type': 'ir.actions.act_window',
                'views': [[self.env.ref('exp_pertenencias.popup_exp_pertenencias').id, "form"]],
                'target': 'new',
                #'tag': 'reload',
            }
        return True
 
    
"""     def _compute_user_check(self):
        print("------------------------------")
        print("---------checkGroup-----------")        
        #user = self.env['res.users'].browse(self._uid)
        if self.env['res.users'].browse(self.env.uid).has_group('base.access_group_exp_pertenencias_escritura'):
            self.writegroup = True
        else:
            self.writegroup = False
        print("self.writegroup: ")
        print(self.writegroup)
        """