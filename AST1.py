debugNode = False


class Node(object):
    def printast(self):
        return "NOT IMPLEMENTED!"

    def insertLineNumInfo(self, linenumber, position):
        self.line_position = (linenumber, position)

    def position(self):
        return "Line %d, Column %d" % self.line_position


class Program(Node):
    def __init__(self, classdecl):
        self.ClassDecl = classdecl

    def __str__(self):
        outputstr = "\n[Program] :\n"
        if self.ClassDecl is not None:
            outputstr += "ClassDecl : " + str(self.ClassDecl)
        return outputstr

    def printast(self):
        outputstr = ""
        outputstr += "[Program]"
        if self.ClassDecl is not None:
            outputstr += self.ClassDecl.printast()
        return outputstr

class ClassDecl(Node):
	def __init__(self,id , methdecl):
		self.id = id
		self.MethDecl = methdecl
	def __str__(self):
		outputstr = "\n[Class]:\n"
		if self.id is not None:
            		outputstr += "id : " + str(self.id)
		if self.MethDecl is not None:
			outputstr += "MethDecl: "+ str(self.MethDecl)
		return outputstr
	def printast(self):
		outputstr = ""
		outputstr += str(self.id)
		outputstr += self.MethDecl.printast()
		return outputstr

class MethDecl(Node):
	def __init__(self,type,id,block):
		self.id = id
		self.Type = type
		self.Block = block
	def __str__(self):
		outputstr = "\n[MethDecl]:\n"
		if self.id is not None:
			outputstr += "id : " + str(self.id)
		if self.Type is not None:
			outputstr += "type:" +str(self.Type)
		if self.Block is not None:
			outputstr += "Block:" + str(self.Block)
		return outputstr
	def printast(self):
		outputstr = ""
		outputstr += self.type.printast() + " "
		outputstr += str(self.id) + " "
		outputstr += self.Block.printast()
		return outputstr

class Type(Node):
    def __init__(self, type):
        self.type = type                    # This value can be either "int" or "float"

    def __str__(self):
        outputstr = "\n[Type] : \n"
        if self.type is not None:
            outputstr += "type : " + str(self.type)
            outputstr += "\n"
        return outputstr

    def printast(self):
        return str(self.type).lower()

class Block(Node):
    def __init__(self, stmtlist, decllist=None): # Note the order of the parameter
        #self.VarDeclList = decllist
        self.StmtList = stmtlist

    def __str__(self):
        outputstr = "\n[Block] : \n"
        ''' if self.VarDeclList is not None:
            outputstr += "VarDeclList : " + str(self.VarDeclList)'''
        if self.StmtList is not None:
            outputstr += "stmtlist : " + str(self.StmtList)
        return outputstr

    def printast(self):
        outputstr = ""
        outputstr += "{\n"
        if self.VarDeclList is not None:
            outputstr += self.VarDeclList.printast() + "\n"
        outputstr += self.StmtList.printast()
        outputstr += "\n}"
        return outputstr

class StmtList(Node):
    def __init__(self):
        self.stmts = []                  # This will be list of Stmt object

    def add_stmt(self, stmt):
        self.stmts.append(stmt)

    def __str__(self):
        outputstr = "\n[StmtList] : \n"
        if self.stmts is not None:
            outputstr += "stmts : "
            outputstr += "["
            for element in self.stmts:
                outputstr += str(element) + " "
            outputstr += "]"
        return outputstr

    def printast(self):
        l = []
        for e in self.stmts:
            l.append(e.printast())
        return "\n".join(l)


class Assign(Node):
    def __init__(self, id, expr):
        self.id = id
        self.Expr = expr
       
    def __str__(self):
        outputstr = "\n[Assign] : \n"
        if self.id is not None:
            outputstr += "id : " + str(self.id)
        if self.Expr is not None:
            outputstr += "\nExpr : " + str(self.Expr)
        return outputstr

    def printast(self):
        return str(self.id)+" = "+self.Expr.printast()

class PrintStmt(Node):
    def __init__(self, val):
        self.mssg = val
       
    def __str__(self):
        outputstr = "\n[PrintStmt] : \n"
        outputstr += "Message : " + str(self.mssg)
        return outputstr

    def printast(self):
        return str(self.mssg)



class ForStmt(Node):
    def __init__(self, initial_assign, conditionexpr, assign, repeatstmt):
        self.initial_assign = initial_assign
        self.conditionexpr = conditionexpr
        self.assign = assign
        self.repeatstmt = repeatstmt

    def __str__(self):
        outputstr = "\n[ForStmt] : \n"
        if self.initial_assign is not None:
            outputstr += "initial_assign : " + str(self.initial_assign)
        if self.conditionexpr is not None:
            outputstr += "conditionexpr : " + str(self.conditionexpr)
        if self.assign is not None:
            outputstr += "assign : " + str(self.assign)
        if self.repeatstmt is not None:
            outputstr += "repeatstmt : " + str(self.repeatstmt)
        return outputstr

    def printast(self):
        outputstr = "for ("
        outputstr += self.initial_assign.printast()+ ";"
        outputstr += self.conditionexpr.printast() + ";"
        outputstr += self.assign.printast() + ")\n"
        outputstr += self.repeatstmt.printast()
        return outputstr

class IfStmt(Node):
    def __init__(self, conditionexpr, thenstmt, elsestmt=None):
        self.conditionexpr = conditionexpr
        self.thenstmt = thenstmt
        self.elsestmt = elsestmt

    def __str__(self):
        outputstr = "\n[If Stmt] : \n"
        if self.conditionexpr is not None:
            outputstr += "conditionexpr : " + str(self.conditionexpr)
        if self.thenstmt is not None:
            outputstr += "\nthenstmt : " + str(self.thenstmt)
        if self.elsestmt is not None:
            outputstr += "\nelsestmt : " + str(self.elsestmt)
        return outputstr

    def printast(self):
        outputstr = "if ("
        outputstr += self.conditionexpr.printast() + ")\n"
        outputstr += self.thenstmt.printast() + "\n"
        if self.elsestmt is not None:
            outputstr += "else\n" + self.elsestmt.printast()
        return outputstr

class VarDeclList(Node):
    def __init__(self):
        self.declarations = []    # This will be list of Declaration object

    def add_decl(self, decl):
        self.declarations.append(decl)

    def __str__(self):
        outputstr = "\n[DecList] : \n"
        if self.declarations is not None:
            outputstr += "Declarations : "
            outputstr += "["
            for element in self.declarations:
                outputstr += str(element) + " "
            outputstr += "]"
        return outputstr

    def printast(self):
        outputstr = ""
        if debugNode:
            outputstr += "[DecList]"
        l = []
        for element in self.declarations:
            l.append(element.printast())
        return outputstr + "\n".join(l)

class Declaration(Node):
    def __init__(self, type, identlist):
        self.type = type
        self.identlist = identlist

    def __str__(self):
        outputstr = "\n[Declaration] : \n"
        if self.type is not None:
            outputstr += "type : " + str(self.type)
        if self.identlist is not None:
            outputstr += "identlist : " + str(self.identlist)
        return outputstr

    def printast(self):
        outputstr = ""
        if debugNode:
            outputstr += "[Declaration]"
        outputstr += self.type.printast().lower() + " "
        outputstr += self.identlist.printast()
        outputstr += ";"
        return outputstr
class IdentList(Node):
    def __init__(self, identifiers):
        self.identifiers = identifiers      # This will be the list of Identifier object

    def add_identifier(self, ident):
        self.identifiers.append(ident)

    def __str__(self):
        outputstr = "\n[IdentList] : \n"
        if self.identifiers is not None:
            outputstr += "identifiers : "
            outputstr += "["
            for element in self.identifiers:
                outputstr += str(element) + " "
            outputstr += "]"
        return outputstr

    def printast(self):
        l = []
        for element in self.identifiers:
            l.append(element.printast())
        return ", ".join(l)


class Identifier(Node):
    def __init__(self, id, intnum=None, idtype="non-array"):
        self.id = id
        self.intnum = intnum
        self.idtype = idtype                # This value is either 'array' or 'non-array'

    def __str__(self):
        outputstr = "\n[Identifier] : \n"
        if self.id is not None:
            outputstr += "id : " + str(self.id) + ","
        return outputstr
    def printast(self):
        return str(self.id)

class Expr(Node):
    def __init__(self, expr_type, operand1=None, operand2=None, operator=None, idval=None, idIDX=None):
        self.expr_type = expr_type
        # This expr_type value is either
        # 'unop', 'binop'
        # 'call', 'intnum', 'floatnum', 'id', 'arrayID'
        self.operator = operator
        # This value can be 'unop',  PLUS, MINUS, TIMES, DIVIDE, ...
        self.idval = idval
        self.idIDX = idIDX
        self.operand1 = operand1
        self.operand2 = operand2

    def __str__(self):
        outputstr = "\n[Expr] : \n"
        if self.expr_type is not None:
            outputstr += "expr_type : " + str(self.expr_type)
        if self.operator is not None:
            outputstr += "\noperator : " + str(self.operator)
        if self.idval is not None:
            outputstr += "\nidval : " + str(self.idval)
        if self.idIDX is not None:
            outputstr += "\nidIDX : " + str(self.idIDX)
        if self.operand1 is not None:
            outputstr += "\noperand1 : " + str(self.operand1)
        if self.operand2 is not None:
            outputstr += "\noperand2 : " + str(self.operand2)
        outputstr += "\n"
        return outputstr

    def printast(self):
        if self.expr_type == "unop":
            return "-"+self.operand1.printast()
        elif self.expr_type == "binop":
            return self.operand1.printast()+str(self.operator)+self.operand2.printast()
        elif self.expr_type == "arrayID":
            return str(self.idval)+"["+self.idIDX.printast()+"]"
        elif self.expr_type == "call":
            return self.operand1.printast()
        elif self.expr_type == "id":
            return str(self.operand1)
        elif self.expr_type == "parenthesis":
            return "("+self.operand1.printast()+")"
        else:  # intnum/floatnum case
            return str(self.operand1)

    def return_type(self):
        if hasattr(self, '_return_type'):
            return self._return_type
        else:
            return None

    def set_return_type(self, return_type):
        setattr(self, '_return_type', return_type)
