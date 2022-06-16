import unittest
from hypothesis import given,  strategies
from lambcal import *

# class LambcalTest(unittest.TestCase):
#     def test_Lambcal(self):
#         i = ''
#         print('oral')
#         print(x)
#         for _ in range(10):
#             x=x.beta()
#             print(x)   
class LexTest(unittest.TestCase):
    def test_first_alpha_reduction(self):
        result = lambda_cli_lex("((lambda x y. (x y)) y)")
        self.assertEqual(next(result), LeftBracket)
        self.assertEqual(next(result), LeftBracket)
        self.assertEqual(next(result), LambdaKeyword)
        var = next(result)
        self.assertIsInstance(var, Parameter)
        self.assertEqual(var.name, 'x')
        var = next(result)
        self.assertIsInstance(var, Parameter)
        self.assertEqual(var.name, 'y')
        self.assertEqual(next(result), Dot)
        self.assertEqual(next(result), LeftBracket)
        var = next(result)
        self.assertIsInstance(var, Variable)
        self.assertEqual(var.name, 'x')
        var = next(result)
        self.assertIsInstance(var, Variable)
        self.assertEqual(var.name, 'y')
        self.assertEqual(next(result), RightBracket)
        self.assertEqual(next(result), RightBracket)
        var = next(result)
        self.assertIsInstance(var, Variable)
        self.assertEqual(var.name, 'y')
        self.assertEqual(next(result), RightBracket)
