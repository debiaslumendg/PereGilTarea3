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
            monto = Decimal(monto)
            self.transacciones.append(Transaccion(monto, fecha, ID_Lugar, 1))
            self.saldo_actual += monto
            
        def consumir(self,monto,fecha,ID_Lugar,PIN):
            
            PIN_prueba, salt = self.PIN.split(':')
            if PIN_prueba != hashlib.sha256(salt.encode() + PIN.encode()).hexdigest():
                return "Su PIN no coincide con el introducido"
            if self.saldo_actual < monto:
                return "No tiene suficiente saldo"
            
            monto = Decimal(monto)
            self.transacciones.append(Transaccion(monto, fecha, ID_Lugar, 0))
            self.saldo_actual -= monto
            
        
            
            

            
a = BilleteraElectronica(1,Usuario("pedrño","pérez",23712077), "123456")

a.recargar(2, datetime(year=1,month=1,day=1), "1")
a.recargar(10, datetime(year=1,month=1,day=1), "1")
print(a.consumir(13, datetime(year=1,month=1,day=1), "2", "123456"))
print(a.saldo())

