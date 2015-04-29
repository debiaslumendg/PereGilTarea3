'''
Created on 29/4/2015

@author: Willians
'''
import unittest


class Test(unittest.TestCase):


    def testName(self):
        pass

     a = BilleteraElectronica(1,Usuario("pedro","perez",23712077), "123456")

a.recargar(2, datetime(year=1,month=1,day=1), "1")
a.recargar(10, datetime(year=1,month=1,day=1), "1")
print(a.consumir(13, datetime(year=1,month=1,day=1), "2", "123456"))
print(a.saldo())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()