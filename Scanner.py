class Scanner(object):
    token_dict = {
        "BEGIN": "beginToken", "END.": "endDotToken", ",": "commaToken", "INTEGER": "idIntToken",
        "BOOLEAN": "idBoolToken", "+": "addToken", "-": "minusToken", "*": "multsteplyToken",
        "STRING": "stringToken", "CHAR": "charToken", "REAL": "realToken", "FLOAT": "floatToken",
        "PROGRAM": "progToken", "WRITELN": "writeLineToken", "READLN": "readLineToken",
        "USES": "useToken", "VAR": "variableToken", "IDENTIFIER": "idenToken", "CASE": "caseToken", "OF": "ofToken",
        "REPEAT": "repeatToken", "OR": "orToken", "NOT": "notToken",
        "=": "equalToToken", "<": "lessThanToken", ">": "greaterThanToken", "<=": "lessOrEqualToken",
        ">=": "greaterOrEqualToken", "DIV": "divFloatToken", "MOD": "modToken", "AND": "andToken",
        "IF": "ifToken", "THEN": "thenToken", "ELSE": "elseToken", "FOR": "forToken", "TO": "toToken", "DO": "doToken",
        "/": "divToken", ";": "semicolonToken", ":": "colonToken",
        "END;": "endToken", "UNTIL": "untilToken", "WHILE": "whileToken", ":=": "assignToken", "(": "leftParenToken",
        ")": "rightParenToken",
    }

    def __init__(self):
        self.row = 1
        self.col = 1
        self.tk = ""
        self.is_comment = False
        self.is_numeric = False
        self.is_real = False
        self.is_string = False
        self.str_content = ""
        self.token_list = []
        self.table_list = []

    def scan_file(self, input):
        output = open(input, "r").readlines()
        for line in output:
            for inputChar in line:
                if self.is_comment:
                    self.get_comment(inputChar)
                    if ord(inputChar) == 10:
                        self.col = 0
                        self.row += 1
                elif self.is_string:
                    self.get_string(inputChar)
                    if ord(inputChar) == 10:
                        self.col = 0
                        self.row += 1
                elif self.is_numeric:
                    self.get_number(inputChar)
                    if ord(inputChar) == 10:
                        self.col = 0
                        self.row += 1
                else:
                    self.get_state(inputChar)
                    if ord(inputChar) == 10:
                        self.col = 0
                        self.row += 1
                self.col += 1
        # self.display()
        return self.token_list

    def display(self):
        print("print scanner result: ")
        for tkn in self.token_list:
            tok = str(tkn[0])
            val = str(tkn[1])
            lin = str(tkn[2])
            print(tok, val, lin)

    def get_string(self, input):
        if ord(input) == 39:
            self.str_content += input
            self.token_list.append(("strTok", self.str_content, self.row, self.col))
            self.table_list.append({"TOKEN": "strTok", "Val": self.str_content, "ROW": self.row, "COL": self.col})
            self.str_content = ""
            self.is_string = False
            return
        else:
            self.str_content += input

    def get_number(self, input):
        if input.isdigit():
            self.str_content += input

        if ord(input) > 57 or ord(input) <= 41:
            self.is_numeric = False
            if self.is_real:
                self.token_list.append(("realTok", self.str_content, self.row, self.col - 1))
                self.table_list.append({"TOKEN": "realTok", "Val": self.str_content, "ROW": self.row, "COL": self.col - 1})
                self.is_real = False
            else:
                self.token_list.append(("intTok", self.str_content, self.row, self.col - 1))
                self.table_list.append({"TOKEN": "intTok", "Val": self.str_content, "ROW": self.row, "COL": self.col - 1})

            if input in self.token_dict:
                if self.tk:
                    self.tk = ""
                self.token_list.append((self.token_dict[input], input, self.row, self.col))
                self.table_list.append(
                    {"TOKEN": self.token_dict[input], "Val": input, "ROW": self.row, "COL": self.col})

            self.str_content = ""
            return

        if ord(input) == 46:
            self.is_real = True
            self.str_content += input
            return

    def get_state(self, input):
        if ord(input) <= 32:
            if self.tk:
                if self.str_content.upper() in self.token_dict:
                    self.token_list.append(
                        (self.token_dict[self.str_content.upper()], self.str_content, self.row, self.col - 1))
                    self.table_list.append(
                        {"TOKEN": self.token_dict[self.str_content.upper()], "Val": self.str_content, "ROW": self.row,
                         "COL": self.col - 1})
                    self.tk = ""
                    self.str_content = ""
                    return
                else:
                    self.token_list.append((self.token_dict[self.tk], self.str_content, self.row, self.col - 1))
                    self.table_list.append(
                        {"TOKEN": self.token_dict[self.tk], "Val": self.str_content, "ROW": self.row, "COL": self.col - 1})
                    self.tk = ""
                    self.str_content = ""
                    return

            else:
                return

        if ord(input) == 39:
            self.str_content = ""
            self.is_string = True
            self.str_content += input
            return

        if input.isdigit():
            self.is_numeric = True
            self.str_content += input
            return

        if ord(input) == 46:
            if self.tk:
                self.str_content += input
                self.token_list.append((self.token_dict[self.str_content.upper()], self.str_content, self.row, self.col))
                self.table_list.append(
                    {"TOKEN": self.token_dict[self.str_content.upper()], "Val": self.str_content, "ROW": self.row,
                     "COL": self.col})
                self.str_content = ""
                self.tk = ""
                return

        if ord(input) == 59 and not self.is_numeric:
            if not self.tk:
                if self.str_content:
                    self.token_list.append((self.token_dict["IDENTIFIER"], self.str_content, self.row, self.col - 1))
                    self.table_list.append({"TOKEN": self.token_dict["IDENTIFIER"], "Val": self.str_content, "ROW": self.row,
                                          "COL": self.col - 1})
            else:
                if self.str_content.upper() == "END":
                    self.str_content += input
                    self.token_list.append(
                        (self.token_dict[self.str_content.upper()], self.str_content, self.row, self.col - 1))
                    self.table_list.append(
                        {"TOKEN": self.token_dict[self.str_content.upper()], "Val": self.str_content, "ROW": self.row,
                         "COL": self.col - 1})
                else:
                    self.token_list.append(
                        (self.token_dict[self.tk.upper()], self.str_content, self.row, self.col - 1))
                    self.table_list.append(
                        {"TOKEN": self.token_dict[self.tk.upper()], "Val": self.str_content, "ROW": self.row,
                         "COL": self.col - 1})
            if self.str_content.upper() != "END;":
                self.token_list.append((self.token_dict[input], input, self.row, self.col))
                self.table_list.append(
                    {"TOKEN": self.token_dict[input], "Val": input, "ROW": self.row, "COL": self.col})
            self.str_content = ""
            self.tk = ""
            return

        if ord(input) == 58:
            if self.str_content:
                self.token_list.append((self.token_dict["IDENTIFIER"], self.str_content, self.row, self.col - 2))
                self.table_list.append(
                    {"TOKEN": self.token_dict["IDENTIFIER"], "Val": self.str_content, "ROW": self.row, "COL": self.col - 2})
            self.str_content = input
            self.tk = input
            return

        if ord(input) == 61:
            if not self.tk:
                if self.str_content != "":
                    self.token_list.append((self.token_dict["IDENTIFIER"], self.str_content, self.row, self.col))
                    self.table_list.append(
                        {"TOKEN": self.token_dict["IDENTIFIER"], "Val": self.str_content, "ROW": self.row, "COL": self.col})
                self.token_list.append((self.token_dict["="], "=", self.row, self.col))
                self.table_list.append({"TOKEN": self.token_dict["="], "Val": "=", "ROW": self.row, "COL": self.col})
                self.str_content = ""
                return
            if self.tk:
                self.str_content += input
                if self.str_content in self.token_dict:
                    self.token_list.append((self.token_dict[self.str_content], self.str_content, self.row, self.col))
                    self.table_list.append(
                        {"TOKEN": self.token_dict[self.str_content], "Val": self.str_content, "ROW": self.row, "COL": self.col})
                    self.str_content = ""
                    self.tk = ""
                    return

        if ord(input) == 43 or ord(input) == 45:
            self.token_list.append((self.token_dict[input], input, self.row, self.col - 1))
            self.table_list.append(
                {"TOKEN": self.token_dict[input], "Val": input, "ROW": self.row, "COL": self.col - 1})
            self.str_content = ""
            return

        if ord(input) == 40:
            if self.str_content:
                self.token_list.append(
                    (self.token_dict[self.str_content.upper()], self.str_content, self.row, self.col - 1))
                self.table_list.append(
                    {"TOKEN": self.token_dict[self.str_content.upper()], "Val": self.str_content, "ROW": self.row,
                     "COL": self.col - 1})
                self.token_list.append((self.token_dict[input], input, self.row, self.col))
                self.table_list.append(
                    {"TOKEN": self.token_dict[input], "Val": input, "ROW": self.row, "COL": self.col})
                self.str_content = ""
                self.tk = input
                return

        if ord(input) == 41:
            if self.tk:
                if self.str_content:
                    self.token_list.append((self.token_dict["IDENTIFIER"], self.str_content, self.row, self.col - 1))
                    self.table_list.append({"TOKEN": self.token_dict["IDENTIFIER"], "Val": self.str_content, "ROW": self.row,
                                          "COL": self.col - 1})
                self.token_list.append((self.token_dict[input], input, self.row, self.col))
                self.table_list.append(
                    {"TOKEN": self.token_dict[input], "Val": input, "ROW": self.row, "COL": self.col})
            self.str_content = ""
            self.tk = ""
            return

        if ord(input) == 42:
            if self.tk:
                self.is_comment = True
                self.str_content += input
                return

        if ord(input) == 44:
            if self.str_content:
                self.token_list.append((self.token_dict["IDENTIFIER"], self.str_content, self.row, self.col - 1))
                self.table_list.append(
                    {"TOKEN": self.token_dict["IDENTIFIER"], "Val": self.str_content, "ROW": self.row, "COL": self.col - 1})
                self.token_list.append((self.token_dict[input], input, self.row, self.col))
                self.table_list.append(
                    {"TOKEN": self.token_dict[input], "Val": input, "ROW": self.row, "COL": self.col})
                self.str_content = ""
                self.tk = ""
                return

        if ord(input) == 60 or ord(input) == 62:
            self.str_content = input
            self.tk = input
            return

        self.str_content += input

        if self.str_content.upper() != "END":
            if self.str_content.upper() not in self.token_dict:
                self.tk = "IDENTIFIER"
                return
            if self.str_content.upper() in self.token_dict:
                self.tk = self.str_content
                return

    def get_comment(self, input):
        if ord(input) == 41:
            if self.tk:
                self.str_content += input
                self.token_list.append(("commTok", self.str_content, self.row, self.col))
                self.table_list.append({"TOKEN": "commTok", "Val": self.str_content, "ROW": self.row, "COL": self.col})
                self.is_comment = False
                self.tk = ""
                self.str_content = ""
                return
        else:
            self.str_content += input


