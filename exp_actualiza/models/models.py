# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import datetime
import time
from datetime import datetime as dt, timedelta, date
import dateutil.parser
# from unidecode import unidecode
import psycopg2
#import psycopg.extras

class exp_actualiza_exp(models.Model):
    _name = 'exp_actualiza_exp'
    _order = "id desc"

    name = fields.Char('Expediente', required=False, readonly=False)#, default=default_name, store=False
    expediente_id = fields.Many2one('expediente.expediente','Expediente', required=False)
    estado = fields.Selection([('0', 'ID, nombre, fecha de actualizacion coinciden.'), 
        ('1', 'No existe el nombre/numero de exp. en la nueva DB.'),
        ('2', 'No existe el id en la nueva DB.'),
        ('3', 'EL id no coincide para el nombre en la nueva DB.'),
        ('4', 'EL id y nombre coincide no la fecha actualizacion.'),
        ], string='Estado', required=True, default="draft",
        help="Determina el estado del expediente")
    observ = fields.Text(string='Observaciones de Pase', translate=True)

class exp_actualiza_pases(models.Model):
    _name = 'exp_actualiza_pases'
    _order = "id desc"

    name = fields.Char('Expediente (Pase de Oficina)', required=False, readonly=False)#, default=default_name, store=False
    expediente_id = fields.Many2one('expediente.expediente','Expediente', required=False)
    estado = fields.Selection([('0', 'ID, nombre, fecha de actualizacion coinciden.'), 
        ('1', 'No existe el nombre/numero de exp. en la nueva DB.'),
        ('2', 'No existe el id en la nueva DB.'),
        ('3', 'EL id no coincide para el nombre en la nueva DB.'),
        ('4', 'EL id y nombre coincide no la fecha actualizacion.'),
        ], string='Estado', required=True, default="draft",
        help="Determina el estado del expediente")
    observ = fields.Text(string='Observaciones de Pase', translate=True)

class exp_actualiza_tareas(models.Model):
    _name = 'exp_actualiza_tareas'
    _order = "id desc"

    name = fields.Char('Expediente (Seguimiento de Tarea)', required=False, readonly=False)#, default=default_name, store=False
    expediente_id = fields.Many2one('expediente.expediente','Expediente', required=False)
    estado = fields.Selection([('0', 'ID, nombre, fecha de actualizacion coinciden.'), 
        ('1', 'No existe el nombre/numero de exp. en la nueva DB.'),
        ('2', 'No existe el id en la nueva DB.'),
        ('3', 'EL id no coincide para el nombre en la nueva DB.'),
        ('4', 'EL id y nombre coincide no la fecha actualizacion.'),
        ], string='Estado', required=True, default="draft",
        help="Determina el estado del expediente")
    observ = fields.Text(string='Observaciones de Pase', translate=True)

class exp_actualiza(models.Model):
    _name = 'exp_actualiza'
    #_inherit = ['mail.thread']
    _order = "write_date desc"  

    def default_user_id(self):
        return self.env.context.get("default_user_id", self.env.user)

    def connect(self):
	    # connecting to the database called test
	    # using the connect function
        print(("CONECTANDO"))
        try:
            conn = psycopg2.connect(dbname = "neuquen06-08-19",
                            #"NQN-08-2021",
                            #dbname ="catamarca-stm",
							user = "postgres",
							password = "123456",
							host = "192.168.2.98",
                            #host = "localhost",
							port = "5432",
                            connect_timeout="10")
		    # creating the cursor object
            cur = conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while conecting PostgreSQL table", error)
	    # returing the conn and cur
	    # objects to be used later
        return conn, cur

    def desconexion(self):
        
        return False

    #def actualiza_exp(self, name, tramite, estado_legal)
    def define_estado_actualizacion(self, id_exp, nombre, fecha_actualiza, clase):
        #DEfinir el estado de actualizaciòn
        #0: id, nombre y fecha de modificacion coincide con el registro nuevo - no accion  , ('write_date', "=", fecha_actualiza)
        #1: No existe el nombre en la nueva base de datos - debe insertarse
        #2: No existe el id en la nueva base de datos - debe insertarse
        #3: El id del registro no coincide con el nombre en la nueva base de datos - debe informarse inconsistencia
        #4: id y nombre coincide en la nueva base de datos, pero no coincide la fecha de actualizacion - Debe actualizarse
        estado_actual = 0
        print(("PARAMETROS RECIBIDOS: ID: " + str(id_exp)))
        #nombre = nombre.replace("\","\\")
        exp_obj = self.env[clase]
        #Condicion 0: id, nombre y fecha de modificacion coincide con el registro nuevo - no accion
        exp_obj_id_na_fe_count = exp_obj.search_count([('id', '=', id_exp), ('name', "=", str(nombre)), ('write_date', '=', fecha_actualiza)])
        exp_obj_id_na_fe = exp_obj.search([('id', '=', id_exp), ('name', "=", str(nombre)), ('write_date', '=', fecha_actualiza)], limit=1)
        print(("ONJETO ENTERO: " + str(exp_obj_id_na_fe)))
        if exp_obj_id_na_fe_count == 1:
            print (("Id, nombre y dmomento de actualizacion coinciden - No se realiza acción."))
            print(("Fecha de actualizaciòn: " + exp_obj_id_na_fe[0].write_date.strftime("%d/%m/%Y, %H:%M:%S")))
            return 0
        if clase=='expediente.expediente':
            print (("Id, nombre y dmomento de actualizacion NOOOO coinciden - Se realiza acción. A continuacuion se tratara"))
            #COndicion 1: No Existe el nombre en la base de datos
            exp_obj_id_na = exp_obj.search([('name', "=", str(nombre))], limit=1)
            exp_obj_na_count = exp_obj.search_count([('name', "=", str(nombre))])
            print(("ONJETO NOMBRE: " + str(exp_obj_id_na)))
            exp_obj_id = exp_obj.search([('id', '=', id_exp)], limit=1)
            exp_obj_id_count = exp_obj.search_count([('id', '=', id_exp)])
            if exp_obj_na_count == 0:
                #No existe el nombre en la base de datos
                print (("No existe el nombre de expediente en la DB"))
                return 1
            elif exp_obj_id_na[0].id == id_exp:
                print (("************************************************************")) 
                print (("El nombre coincide con ID, pero no la fecha de actualizaciò.")) 
                print (("************************************************************")) 
                return 4
            elif exp_obj_id != False:
                print (("EL ID del registro no coincide en la nueva DB, se debe informar inconsistencia"))
                return 3
            else:
                print (("No existe el id en la BD, tampoco se encontro el nombre de exp."))
                return 2
        if clase=='pase.pase':
            exp_obj_id = exp_obj.search([('id', '=', id_exp)], limit=1)
            exp_obj_id_count = exp_obj.search_count([('id', '=', id_exp)])
            if exp_obj_id_count == 0:
                return 2
            if exp_obj_id_count == 1:
                print (("EL ID SE ENCUENTRA Y SE DEBE ACTUALIZAR"))
                return 4

    def usuario_existe(self, user_id):
        usr_obj = self.env['res.users']
        usr_obj_count = usr_obj.search_count([('id', '=', user_id)])
        if usr_obj_count==0:
            return 1
        else:
            return user_id



    def inserta_registro(self, reg_nuevo,clase):
        print(("CREANDO REGISTRO"))
        #Campos obligatorios: name, state, procedimiento_id, folios, nombre_pedimento, momento_inicio, active, ultimo_pase_id, ubicacion_actual
        # recibido, provincia
        #Update Sequence#
        #query_sec = """ALTER SEQUENCE IF EXISTS public.%s_id_seq minvalue 1 increment 1;"""
        exp_obj = self.env[clase]
        usr_origen_valido =  self.usuario_existe(reg_nuevo['user_origen_id'])
        usr_rec_valido =  self.usuario_existe(reg_nuevo['user_recep_id'])
        if clase=='expediente.expediente':
            query_sec = "SELECT setval('expediente_expediente_id_seq', %s, true);"
            print (("Estableciendo el valor del id actual en : " + str(reg_nuevo['id']-1)))
            self.env.cr.execute(query_sec, [reg_nuevo['id']-1])
            self.env.cr.commit()
            reg_creado = exp_obj.create([{'name': reg_nuevo['name'] , 'state': reg_nuevo['state'], 'procedimiento_id': reg_nuevo['procedimiento_id'], 
                                'folios': reg_nuevo['folios'], 'nombre_pedimento': 'Gualcamayo', 'active': True , 
                                'ubicacion_actual': reg_nuevo['ubicacion_actual'], 'en_flujo': reg_nuevo['en_flujo'],
                                'recibido': reg_nuevo['recibido'], 'provincia': 566, 'cant_pertenencias': 0}]) 
        if clase=='pase.pase':
            query_sec = "SELECT setval('pase_pase_id_seq', %s, true);"
            print (("Estableciendo el valor del id actual en : " + str(reg_nuevo['id']-1)))
            self.env.cr.execute(query_sec, [reg_nuevo['id']-1])
            self.env.cr.commit()
            #keys =  ['id', 'name', 'write_date', 'expediente_id', 'depart_origen_id', 'depart_destino_id', 'user_origen_id', 'user_recep_id', 
            #'fecha_hora_envio', 'fecha_hora_recep', 'folios', 'observ_pase']
            reg_creado = exp_obj.create([{'name': reg_nuevo['name'] , 'expediente_id': reg_nuevo['expediente_id'], 
                                'depart_origen_id': reg_nuevo['depart_origen_id'], 
                                'depart_destino_id': reg_nuevo['depart_destino_id'], 'user_origen_id': usr_origen_valido, 
                                'user_recep_id': usr_rec_valido, 
                                'fecha_hora_envio': reg_nuevo['fecha_hora_envio'], 'fecha_hora_recep': reg_nuevo['fecha_hora_recep'],
                                'folios': reg_nuevo['folios'], 'observ_pase': reg_nuevo['observ_pase']}])
        self.env.cr.commit()
        #Nota el id correspondiente al ùltmimo pase se insertara cuando se actualice la tabla pases.pases
        #'ultimo_pase_id': 14,
        print(("REGISTRO CREADO: " + str(reg_creado)))
        return True

    def actualiza_registro(self, reg_modificado, id_reg_modificar, clase):
        #Modificar registro para actualizarlo
        print(("EL ID DE "+ clase +" QUE VIENE ES: " + str(id_reg_modificar)))
        exp_obj = self.env[clase].browse([id_reg_modificar])
        print (("ACTUALIZANDO REGISTRO "+clase+" : " + str(exp_obj)))
        usr_rec_valido =  self.usuario_existe(reg_modificado['user_recep_id'])
        if clase =="expediente.expediente":
            #keys =  ['id', 'name', 'write_date', 'procedimiento_id', 'folios', 'estado_legal_actual', 'ubicacion_actual', 'tarea_actual', 'en_flujo']
            exp_obj.write({'procedimiento_id': reg_modificado['procedimiento_id'], 'folios' : reg_modificado['folios'],  
                'ubicacion_actual': reg_modificado['ubicacion_actual'], 'en_flujo': reg_modificado['en_flujo'], 'state': reg_modificado['state'],
                'tarea_actual': reg_modificado['tarea_actual']})
        if clase =="pase.pase":
            #keys =  ['id', 'name', 'write_date', 'expediente_id', 'depart_origen_id', 'depart_destino_id', 'user_origen_id', 'user_recep_id', 
            #    'fecha_hora_envio', 'fecha_hora_recep', 'folios', 'observ_pase']
            exp_obj.write({'write_date': reg_modificado['write_date'], 'folios' : reg_modificado['folios'],  
                'depart_origen_id': reg_modificado['depart_origen_id'], 'depart_destino_id': reg_modificado['depart_destino_id'],
                'user_recep_id': usr_rec_valido, 'fecha_hora_recep': reg_modificado['fecha_hora_recep']})
        return True

    def inserta_comunicacion(self, id_exp, nombre, fecha_actualiza, estado, clase, obs):
        if estado == "2":
            id_exp = False
        if clase == "expediente":
            exp_obj = self.env['exp_actualiza_exp']
            print (("CREANDO COMUNICACION EXPEDIENTE"))
            exp_obj.create([{'name': nombre, 'expediente_id' : id_exp, 'estado' : estado, 'observ': obs},])        
        return True


    def accion_necesaria(self, record_dict, estado, clase):
    #keys =  ['id', 'name', 'write_date', 'procedimiento_id', 'folios', 'estado_legal_actual', 'ubicacion_actual', 'tarea_actual', 'en_flujo']
        if estado == 0:
            print (("No llamar a metodo de actualizacion de registro"))
        elif estado == 1:
            print (("Informar Faltante de Registro, no encontrado por nombre"))
            obs = "Informar Faltante de Registro, no encontrado por nombre, INSETANDO EL REGISTRO"
            print (("########################################### INSERTANDO REGISTRO ###########################"))
            self.inserta_registro(record_dict, clase)
            #self.inserta_comunicacion(record_dict['id'], record_dict['name'], record_dict['write_date'], str(estado), clase, obs)
            exit()
        elif estado == 2:
            print (("No existe el nombre ni ID en la nueva DB"))
            obs = "No existe el nombre ni ID en la nueva DB"
            self.inserta_comunicacion(record_dict['id'], record_dict['name'], record_dict['write_date'], str(estado), clase, obs)
        elif estado==3:
            print (("El id del registro no coincide con el nombre en la nueva base de datos - debe informarse inconsistencia"))
            obs = "El id del registro no coincide con el nombre en la nueva base de datos - debe informarse inconsistencia"
            self.inserta_comunicacion(record_dict['id'], record_dict['name'], record_dict['write_date'], str(estado), clase, obs)
        elif estado==4:
            print(("******************************************"))
            print(("Id y nombre coincide en la nueva base de datos, pero no coincide la fecha de actualizacion - Debe actualizarse"))
            print(("******************************************"))
            obs = "Id y nombre coincide en la nueva base de datos, pero no coincide la fecha de actualizacion - Se actualizará autommáticamente"
            self.inserta_comunicacion(record_dict['id'], record_dict['name'], record_dict['write_date'], str(estado), clase, obs)
            self.actualiza_registro(record_dict, record_dict['id'], clase)
            #exit()
        return True

    def list_to_dict(self, keys1, record):
        # using naive method to convert lists to dictionary
        # = {}
        record_dict = dict(zip(keys1, record))
        #print ("Resultant dictionary is : " +  str(record_dict))
        return record_dict

    def consulta_exp(self):
        print(("INGRESANDO POR CONSULTA"))
        conn, cur = self.connect()        
        # Open a cursor to perform database operations    
        keys =  ['id', 'name', 'write_date', 'procedimiento_id', 'folios', 'estado_legal_actual', 'ubicacion_actual', 'tarea_actual', 'en_flujo', 'state', 'recibido']
        cur.execute("SELECT id, name, write_date, procedimiento_id, folios, estado_legal_actual, ubicacion_actual, tarea_actual, en_flujo, state, recibido FROM expediente_expediente")
        cur.fetchone()
        # will return (1, 100, "abc'def")
        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            print(("EL EXPEDIENTE ES: " + str(record[1])))
            estado = self.define_estado_actualizacion(record[0], record[1], record[2], 'expediente.expediente')
            record_dict = self.list_to_dict(keys, record)
            self.accion_necesaria(record_dict, estado, 'expediente.expediente')
        return True

    def consulta_pases(self):
        print(("CONSULTANDO PASES"))
        conn, cur = self.connect()        
        # Open a cursor to perform database
        #  operations    
        keys =  ['id', 'name', 'write_date', 'expediente_id', 'depart_origen_id', 'depart_destino_id', 'user_origen_id', 'user_recep_id', 
                'fecha_hora_envio', 'fecha_hora_recep', 'folios', 'observ_pase']
        cur.execute("SELECT id, name, write_date, expediente_id, depart_origen_id, depart_destino_id, user_origen_id, user_recep_id, fecha_hora_envio, fecha_hora_recep, folios, observ_pase FROM pase_pase")
        cur.fetchone()
        # will return (1, 100, "abc'def")
        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            print(("EL PASE TRABAJADO CORRESPONDE AL EXPTE: " + str(record[1])))
            estado = self.define_estado_actualizacion(record[0], record[1], record[2], 'pase.pase')
            record_dict = self.list_to_dict(keys, record)
            self.accion_necesaria(record_dict, estado, 'pase.pase')
        return True

    def consulta_historial_tareas(self):
        return True


    def rastreo(self):
        #self.conexion_externa()
        #self.consulta_exp()
        self.consulta_pases()
        return True

