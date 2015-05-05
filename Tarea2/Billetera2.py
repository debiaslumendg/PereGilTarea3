# -*- coding: utf-8 -*-

'''
Created on 29/4/2015

@author: Virginia Gil 11-10371
         Pedro Pérez 10-10548
'''
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
import hashlib
import uuid

class Usuario(object):
    def __init__(self, nombres, apellidos, CI):
        self.nombres = nombres
        self.apellidos = apellidos
        self.CI = CI

class Transaccion(object):
    def __init__(self,monto,fecha,ID_Lugar,tipo):
        self.monto = monto
        self.fecha = fecha
        self.ID_Lugar = ID_Lugar
        self.tipo = tipo #1=credito, 0=debito
                
class BilleteraElectronica(object):
    #=)
        def __init__(self, identificador,usuario,PIN):
            self.identificador = identificador
            self.usuario = usuario
            
            salt = uuid.uuid4().hex
            self.PIN = hashlib.sha256(salt.encode() + PIN.encode()).hexdigest() + ':' + salt
            
            self.transacciones = []
            self.saldo_actual = Decimal(0)
            
        def saldo(self):
            return self.saldo_actual
        
        def recargar(self,monto,fecha,ID_Lugar): 
            if monto <= 0:
                raise Exception
            try:
                monto = Decimal(monto);
            except:
                raise Exception
                                
            self.saldo_actual += monto;