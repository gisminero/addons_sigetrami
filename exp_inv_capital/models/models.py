from odoo import models, fields, api, exceptions
import datetime


class  exp_inv_capital(models.Model):
	_name = 'exp_inv_capital'
	_description = 'Declaracion jurada de inversion de capital'

	name = fields.Char('Titulo', required=True, readonly=False)
	year = fields.Integer('Año al que pertenece', required=True, readonly=False)
	presentation_date = fields.Date('Fecha de presentacion', required=True, readonly=False)
	file_name = fields.Char('Declarcion Jurada')
	file = fields.Binary('Adjuntar archivo')
	registration_date = fields.datetime.now()
	user_register = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)
	validated = fields.Boolean('Validar')
	exp_id = fields.Many2one('expediente.expediente', 'Declaracion', required=1, ondelete='cascade')


	def validar(self):
		self.write({'validated': True})
		return True

class expediente(models.Model):
	_name = 'expediente.expediente'
	_inherit = 'expediente.expediente'
	_description = 'Asociando declaraciones de inversion de capital'

	declaracion_jurada_id = fields.One2many('exp_inv_capital', 'exp_id', string='Inversiones', required=False)
