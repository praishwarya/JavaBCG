from lex import tokens
import ply.yacc as yacc

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
    

def p_ClassDeclList(p):
    'ClassDeclList : ClassDecl ClassDeclList'

def p_ListaClassDecl1(p):
    'ClassDeclList : empty'

# classDecl ::= class id[extend id] '{' (fieldDecl | methDecl)* '}' 

def p_ClassDecl(p):
    'ClassDecl : CLASS NAME ExtendClass LEFTBRACE FieldMethDecl RIGHTBRACE'

def p_ExtendClass(p):
    'ExtendClass : EXTENDS NAME'

def p_ExtendClass1(p):
    'ExtendClass : empty'

def p_FieldMethDecl(p):
    'FieldMethDecl : FieldMeth FieldMethDecl'

def p_FieldMethDecl1(p):
    'FieldMethDecl : empty'

def p_FieldMeth(p):
    '''FieldMeth : FieldDecl
                 | MethDecl'''

# fieldDecl ::=type id( ',' id)* ';' 

def p_FieldDecl(p):
    'FieldDecl : Type NAME NAMECommaList SEMICOLON'

def p_NAMECommaList(p):
    'NAMECommaList : NAMEComma NAMECommaList'

def p_NAMECommaList1(p):
    'NAMECommaList : empty'
   
def p_NAMEComma(p):
    'NAMEComma : COMMA NAME'
    
# methDecl ::= (type | void) id '(' [formals] ')' block #

def p_MethDecl(p):
    'MethDecl : Accesspecifier STATIC MethType NAME LEFTPARENT Args RIGHTPARENT Block'

def p_Accesspecifier(p):
    'Accesspecifier : PUBLIC'

def p_MethType(p):
    'MethType : Type'
   
def p_MethdType1(p):
    'MethType : VOID'
    
def p_Args(p):
    '''Args : Formals
            | empty'''
    
#  formals ::= type id ( ',' type id)* 

def p_Formals(p):
    'Formals : Type NAME NAMETypeCommaList'
    
def p_NAMETypeCommaList(p):
    'NAMETypeCommaList : CommaTypeId NAMETypeCommaList'
    
def p_NAMETypeCommaList1(p):
    'NAMETypeCommaList : empty'
   
def p_CommaTypeId(p):
    'CommaTypeId : COMMA Type NAME'
    p[0] = CommaTypeId(p[2],Id(p[3],p.lineno(1)))
   
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
   

def p_Array(p):
    'Array : Type LEFTSQRBRACKET RIGHTSQRBRACKET'
    
# block ::= '{' varDecl* stmt* '}' 

def p_Block(p):
    'Block : LEFTBRACE VarDeclList StmtList RIGHTBRACE'
    
def p_StmtList(p):
    'StmtList : Stmt StmtList'
    

def p_StmtList1(p):
    'StmtList : empty'
    
# varDecl ::= type id ['=' expr] ( ',' id ['=' expr] )* ';' 
def p_VarDeclList(p):
    '''VarDeclList : NAME ExpDecl ExpDeclList SEMICOLON
                   | Type NAME ExpDecl ExpDeclList SEMICOLON VarDeclList'''

def p_VarDeclList1(p):
    'VarDeclList : empty'

def p_ExpDeclList(p):
    'ExpDeclList : CommaExpDecl ExpDeclList'
    

def p_ExpDeclList1(p):
    'ExpDeclList : empty'
    
def p_CommaExpDecl(p):
    'CommaExpDecl : COMMA NAME ExpDecl'
    

def p_Decl(p):
    'ExpDecl : ASSIGNMENT Expr'
    

def p_Decl1(p):
    'ExpDecl : empty'
    
# stmt ::= assign ';'                 
#  | call ';'                         
#  | return [expr] ';'                
#  | if '(' expr ')' stmt [else stmt] 
#  | while '(' expr ')' stmt          
#  | break ';' | continue ';'         
#  | block                            


def p_Stmt(p):
    '''Stmt : Assign SEMICOLON
            | Call SEMICOLON
            | Return
            | IfStmt
            | WhileStmt
            | ForStmt
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | Block
            | PrintStmt SEMICOLON'''
    


def p_PrintStmt(p):
    'PrintStmt : NAME DOT NAME DOT NAME LEFTPARENT STRING_LITERAL RIGHTPARENT'
    print("hvdf")
# assign ::= location '=' expr 

def p_Assign(p):
    'Assign : Location ASSIGNMENT Expr'

# location ::= id|expr '.' id|expr '[' ']' 
def p_Location(p):
    'Location : NAME'

def p_Location1(p):
    'Location : Expr DOT NAME'

def p_Location2(p):
    'Location : Expr LEFTSQRBRACKET Expr RIGHTSQRBRACKET'


# call ::= method '(' [actuals] ')' 

def p_Call(p):
    'Call : Method LEFTPARENT Actuals RIGHTPARENT'
    
# method ::= id|expr '.' id 

def p_Method(p):
    'Method : NAME'

def p_Method1(p):
    'Method : Expr DOT NAME'


# actuals ::= expr (',' expr )* 

def p_Actuals(p):
    'Actuals : Expr ExprCommaList'

def p_ExprCommaList(p):
    'ExprCommaList : ExprComma ExprCommaList'

def p_ExprCommaList1(p):
    'ExprCommaList : empty'

def p_ExprComma(p):
    'ExprComma : COMMA Expr'


# return [expr] ';' 

def p_Return(p):
    'Return : RETURN ReturnExpr SEMICOLON'
    

def p_ReturnExpr(p):
    'ReturnExpr : Expr'
    

def p_ReturnExpr1(p):
    'ReturnExpr : empty'
    
# if '(' expr ')' stmt [else stmt] 

def p_IfStmt(p):
    'IfStmt : IF LEFTPARENT Expr RIGHTPARENT Stmt ElseStmt'
    print(p[2])

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
   
# new id '(' ')' 

def p_NewId(p):
    'NewId : NEW NAME LEFTPARENT RIGHTPARENT'
    
# new type '[' expr ']' 

def p_NewTypeExpr(p):
    'NewTypeExpr : NEW Type LEFTSQRBRACKET Expr LEFTSQRBRACKET'
   
# expr '.' length 

def p_ExprLength(p):
    'ExprLength : Expr DOT LENGTH'


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
    
## binary ::= '+' | '-' | '*' | '/' | '%' | '&&' | '||'   
##                | '<' | '<=' | '>' | '>=' | '==' | '!=' 

# unary ::= '-' | '!' 

def p_UnaryExpr(p):
    '''UnaryExpr : Expr NOT
                 | Expr MINUSMINUS
                 | Expr PLUSPLUS'''
    

# literal ::= integer-literal | STRING_LITERAL-literal | true | false | null 

def p_Literal(p):
    '''Literal : INT
               | STRING_LITERAL
               | TRUE
               | FALSE
               | NULL'''

def p_ParentExprParent(p):
    'ParentExprParent : LEFTPARENT Expr RIGHTPARENT'

def p_Number(p):
    '''Number : NUMBER'''

def p_empty(p):
    'empty : '


def p_error(error):
    print("Syntax Error %s : Unexpected '%s', near line '%s' " % (error, error.value, error.lineno) )
# Build the parser
parser = yacc.yacc()
my_inp = open('Simple.java','r').read()
parser.parse(my_inp)
