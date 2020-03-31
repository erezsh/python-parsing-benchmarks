
import pe
from pe.actions import first, constant, pack

from bench.helpers import json_unescape


Json = pe.compile(
    r'''
    # Syntactic rules
    Start    <- Spacing Value EOF
    Value    <- Object / Array / String / Number / Constant
    Object   <- LBRACE (Member (COMMA Member)*)? RBRACE
    Member   <- String COLON Value
    Array    <- LBRACK (Value (COMMA Value)*)? RBRACK
    String   <- ~( ["] CHAR* ( ESC CHAR* )* ["] )
    Number   <- ~( INTEGER FRACTION? EXPONENT? )
    Constant <- TRUE / FALSE / NULL

    # Lexical rules
    CHAR     <- [ !#-\[\]-\U0010ffff]
    ESC      <- '\\' ( ["\\/bfnrt]
                     / 'u' HEX HEX HEX HEX )
    HEX      <- [0-9a-fA-F]
    INTEGER  <- "-"? ("0" / [1-9] [0-9]*)
    FRACTION <- "." [0-9]+
    EXPONENT <- [eE] [-+]? [0-9]+
    TRUE     <- "true"
    FALSE    <- "false"
    NULL     <- "null"
    LBRACE   <- "{" Spacing
    RBRACE   <- Spacing "}"
    LBRACK   <- "[" Spacing
    RBRACK   <- Spacing "]"
    COMMA    <- Spacing "," Spacing
    COLON    <- Spacing ":" Spacing
    Spacing  <- [\t\n\r ]*
    EOF      <- Spacing !.
    ''',
    actions={
        'Start': first,
        'Object': pack(dict),
        'Member': pack(tuple),
        'Array': pack(list),
        'String': json_unescape,
        'Number': float,
        'TRUE': constant(True),
        'FALSE': constant(False),
        'NULL': constant(None),
    },
    flags=pe.OPTIMIZE,
)


def parse(s):
    return Json.match(s, flags=pe.STRICT).value()
