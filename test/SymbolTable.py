import sys
class SymbolTable:

    def __init__(self):
        self.SymbolTable = {
                'start' : {
                    'name' : 'start',
                    'variables' : {},
                    'function' : {},
                    'type' : 'start',
                    'parent' : None,
                    }
                }
        self.currScope = 'start'
        self.tNo = -1
        self.scopeNo = -1

    def variableAdd(self, idVal, place, idType,idDimension=[]):
        idSize = 4
        scope = self.getScope(idVal)
        if scope != self.currScope:
            sc = str(self.currScope)+'_'+place
            self.SymbolTable[self.currScope]['variables'][idVal] = {
                    'place' : sc,
                    'type' : idType,
                    'size' : idSize,
                    'dimension' : idDimension
                    }
        else:
            sys.exit('Variable '+idVal+" is already initialised in this scope")
        # print(self.SymbolTable[self.currScope]['variables'])


    def variableSearch(self, idVal):
        scope = self.getScope(idVal)
        # print(scope)
        if(scope == None):
            return False
        else:
            return scope

    def functionAdd(self, func):
        # this is added to handle parameterised function
        self.SymbolTable[func] = {
                'name' : func,
                'type' : 'function',
                'variables' : {},
                'function' : {},
                'rType' : 'UNDEFINED_TYPE',
                'parent' : self.currScope,
                # 'arguments' : []                  need when i am doing function overloading 
                }

        self.SymbolTable[self.currScope]['function'][func] = {
                'fName' : func
                }
        self.currScope = func

    def newScope(self):
        scope = self.newScopeName()
        self.SymbolTable[scope] = {
                'name' : scope,
                'type' : 'block',
                'variables' : {},
                'function' : {},
                'type' : 'scope',
                'parent' : self.currScope,
                }
        self.currScope = scope

    def endScope(self):
        self.currScope = self.SymbolTable[self.currScope]['parent']
    def endFunction(self):
        self.currScope = self.SymbolTable[self.currScope]['parent']


    def retScope(self):
        return self.currScope


    def getScopeType(self, scope):
        return self.SymbolTable[scope]['type']

    def setRType(self, dataType):
        self.SymbolTable[self.currScope]['rType'] = dataType

    def getRType(self, scope):
        return self.SymbolTable[scope]['rType']

    def getFunction(self):
        scope = self.currScope
        while self.SymbolTable[scope]['type'] not in ['function']:
            scope = self.SymbolTable[scope]['parent']
        return self.SymbolTable[scope]['name']

    def variableSave(self,scope):
        lis = []
        while(self.SymbolTable[scope]['type'] not in  ['function']):
            h = self.getScopeVariables(scope)
            lis = lis +h
            scope = self.SymbolTable[scope]['parent']

        h = self.getScopeVariables(scope)
        lis = lis +h
        return lis

    def getScopeVariables(self, scope):
        l = self.SymbolTable[scope]['variables']
        lis = []
        for i in l:
            if(i not in ['in']):
                lis.append(l[i]['place'])
            # print(l[i]['place'])
        return lis


    def getData(self, idVal, search):
        scope = self.getScope(idVal)
        if scope != None:
            return  self.SymbolTable[scope]['variables'][idVal].get(search)
        else:
            return None

    def setDimension(self, idVal, NewDimension):
        scope = self.getScope(idVal)
        # print(scope)
        if scope != None:
            self.SymbolTable[scope]['variables'][idVal]['dimension'] = NewDimension
            return
        else:
            return None

    

    def getScope(self, idVal):
        scope = self.currScope
        while self.SymbolTable[scope]['type'] not in ['start']:
            if idVal in self.SymbolTable[scope]['variables']:
                return scope
            scope = self.SymbolTable[scope]['parent']
        if idVal in self.SymbolTable[scope]['variables']:
            return scope
        return None

    def getTemp(self):
        self.tNo += 1
        newTemp = "t"+str(self.tNo)
        self.variableAdd(newTemp,newTemp,'INT')
        return self.currScope+'_'+newTemp

    def newScopeName(self):
        self.scopeNo += 1
        newScope = "s"+str(self.scopeNo) 
        return newScope

    def printTable(self):
        print(self.SymbolTable)