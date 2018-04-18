#!/usr/bin/python
import ply.lex as lex
import sys
from ply.lex import TOKEN
ReservedWords=["TRUE","true","FALSE","false","null"]
tokens = (
    'Keyword',
    'Identifier',
    'FloatingLiteral',
    'IntegerLiteral',
    'BooleanLiteral',
    'CharacterLiteral',
    'StringLiteral',
    'Separator',
    'Comments',
    'Operator',
    'OP_DIM'
)

# Regular expression rules for simple tokens
Alphabets = r'([a-zA-Z])'
Numeric = r'([0-9])'
Alphanum = r'([a-zA-Z0-9])'
Special = r'([\]!%\^&$*()\-+={}|~[\;:<>?,./#@`_])'
Graphic = r'([a-zA-Z0-9]|'+ Special + r')'
IdentifierStart = r'([0-9a-zA-Z$_])'
Identifier = r'[a-zA-Z$_][a-zA-Z0-9$_]*'

# print(Identifier)
Keyword = r'(continue|for|new|switch|assert|default|goto|boolean|do|if|finally|final|private|this|class|break|double|protected|byte|else|import|public|case|enum|return|catch|extends|int|short|try|char|static|void|long|volatile|const|float|String|while|interfaces|throw|throws)'+r'[^0-9a-zA-Z$_]'
Separator = r'[;,.(){}[\] \"\']'
Comments = r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
Operator = r'(>>>=|<<=|>>=|<<|>>|>>>|<=|>=|<|>|\+\+[^+=]|--[^\-=]|[+\-*/%&\^|]=|\+[^+=]|-[^\-=]|\*|/|==|=|~|!=|%|instanceof|!|&&|\^|\|\||&|\|)'

FloatingLiteral=r'(([0-9]+)?\.([0-9]+)((e|E)((\+|-)?[0-9]+))?([fFdD])?|[0-9]+(e|E)(\+|-)?[0-9]+)'
IntegerLiteral=r'[0-9]+'
BooleanLiteral=r'(true|false|TRUE|FALSE)'
CharacterLiteral=r'(\'(' + Graphic + r'|\ |\\[n\\ta"\'])\')'
StringLiteral=r'(\"(' + Graphic + r'|\ |\\[n\\ta"\'])*\")'
# Literals= r'('+FloatingLiteral+r'|null|'+IntegerLiteral+r'|'+BooleanLiteral+r'|'+CharacterLiteral+r'|'+StringLiteral+r')'
Illegals = r'('+IntegerLiteral + r'[a-zA-Z]+)'
OP_DIM=r'\[[\t ]*\]'
# A regular expression rule with some action code
# Note addition of self parameter since we're in a class
# print("hsbdfbdfh")
@TOKEN(Comments)
def t_Comments(t):
    t.lexer.lineno+=t.value.count('\n')
    pass
@TOKEN(Illegals)
def t_Illegals(t):
    print("Line :: %d  Illegal entry '%s'" %(t.lexer.lineno, t.value))
    pass

@TOKEN(Keyword)
def t_Keyword(t):
    # t.type=t.value.upper()
    t.type = keywords[t.value[:-1]]
    # print(keywords[t.value[:-1]])
    # print(t.type)
    # print(t.type)
    # print(t)
    t.lexer.lexpos-=1;
    v= t.value[:-1]
    t.value = v
    return t

@TOKEN(Identifier)
def t_Identifier(t):
    # print t.value
    if(t.value in ReservedWords):
        t.type="BooleanLiteral"
    return t

@TOKEN(FloatingLiteral)
def t_FloatingLiteral(t):
    return t

@TOKEN(IntegerLiteral)
def t_IntegerLiteral(t):
    return t

@TOKEN(BooleanLiteral)
def t_BooleanLiteral(t):
    return t
    
@TOKEN(CharacterLiteral)
def t_CharacterLiteral(t):
    return t

@TOKEN(StringLiteral)
def t_StringLiteral(t):
    return t

@TOKEN(OP_DIM)
def t_OP_DIM(t):
    # t.type = separators[t.value]
    return t

@TOKEN(Separator)
def t_Separator(t):
    t.type = separators[t.value]
    return t

@TOKEN(Operator)
def t_Operator(t):
    # t.type=OP[t.value]
    # t.type=t.value.upper()
    # print t.value
    cond1=t.value[:-1]=='+' or t.value[:-1]=='-' or t.value[:-1]=='++' or t.value[:-1]=='--'
    if(cond1 and t.value[-1] != '=' ):
        t.value=t.value[:-1]
        # print t.value
        t.lexer.lexpos=t.lexer.lexpos-1
    t.type = operators[t.value]
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Line :: %d  Illegal entry '%s'" %(t.lexer.lineno, t.value))
    t.lexer.skip(1)


keyw = ['continue','for','new','switch','assert','default','goto','boolean','final' ,'do','if','private','this','break','double','protected','byte','else','import','public','case','enum','return','catch','extends','int','short','try','char','static','void','class','long','volatile','const','finally','float','String','while','interfaces','throw','throws']
keywords ={}
for i in keyw:
    keywords[i]="KEY"+ str(i).upper()
tokens = tokens + tuple(keywords.values())
# op = ['=','<','>' ,'<=','>=','+','-','*' , '?' ,'/' ,'==' ,'++' , '--', '~', '!' ,'%' , '<<' , '>>', '>>>' , 'instanceof', '!=','&' , '^', '|' , '&&' , '||' , '+=' , '/=', '-=', '*=' , '%=', '&=', '^=', '|=' , '<<=' , '>>=' ,'>>>=' ]

operators = {
    '+':    'PLUS',
    '-':    'MINUS',
    '*':    'MULTIPLY',
    '/':    'DIVIDE',
    '%':    'MOD',
    '=':    'EQUAL',
    '<=':   'LESSEQ',
    '>=':   'GREATEQ',
    '<':    'LESSER',
    '>':    'GREATER',
    '==':   'CHECKEQ',
    '++':   'INCREMENT',
    '--':   'DECREMENT',
    '~' :   'TILDE',
    '!' :   'NOT',
    '<<':   'LEFTSHIFT',
    '>>':   'RIGHTSHIFT',
    '>>>':  'LOGICALSHIFT',
    'instanceof':   'INSTANCEOF',
    '!=':   'NOTEQ',
    '&' :   'BINAND',
    '^' :   'XOR',
    '|' :   'BINOR',
    '?' :   'TERNARY',
    '&&' :  'AND',
    '||' :  'OR',
    '+=' :  'PLUSEQ',
    '/=' :  'DIVIDEEQ',
    '-=' :  'MINUSEQ',
    '*=' :  'MULTIPLYEQ',
    '%=' :  'MODEQ',
    '&=' :  'BINANDEQ',
    '^=' :  'XOREQ',
    '|=' :  'BINOREQ',
    '<<=' : 'LEFTSHIFTEQ',
    '>>=' : 'RIGHTSHIFTEQ',
    '>>>=' : 'LOGICALSHIFTEQ'

}
for i in operators:
    operators[i] = "OP" + operators[i]
tokens = tokens + tuple(operators.values())
separators = {
    ';' : 'SEMICOLON',
    ',' : 'COMMA',
    '.' : 'DOT' ,
    '(' : 'LEFTBRACE',
    ')' : 'RIGHTBRACE',
    '{' : 'LEFTPARAN',
    '}' : 'RIGHTPARAN',
    '[' : 'LEFTSQBR',
    ']' : 'RIGHTSQBR',
    '"' : 'DOUBLEINCO',
    '\'' : 'SINGLEINCO',
    ':' : 'COLON'
}
for i in separators:
    separators[i] = "SEP" + separators[i]
tokens = tokens + tuple(separators.values())
lexer = lex.lex()
# filename = sys.argv[1]
# print("great")
# f = open(filename, 'r')
# data = f.read()
# lexer.input(data)
# for tok in lexer:
#     print tok