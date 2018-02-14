import ply.lex as lex
from tabulate import tabulate
import random

class JavaLex(object):
    keywords = ('this', 'class', 'void', 'super', 'extends', 'implements', 'enum', 'interface',
                'byte', 'short', 'int', 'long', 'char', 'float', 'double', 'boolean', 'null',
                'true', 'false',
                'final', 'public', 'protected', 'private', 'abstract', 'static', 'strictfp', 'transient', 'volatile',
                'synchronized', 'native',
                'throws', 'default',
                'instanceof',
                'if', 'else', 'while', 'for', 'switch', 'case', 'assert', 'do',
                'break', 'continue', 'return', 'throw', 'try', 'catch', 'finally', 'new',
                'package', 'import')
    tokens = [
        'NAME',
        'NUMBER',
        'CHAR_LITERAL',
        'STRING_LITERAL',
        'LINE_COMMENT', 'BLOCK_COMMENT',
        'MULT_ASSIGN', 'DIVIDE_ASSIGN', 'REMAINDER_ASSIGN',
        'PLUS_ASSIGN', 'MINUS_ASSIGN', 'LSHIFT_ASSIGN', 'RSHIFT_ASSIGN', 'RRSHIFT_ASSIGN',
        'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN',
        'OR', 'AND',
        'EQUAL', 'NEQUAL', 'GTEQ', 'LTEQ',
        'LSHIFT', 'RSHIFT', 'RRSHIFT',
        'PLUSPLUS', 'MINUSMINUS',
        'ELLIPSIS'] 

    tokens += [kwd.upper() for kwd in keywords]

    literals = '()+-*/=?:,.^|&~!=[]{};<>@%'

    t_NUMBER = r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'
    t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
    t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'
    t_OR = r'\|\|'
    t_AND = '&&'
    t_EQUAL = '=='
    t_NEQUAL = '!='
    t_GTEQ = '>='
    t_LTEQ = '<='
    t_LSHIFT = '<<'
    t_RSHIFT = '>>'
    t_RRSHIFT = '>>>'
    t_MULT_ASSIGN = r'\*='
    t_DIVIDE_ASSIGN = '/='
    t_REMAINDER_ASSIGN = '%='
    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = '-='
    t_LSHIFT_ASSIGN = '<<='
    t_RSHIFT_ASSIGN = '>>='
    t_RRSHIFT_ASSIGN = '>>>='
    t_AND_ASSIGN = '&='
    t_OR_ASSIGN = r'\|='
    t_XOR_ASSIGN = '\^='
    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'\-\-'
    t_ELLIPSIS = r'\.\.\.'
    t_ignore = ' \t\f'
    t_ignore_COMMENT = r'//.* | /\*(.|\n)*?\*/' 
 
    def t_NAME(self, t):
        '[A-Za-z_$][A-Za-z0-9_$]*'
        if t.value in JavaLex.keywords:
            t.type = t.value.upper()
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_RNEWLINE(self, t):
        r'(\r\n)+'
        t.lexer.lineno += len(t.value) / 2

    def t_error(self, t):
        print("ERROR : Unknown character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
        t.lexer.skip(1)

if __name__ == '__main__':
    JavaLexer = lex.lex(module = JavaLex())
    my_inp = open('Simple1.java','r').read()
    JavaLexer.input(my_inp)
    sym_table=dict()
    s=dict()
    sym_table['outer']=s
    flag=0
    i = 0
    l=[]
    for token in JavaLexer:
        print(token)
        if(token.type=='{'):
           l.append(s)
           s=dict()
        if(token.type=='}'):
           i=i+1
           sym_table["inner_"+str(i)]=s
           print("\n\n[Table for scope: inner_"+str(i),"]\n")
           print(tabulate([[sym, s[sym]] for sym in s], headers = ['NAME', 'VALUE'], tablefmt='orgtbl'))
           s=l.pop()
        if(token.type=='NAME'):
              s[token.value]=(token.lineno, token.lexpos)
    sym_table['outer']=s
    print("\n\n[Table for scope: outer]\n\n")
    print(tabulate([[sym, s[sym]] for sym in s], headers = ['NAME', 'VALUE'], tablefmt='orgtbl'))
#print(sym_table)
