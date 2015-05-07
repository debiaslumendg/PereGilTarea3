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
from Billetera import * 
import Billetera
import xdrlib


class TestBilleteraExists(unittest.TestCase):
    
    def testBilleteraExists(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        
    def testBilleteraCaracterRaro(self):
        a = BilleteraElectronica(1, "Vïrçíñî@", "$th&lê <3", 23712077, "123456")
        self.assertEqual(a.nombreUsuario + a.apellidoUsuario, "Vïrçíñî@" + "$th&lê <3")
    
    def testNombreVacio(self):    
        self.assertRaises(VoidException, BilleteraElectronica,1,"","",23631926,"243")
    
    def testNombreNull(self):    
        self.assertRaises(VoidException, BilleteraElectronica,1,None,None,23631926,"243")
    
    def testNombreNoString(self):    
        self.assertRaises(VoidException, BilleteraElectronica,1,123,Decimal(0.5),23631926,"243")
        
    def testPINVacio(self):
        self.assertRaises(VoidException, BilleteraElectronica,1,"pedro","perez",23631926,"")
    
    def testPINNulo(self):
        self.assertRaises(VoidException, BilleteraElectronica,1,"pedro","perez",23631926,None)
       
    def testSaldoEsDecimal(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        self.assertTrue(isinstance(a.saldo(), Decimal))
    
    def testRecargaDesdeCero(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(10, fecha, 1)
        self.assertEqual(a.saldo(), 10)
        
    def testRecargaDesdeNoCero(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(10, fecha, 1)
        a.recargar(10, fecha, 1)
        self.assertEqual(a.saldo(), 20)
    
    def testRecargaVacia(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        self.assertRaises(ZeroException, a.recargar, 0, fecha, 1)
        
    def testRecargaNegativa(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")    
        fecha = datetime(year = 1, month = 1, day = 1)    
        self.assertRaises(NegativeException, a.recargar, -1, fecha, 1)
        
    def testRecargaMuyAltaDesde0(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1) 
        a.recargar(2**31, fecha, 1)
        self.assertEqual(a.saldo(), 2**31)
        
    def testRecargaMuyAltaDesdeNo0(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1) 
        a.recargar(1, fecha, 1)
        a.recargar((2**31), fecha, 1)
        self.assertEqual(a.saldo(), 2**31 + 1)
    
    def testRecargaDecimalBajaDesde0(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1) 
        a.recargar(0.01, fecha, 1)
        self.assertAlmostEqual(a.saldo(), Decimal(0.01), 2)
        
    def testRecargaDecimalBajaDesdeNo0(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(10, fecha, 1)
        a.recargar(0.01, fecha, 1)
        self.assertAlmostEqual(a.saldo(), Decimal(10.01), 2)
        
    def testCreditoAgregado(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        self.assertEqual(a.creditos, [])
        a.recargar(10, fecha, 1)
        self.assertEqual(a.creditos[-1].monto, Decimal(10))
        self.assertEqual(a.creditos[-1].fecha, fecha)
        self.assertEqual(a.creditos[-1].ID_Lugar, 1)
        self.assertEqual(len(a.creditos), 1)
        
    def testCreditoAgregadoMultiple(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        self.assertEqual(a.creditos, [])
        a.recargar(10, fecha, 1)
        a.recargar(2**31, fecha, 2)
        self.assertEqual(a.creditos[-1].monto, Decimal(2**31))
        self.assertEqual(a.creditos[-1].fecha, fecha)
        self.assertEqual(a.creditos[-1].ID_Lugar, 2)
        self.assertEqual(len(a.creditos), 2)

    def testConsumo0(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        self.assertRaises(ZeroException, a.consumir, 0, fecha, 1, "123456")
        
    def testConsumoNegativo(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        self.assertRaises(NegativeException, a.consumir, -1, fecha, 1, "123456")
    
    def testConsumoRegular(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(10, fecha, 1)
        a.consumir(5, fecha, 1, "123456")
        self.assertEquals(a.saldo(), Decimal(5))
        
    def testConsumoDecimal(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(10, fecha, 1)
        a.consumir(2.01, fecha, 1, "123456")
        self.assertAlmostEqual(a.saldo(), Decimal(7.99), 2)
        
    def testConsumoSaldoInsuficiente(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(1, fecha, 1)
        self.assertRaises(NoFundsException, a.consumir, 2, fecha, 1, "123456")
     
    def testConsumoSaldoInsuficienteMargenMinimo(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(1, fecha, 1)
        self.assertRaises(NoFundsException, a.consumir, 1.01, fecha, 1, "123456")
    
    def testConsumoPINErroneo(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(10, fecha, 1)
        self.assertRaises(WrongPINException, a.consumir, 5, fecha, 1, "12345")
    
    def testConsumoMuyAlto(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(2**31, fecha, 1)
        a.consumir(2**31, fecha, 1, "123456")
        self.assertEquals(a.saldo(), Decimal(0))
    
    def testConsumoDecimalMuyAlto(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        a.recargar(2**31 + 0.01, fecha, 1)
        a.consumir(2**31, fecha, 1, "123456")
        self.assertAlmostEqual(a.saldo(), Decimal(0.01), 2)
        
    def testDebitoAgregado(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        self.assertEqual(a.debitos, [])
        a.recargar(10, fecha, 1)
        a.consumir(10, fecha, 1, "123456")
        self.assertEqual(a.debitos[-1].monto, Decimal(10))
        self.assertEqual(a.debitos[-1].fecha, fecha)
        self.assertEqual(a.debitos[-1].ID_Lugar, 1)
        self.assertEqual(len(a.debitos), 1)
        
    def testDebitoAgregadoMultiple(self):
        a = BilleteraElectronica(1, "Virginia", "Gil", 23712077, "123456")
        fecha = datetime(year = 1, month = 1, day = 1)
        self.assertEqual(a.debitos, [])
        a.recargar(10, fecha, 1)
        a.consumir(5, fecha, 2, "123456")
        a.consumir(5, fecha, 2, "123456")
        self.assertEqual(a.debitos[-1].monto, Decimal(5))
        self.assertEqual(a.debitos[-1].fecha, fecha)
        self.assertEqual(a.debitos[-1].ID_Lugar, 2)
        self.assertEqual(len(a.debitos), 2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()