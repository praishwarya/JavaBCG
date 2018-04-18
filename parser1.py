from lex import tokens
import ply.yacc as yacc
import warnings
from AST1 import *

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

sym_table = dict()

precedence = (
    ('right', 'ASSIGNMENT'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NEQUAL', 'EQUAL'),
    ('left', 'GT', 'LT', 'GTEQ', 'LTEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
    ('right','NEW', 'NOT'),
    ('left', 'DOT')
)

def p_Program(p):
    'Program : ClassDecl'
    p[0] = Program(p[1])

def p_ClassDecl(p):
    'ClassDecl : CLASS NAME LEFTBRACE MethDecl RIGHTBRACE'
    p[0] = ClassDecl(p[2], p[4])
    

def p_MethDecl(p):
    'MethDecl : PUBLIC STATIC Type NAME LEFTPARENT RIGHTPARENT Block'
    p[0] = MethDecl(p[3],p[4],p[7])

   

def p_Type(p):
    '''Type : INT
            | VOID
            | BOOLEAN
            | FLOAT
            | LONG
            | DOUBLE
            | CHAR '''

    if(p[1] == "int"):
        p[0] = Type("INT")
    elif(p[1] == "float"):
        p[0] = Type("FLOAT")
    elif(p[1] == "void"):
        p[0] = Type("VOID")
    

def p_Block(p):
    'Block : LEFTBRACE StmtList RIGHTBRACE'
    p[0] = Block(p[2])    

def p_StmtList(p):
    '''StmtList : StmtList Stmt
                | empty  '''
    if(len(p) == 3):
        p[1].add_stmt(p[2])
        p[0] = p[1]
    else:
        p[0]= StmtList()

def p_VarDeclList(p):
    '''VarDeclList : Declaration
                   | VarDeclList Declaration '''
    if len(p) == 2:
        p[0] = VarDeclList()
        p[0].add_decl(p[1])
    else:
        p[1].add_decl(p[2])
        p[0] = p[1]

def p_Declaration(p):
    'Declaration : Type IdentList SEMICOLON'
    p[0] = Declaration(p[1], p[2])

def p_IdentList(p):
    """ IdentList : Identifier 
                  | IdentList COMMA Identifier 
    """
    if len(p) == 2:
        p[0] = IdentList([p[1]])
    else:
        p[1].add_identifier(p[3])
        p[0] = p[1]

def p_Identifier(p):
    'Identifier : NAME'
    p[0] = Identifier(p[1])   


def p_Stmt(p):
    '''Stmt : PrintStmt
            | Assign SEMICOLON
            | IfStmt
            | VarDeclList
            | ForStmt
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | Block'''
    p[0] = p[1]

def p_PrintStmt(p):
   'PrintStmt : NAME DOT NAME DOT NAME LEFTPARENT STRING_LITERAL RIGHTPARENT SEMICOLON'
   p[0] = PrintStmt(p[7])

def p_Assign(p):
    'Assign : NAME ASSIGNMENT Expr'
    #print("\n*******************",p[1])
    p[0] = Assign(p[1], p[3])


def p_IfStmt(p):
    '''IfStmt : IF LEFTPARENT Expr RIGHTPARENT Stmt
              | IF LEFTPARENT Expr RIGHTPARENT Stmt ELSE Stmt '''

    if(len(p) == 6):
       p[0] = IfStmt(p[3], p[5])
    else:
       p[0] = IfStmt(p[3], p[5],p[7])
    

def p_ForStmt(p):
    'ForStmt : FOR LEFTPARENT Assign SEMICOLON Expr SEMICOLON Assign RIGHTPARENT Stmt'
    p[0] = ForStmt(p[3],p[5],p[7],p[9])

def p_Expr(p):
    '''Expr : NAME
            | Expr PLUS Expr
            | Expr MINUS Expr
            | Expr MULTIPLY Expr
            | Expr DIVIDE Expr
            | Expr MODULO Expr
            | Expr AND Expr
            | Expr OR Expr
            | Expr CONCAT Expr
            | Expr LT Expr
            | Expr LTEQ Expr
            | Expr GT Expr
            | Expr GTEQ Expr
            | Expr EQUAL Expr
            | Expr NEQUAL Expr
            | Expr NOT
            | Expr MINUSMINUS
            | Expr PLUSPLUS
            | LEFTPARENT Expr RIGHTPARENT
            | NUMBER '''
    if len(p) == 4:
        if p[1] == '(':
            p[0] = Expr("paren", operand1=p[2])
        else:
            p[0] = Expr("binop", operator=p[2], operand1=p[1], operand2=p[3])
    elif len(p) == 3:
        p[0] = Expr("unop", operand1=p[2])
    elif len(p) == 2:
        if (p[1].isdigit()==True):
            p[0] = Expr('intnum', operand1=p[1])
        else:
            p[0] = Expr("id", operand1=p[1])
       

def p_empty(p):
    'empty : '

def p_error(error):
    print("Syntax Error %s : Unexpected '%s', near line '%s' " % (error, error.value, error.lineno) )
# Build the parser

parser = yacc.yacc(method='SLR')
my_inp = open('Simple.java','r').read()
result = parser.parse(my_inp,debug = 0)
if result is not None:
	print(result)
