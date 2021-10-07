import sys


class StackMachine(object):
    def __init__(self, symbol_table, opcode_list):
        self.symbol_table = symbol_table
        self.opcode_list = opcode_list
        self.stack = []
        self.step = 0

    def run(self):
        # print("Stack Machine")

        while (1):
            # print(self.stack)
            # print("Step Processing: " + str(self.opcode_list[self.step]["instruction"]) + " " + str(self.opcode_list[self.step]["val"]))
            if self.opcode_list[self.step]["instruction"] == "push":
                if self.opcode_list[self.step]["type"] == "idenToken":
                    # print(self.opcode_list[self.step]["val"])
                    self.valPush(self.opcode_list[self.step]["val"])
                else:
                    self.push(self.opcode_list[self.step]["val"])
            elif self.opcode_list[self.step]["instruction"] == "pop":
                self.pop(self.opcode_list[self.step]["val"])
            elif self.opcode_list[self.step]["instruction"] == "add":
                self.add()
            elif self.opcode_list[self.step]["instruction"] == "subtract":
                self.subtract()
            elif self.opcode_list[self.step]["instruction"] == "multiply":
                self.multiply()
            elif self.opcode_list[self.step]["instruction"] == "divide":
                self.divide()
            elif self.opcode_list[self.step]["instruction"] == "less":
                self.less()
            elif self.opcode_list[self.step]["instruction"] == "greater":
                self.greater()
            elif self.opcode_list[self.step]["instruction"] == "equals":
                self.equals()
            elif self.opcode_list[self.step]["instruction"] == "modulus":
                self.modulus()
            elif self.opcode_list[self.step]["instruction"] == "done":
                self.done()
            elif self.opcode_list[self.step]["instruction"] == "jump":
                self.jump(self.opcode_list[self.step]["val"])
            elif self.opcode_list[self.step]["instruction"] == "notJmp":
                self.notJmp(self.opcode_list[self.step]["val"])
            elif self.opcode_list[self.step]["instruction"] == "yesJmp":
                self.yesJmp(self.opcode_list[self.step]["val"])
            elif self.opcode_list[self.step]["instruction"] == "lineWrite":
                # print(self.opcode_list[self.step + 1])
                self.lineWrite()
            self.step += 1
            # print("Stack: " + str(self.stack))

    def done(self):
        # self.display()
        sys.exit(0)

    def jump(self, val):
        self.step = val - 1

    def notJmp(self, val):
        val1 = self.stack.pop()
        if val1 == False:
            self.step = val - 1

    def yesJmp(self, val):
        val1 = self.stack.pop()
        if val1 == True:
            self.step = val - 1

    def lineWrite(self):
        val1 = self.stack.pop()
        print(val1)

    def display(self):
        print("Stack machine")
        for tkn in self.symbol_table:
            print(str(tkn["Name"]), str(tkn["Val"]), str(tkn["Type"]), tkn["Addr"])

    def pop(self, val):
        val1 = self.stack.pop()
        for sym in self.symbol_table:
            if val == sym["Name"]:
                # print(val)
                sym["Val"] = val1

    def push(self, val):
        self.stack.insert(0, val)

    def valPush(self, val):
        for sym in self.symbol_table:
            if val == sym["Name"]:
                self.stack.insert(0, sym["Val"])

    def add(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()

        tmp1 = str(val1)
        tmp2 = str(val2)

        if tmp1.isnumeric() and tmp2.isnumeric():
            tkn = int(val1) + int(val2)
        else:
            tkn = float(val1) + float(val2)
        self.push(tkn)

    def multiply(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tmp1 = str(val1)
        tmp2 = str(val2)

        if tmp1.isnumeric() and tmp2.isnumeric():
            tkn = int(val1) * int(val2)
        else:
            tkn = float(val1) * float(val2)
        self.push(tkn)

    def divide(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tmp1 = str(val1)
        tmp2 = str(val2)

        if tmp1.isnumeric() and tmp2.isnumeric():
            tkn = int(val1) / int(val2)
        else:
            tkn = float(val1)/float(val2)
        self.push(tkn)

    def subtract(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tmp1 = str(val1)
        tmp2 = str(val2)

        if tmp1.isnumeric() and tmp2.isnumeric():
            tkn = int(val1) - int(val2)
        else:
            tkn = float(val1) - float(val2)
        self.push(tkn)

    def modulus(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = int(val1) % int(val2)
        self.push(tkn)

    def less(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = float(val1) < float(val2)
        self.push(tkn)

    def greater(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = float(val1) > float(val2)
        self.push(tkn)

    def equals(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        # print(type(val1))
        if type(val1) is int:
            tkn = (int(val1) == int(val2))
        if type(val1) is str:
            tkn = val1 == val2
        if type(val1) is float:
            tkn = (float(val1) == float(val2))
        self.push(tkn)