import re
from typing import NamedTuple, Iterable


class Token(NamedTuple):
    kind: str
    value: str


def lex(code: str) -> Iterable[Token]:
    """
    Retorna sequência de objetos do tipo token correspondendo à análise léxica
    da string de código fornecida.
    """
    array = []
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('NUMBER',   	r'[+-]?\d+(\.\d*)?'),  		# Integer or decimal number
        ('STRING',		r'"[A-Za-z-?>%!\s\\"]+"'),	# Strings
        ('NAME',       	r'[A-Za-z-?>%!+\.]+'),    		# Identifiers
        ('LPAR',		r'\('),						# Identificador (
        ('RPAR',		r'\)'),						# Identificador )
        ('BOOL',		r'#t|#f'),					# Boolean
        ('OP',       	r'[+\-*/]'),      			# Arithmetic operators
        ('QUOTE',       r"'"),      				# Quote
        ('COMMENT',     r";;.*[^\n]"),      		# Comments
        ('CHAR',		r'#\\[A-Za-z]*'),			# Char

        ('NEWLINE',  	r'\n'),           			# Line endings
        ('SKIP',     	r'[ \t]+'),       			# Skip over spaces and tabs
        ('ASSIGN',   	r'='),           			# Assignment operator
        ('END',      	r';'),            			# Statement terminator
        ('ERROR', 		r'.'),            			# Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NAME' and value in keywords:
            kind = value
        elif kind == 'COMMENT':
            continue
        elif kind == 'NEWLINE':
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'ERROR':
            raise RuntimeError(f'{value!r}')
        array.append(Token(kind, value))
    
    print(array)
    # return [Token('INVALIDA', 'valor inválido')]
    return array