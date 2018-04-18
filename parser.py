from lex import tokens
import ply.yacc as yacc
import warnings
from AST import *

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
    'Program : ClassDeclList'
    p[0] = Program(p[1])

def p_ClassDeclList(p):
    'ClassDeclList : ClassDecl ClassDeclList'
    p[0] = ClassDeclList(p[1], p[2])

def p_ListaClassDecl1(p):
    'ClassDeclList : empty'
    p[0] = NullNode()

# classDecl ::= class id[extend id] '{' (fieldDecl | methDecl)* '}' 

def p_ClassDecl(p):
    'ClassDecl : CLASS NAME ExtendClass LEFTBRACE FieldMethDecl RIGHTBRACE'
    p[0] = ClassDecl(Name(p[2],p.lineno(1)), p[3], p[5])

def p_ExtendClass(p):
    'ExtendClass : EXTENDS NAME'
    p[0] = ExtendClass(Name(p[2],p.lineno(1)))

def p_ExtendClass1(p):
    'ExtendClass : empty'
    p[0] = NullNode()

def p_FieldMethDecl(p):
    'FieldMethDecl : FieldMeth FieldMethDecl'
    p[0] = FieldMethDecl(p[1],p[2])    

def p_FieldMethDecl1(p):
    'FieldMethDecl : empty'
    p[0] = NullNode()

def p_FieldMeth(p):
    '''FieldMeth : FieldDecl
                 | MethDecl'''
    p[0] = FieldMeth(p[1])

# fieldDecl ::=type id( ',' id)* ';' 

def p_FieldDecl(p):
    'FieldDecl : Type NAME NAMECommaList SEMICOLON'
    p[0] = FieldDecl(p[1], Name(p[2], p.lineno(1)), p[3])

def p_NAMECommaList(p):
    'NAMECommaList : NAMEComma NAMECommaList'
    p[0] = NameCommaList(p[1], p[2])

def p_NAMECommaList1(p):
    'NAMECommaList : empty'
    p[0] = NullNode()
   
def p_NAMEComma(p):
    'NAMEComma : COMMA NAME'
    p[0] = NameComma(Name(p[2],p.lineno(1)))
    
# methDecl ::= (type | void) id '(' [formals] ')' block #

def p_MethDecl(p):
    'MethDecl : Accesspecifier STATIC MethType NAME LEFTPARENT Args RIGHTPARENT Block'
    p[0] = MethDecl(p[3],Name(p[4],p.lineno(1)),p[6],p[8])

def p_Accesspecifier(p):
    'Accesspecifier : PUBLIC'
    p[0] = p[1]

def p_MethType(p):
    'MethType : Type'
    p[0] = MethType(p[1])
   
def p_MethdType1(p):
    'MethType : VOID'
    p[0] = MethType(p[1])    

def p_Args(p):
    '''Args : Formals
            | empty'''
    p[0] = Args(p[1])
    
#  formals ::= type id ( ',' type id)* 

def p_Formals(p):
    'Formals : Type NAME NAMETypeCommaList'
    p[0] = Formals(p[1],Name(p[2],p.lineno(1)),p[3])
    
def p_NAMETypeCommaList(p):
    'NAMETypeCommaList : CommaTypeId NAMETypeCommaList'
    p[0] = NameTypeCommaList(p[1],p[2])
    
def p_NAMETypeCommaList1(p):
    'NAMETypeCommaList : empty'
    p[0] = NullNode()
   
def p_CommaTypeId(p):
    'CommaTypeId : COMMA Type NAME'
    p[0] = CommaTypeId(p[2],Name(p[3],p.lineno(1)))
   
# type ::= int | boolean | STRING_LITERAL | id | type '[' ']' id 

def p_Type(p):
    '''Type : INT
            | BOOLEAN
            | FLOAT
            | LONG
            | DOUBLE
            | CHAR
            | STRING_LITERAL
            | NAME
            | Array'''
    p[0] = Type(p[1])
    #print(p[0])

def p_Array(p):
    'Array : Type LEFTSQRBRACKET RIGHTSQRBRACKET'
    p[0] = Array(p[1])
    
# block ::= '{' varDecl* stmt* '}' 

def p_Block(p):
    'Block : LEFTBRACE VarDeclList StmtList RIGHTBRACE'
    p[0] = Block(p[2],p[3])    

def p_StmtList(p):
    'StmtList : Stmt StmtList'
    p[0] = StmtList(p[1],p[2])

def p_StmtList1(p):
    'StmtList : empty'
    p[0] = NullNode()
    
# varDecl ::= type id ['=' expr] ( ',' id ['=' expr] )* ';' 
def p_VarDeclList(p):
    'VarDeclList : NAME ExpDecl ExpDeclList SEMICOLON'
    p[0] = VarDeclList(Name(p[1],p.lineno(1)),p[2],p[3])

def p_VarDeclList1(p):
    'VarDeclList : Type NAME ExpDecl ExpDeclList SEMICOLON VarDeclList'
    p[0] = VarDeclList1(p[1],Name(p[2],p.lineno(1)),p[3],p[4], p[6])

def p_VarDeclList2(p):
    'VarDeclList : empty'
    p[0] = NullNode()

def p_ExpDeclList(p):
    'ExpDeclList : CommaExpDecl ExpDeclList'
    p[0] = ExpDeclList(p[1],p[2])
    

def p_ExpDeclList1(p):
    'ExpDeclList : empty'
    p[0] = NullNode()
    
def p_CommaExpDecl(p):
    'CommaExpDecl : COMMA NAME ExpDecl'
    p[0] = CommaExpDecl(Name(p[2],p.lineno(1)), p[3])

def p_Decl(p):
    'ExpDecl : ASSIGNMENT Expr'
    p[0] = Decl(p[2])
    #p[0] = Node("unop", p[1], p[2])
    #print(p[0].type, ":", p[0].leaf, "->", p[0].children)
    

def p_Decl1(p):
    'ExpDecl : empty'
    p[0] = NullNode()
    
# stmt ::= assign ';'                 
#  | call ';'                         
#  | return [expr] ';'                
#  | if '(' expr ')' stmt [else stmt] 
#  | while '(' expr ')' stmt          
#  | break ';' | continue ';'         
#  | block                            


def p_Stmt(p):
    '''Stmt : PrintStmt 
	    | Assign SEMICOLON
            | Call SEMICOLON
            | Return
            | IfStmt
            | WhileStmt
            | ForStmt
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | Block'''
    p[0] = Stmt(p[1])

def p_PrintStmt(p):
   'PrintStmt : NAME DOT NAME DOT NAME LEFTPARENT STRING_LITERAL RIGHTPARENT SEMICOLON'
    

# assign ::= location '=' expr 

def p_Assign(p):
    'Assign : Location ASSIGNMENT Expr'
    #print(p)
    '''p[0] = p[1] + p[2] + p[3]
    node = ast.parse(p[0], mode='eval')
    print(p[0])
    print(ast.dump(node.body).replace(',','\n'))
    print(" ")'''
    p[0] = Assign(p[1], p[3])
    #p[0] = Node("assign", p[0], p[2])
    #p[0] = Node("assign", [p[1],p[3]], p[2])
    #print(p[0].type, ":", p[0].leaf, "->", p[0].children)

# location ::= id|expr '.' id|expr '[' ']' 
def p_Location(p):
    'Location : NAME'
    #p[0] = Name(p[1],p.lineno(1))

def p_Location1(p):
    'Location : Expr DOT NAME'
    #p[0]=Location1(p[1],Name(p[3],p.lineno(1)))

def p_Location2(p):
    'Location : Expr LEFTSQRBRACKET Expr RIGHTSQRBRACKET'
    #p[0]=Location2(p[1],p[3])


# call ::= method '(' [actuals] ')' 

def p_Call(p):
    'Call : Method LEFTPARENT Actuals RIGHTPARENT'
    #p[0]=Call(p[1],p[3])
    
# method ::= id|expr '.' id 

def p_Method(p):
    'Method : NAME'
    #p[0] = Name(p[1],p.lineno(1))

def p_Method1(p):
    'Method : Expr DOT NAME'
    #p[0] = Method(p[1],Name(p[3],p.lineno(1)))


# actuals ::= expr (',' expr )* 

def p_Actuals(p):
    'Actuals : Expr ExprCommaList'
    #p[0] = Actuals(p[1], p[2])

def p_ExprCommaList(p):
    'ExprCommaList : ExprComma ExprCommaList'
    #p[0] = ExprCommaList(p[1], p[2])

def p_ExprCommaList1(p):
    'ExprCommaList : empty'
    #p[0] = NullNode()

def p_ExprComma(p):
    'ExprComma : COMMA Expr'
    #p[0] = ExprComma(p[2])

# return [expr] ';' 

def p_Return(p):
    'Return : RETURN ReturnExpr SEMICOLON'
    #p[0] = Return(p[1], p[2])
    

def p_ReturnExpr(p):
    'ReturnExpr : Expr'
    #p[0] = ReturnExpr(p[1])
    

def p_ReturnExpr1(p):
    'ReturnExpr : empty'
    #p[0] = NullNode()
    
# if '(' expr ')' stmt [else stmt] 

def p_IfStmt(p):
    'IfStmt : IF LEFTPARENT Expr RIGHTPARENT Stmt ElseStmt'

def p_ElseStmt(p):
    'ElseStmt : ELSE Stmt'
    
def p_ElseStmt1(p):
    'ElseStmt : empty'
    

# while '(' expr ')' stmt 

def p_WhileStmt(p):
    'WhileStmt : WHILE LEFTPARENT Expr RIGHTPARENT Stmt'

def p_ForStmt(p):
    'ForStmt : FOR LEFTPARENT VarDeclList Actuals SEMICOLON Actuals RIGHTPARENT Stmt'
# expr ::= location        
#  | call                  
#  | this                  
#  | new id '(' ')'        
#  | new type '[' expr ']' 
#  | expr '.' length       
#  | expr binary expr      
#  | unary expr            
#  | literal               
#  | '(' expr ')'          

def p_Expr(p):
    '''Expr : Location
            | Call
            | THIS
            | NewId
            | NewTypeExpr
            | ExprLength
            | ExprBinaryExpr
            | UnaryExpr
            | Literal
            | Number
            | ParentExprParent'''
    p[0] = p[1]
   
# new id '(' ')' 

def p_NewId(p):
    'NewId : NEW NAME LEFTPARENT RIGHTPARENT'
    
# new type '[' expr ']' 

def p_NewTypeExpr(p):
    'NewTypeExpr : NEW Type LEFTSQRBRACKET Expr LEFTSQRBRACKET'
   
# expr '.' length 

def p_ExprLength(p):
    'ExprLength : Expr DOT LENGTH'

'''def make_lt_compare(left, right):
    return ast.Compare(left, [('<', right), ])


def make_gt_compare(left, right):
    return ast.Compare(left, [('>', right), ])


def make_eq_compare(left, right):
    return ast.Compare(left, [('==', right), ])

binary_ops = {
    "+": ast.Add,
    "-": ast.Sub,
    "*": ast.Mul,
    "/": ast.Div,
    "<": ast.Compare,
    ">": make_gt_compare,
    "==": make_eq_compare,
}
unary_ops = {
    "+": ast.UnaryAdd,
    "-": ast.UnarySub,
}'''

# expr binary expr 

def p_ExprBinaryExpr(p):
    '''ExprBinaryExpr : Expr PLUS Expr
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
                      | Expr NEQUAL Expr'''
    #print(p[1])
    #p[0] = ('binary-expression', p[2], p[1], p[3])
    #p[0] = Node("binop", [p[1],p[3]], p[2])
    #p[0] = binary_ops[p[2]]((p[1], p[3]))
    #p[0] = BinOp(p[1],p[2],p[3])
    #p[0] = p[1] + p[2] + p[3]
    #node = ast.parse(p[0], mode='eval')
    #print("Expression: ")
    #print(p[0])
    #print(ast.dump(node.body))
    #print(" ")
    #print(p[0].type, ":", p[0].leaf, "->", p[0].children)	
    #print(p[0].type, ":", p[0].op, "->", p[0].left, p[0].right)	

## binary ::= '+' | '-' | '*' | '/' | '%' | '&&' | '||'   
##                | '<' | '<=' | '>' | '>=' | '==' | '!=' 

# unary ::= '-' | '!' 

def p_UnaryExpr(p):
    '''UnaryExpr : Expr NOT
                 | Expr MINUSMINUS
                 | Expr PLUSPLUS'''
    #p[0] = ('unary-expression', p[2], p[1])
    #p[0] = Node("unop", p[1], p[2])
    #p[0] = unary_ops[p[1]](p[2])
    #p[0] = p[2]+ p[1]
    #node = ast.parse(p[0], mode='eval')
    #print("Expression: ")
    #print(p[0])
    #print(ast.dump(node.body))
    #print(" ")
    #print(p[0].type, ":", p[0].leaf, "->", p[0].children)
    

# literal ::= integer-literal | STRING_LITERAL-literal | true | false | null 

def p_Literal(p):
    '''Literal : INT
               | STRING_LITERAL
               | TRUE
               | FALSE
               | NULL'''
    p[0] = p[1]

def p_ParentExprParent(p):
    'ParentExprParent : LEFTPARENT Expr RIGHTPARENT'
    p[0] = p[2]

def p_Number(p):
    '''Number : NUMBER'''
    p[0] = p[1]
    #p[0] = ast.Const(p[1])

def p_empty(p):
    'empty : '


def p_error(error):
    print("Syntax Error %s : Unexpected '%s', near line '%s' " % (error, error.value, error.lineno) )
# Build the parser

parser = yacc.yacc(method='SLR')
my_inp = open('Simple.java','r').read()
raiz = yacc.parse(my_inp)

raiz.show()
