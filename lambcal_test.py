import unittest
# from hypothesis import given,  strategies
from lambcal import lambda_cli_lex, LeftBracket, LambdaKeyword
from lambcal import Parameter, Dot, Variable, RightBracket, steps
import logging
logging.basicConfig(level=logging.INFO)


class LambTest(unittest.TestCase):
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

    def test_Visualize(self):
        i = '((lambda x. (lambda z. (x z))) (z g))'
        for r in steps(i):
            logging.info("lambda term is {r}".format(r))
#             print(r)
