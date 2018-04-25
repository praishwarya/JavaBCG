import sys
class ThreeAddressCode:

    def __init__(self):
        self.lNo = -1
        self.code = []
    
    def newLabel(self):
        self.lNo += 1
        return "l" + str(self.lNo)

    def output(self):
        for i in self.code:
            print(i)

    def emit(self,des, src1, src2, op):
        self.code.append([des,src1,src2,op])

    def error(self,error):
        self.output3AC()
        # print(error)
        sys.stderr.write(error+"\n")
        sys.exit(127)

    def output3AC(self):
        count =0
        for i in self.code:
            count+=1
            if(i[0]=='ifgoto'):
                x = i[2].split(' ')
                print(str(count)+", "+i[0]+", "+x[0]+", "+i[1]+", "+x[1]+", "+i[3])
            elif(i[0]=='goto' or i[0]=='call'):
                print(str(count)+", "+i[0]+", "+i[1])
            elif(i[0]=='iffalse'):
                print(str(count)+", iffalse " + i[1] + " goto " + i[2])
            elif(i[0]=='label'):
                print(str(count)+", label, "+i[1])
            elif(i[0]=='input'):
                print(str(count)+", "+i[0]+", "+i[1])
            elif(i[0]=='func'):
                if(len(i[2])==2):
                    print(str(count)+", func, "+i[1])
                else:
                    l = len(i[2])
                    f = i[2][1]+'_'+i[2][2][0]
                    for j in range(3,l):
                        f = f+", "+i[2][1]+'_'+i[2][j][0]
                    # print(f)
                    print(str(count)+", func, "+i[1]+", "+f)
                    # print(i[2])
            elif(i[0]=='declare'):
                print(str(count)+", declare" +", "+i[1]+", "+i[2])
            elif(i[0]=='print'):
                print(str(count)+", print, " + i[1])
            elif(i[0]=='printf'):
                l = len(i[1])
                f = i[1][0]
                for j in range(1,l):
                    f = f + ", " + i[1][j]
                print(str(count)+", print, "+f)
            elif(i[0]=='push' or i[0]=='pop'):
                print(str(count)+", "+i[0]+", "+i[1])
            elif(i[0]=='error'):
                print(i[1] + " = "+ i[2])
                sys.exit(0)
            elif(i[0]=='ret'):
                if(i[1]==''):
                    print(str(count)+", ret")
                else:
                    print(str(count)+", ret, "+i[1])
            else:
                if(i[3]=='='):
                    print(str(count)+", "+i[3]+", "+i[0]+", "+i[1])
                else:
                    print(str(count)+", "+i[3]+", "+i[0]+", "+i[1]+", "+i[2])