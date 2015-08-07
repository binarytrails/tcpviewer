import unittest

from Utilities import *

class Test(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
  
    def test_ipv4_regex(self):
        pass

    def test_ipv4s_regex(self):
        pass

    def test_ipv4_colon_port_regex(self):
        pass

    def test_validate_ipv4s(self):
        pass

    def test_validate_ipv4_colon_port(self):
        pass

    def test_remove_ipv4_leading_zeros(self): 
        ipv4 = remove_ipv4_leading_zeros('127.00.0.1')
        self.assertTrue(ipv4, '127.0.0.1')
        
        ipv4 = remove_ipv4_leading_zeros('100.00.0.001')
        self.assertTrue(ipv4, '100.0.0.1')

        ipv4 = remove_ipv4_leading_zeros('000.00.000.000')
        self.assertTrue(ipv4, '0.0.0.0')

        ipv4 = remove_ipv4_leading_zeros('0.1.003.11')
        self.assertTrue(ipv4, '0.1.3.11')

