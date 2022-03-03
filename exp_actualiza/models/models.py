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
        ], string='Estado', required=False, default="draft",
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
            conn = psycopg2.connect(dbname = "nombre_base",
							user = "postgres",
							password = "******",
							host = "localhost",
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
            #print(("ONJETO NOMBRE: " + str(exp_obj_id_na)))
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
                print (("SE ENCONTRO UN REGISRTO QUE NO SE ENCUETRA EN LA NUEVA BD ..... " + str(id_exp) ))
                #exit()
                return 1
            if exp_obj_id_count == 1:
                print (("EL ID SE ENCUENTRA Y SE DEBE ACTUALIZAR"))
                return 4
        if clase=='seguimiento':
            exp_obj_id = exp_obj.search([('id', '=', id_exp)], limit=1)
            exp_obj_id_count = exp_obj.search_count([('id', '=', id_exp)])
            if exp_obj_id_count == 0:
                #print (("SE ENCONTRO UN REGISRTO QUE NO SE ENCUETRA EN LA NUEVA BD ..... " + str(id_exp) ))
                return 1 #no esxiste la actualizacion para ese registro.
        if clase=='seguimiento_linea':
            exp_obj_id = exp_obj.search([('id', '=', id_exp)], limit=1)
            exp_obj_id_count = exp_obj.search_count([('id', '=', id_exp)])
            if exp_obj_id_count == 0:
                print (("SE ENCONTRO UN REGISRTO QUE NO SE ENCUETRA EN LA NUEVA BD ..... " + str(id_exp) ))
                #exit()
                return 1
            if exp_obj_id_count == 1:
                print (("EL ID SE ENCUENTRA Y SE DEBE ACTUALIZAR"))
                return 4


    def usuario_existe(self, user_id):
        usr_obj = self.env['res.users']
        #print(("EL USUARIO QUE SE DEBE TRASNFORMAR ES: " + str(user_id)))
        if user_id == None:
            return None
        usr_obj_count = usr_obj.search_count([('id', '=', user_id)])
        if usr_obj_count==0:
            return 1
        else:
            return user_id



    def inserta_registro(self, reg_nuevo,clase):
        #print(("CREANDO REGISTRO"))
        exp_obj = self.env[clase]
        if clase=='expediente.expediente':
            query_sec = "SELECT setval('expediente_expediente_id_seq', %s, true);"
            #print (("Estableciendo el valor del id actual en : " + str(reg_nuevo['id']-1)))
            self.env.cr.execute(query_sec, [reg_nuevo['id']-1])
            self.env.cr.commit()
            reg_creado = exp_obj.create([{'name': reg_nuevo['name'] , 'state': reg_nuevo['state'], 'procedimiento_id': reg_nuevo['procedimiento_id'], 
                                'folios': reg_nuevo['folios'], 'nombre_pedimento': 'Gualcamayo', 'active': True , 
                                'ubicacion_actual': reg_nuevo['ubicacion_actual'], 'en_flujo': reg_nuevo['en_flujo'],
                                'recibido': reg_nuevo['recibido'], 'provincia': 566, 'cant_pertenencias': 0,
                                'observaciones': reg_nuevo['observaciones']}]) 
        if clase=='pase.pase':
            usr_origen_valido =  self.usuario_existe(reg_nuevo['user_origen_id'])
            usr_rec_valido =  self.usuario_existe(reg_nuevo['user_recep_id'])
            query_sec = "SELECT setval('pase_pase_id_seq', %s, true);"
            #print (("Estableciendo el valor del id actual en : " + str(reg_nuevo['id']-1)))
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
        if clase=='seguimiento':
            query_sec = "SELECT setval('seguimiento_id_seq', %s, true);"
            #print (("Estableciendo el valor del id actual en : " + str(reg_nuevo['id']-1)))
            self.env.cr.execute(query_sec, [reg_nuevo['id']-1])
            self.env.cr.commit()
            #print(("el id de expediente traiso es: " + str(reg_nuevo['expediente_id'])))
            reg_creado = exp_obj.create([{'name': reg_nuevo['name'] , 'expediente_id': reg_nuevo['expediente_id']}]) 
        if clase=='seguimiento_linea':
            query_sec = "SELECT setval('seguimiento_linea_id_seq', %s, true);"
            #print (("Estableciendo el valor del id actual en : " + str(reg_nuevo['id']-1)))
            self.env.cr.execute(query_sec, [reg_nuevo['id']-1])
            self.env.cr.commit()
            #print(("el id de expediente traiso es: " + str(reg_nuevo['seguimiento_id'])))
            reg_creado = exp_obj.create([{'name': reg_nuevo['name'] , 'seguimiento_id': reg_nuevo['seguimiento_id'], 'tarea': reg_nuevo['tarea'], 
                                        'tarea_inicio': reg_nuevo['tarea_inicio'], 
                                        'subproc': reg_nuevo['subproc'], 'observ_segui': reg_nuevo['observ_segui'], 'create_uid': reg_nuevo['create_uid'] }]) 
        self.env.cr.commit()
        #Nota el id correspondiente al ùltmimo pase se insertara cuando se actualice la tabla pases.pases
        #'ultimo_pase_id': 14,
        #print(("REGISTRO CREADO: " + str(reg_creado)))
        return True

    def actualiza_registro(self, reg_modificado, id_reg_modificar, clase):
        #Modificar registro para actualizarlo
        #print(("EL ID DE "+ clase +" QUE VIENE ES: " + str(id_reg_modificar)))
        exp_obj = self.env[clase].browse([id_reg_modificar])
        #print (("ACTUALIZANDO REGISTRO "+clase+" : " + str(exp_obj)))
        #print (("UBICACION ACTUAL "+clase+" : " + str(reg_modificado['tarea_actual'])))
        if clase =="expediente.expediente":
            #keys =  ['id', 'name', 'write_date', 'procedimiento_id', 'folios', 'estado_legal_actual', 'ubicacion_actual', 'tarea_actual', 'en_flujo']
            exp_obj.write({'procedimiento_id': reg_modificado['procedimiento_id'], 'folios' : reg_modificado['folios'],  
                'ubicacion_actual': reg_modificado['ubicacion_actual'], 'en_flujo': reg_modificado['en_flujo'], 'state': reg_modificado['state'],
                'tarea_actual': reg_modificado['tarea_actual'], 'recibido': reg_modificado['recibido'], 'observaciones': reg_modificado['observaciones'],
                'oficina_destino': reg_modificado['oficina_destino']})
        if clase =="pase.pase":
            #print(("FECHA HORA DE RECEPCION: " + str(reg_modificado['fecha_hora_recep'])))
            usr_rec_valido =  self.usuario_existe(reg_modificado['user_recep_id'])
            #keys =  ['id', 'name', 'write_date', 'expediente_id', 'depart_origen_id', 'depart_destino_id', 'user_origen_id', 'user_recep_id', 
            #    'fecha_hora_envio', 'fecha_hora_recep', 'folios', 'observ_pase']
            exp_obj.write({'write_date': reg_modificado['write_date'], 'folios' : reg_modificado['folios'],  
                'depart_origen_id': reg_modificado['depart_origen_id'], 'depart_destino_id': reg_modificado['depart_destino_id'],
                'user_recep_id': usr_rec_valido, 'fecha_hora_recep': reg_modificado['fecha_hora_recep']})
        self.env.cr.commit()
        return True

    def inserta_comunicacion(self, id_exp, nombre, fecha_actualiza, estado, clase, obs):
        if estado == "2":
            id_exp = False
        if clase == "expediente":
            exp_obj = self.env['exp_actualiza_exp']
            #print (("CREANDO COMUNICACION EXPEDIENTE"))
            exp_obj.create([{'name': nombre, 'expediente_id' : id_exp, 'estado' : estado, 'observ': obs},])        
        if clase == "departamento":
            exp_obj = self.env['exp_actualiza_exp']
            #print (("CREANDO COMUNICACION EXPEDIENTE"))
            exp_obj.create([{'name': nombre, 'expediente_id' : id_exp, 'estado' : estado, 'observ': obs},])        
        return True


    def accion_necesaria(self, record_dict, estado, clase):
    #keys =  ['id', 'name', 'write_date', 'procedimiento_id', 'folios', 'estado_legal_actual', 'ubicacion_actual', 'tarea_actual', 'en_flujo']
        if estado == 0:
            print (("No llamar a metodo de actualizacion de registro"))
        elif estado == 1:
            #print (("Informar Faltante de Registro, no encontrado por nombre"))
            obs = "Informar Faltante de Registro, no encontrado por nombre, INSETANDO EL REGISTRO"
            #print (("########################################### INSERTANDO REGISTRO ###########################"))
            self.inserta_registro(record_dict, clase)
            #self.inserta_comunicacion(record_dict['id'], record_dict['name'], record_dict['write_date'], str(estado), clase, obs)
            #exit()
        elif estado == 2:
            #print (("No existe el nombre ni ID en la nueva DB"))
            obs = "No existe el nombre ni ID en la nueva DB"
            self.inserta_comunicacion(record_dict['id'], record_dict['name'], record_dict['write_date'], str(estado), clase, obs)
        elif estado==3:
            #print (("El id del registro no coincide con el nombre en la nueva base de datos - debe informarse inconsistencia"))
            obs = "El id del registro no coincide con el nombre en la nueva base de datos - debe informarse inconsistencia"
            self.inserta_comunicacion(record_dict['id'], record_dict['name'], record_dict['write_date'], str(estado), clase, obs)
        elif estado==4:
            #print(("******************************************"))
            #print(("Id y nombre coincide en la nueva base de datos, pero no coincide la fecha de actualizacion - Debe actualizarse"))
            #print(("******************************************"))
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
        keys =  ['id', 'name', 'write_date', 'procedimiento_id', 'folios', 'estado_legal_actual', 'ubicacion_actual', 'tarea_actual', 'en_flujo', 'state', 'recibido', 'observaciones', 'oficina_destino']
        cur.execute("SELECT id, name, write_date, procedimiento_id, folios, estado_legal_actual, ubicacion_actual, tarea_actual, en_flujo, state, recibido, observaciones, oficina_destino FROM expediente_expediente ORDER BY id ASC")
        cur.fetchone()
        for record in cur:
            print(("EL EXPEDIENTE ES: " + str(record[1])))
            estado = self.define_estado_actualizacion(record[0], record[1], record[2], 'expediente.expediente')
            record_dict = self.list_to_dict(keys, record)
            self.accion_necesaria(record_dict, estado, 'expediente.expediente')
        return True

    def consulta_pases(self):
        #print(("CONSULTANDO PASES"))
        conn, cur = self.connect()        
        keys =  ['id', 'name', 'write_date', 'expediente_id', 'depart_origen_id', 'depart_destino_id', 'user_origen_id', 'user_recep_id', 
                'fecha_hora_envio', 'fecha_hora_recep', 'folios', 'observ_pase']
        cur.execute("SELECT id, name, write_date, expediente_id, depart_origen_id, depart_destino_id, user_origen_id, user_recep_id, fecha_hora_envio, fecha_hora_recep, folios, observ_pase FROM pase_pase ORDER BY id ASC")
        cur.fetchone()
        for record in cur:
            #print(("EL PASE TRABAJADO CORRESPONDE AL EXPTE: " + str(record[1])))
            estado = self.define_estado_actualizacion(record[0], record[1], record[2], 'pase.pase')
            record_dict = self.list_to_dict(keys, record)
            self.accion_necesaria(record_dict, estado, 'pase.pase')
        return True

    def consulta_seguimiento(self):
        conn, cur = self.connect()        
        keys =  ['id', 'name', 'write_date', 'expediente_id']
        cur.execute("SELECT id, name, write_date, expediente_id FROM seguimiento ORDER BY id ASC")
        cur.fetchone()
        # will return (1, 100, "abc'def")
        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            #print(("EL SEGIMIENTO TRABAJADO CORRESPONDE AL EXPTE: " + str(record[1])))
            estado = self.define_estado_actualizacion(record[0], record[1], record[2], 'seguimiento')
            record_dict = self.list_to_dict(keys, record)
            self.accion_necesaria(record_dict, estado, 'seguimiento')
        return True

    def consulta_seguimiento_linea(self):
        #print(("CONSULTANDO SEGUIMIENTO_LINEA"))
        conn, cur = self.connect()        
        # Open a cursor to perform database
        #  operations    
        keys =  ['id', 'name', 'write_date', 'create_uid', 'tarea_inicio', 'seguimiento_id', 'observ_segui', 'tarea', 'subproc']
        cur.execute("SELECT id, name, write_date, create_uid, tarea_inicio, seguimiento_id, observ_segui, tarea, subproc FROM seguimiento_linea ORDER BY id ASC")
        cur.fetchone()
        # You can use()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            #print(("EL SEGUIMIENTO LINEA TRABAJADO CORRESPONDE AL EXPTE: " + str(record[1])))
            estado = self.define_estado_actualizacion(record[0], record[1], record[2], 'seguimiento_linea')
            record_dict = self.list_to_dict(keys, record)
            self.accion_necesaria(record_dict, estado, 'seguimiento_linea')
        return True

    def obtener_nuevo_id(self, record_dict, clase):
        nuevo_depart_id = 1
        obj = self.env[clase]
        obj_count = obj.search_count([('name', '=', record_dict['name'])])#, ('active','=', True)
        if obj_count > 0:
            obj = obj.search([('name', '=', record_dict['name'])])#, ('active','=', True)
            if clase == 'departamento.departamento':
                return obj[0].id, obj[0].state_id.id
            if clase == 'mineral':
                return obj[0].id, obj[0].categoria
        else:
            print(("EL DEPARTAMENTO/MINERAL NO ENOTRADO ES:" + record_dict['name']))
            self.inserta_comunicacion(record_dict['expediente_expediente_id'], record_dict['name'], False, "1", "departamento", "No se encontró el departamento/mineral por nombre: " + record_dict['name'])
            self.env.cr.commit()
            print(("Retornando False"))
            return False, False

    def insert_expte_en_tabla(self, exp_id, tabla, nuevo_id, state_id):
        if tabla == "departamento":
            depart_obj = self.env['exp_depart']
            exp_obj_count = depart_obj.create({'departamento_id': nuevo_id, 
                                                'exp_id': exp_id,
                                                'state_id_exp': state_id})
        if tabla == "mineral":
            min_obj = self.env['exp_mineral']
            print(("LA categoria que se intenta ingresar es: " + str(state_id)))
            exp_obj_count = min_obj.create({'mineral_id': nuevo_id, 
                                                'exp_id': exp_id,
                                                'categoria_mineral_exp': state_id})
        self.env.cr.commit()
        return True


    def actualizar_si_es_necesario(self, record_dict, tabla):
        if tabla == "departamento":
            nuevo_depart_id, nuevo_state_id = self.obtener_nuevo_id(record_dict, 'departamento.departamento')
            if nuevo_depart_id is False:
                print(("DEPARTAMENTO NO ENCONTRADO POR NOMBRE EN LA NUEVA TABLA"))
                print(("-----------------------   " + record_dict['name'] + " --------------------"))
                return False
            else:
                print(("EL id del departamento en la nueva tabla es: " + str(nuevo_depart_id)))
            print(("Buscando la combinacion expediente/departamento."))
            depart_obj = self.env['exp_depart']
            exp_obj_count = depart_obj.search_count([('exp_id', '=', record_dict['expediente_expediente_id']), 
                            ('departamento_id', '=', nuevo_depart_id)])
            if exp_obj_count == 0:
                print (("EL EXPEDIENTE NO TIENE CARGADO EL DEPARTAMENTO ENCONTRADO: " + record_dict['name'] + "  EL ID VIEJO ES: " + str(record_dict['departamento_departamento_id'])))
                self.insert_expte_en_tabla(record_dict['expediente_expediente_id'], tabla, nuevo_depart_id, nuevo_state_id)
        if tabla == "mineral":
            nuevo_mineral_id, categoria = self.obtener_nuevo_id(record_dict, 'mineral')
            if nuevo_mineral_id is False:
                print(("MINERAL NO ENCONTRADO POR NOMBRE EN LA NUEVA TABLA"))
                print(("-----------------------   " + record_dict['name'] + " --------------------"))
                return False
            else:
                print(("EL id del MINERAL en la nueva tabla es: " + str(nuevo_mineral_id)))
            print(("Buscando la combinacion expediente/mineral."))
            mineral_obj = self.env['exp_mineral']
            exp_obj_count = mineral_obj.search_count([('exp_id', '=', record_dict['expediente_expediente_id']), 
                            ('mineral_id', '=', nuevo_mineral_id)])
            if exp_obj_count == 0:
                print (("EL EXPEDIENTE NO TIENE CARGADO EL mineral ENCONTRADO: " + record_dict['name']  ))
                self.insert_expte_en_tabla(record_dict['expediente_expediente_id'], tabla, nuevo_mineral_id, categoria.lower())
        return True

    def consulta_depart_exp(self):
        #print(("CONSULTANDO SEGUIMIENTO_LINEA"))
        conn, cur = self.connect()        
        # Open a cursor to perform database
        #  operations
        # Como operacion previa se puede borrar la tabla entera (DROP), para insertar todos los registros
        # Nuevamente    
        keys =  ['expediente_expediente_id', 'departamento_departamento_id', 'name']
        cur.execute("SELECT expediente_expediente_id, departamento_departamento_id, name FROM departamento_departamento_expediente_expediente_rel \
                    INNER JOIN departamento_departamento \
                    ON departamento_departamento_expediente_expediente_rel.departamento_departamento_id = departamento_departamento.id \
                    ORDER BY id ASC")
        # WHERE departamento_departamento_expediente_expediente_rel.expediente_expediente_id = 26432 \
        res = cur.fetchall()
        for record in res:
            record_dict = self.list_to_dict(keys, record)
            print(("Registro encontrado"))
            self.actualizar_si_es_necesario(record_dict, 'departamento')
        return True

    def consulta_mineral_exp(self):
        #print(("CONSULTANDO SEGUIMIENTO_LINEA"))
        conn, cur = self.connect()        
        # Open a cursor to perform database
        #  operations
        # Como operacion previa se puede borrar la tabla entera (DROP), para insertar todos los registros
        # Nuevamente    
        keys =  ['expediente_expediente_id', 'mineral_id', 'name']
        cur.execute("SELECT expediente_expediente_id, mineral_id, name FROM expediente_expediente_mineral_rel \
                    INNER JOIN mineral \
                    ON expediente_expediente_mineral_rel.mineral_id = mineral.id \
                    ORDER BY id ASC")
        #WHERE expediente_expediente_mineral_rel.expediente_expediente_id = 22080 \
        res = cur.fetchall()
        for record in res:
            record_dict = self.list_to_dict(keys, record)
            print(("Registro encontrado"))
            self.actualizar_si_es_necesario(record_dict, 'mineral')
        return True

    def rastreo(self):
        #self.consulta_exp()
        #self.consulta_pases()
        #self.consulta_seguimiento()
        #self.consulta_seguimiento_linea()
        #self.consulta_depart_exp()
        self.consulta_mineral_exp()
        return True

