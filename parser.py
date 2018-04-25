from lex import tokens
import ply.yacc as yacc
import warnings
from AST import *
import AST, sys
import TAC
import copy

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
    'Program : ClassDecls'
    p[0] = Program(p[1])

def p_ClassDecls(p):
    '''ClassDecls : ClassDecls ClassDecl
                  | empty'''
    if len(p) == 3:
        p[1].add_class(p[2])
        p[0] = p[1]
    else:
        p[0] = ClassDecls()

def p_ClassDecl(p):
    '''ClassDecl : CLASS NAME LEFTBRACE MethDecl RIGHTBRACE
                 | CLASS NAME Oop LEFTBRACE MethDecl RIGHTBRACE'''
    if len(p) == 6:
        p[0] = ClassDecl(p[2], p[4])
    elif len(p) == 7:
        p[0] = ClassDecl(p[2], p[5])

def p_Oop(p):
    '''Oop : EXTENDS NAME
           | IMPLEMENTS NAME'''
    

def p_MethDecl(p):
    '''MethDecl : Access STATIC Type NAME LEFTPARENT RIGHTPARENT Block
              | Access Type NAME LEFTPARENT RIGHTPARENT Block
              | Type NAME LEFTPARENT RIGHTPARENT Block'''
    if len(p) == 8:
        p[0] = MethDecl(p[3],p[4],p[7])
    elif len(p) == 7:
        p[0] = MethDecl(p[2],p[3],p[6])        
    elif len(p) == 6:
        p[0] = MethDecl(p[1],p[2],p[5]) 

def p_access(p):
    '''Access : PUBLIC
              | PRIVATE
              | PROTECTED '''
   

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
    '''Identifier : NAME
                  | NAME DOT NAME''' 
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
    '''ForStmt : FOR LEFTPARENT Assign SEMICOLON Expr SEMICOLON Assign RIGHTPARENT Stmt'''
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
            | Expr COMMA Expr
            | LEFTPARENT Expr RIGHTPARENT
            | MethodCall
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
       
def p_MethodCall(p):
    '''MethodCall : NAME LEFTPARENT ArgList RIGHTPARENT
                  | NAME LEFTPARENT RIGHTPARENT '''

def p_ArgList(p):
    '''ArgList : Expr COMMA Expr
               | Expr '''

def p_empty(p):
    'empty : '

def p_error(error):
    print("Syntax Error %s : Unexpected '%s', near line '%s' " % (error, error.value, error.lineno) )
# Build the parser

parser = yacc.yacc(method='SLR')
my_inp = open('Simple.java','r').read()
result = parser.parse(my_inp,debug = 0)
if len(sys.argv) > 1 and sys.argv[1] == 'tree':
    if result is not None:
        print(result)
    exit(0)

# ====== TAC ====== #
tac = TAC.ThreeAddressCode()

def prefix_eval(tokens):
    stack = []
    for t in reversed(tokens):
        if   t == '+': stack[-2:] = [stack[-1] + stack[-2]]
        elif t == '-': stack[-2:] = [stack[-1] - stack[-2]]
        elif t == '*': stack[-2:] = [stack[-1] * stack[-2]]
        elif t == '/': stack[-2:] = [stack[-1] / stack[-2]]
        else: stack.append(t)
    assert len(stack) == 1, 'Malformed expression'
    return stack[0]

def eval_expr(expr):
    global prefix
    ops = []
    dat = []
    #print(expr.expr_type)
    for elem in vars(expr):
        #print('e', elem)
        if elem == 'expr_type':
            if expr.expr_type == 'intnum':
                return int(expr.operand1)
            elif expr.expr_type == 'id':
                return str(expr.operand1)
            elif expr.expr_type == 'binop':
                ret1 = eval_expr(expr.operand1)
                ret2 = eval_expr(expr.operand2)
                if type(ret1) == str or type(ret2) == str:
                    return str(ret1) + " " +  expr.operator + " " + str(ret2)
                else:
                    return eval(str(ret1) + " " +  expr.operator + " " + str(ret2))


temp_count = 0
label_count = 0
prefix = ['']

def assigner(elem):
    global temp_count
    ret = eval_expr(elem.Expr)
    if type(ret) == str and len(ret) > 1 :
        #print(ret)
        ret = ret.split(' ')
        temp = list()
        for i in ret:
            temp.append(i)
            if len(temp) == 3:
                #print("tt", temp)
                try:
                    int(temp[0])
                except:
                    if temp[0][0] != 't':
                        temp[0] = prefix[-1] + temp[0]

                '''try:
                    int(temp[1])
                except:
                    if len(temp) ==
                        temp[1] = prefix[-1] + temp[1]'''
                
                try:
                    int(temp[2])
                except:
                    if temp[2][0] != 't':
                        temp[2] = prefix[-1] + temp[2]
                    
                tac.emit('t'+str(temp_count), temp[0], temp[2], temp[1])
                temp = ['t'+str(temp_count)]
                temp_count += 1
        try:
            int(temp[-1])
        except:
            if temp[-1][0] != 't':
                temp[-1] = prefix[-1] + temp[-1]
        tac.emit(prefix[-1] + elem.id, temp[-1], ' ', '=')
    else :
        try:
            int(ret)
        except:
            if ret != 't':
                ret = prefix[-1] + ret
        tac.emit(prefix[-1] + elem.id, str(ret), " ", "=")


def conditioner(elem):
    global temp_count
    global label_count
    ret = eval_expr(elem)
    
    realRet = []
    for r in ret.split(' '):
        if r not in '+-*/><=>=<=%==!=':
            try:
                int(r)
                realRet.append(r)
            except:
                realRet.append(prefix[-1] + r)
        else:
            realRet.append(r)


    #print('HERE', ret)
    return ''.join(realRet)

def replace(subtree, var):
    try :
        #print('\n\n\n\nreplace at', subtree)
        #exit(0)
        for i in subtree.stmts:
            #print("STMTS ", i)
            replace(i, var)
    except:
        for i in vars(subtree):
            #print("1VARS ", i)
            if type(vars(subtree)[i]) != str and not vars(subtree)[i] is None:
                #print('replacing', vars(subtree)[i])
                replace(vars(subtree)[i], var)
            #print("\n\nCHECK : ", i)
            if 'operand' in i:
                #print("VARS ", vars(subtree)[i], var)
                if vars(subtree)[i] == var:
                    vars(subtree)[i] = var + str(" + 1")

def loop_handler(elem, flag):
    global temp_count
    global label_count

    loop_variable = elem.initial_assign.id

    assigner(elem.initial_assign)

    start_label = label_count
    tac.emit('label', 'L'+str(label_count), ' ', ' ')
    label_count += 1

    end_label = label_count
    ret = conditioner(elem.conditionexpr)
                
    tac.emit('iffalse', ret, 'L'+str(label_count), ' ')
    label_count += 1

    generate_tac(elem.repeatstmt.StmtList)

    if flag:
        subtree = copy.deepcopy(elem.repeatstmt.StmtList)
        replace(subtree, loop_variable)
        generate_tac(subtree)

    assigner(elem.assign)

    tac.emit('goto', 'L'+str(start_label), ' ', ' ')
    tac.emit('label', 'L'+str(end_label), ' ', ' ')

def generate_tac(root):
    global temp_count
    global label_count
    #print("root", type(root))
    
    try:
        for elem in vars(root):
            #print("t", type(type(vars(root)[elem])), type(str()), type(type(vars(root)[elem])) != type(str()))
            e = vars(root)[elem]
            if type(e) == AST.ClassDecl:
                prefix.append(prefix[-1] + e.id + '_')

            elif type(e) == AST.MethDecl:
                prefix.append(prefix[-1] + e.id + '_')
                generate_tac(vars(root)[elem])
                prefix.pop()
            elif (type(vars(root)[elem])) != type(str()):
                #print(elem, type(vars(root)[elem]))
                generate_tac(vars(root)[elem])
    except:
        for elem in root:
            #print("list -", type(elem), AST.IfStmt,type(elem) == AST.IfStmt)
            if type(elem) == AST.ClassDecl:
                generate_tac(elem)

            elif type(elem) == AST.PrintStmt:
                tac.emit("print", elem.mssg, ' ', ' ')

            elif type(elem) == (AST.IfStmt):
                ret = conditioner(elem.conditionexpr)
                else_label = label_count
                tac.emit('iffalse', ret, 'L'+str(label_count), ' ')
                label_count += 1
                
                generate_tac(elem.thenstmt)
                if elem.elsestmt != None:
                    tac.emit('goto', 'L'+str(label_count), ' ', ' ')
                    end_label = label_count
                    label_count += 1

                    tac.emit('label', 'L'+str(else_label), ' ', ' ')

                    generate_tac(elem.elsestmt)
                    tac.emit('label', 'L'+str(end_label), ' ', ' ')
                else:
                    tac.emit('label', 'L'+str(else_label), ' ', ' ')

            elif type(elem) == AST.ForStmt:
                flag = False

                init_val = int(elem.initial_assign.Expr.operand1)
                conditional_val = int(elem.conditionexpr.operand2.operand1)
                update_val = int(elem.assign.Expr.operand2.operand1)
                
                if abs(conditional_val - init_val) > 20 :
                    elem.assign.Expr.operand2.operand1 = str(int(elem.assign.Expr.operand2.operand1) * 2)
                    flag = True

                loop_handler(elem, flag)

            elif type(elem) == AST.Assign:
                assigner(elem)

            elif type(elem) == AST.ClassDecl:
                prefix.append(prefix[-1] + '_' + elem.id)

            elif type(elem) == AST.MethDecl:
                #print(elem)
                #exit(0)
                prefix.append(prefix[-1] + '_' + elem.id)

generate_tac(result)
tac.output3AC()