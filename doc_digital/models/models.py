# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
#from unidecode import unidecode
#from PyPDF2 import PdfFileWriter, PdfFileReader, utils.PdfReadError
import PyPDF2
#pip install pypdf2
import time
import os
import urllib
import base64
import pybase64
# from endesive-master import examples
# from endesivemaster.examples.pdfsigncmssigetrami import hash
# import subprocess
import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive.pdf import cms

from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *

class doc_digital_archivo(models.Model):
        _name = 'doc_digital.archivo'
        _order = "id asc"

        def default_archivo_name(self):
                nombre = ""
                return nombre

        def user_emple(self, user_id):
                num_empl = self.env['hr.employee'].search_count([('user_id', '=', [user_id])])
                if num_empl < 1:
                        print(("No se encuentra el empleado asociado al usuario: " + str(user_id)))
                        return False
                elif num_empl > 1:
                        print(("Hay mas de un emplado asociado al usuario: " + str(user_id)))
                        return False
                else:
                        empl_obj = self.env['hr.employee'].search([('user_id', '=', [user_id])])
                        if empl_obj.id:
                                return empl_obj.id
                        else:
                                return False

        def _default_archivo_emple(self):
                user_id = self.env.user.id
                emple_id = self.user_emple(user_id)
                return emple_id

        name = fields.Char('Nombre', required=True, default=default_archivo_name, readonly=True)
        archivo = fields.Binary('Archivo', required=True, filters='*.png,*.gif')
        # archivo_name = fields.Char('Nombre Archivo', required=False)
        doc_digital_id = fields.Many2one('doc_digital', string='Doc. Digital')
        state = fields.Selection([('draft', 'Borrador'), ('active', 'Activo'), ],
                                 string='Estado', required=True, default="draft",
                                 help="Determina el estado del expediente")
        empleado_envia = fields.Many2one('hr.employee', 'Enviado por', readonly=True, default=_default_archivo_emple)
        firmas_encontradas = fields.Text('Firmas Digitales Encontradas', required=False, readonly=False)

        def reload_view(self):
                action = {
                        'type': 'ir.actions.client',
                        'tag': 'reload',
                }
                return action

        def eliminar_linea(self):
                # print (("ELIMINAND0 LINEA"))
                active_id = self.env.context.get('id_activo')
                dda_obj = self.browse([active_id])
                doc_digital_id = dda_obj.doc_digital_id
                dda_obj.unlink()
                # print (("EL ID DE DOC DIGITAL ES: " + str(doc_digital_id.id)))
                return {
                        'name': "Documentos Digitales Asociados al Expediente",
                        'view_mode': 'form',
                        'res_id': doc_digital_id.id,
                        # 'view_id': self.env.ref('pase.form_enviar').id,
                        'res_model': 'doc_digital',
                        'type': 'ir.actions.act_window',
                        # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                        # 'domain': [('id', 'in', ids_plantillas)],
                        # 'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
                        'views': [[self.env.ref('doc_digital.form').id, "form"]],
                        'target': 'current',  # 'target': 'new',
                }

        # @api.constrains('name')
        @api.onchange('name')
        def onchange_nombre(self):
                nombre = self.name
                if nombre:
                        return {'value': {'name': nombre+".pdf"}}
                else:
                        return False
                # nombre_array = nombre.split('.')
                # if len(nombre_array) > 2:
                #         raise ValidationError(('El nombre de archivo solo puede tener un punto.'))
                # if nombre_array[1] != 'pdf':
                #         raise ValidationError(('Solo se admiten archivos .pdf.'))
                # return True

        def valida_archivo(self, full_path2):
                try:
                    doc = PyPDF2.PdfFileReader(open(full_path2, "rb"), strict=False)
                    number_of_pages = doc.getNumPages()
                    print (("EL NUMERO DE PAGINAS ES: " + str(number_of_pages)))
                except PyPDF2.utils.PdfReadError:
                    print("invalid PDF file.....................")
                    return False
                else:
                    pass
                return True

        @api.constrains('archivo')
        def onchange_archivo(self):
                # En Python 3 hay diferencia entre archivos texto y binarios
                # En esta ocasion para crear un archivo de textto en Python 2 usabamos W+, lo cual cambiamos
                # por wb en Python 3 para indicar Binario
                print (("SE SUBIO UN ARCHIVO CUALQUIERA..."))
                foldertemp = os.path.dirname(os.path.abspath(__file__)) + "/temp"
                print (("EL PATH DE TRABAJO ES..." + str(foldertemp)))
                archivo_bin_odoo = self.archivo
                archivo_escribir = base64.b64decode(archivo_bin_odoo)
                full_path = foldertemp + '/temporal.pdf'
                f = open(full_path, 'wb')
                print(('CASI ESCRIBO'))
                f.write(archivo_escribir)
                f.close
                f = None
                time.sleep(1)
                if not self.valida_archivo(full_path):
                    raise ValidationError(('Esta intentando ingresar un archivo PDF con formato no válido.'))
                return True

        def verify_sign(public_key_loc, signature, data):
                '''
                Verifies with a public key from whom the data came that it was indeed
                signed by their private key
                param: public_key_loc Path to public key
                param: signature String signature to be verified
                return: Boolean. True if the signature is valid; False otherwise.
                fuente: https://gist.github.com/lkdocs/6519372
                '''
                from Crypto.PublicKey import RSA
                from Crypto.Signature import PKCS1_v1_5
                from Crypto.Hash import SHA256
                from base64 import b64decode
                pub_key = open(public_key_loc, "r").read()
                rsakey = RSA.importKey(pub_key)
                signer = PKCS1_v1_5.new(rsakey)
                digest = SHA256.new()
                # Assumes the data is base64 encoded to begin with
                digest.update(b64decode(data))
                if signer.verify(digest, b64decode(signature)):
                        return True
                return False

class doc_digital(models.Model):
        _name = 'doc_digital'
        _order = "write_date desc"

        name = fields.Char('Nombre', readonly=False, required=False)
        descrip = fields.Char('Descripcion', required=False)
        expediente_id = fields.Many2one('expediente.expediente', 'Id Expediente', required=True)
        archivos_id = fields.One2many('doc_digital.archivo', 'doc_digital_id', string='Archivos Asociados')
        _sql_constraints = [('exp_uniq_doc_digital', 'unique(expediente_id)', 'El panel de archivos asociados a un expediente debe ser único')]

        def _get_permiso_asignacion(self):
                desired_group_name = self.env['res.groups'].search([('name', '=', 'Asignacion')])
                is_desired_group = self.env.user.id in desired_group_name.users.ids
                if is_desired_group:
                        #print(("EL USUARIO SE ENCUENTRA HABILITADO PARA INSERTAR EXPEDIENTES"))
                        return True
                else:
                        #print(("NOOO EL USUARIO SE ENCUENTRA HABILITADO INSERTAR EXPEDIENTES"))
                        return False

        def user_emple(self, user_id):
                num_empl = self.env['hr.employee'].search_count([('user_id', '=', [user_id])])
                if num_empl < 1:
                        print(("No se encuentra el empleado asociado al usuario: " + str(user_id)))
                        return False
                elif num_empl > 1:
                        print(("Hay mas de un emplado asociado al usuario: " + str(user_id)))
                        return False
                else:
                        empl_obj = self.env['hr.employee'].search([('user_id', '=', [user_id])])
                        if empl_obj.id:
                                return empl_obj.id
                        else:
                                return False
        def nombre_usuario(self):
                user_id = self.env.user.id
                obj_empl = self.env['hr.employee'].search([('user_id', '=', user_id)])
                nombre = obj_empl[0].name
                return nombre

        def firmar_pdf_endevise(self, full_path, cant_pag):
                # print (("LLAMANDO A A ENDESIVE CON : " + path_all))
                # date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
                # date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
                #####FECHA PARA EL OBJETO#####
                date = datetime.datetime.now() - datetime.timedelta(hours=3)
                date = date.strftime("D:%Y%m%d%H%M%S")#+00'00'
                date2 = datetime.datetime.now() - datetime.timedelta(hours=3)
                date1 = date2.isoformat()
                #####FECHA PARA EL OBJETO#######
                #####FECHA PARA MOSTRAR#####
                # date1 = datetime.utcnow() - timedelta(hours=12)
                # date1 = date.strftime("D:%Y%m%d%H%M%S+00'00'")
                # print (("UTCNOW: " + str(date1) + " DELTA: " + str(timedelta(hours=12)) + " RESULTADO: " + str(date1)))
                ####FECHA PARA MOSTRAR####
                dct = {
                        "aligned": 0,
                        "sigflags": 3,
                        "sigflagsft": 132,#Valor original 132
                        "sigpage": cant_pag - 1,
                        "sigbutton": True,
                        "sigfield": "Firma Digital",
                        "sigandcertify": True,
                        # "signaturebox": (470, 840, 570, 540),
                        "signaturebox": (0, 0, 100, 100),
                        "signature": "SIGETRAMI PNUD ARG17/012 " + str(date1[0:20]) + " "+ self.nombre_usuario(),
                        #        "signature_img": "signature_test.png",
                        "contact": "gismineronacional@gmail.com",
                        "location": "Argentina",
                        "signingdate": date,
                        "reason": "Todos los documentos validado en SIGETRAMI son firmados digitalmente.",
                        "password": "123456",
                }
                # with open("/opt/odoo11/addonsgis/doc_digital/models/endesive-master/examples/demo2_user1.p12", "rb") as fp:
                folder = os.path.dirname(os.path.abspath(__file__))
                print(("EL PATH ACTUAL ES ...." + str(folder)))
                with open(folder + "/endesive-master/examples/mycert1.pfx", "rb") as fp:
                        p12 = pkcs12.load_key_and_certificates(
                                fp.read(), b"123456", backends.default_backend()
                        )
                # fname = "/opt/odoo11/addonsgis/doc_digital/models/docs/ANEXO.pdf"
                fname = full_path
                # if len(sys.argv) > 1:
                #         fname = sys.argv[1]
                datau = open(fname, "rb").read()
                datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
                fname = fname.replace(".pdf", "-signed-SiGeTraMi.pdf")
                with open(fname, "wb") as fp:
                        fp.write(datau)
                        fp.write(datas)
                fp.close
                fp = None
                return fname

        def _paginas(self, full_path):
                print(("contando paginas: " + full_path))
                try:
                        f = open(full_path, "rb")
                        doc = PyPDF2.PdfFileReader(f, strict=False)
                        number_of_pages = doc.getNumPages()
                        print (("EL NUMERO DE PAGINAS ES: " + str(number_of_pages)))
                except PyPDF2.utils.PdfReadError:
                        print("invalid PDF file.....................")
                        return False
                else:
                        pass
                f.close
                f = None
                return number_of_pages

        def _descargar(self, archivo):
                print (("EL NOMBRE DEL ARCHIVO ES: " + archivo.name))
                foldertemp = os.path.dirname(os.path.abspath(__file__)) + "/docs"
                full_path = foldertemp + '/para_firmar.pdf'
                f = open(full_path, 'wb+')
                f.write(base64.b64decode(archivo.archivo))
                f.close
                f = None
                return full_path

        def _cargar(self, archivo_obj, full_path):
                # print (("EL NOMBRE DEL ARCHIVO ES: " + archivo.name))
                # foldertemp = os.path.dirname(os.path.abspath(__file__)) + "/docs"
                # full_path = foldertemp + '/ANEXO-signed-SiGeTraMi2020.pdf'
                f = open(full_path, 'rb')
                firmado = base64.b64encode(f.read())
                f.close
                archivo_obj.write({'archivo': firmado})
                f = None
                return True

        def _eliminar(self, full_paths):
                for path in full_paths:
                        if os.path.isdir(path):
                                print("Imposible borrar {0}!. Es una carpeta.".format(path))
                        elif os.path.isfile(path):
                                try:
                                        os.remove(path)
                                except OSError as e: print("Error: %s - %s." % (e.filename, e.strerror))
                        else:
                                print("Error. No se ha encontrado {0}.".format(path))
                return True

        def activar_archivos(self):
                active_id = self.env.context.get('id_activo')
                print(("ACTIVANDO LOS ARCHIVOS ADJUNTOS EN EL EXPEDIENTE-: ID :" + str(active_id)))
                doc_digital_obj = self.browse([active_id])
                user_id = self.env.user.id
                emple_id = self.user_emple(user_id)
                print (("QUE TRAE DESDE EL :" + str(emple_id)))
                for archivo in doc_digital_obj.archivos_id:
                        if archivo.state == 'draft' and archivo.empleado_envia.id == emple_id:
                                full_path = self._descargar(archivo)
                                cant_pag = self._paginas(full_path)
                                full_path_signed = self.firmar_pdf_endevise(full_path, cant_pag)
                                self._cargar(archivo, full_path_signed)
                                self._eliminar([full_path, full_path_signed])
                                archivo.write({'state': 'active'})
                return True

        def prepara_union(self):
            foldertemp = os.path.dirname(os.path.abspath(__file__)) + "/temp/union"
            archivos_adjuntos = self.archivos_id
            count = 0
            for archivo in archivos_adjuntos:
                count = count + 1
                archivo_bin_odoo = archivo.archivo
                archivo_escribir = archivo_bin_odoo.decode('base64')
                full_path = foldertemp + '/temp' + str(count) + '.pdf'
                #full_path2 = '/opt/odoo/server/addonsgis/doc_digital/models/hoypdf.pdf'
                f = open(full_path, 'w+')
                f.write(archivo_escribir)
                f.close
                f = None
            #time.sleep(1)
            return count

        def crear_union_pdf(self):
            if self.prepara_union() > 0:
                foldertemp = os.path.dirname(os.path.abspath(__file__)) + "/temp/union/"
                #pdfs = [foldertemp + "hola3.pdf", foldertemp + "hola4.pdf"]
                pdfs = []
                arr_arch = os.listdir(foldertemp)
                for arch in arr_arch:
                    pdfs.append(foldertemp + arch)
                nombre_archivo_salida = foldertemp + "salida2.pdf"
                fusionador = PyPDF2.PdfFileMerger()
                for pdf in pdfs:
                    fusionador.append(open(pdf, 'rb'))
                with open(nombre_archivo_salida, 'wb') as salida:
                    fusionador.write(salida)
                fusionador.close
                fusionador = None
                time.sleep(1)
                urllib.urlretrieve ("http://www.example.com/songs/mp3.mp3", foldertemp+"salida.pdf")
                return True
            else:
                return True

class expediente(models.Model):
        _name = 'expediente.expediente'
        _inherit = 'expediente.expediente'
        _description = "Agregar Asociacion con Flujos de Tareas"

        # empleado_seg = fields.Many2one('hr.employee', 'Empleado Asignado', readonly=False)
        # empleado_seg = fields.Char('Tenencia de Expte.', readonly=True, store=True)

        def administrar_digitales(self):
                active_id = self.env.context.get('id_activo')
                # print (("ENVIANDO .... " + str(active_id)))
                user_id = self.env.user.id
                # print (())
                expte_obj = self.browse([active_id])
                # tiene_flujo_asociado = self.tiene_flujo(expte_obj.procedimiento_id.id)
                depart_actual_id = expte_obj.ubicacion_actual
                #####################################
                # depart_actual_expte_id = expte_obj.ubicacion_actual
                depart_user_actual_id = self.userdepart(user_id)
                if not depart_user_actual_id:
                        print(("No hay oficina actual asignada."))
                if depart_user_actual_id != depart_actual_id.id:
                        print(("No pertenece a la misma oficina que el expediente."))
                        raise ValidationError(
                                ('Solo puede acceder a esta informacion si el expediente se encuentra en la oficina.'))
                ################################
                if not depart_actual_id:
                        print(("No hay oficina actual asignada."))
                # CONSULTANDO PLANTILLAS PARA OFICINA Y TAREA ACTUAL
                if expte_obj.tarea_actual:
                        doc_digital_obj_cant = self.env['doc_digital'].search_count(
                                [('expediente_id', '=', expte_obj.id)])
                        doc_digital_obj = self.env['doc_digital'].search(
                                [('expediente_id', '=', expte_obj.id)])
                else:
                        doc_digital_obj_cant = self.env['doc_digital'].search_count(
                                [('expediente_id', '=', expte_obj.id)])
                        doc_digital_obj = self.env['doc_digital'].search(
                                [('expediente_id', '=', expte_obj.id)])
                if doc_digital_obj_cant > 0:
                        # NUEVO PASE A OFICINA
                        return {
                                'name': "Documentos Digitales Asociados al Expediente",
                                'view_mode': 'form',
                                'res_id': doc_digital_obj[0].id,
                                # 'view_id': self.env.ref('pase.form_enviar').id,
                                'res_model': 'doc_digital',
                                'type': 'ir.actions.act_window',
                                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                                #'domain': [('id', 'in', ids_plantillas)],
                                #'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
                                'views': [[self.env.ref('doc_digital.form').id, "form"]],
                                'target': 'current', #'target': 'new',
                        }
                else:
                        return {
                                'name': "Documentos Digitales Asociados al Expediente",
                                'view_mode': 'form',
                                # 'res_id': doc_digital_obj[0].id,
                                'res_model': 'doc_digital',
                                'type': 'ir.actions.act_window',
                                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                                #'domain': [('id', 'in', ids_plantillas)],
                                'context': {'default_expediente_id': expte_obj.id, 'default_name': expte_obj.name},
                                'views': [[self.env.ref('doc_digital.form').id, "form"]],
                                'target': 'current', #'target': 'new',
                        }
                return True