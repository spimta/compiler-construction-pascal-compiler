class Parser(object):
    def __init__(self, tokList, tk):
        self.tokList = tokList
        self.tk = tk
        self.tok_iter = iter(self.tokList)
        self.opcode_list = []
        self.nodes = []
        self.symbol_table = []
        self.step = 0
        self.op = False
        self.addr = 0
        self.LHS = ""
        self.RHS = ""
        self.tmp = False
        self.switchOn = False
        self.hSwitch = 0

    def run(self):
        self.next_token()
        self.start_parse()
        # self.display()
        return {"symbol_table": self.symbol_table, "opcode_list": self.opcode_list}

    def display(self):
        print("")
        print("OP_CODE")

        for tkn in self.opcode_list:
            print(str(tkn["instruction"]), str(tkn["val"]))

        print("\nSymbol Table")

        for tkn in self.symbol_table:
            print(str(tkn["Name"]), str(tkn["Val"]), str(tkn["Type"]), tkn["Addr"])

    def next_token(self):
        self.tk = next(self.tok_iter)

    def declarations(self):
        self.initial_vars()

    def wrong_token(self, tkn):
        print("Wrong token")

    def start_parse(self):
        if self.tk[0] == "progToken":
            self.match("progToken")
            self.declarations()
            self.match_begin()
            if self.tk[0] == "endToken":
                self.match("endToken")
                if self.tk[0] == "endDotToken":
                    self.opcode_list.append({"instruction": "done", "step": self.step, "val": self.tk[1]})
            else:
                self.opcode_list.append({"instruction": "done", "step": self.step, "val": self.tk[1]})

    def initial_vars(self):
        if self.tk[0] == "variableToken":
            self.match("variableToken")
        else:
            self.match_begin()
            return

        while (True):
            if self.tk[0] == "idenToken":
                self.symbol_table.append({"Name": self.tk[1], "Addr": self.addr, "Type": "none", "Val": 0})
                self.match("idenToken")
                self.addr += 4
            elif self.tk[0] == "commaToken":
                self.match("commaToken")
            elif self.tk[0] == "colonToken":
                self.match("colonToken")
                break
            else:
                break

        if self.tk[0] == "idIntToken":
            for sym in self.symbol_table:
                if sym["Type"] == "none":
                    sym["Type"] = "int"
            self.match("idIntToken")

        if self.tk[0] == "stringToken":
            for sym in self.symbol_table:
                if sym["Type"] == "none":
                    sym["Type"] = "str"
            self.match("stringToken")

        if self.tk[0] == "charToken":
            for sym in self.symbol_table:
                if sym["Type"] == "none":
                    sym["Type"] = "char"
            self.match("charToken")

        if self.tk[0] == "realToken":
            for sym in self.symbol_table:
                if sym["Type"] == "none":
                    sym["Type"] = "real"
            self.match("realToken")

        if self.tk[0] == "idBoolToken":
            for sym in self.symbol_table:
                if sym["Type"] == "none":
                    sym["Type"] = "bool"
            self.match("idBoolToken")

        if self.tk[0] == "semicolonToken":
            self.match("semicolonToken")

        self.initial_vars()

    def exprn(self):
        self.trm()
        self.prime_exprn()

    def match_begin(self):
        if self.tk[0] == "beginToken":
            self.match("beginToken")
        self.token_matching()

    def token_matching(self):
        while (1):
            if self.tk[0] == "idenToken":
                self.LHS = self.tk
                self.match("idenToken")
                self.exprn()

            if self.tk[0] == "forToken":
                self.for_loop()

            if self.tk[0] == "caseToken":
                self.switch_stmnt()

            if self.tk[0] == "repeatToken":
                self.repeat_loop()

            if self.tk[0] == "whileToken":
                self.while_loop()

            if self.tk[0] == "writeLineToken":
                self.keyword_write()

            if self.tk[0] == "ifToken":
                self.if_stmnt()

            if self.tk[0] == "assignToken":
                self.match("assignToken")
                self.exprn()
                self.op = True

            if self.tk[0] == "semicolonToken":
                self.match("semicolonToken")
                if self.op:
                    self.opcode_list.append({"instruction": "pop", "val": self.LHS[1], "step": self.step})
                    self.step += 1
                    self.op = False
                if self.switchOn:
                    break
                else:
                    self.initial_vars()

            if self.tk[0] == "untilToken" or self.tk[0] == "toToken":
                return

            if self.tk[0] == "elseToken":
                return

            if self.tk[0] == "endDotToken" or self.tk[0] == "endToken":
                break

    def cmp_signs(self):
        if self.tk[0] == "equalToToken":
            self.match("equalToToken")
            self.exprn()
            self.after_modify("equalToToken")
        elif self.tk[0] == "greaterThanToken":
            self.match("greaterThanToken")
            self.exprn()
            self.after_modify("greaterThanToken")
        elif self.tk[0] == "lessOrEqualToken":
            self.match("lessOrEqualToken")
            self.exprn()
            self.after_modify("lessOrEqualToken")
        elif self.tk[0] == "greaterOrEqualToken":
            self.match("greaterOrEqualToken")
            self.exprn()
            self.after_modify("greaterOrEqualToken")
        else:
            self.exprn()

    def switch_stmnt(self):
        self.switchOn = True
        self.match("caseToken")
        self.match("leftParenToken")
        target = self.tk
        self.exprn()
        self.match("rightParenToken")
        self.match("ofToken")
        self.run_parse(target)
        self.token_matching()

    def run_parse(self, target):
        # print("run Parse Statement")
        while (True):
            # print(str(target) + "  " + str(self.tk))
            self.hSwitch = self.step
            # print("switchhole " + str(self.hSwitch))
            self.label_parse(target)
            if self.tk[0] == "endToken":
                self.match("endToken")
                break

        for sym in self.opcode_list:
            if sym["instruction"] == "jump":
                if sym["val"] == 0:
                    sym["val"] = self.step

    def label_parse(self, target):
        # print("self.step" + str(self.step))
        if self.tk[0] == "strTok":
            if not self.tmp:
                self.opcode_list.append({"instruction": "push", "val": self.tk[1], "type": self.tk[0], "step": self.step})
                self.step += 1
                self.tmp = True
            else:
                self.opcode_list.append({"instruction": "push", "val": target[1], "type": target[0], "step": self.step})
                self.step += 1
                self.opcode_list.append({"instruction": "push", "val": self.tk[1], "type": self.tk[0], "step": self.step})
                self.step += 1
            self.opcode_list.append({"instruction": "equals", "val": "equals", "type": self.tk[0], "step": self.step})
            self.step += 1
            self.opcode_list.append({"instruction": "yesJmp", "val": self.step + 2, "step": self.step})
            self.step += 1
            self.opcode_list.append({"instruction": "jump", "val": self.step + 4, "step": self.step})
            self.step += 1
            self.match("strTok")
        elif self.tk[0] == "commaToken":
            self.match("commaToken")
            self.opcode_list[self.step - 1]["val"] = self.step
        elif self.tk[0] == "colonToken":
            self.match("colonToken")
            self.token_matching()
            self.opcode_list.append({"instruction": "jump", "val": 0, "step": self.step})
            self.step += 1

    def trm(self):
        self.fact_keyword()
        self.prime_trm()

    def if_stmnt(self):
        self.match("ifToken")
        self.match("leftParenToken")
        self.exprn()
        self.cmp_signs()
        self.match("rightParenToken")
        self.match("thenToken")
        hole1 = self.step
        self.opcode_list.append({"instruction": "notJmp", "step": self.step, "val": self.step})
        self.step += 1
        self.token_matching()

        if self.tk[0] == "elseToken":
            self.match("elseToken")
            hole2 = self.step
            self.opcode_list.append({"instruction": "jump", "step": self.step, "val": 0})
            self.step += 1
            self.opcode_list[hole1]["val"] = self.step
            self.token_matching()
            self.opcode_list[hole2]["val"] = self.step

    def for_loop(self):
        self.match("forToken")
        for sym in self.symbol_table:
            if self.tk[1] == sym["Name"]:
                loop_variable = self.tk
                break
        self.match("idenToken")
        self.match("assignToken")
        self.opcode_list.append({"instruction": "push", "val": self.tk[1], "type": self.tk[0], "step": self.step})
        self.step += 1
        self.opcode_list.append({"instruction": "pop", "val": loop_variable[1], "type": loop_variable[0], "step": self.step})
        self.step += 1
        target = self.step
        self.opcode_list.append(
            {"instruction": "push", "val": loop_variable[1], "type": loop_variable[0], "step": self.step})
        self.step += 1
        self.match("intTok")
        self.match("toToken")
        self.opcode_list.append({"instruction": "push", "val": self.tk[1], "type": self.tk[0], "step": self.step})
        self.step += 1
        self.match("intTok")
        self.match("doToken")
        self.opcode_list.append({"instruction": "greater", "val": "greater", "type": loop_variable[0], "step": self.step})
        self.step += 1
        hole = self.step
        self.opcode_list.append({"instruction": "yesJmp", "val": self.step, "step": hole})
        self.step += 1
        self.match("beginToken")
        self.token_matching()
        self.opcode_list.append(
            {"instruction": "push", "val": loop_variable[1], "type": loop_variable[0], "step": self.step})
        self.step += 1
        self.opcode_list.append({"instruction": "push", "val": 1, "type": "intTok", "step": self.step})
        self.step += 1
        self.opcode_list.append({"instruction": "add", "val": "+", "step": self.step})
        self.step += 1
        self.opcode_list.append({"instruction": "pop", "val": loop_variable[1], "type": loop_variable[0], "step": self.step})
        self.step += 1
        self.opcode_list.append({"instruction": "jump", "val": target, "step": self.step})
        self.step += 1
        self.opcode_list[hole]["val"] = self.step

    def repeat_loop(self):
        target = self.step
        self.match("repeatToken")
        self.token_matching()
        self.match("untilToken")
        self.exprn()
        self.cmp_signs()
        self.opcode_list.append({"instruction": "notJmp", "step": self.step, "val": target})
        self.step += 1

    def match(self, tkn):
        if (self.tk[0] == tkn):
            if (self.tk[1] == ")" or self.tk[1] == "("):
                pass
            else:
                self.nodes.append(self.tk[1])
            self.next_token()
            return True

    def while_loop(self):
        self.match("whileToken")
        target = self.step
        self.cmp_signs()
        self.match("doToken")
        self.opcode_list.append({"instruction": "notJmp", "step": self.step, "val": target})
        hole = self.step
        self.step += 1
        self.match_begin()
        self.opcode_list.append({"instruction": "jump", "step": self.step, "val": target})
        self.step += 1
        self.opcode_list[hole]["val"] = self.step

    def after_modify(self, tkn):
        if tkn == "addToken":
            self.opcode_list.append({"instruction": "add", "val": "+", "type": tkn, "step": self.step})
        elif tkn == "minusToken":
            self.opcode_list.append({"instruction": "subtract", "val": "-", "type": tkn, "step": self.step})
        elif tkn == "multsteplyToken":
            self.opcode_list.append({"instruction": "multiply", "val": "*", "type": tkn, "step": self.step})
        elif tkn == "divToken":
            self.opcode_list.append({"instruction": "divide", "val": "/", "type": tkn, "step": self.step})
        elif tkn == "modToken":
            self.opcode_list.append({"instruction": "modulus", "val": "modulus", "type": tkn, "step": self.step})
        elif tkn == "equalToToken":
            self.opcode_list.append({"instruction": "equals", "val": "equals", "type": tkn, "step": self.step})
        elif tkn == "lessThanToken":
            self.opcode_list.append({"instruction": "less", "val": "less", "type": tkn, "step": self.step})
        elif tkn == "greaterThanToken":
            self.opcode_list.append({"instruction": "greater", "val": "greater", "type": tkn, "step": self.step})
        elif tkn == "greaterOrEqualToken":
            self.opcode_list.append({"instruction": "gtr_equal", "val": "gtr_equal", "type": tkn, "step": self.step})
        elif tkn == "lessOrEqualToken":
            self.opcode_list.append({"instruction": "lss_equal", "val": "lss_eq", "type": tkn, "step": self.step})
        elif tkn[0] == "idenToken":
            self.opcode_list.append({"instruction": "push", "val": self.tk[1], "type": self.tk[0], "step": self.step})
        elif tkn[0] == "strTok":
            self.opcode_list.append({"instruction": "push", "val": self.tk[1], "type": self.tk[0], "step": self.step})
        elif tkn[0] == "intTok":
            self.opcode_list.append({"instruction": "push", "val": self.tk[1], "type": self.tk[0], "step": self.step})
        elif tkn[0] == "realTok":
            self.opcode_list.append({"instruction": "push", "val": self.tk[1], "type": self.tk[0], "step": self.step})
        elif tkn == "writeLineToken":
            self.opcode_list.append({"instruction": "lineWrite", "val": "lineWrite", "type": tkn, "step": self.step})
        else:
            pass
        self.step += 1

    def keyword_write(self):
        if self.tk[0] == "writeLineToken":
            self.match("writeLineToken")
            self.match("leftParenToken")
            self.exprn()
            self.match("rightParenToken")
            self.after_modify("writeLineToken")

    def prime_exprn(self):
        if self.tk[0] == "addToken":
            self.match("addToken")
            self.trm()
            self.after_modify("addToken")
            self.prime_exprn()
        elif self.tk[0] == "minusToken":
            self.match("minusToken")
            self.trm()
            self.after_modify("minusToken")
            self.prime_exprn()
        else:
            pass

    def prime_trm(self):
        if self.tk[0] == "multsteplyToken":
            self.match("multsteplyToken")
            self.fact_keyword()
            self.after_modify("multsteplyToken")
            self.prime_trm()
        elif self.tk[0] == "divToken":
            self.match("divToken")
            self.fact_keyword()
            self.after_modify("divToken")
            self.prime_trm()
        elif self.tk[0] == "modToken":
            self.match("modToken")
            self.fact_keyword()
            self.after_modify("modToken")
            self.prime_trm()
        elif self.tk[0] == "equalToToken":
            self.match("equalToToken")
            self.exprn()
            self.after_modify("equalToToken")
        elif self.tk[0] == "lessThanToken":
            self.match("lessThanToken")
            self.exprn()
            self.after_modify("lessThanToken")
        else:
            pass

    def fact_keyword(self):
        if self.tk[0] == "idenToken":
            self.after_modify(self.tk)
            self.match("idenToken")
            return

        if self.tk[0] == "strTok":
            self.after_modify(self.tk)
            self.match("strTok")
            return

        if self.tk[0] == "intTok":
            self.after_modify(self.tk)
            self.match("intTok")
            return

        if self.tk[0] == "realTok":
            self.after_modify(self.tk)
            self.match("realTok")
            return

        if self.tk[0] == "notToken":
            self.match("notToken")
            self.fact_keyword()
            self.after_modify(self.tk)
            self.opcode_list.append({"instruction": "not", "val": "not", "type": "notToken"})
            return