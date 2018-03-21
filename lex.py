import ply.lex as lex
from tabulate import tabulate
keywords = ('this', 'class', 'void', 'super', 'extends', 'implements', 'enum', 'interface',
                'byte', 'short', 'int', 'long', 'char', 'float', 'double', 'boolean', 'null',
                'true', 'false',
                'final', 'public', 'protected', 'private', 'abstract', 'static', 'strictfp', 'transient', 'volatile',
                'synchronized', 'native',
                'throws', 'default',
                'instanceof',
                'if', 'else', 'while', 'for', 'switch', 'case', 'assert', 'do',
                'break', 'continue', 'return', 'throw', 'try', 'catch', 'finally', 'new',
                'package', 'import','length')
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
        'EQUAL', 'NEQUAL','GT' ,'GTEQ','LT', 'LTEQ',
        'LSHIFT', 'RSHIFT', 'RRSHIFT',
        'PLUSPLUS', 'MINUSMINUS', 'MODULO', 'LEFTPARENT' , 'RIGHTPARENT',
        'ELLIPSIS' , 'LEFTBRACE','RIGHTBRACE', 'PLUS', 'MINUS','MULTIPLY','DIVIDE', 'ASSIGNMENT',
        'SEMICOLON' , 'COMMA', 'LEFTSQRBRACKET', 'RIGHTSQRBRACKET', 'CONCAT','DOT','NOT'] 

tokens += [kwd.upper() for kwd in keywords]

literals = '()+-*/=?:,.^|&~!=[]{};<>@%'

t_NUMBER = r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'
t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'
t_ignore_LINE_COMMENT = '//.*'
t_ignore_BLOCK_COMMENT =  r'/\*(.|\n)*?\*/'
t_OR = r'\|\|'
t_AND = '&&'
t_EQUAL = '=='
t_NEQUAL = '!='
t_GT = '>'
t_GTEQ = '>='
t_LTEQ = '<='
t_LT = '<'
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
t_MODULO = r'%'
t_ELLIPSIS = r'\.\.\.'
t_LEFTBRACE  = r'\{'
t_RIGHTBRACE = r'\}'
t_PLUS = '\+'
t_MINUS = '\-'
t_MULTIPLY = r'\*'
t_DIVIDE = '\/'
t_ASSIGNMENT = r'='
t_SEMICOLON = r';'
t_COMMA = r','
t_LEFTSQRBRACKET = r'\['
t_RIGHTSQRBRACKET = r'\]'
t_CONCAT = r'\+'
t_DOT = r'\.'
t_LEFTPARENT = r'\('
t_RIGHTPARENT = r'\)'
t_NOT = r'!'
t_ignore = ' \t\f'


def t_NAME(t):
        '[A-Za-z_$][A-Za-z0-9_$]*'
        if t.value in keywords:
            t.type = t.value.upper()
        return t

def t_NEWLINE(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

def t_RNEWLINE(t):
        r'(\r\n)+'
        t.lexer.lineno += len(t.value) / 2

def t_error(t):
        print("ERROR : Unknown character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
        t.lexer.skip(1)


my_inp = open('Simple.java','r').read()
data_types=['byte', 'short', 'int', 'long', 'char', 'float', 'double', 'boolean','void','class']
lex.lex()
lex.input(my_inp)

#SYMBOL TABLE 
sym_table = dict()
s=dict()
sym_table['outer']=s
flag=0
i = 0
l=[]
while 1:
    t = lex.token()
    #print(t)
    if not t: 
         break  
    if(t.type=='LEFTBRACE'):
       l.append(s)
       s=dict()
    if(t.type=='RIGHTBRACE'):
       i=i+1
       sym_table["inner_"+str(i)]=s
       print("\n\n[Table for scope: inner_"+str(i),"]\n")
       print(tabulate([[sym, s[sym]] for sym in s], headers = ['SYMBOL', 'VALUE(lineno,datatype,function/var)'], tablefmt='orgtbl'))
       s=l.pop()
    if(t.value in keywords):
       if(t.value in s):
          line = str(s[t.value][0])
          s[t.value] = (line+','+str(t.lineno),"Keyword")
       else:
          s[t.value] = ( t.lineno , "Keyword")
    if(t.value in data_types):
       flag = 1
       typ = t.value
    if(t.type=='SEMICOLON'):
       flag = 0
    if(t.type == 'NAME'):
       next = lex.token()
       if(next.type == 'LEFTPARENT'):
          if(flag == 1):
             flag = 0
             if(t.value in s):
                 line = str(s[t.value][0])
                 s[t.value] = (line+','+str(t.lineno),typ,"Function")
             else:
                 s[t.value] = (t.lineno,typ,"Function")
          else:
             if(t.value in s):
                 line = str(s[t.value][0])
                 s[t.value] = (line+','+str(t.lineno),"Predefined","Function")
             else:
                 s[t.value] = (t.lineno,"Predefined","Function")
       else:
          if(next.type == 'LEFTBRACE' and flag==1):
             flag = 0
             s[t.value] = (t.lineno,typ,"Class")
             l.append(s)
             s=dict()
          elif(flag==1):
             if(t.value in s):
                line = str(s[t.value][0])
                s[t.value] = (line+','+str(t.lineno),typ,"Variable")
             else:
                s[t.value] = (t.lineno,typ,"Variable")   
sym_table['outer']=s
print("\n\n[Table for scope: outer]\n\n")
print(tabulate([[sym, s[sym]] for sym in s], headers = ['SYMBOL', 'VALUE(lineno,datatype,function/var)'], tablefmt='orgtbl'))

