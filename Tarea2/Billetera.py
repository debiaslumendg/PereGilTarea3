# -*- coding: utf-8 -*-

'''
Created on 29/4/2015

@author: Virginia Gil 11-10371
         Pedro Pérez 10-10548
'''
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from abc import ABCMeta
import hashlib
import uuid
from builtins import str

class ZeroException(Exception):
    pass

class NegativeException(Exception):
    pass

class NoFundsException(Exception):
    pass

class WrongPINException(Exception):
    pass

class VoidException(Exception):
    pass


class Usuario(object):
    
    __metaclass__ = ABCMeta
    
    def __init__(self, nombres, apellidos, CI):
        self.nombres = nombres
        self.apellidos = apellidos
        self.CI = CI

class Debito(object):
    def __init__(self,monto,fecha,ID_Lugar):
        self.monto = monto
        self.fecha = fecha
        self.ID_Lugar = ID_Lugar
    
    def getMonto(self):
        return self.monto
        
class Credito(object):
    def __init__(self,monto,fecha,ID_Lugar):
        self.monto = monto
        self.fecha = fecha
        self.ID_Lugar = ID_Lugar
    
    def getMonto(self):
        return self.monto
                
class BilleteraElectronica(object):
    #=)
        def __init__(self, identificador, nombreUsuario, apellidoUsuario, ciUsuario, PIN):
            self.identificador = identificador
            
            if ((nombreUsuario == "" or apellidoUsuario == "" or PIN == "") or
            not(isinstance(nombreUsuario, str)) or
            not(isinstance(apellidoUsuario, str)) or
            not(isinstance(PIN, str))) :
                raise VoidException
            
            self.nombreUsuario = nombreUsuario
            self.apellidoUsuario = apellidoUsuario
            self.ciUsuario = ciUsuario
            
            salt = uuid.uuid4().hex
            self.PIN = hashlib.sha256(salt.encode() + PIN.encode()).hexdigest() + ':' + salt
            
            self.debitos = []
            self.creditos = []
            self.saldo_actual = Decimal(0)
            
        def saldo(self):
            return self.saldo_actual
        
        def recargar(self,monto,fecha,ID_Lugar): 
            if monto == 0:
                raise ZeroException
            if monto <= 0:
                raise NegativeException
            
            self.creditos += [Credito(Decimal(monto), fecha, ID_Lugar)]                   
            self.saldo_actual += Decimal(monto)
            
        def consumir(self,monto,fecha,ID_Lugar,PIN):
            if monto == 0:
                raise ZeroException
            elif monto < 0:
                raise NegativeException
            elif Decimal(monto) > self.saldo_actual:
                raise NoFundsException
            
            PIN_prueba, salt = self.PIN.split(':')
            if PIN_prueba != hashlib.sha256(salt.encode() + PIN.encode()).hexdigest():
                raise WrongPINException
            
            self.debitos += [Debito(Decimal(monto), fecha, ID_Lugar)]
            self.saldo_actual -= Decimal(monto).quantize(Decimal('1.00'))