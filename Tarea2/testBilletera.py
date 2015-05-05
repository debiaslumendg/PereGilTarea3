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
import unittest
from Billetera2 import * 
import Billetera2


class Test(unittest.TestCase):

  

    def testSaldo1(self):
        a = BilleteraElectronica(1,Usuario("pedro","perez",23712077), "123456")      
        self.assertEqual(a.saldo(),a.saldo_actual)
    
    def testRecargaNormalDesdeCero(self):
        a = BilleteraElectronica(1,Usuario("pedro","perez",23712077), "123456")
        a.recargar(1, datetime(year =1, month =1, day =1), 1)
        self.assertEqual(a.saldo(), 1)
    
    '''def testRecargaVacia(self):
        a = BilleteraElectronica(1,Usuario("pedro","perez",23712077), "123456")
        a.recargar(0, datetime(year =1, month =1, day =1), 1)
        self.assertRaisesRegex(Exception, )'''
        
    '''def testRecargaNegativa(self):
        a = BilleteraElectronica(1,Usuario("pedro","perez",23712077), "123456")
        a.recargar(-1, None, None)
        self.assertEqual(a.saldo, 0)'''
        
    def testRecargaMuyAltaDesde0(self):
        a = BilleteraElectronica(1,Usuario("pedro","perez",23712077), "123456")
        a.recargar(2**31, None, None)
        self.assertEqual(a.saldo(), 2**31)
        
    def testRecargaDesdeNoCero(self):
        a = BilleteraElectronica(1,Usuario("pedro","perez",23712077), "123456")
        a.recargar(10, None, None)
        a.recargar(10, None, None)
        self.assertEqual(a.saldo(), 20)
        
    def testRecargaMuyAltaDesdeNo0(self):
        a = BilleteraElectronica(1,Usuario("pedro","perez",23712077), "123456")
        a.recargar(1, None, None)
        a.recargar((2**31)-1, None, None)
        self.assertEqual(a.saldo(), 2**31)
        
    
        
    ''''a = BilleteraElectronica(1,Usuario("pedro","perez",23712077), "123456")

a.recargar(2, datetime(year=1,month=1,day=1), "1")
a.recargar(10, datetime(year=1,month=1,day=1), "1")
print(a.consumir(13, datetime(year=1,month=1,day=1), "2", "123456"))
print(a.saldo())'''

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()