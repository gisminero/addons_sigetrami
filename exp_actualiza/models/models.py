# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import datetime
import time
from datetime import datetime as dt, timedelta, date
import dateutil.parser
# from unidecode import unidecode
import psycopg
#import psycopg.extras


class exp_actualiza(models.Model):
    _name = 'exp_actualiza'
    #_inherit = ['mail.thread']
    _order = "write_date desc"  

    def default_user_id(self):
        return self.env.context.get("default_user_id", self.env.user)

    def conexion_externa(self):
        print (("CONECTANDO..."))
        with psycopg.connect("host=localhost user=postgres password=123456 port=5432 dbname=catamarca-stm connect_timeout=10") as conn:
            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                # Query the database and obtain data as Python objects.
                cur.execute("SELECT * FROM expediente_expediente")
                cur.fetchone()
                # will return (1, 100, "abc'def")
                # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
                # of several records, or even iterate on the cursor
                for record in cur:
                    print(record)

        # Make the changes to the database persistent
        #conn.commit()
        return False

    def connect(self):
	    # connecting to the database called test
	    # using the connect function
	    try:
		    conn = psycopg.connect(dbname ="catamarca-stm",
							user = "postgres",
							password = "123456",
							host = "localhost",
							port = "5432",
                            connect_timeout="10")
		    # creating the cursor object
		    cur = conn.cursor()
	    except (Exception, psycopg.DatabaseError) as error:
		    print ("Error while creating PostgreSQL table", error)
	    # returing the conn and cur
	    # objects to be used later
	    return conn, cur

    def desconexion_externa(self):
        
        return False

    def consulta_exp(self):
        conn, cur = self.connect()        
        # Open a cursor to perform database operations        
        cur.execute("SELECT * FROM expediente_expediente")
        cur.fetchone()
        # will return (1, 100, "abc'def")
        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            print(("EL EXPEDIENTE ES: " + str(record[1])))
            print(record)
        return True

    def consulta_pases(self):
        return True

    def consulta_historial_tareas(self):
        return True


    def rastreo(self):
        #self.conexion_externa()
        self.consulta_exp()
        return True

