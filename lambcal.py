from typing import Any
from grammpy import Grammar, Nonterminal, Rule, EPS  # type: ignore
import interpreter  # type: ignore
# parsings
from grammpy.transforms import ContextFree, InverseCommon  # type: ignore
from grammpy.transforms import InverseContextFree
from grammpy.parsers import cyk  # type: ignore
# from pyparsers import cyk  # type: ignore
from ply import lex  # type: ignore


class ParsingException(Exception):
    pass


class LexException(Exception):
    pass


class CYKException(Exception):
    pass


class LambdaKeyword:
    pass


class Dot:
    pass


class LeftBracket:
    pass


class RightBracket:
    pass


class Number:
    def __init__(self, value) -> None:
        self.value = value

    def __hash__(self) -> Any:
        return hash(Number)


class Variable:
    def __init__(self, name) -> None:
        self.name = name

    def __hash__(self) -> Any:
        return hash(Variable)


class Parameter:
    def __init__(self, name) -> None:
        self.name = name

    def __hash__(self) -> Any:
        return hash(Parameter)


all_terms = [
    LambdaKeyword,
    Dot,
    Number,
    Variable,
    Parameter,
    LeftBracket,
    RightBracket
]


class Expression(Nonterminal):  # type: ignore
    def get_representation(self) -> Any:
        return self.to_rule.to_symbols[1].get_representation()


class Lambda(Nonterminal):
    def get_representation(self) -> Any:
        parameters = list(self.to_rule.to_symbols[2].parameters())
        expression = self.to_rule.to_symbols[-2].get_representation()
        return interpreter.Lambda(parameters, expression)


class Parameters(Nonterminal):
    def parameters(self) -> Any:
        term = self.to_rule.to_symbols[0].s  # type: Parameter
        if term is EPS:
            return []
        yield term.name
        try:
            yield from self.to_rule.to_symbols[1].parameters()
        except IndexError:
            return


class NoBracketExpression(Nonterminal):
    def get_representation(self) -> Any:
        body = list(self.to_rule.to_symbols[0].get_body())
        return interpreter.Expression(body)


class ExpressionBody(Nonterminal):
    def get_body(self) -> Any:
        return self.to_rule.get_body()


class ExpressionBodyToVariable(Rule):
    rules = [
        ([ExpressionBody], [Variable, ExpressionBody]),
        ([ExpressionBody], [Variable])
    ]

    def get_body(self) -> Any:
        variable = self.to_symbols[0].s  # type: Variable
        yield interpreter.Variable(variable.name)
        try:
            yield from self.to_symbols[1].get_body()
        except IndexError:
            return


class ExpressionBodyToNumber(Rule):
    rules = [
        ([ExpressionBody], [Number, ExpressionBody]),
        ([ExpressionBody], [Number])
    ]

    def get_body(self) -> Any:
        num = self.to_symbols[0].s  # type: Number
        yield interpreter.Variable(num.value)
        try:
            yield from self.to_symbols[1].get_body()
        except IndexError:
            return


class ExpressionBodyToLambda(Rule):
    rules = [
        ([ExpressionBody], [Lambda, ExpressionBody]),
        ([ExpressionBody], [Lambda])
    ]

    def get_body(self) -> Any:
        lam = self.to_symbols[0]  # type: Lambda
        yield lam.get_representation()
        try:
            yield from self.to_symbols[1].get_body()
        except IndexError:
            return


class ExpressionBodyToExpression(Rule):
    rules = [
        ([ExpressionBody], [Expression, ExpressionBody]),
        ([ExpressionBody], [Expression])
    ]

    def get_body(self) -> Any:
        expr = self.to_symbols[0]  # type: Expression
        yield expr.get_representation()
        try:
            yield from self.to_symbols[1].get_body()
        except IndexError:
            return


class NoBracketExpressionRule(Rule):
    fromSymbol = NoBracketExpression
    toSymbol = ExpressionBody


class ExpressionRule(Rule):
    fromSymbol = Expression
    right = [LeftBracket, NoBracketExpression, RightBracket]


class LambdaRule(Rule):
    fromSymbol = Lambda
    right = [LeftBracket, LambdaKeyword, Parameters,
             Dot, NoBracketExpression, RightBracket]


class ParametersRule(Rule):
    rules = [
        ([Parameters], [EPS]),
        ([Parameters], [Parameter, Parameters]),
        ([Parameters], [Parameter])
    ]


lambda_grammar = Grammar(
    terminals=all_terms,
    nonterminals=[
        NoBracketExpression,
        Expression,
        ExpressionBody,
        Lambda,
        Parameters
    ],
    rules=[
        NoBracketExpressionRule,
        ExpressionBodyToExpression,
        ExpressionBodyToLambda,
        ExpressionBodyToNumber,
        ExpressionBodyToVariable,
        ExpressionRule,
        LambdaRule,
        ParametersRule
    ],
    start_symbol=NoBracketExpression)
states = (
    ('parameters', 'exclusive'),
)

tokens = (
    'LAMBDA',
    'DOT',
    'NUMBER',
    'VARIABLE',
    'PARAMETER',
    'LEFTBRACKET',
    'RIGHTBRACKET',
)

t_INITIAL_parameters_ignore = ' \t'


def t_INITIAL_LAMBDA(t: Any) -> Any:
    r"""lambda"""
    t.value = LambdaKeyword
    t.lexer.begin('parameters')
    return t


def t_parameters_DOT(t: Any) -> Any:
    r"""\."""
    t.value = Dot
    t.lexer.begin('INITIAL')
    return t


def t_INITIAL_NUMBER(t: Number) -> Number:
    r"""\d+"""
    t.value = Number(int(t.value))
    return t


def t_INITIAL_VARIABLE(t: Any) -> Any:
    r"""[a-zA-Z\']+"""
    t.value = Variable(t.value)
    return t


def t_parameters_PARAMETER(t: Any) -> Any:
    r"""[a-zA-Z\']+"""
    t.value = Parameter(t.value)
    return t


def t_INITIAL_LEFTBRACKET(t: Any) -> Any:
    r"""\("""
    t.value = LeftBracket
    return t


def t_INITIAL_RIGHTBRACKET(t: Any) -> Any:
    r"""\)"""
    t.value = RightBracket
    return t


def t_INITIAL_parameters_error(t: Any) -> Any:
    raise LexException(t)


lexer = lex.lex()


def lambda_cli_lex(input: Any) -> Any:
    lexer.input(input)
    while True:
        tok = lexer.token()
        if not tok:
            return  # No more input
        yield tok.value


# parsings
_g = ContextFree.remove_useless_symbols(lambda_grammar)
_g = ContextFree.remove_rules_with_epsilon(_g)
_g = ContextFree.remove_unit_rules(_g)
_g = ContextFree.remove_useless_symbols(_g)
_g = ContextFree.transform_to_chomsky_normal_form(_g)


def parse_from_tokens(input: Any) -> Any:
    try:
        parsed = cyk(_g, input)
    except NotImplementedError:
        raise ParsingException
    parsed = InverseContextFree.transform_from_chomsky_normal_form(parsed)
    parsed = InverseContextFree.unit_rules_restore(parsed)
    parsed = InverseContextFree.epsilon_rules_restore(parsed)
    parsed = InverseCommon.splitted_rules(parsed)
    return parsed.get_representation()


def parse(input: Any) -> Any:
    return parse_from_tokens(lambda_cli_lex(input))


def steps(input: Any) -> Any:
    repr = parse(input)
    yield repr.representation()
    while repr.beta_reduction():
        yield repr.representation()
