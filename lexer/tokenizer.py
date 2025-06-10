# lexer.py
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        palavras_reservadas = ["printlog","BREAK", "if","sqrt", "sin","cos","tan","log","exp","pow","pi","while", "scanf", "else", "int", "str","float", "bool", "STOP", "name", "id", "station", "speed", "region", "rotation", "START","FINISH"]

        while (self.position < len(self.source)) and (self.source[self.position] == " " or self.source[self.position] == "\n"):
            self.position += 1

        value = ""
        type = ""

        if len(self.source) > self.position:
            if self.source[self.position] == '"':
                self.position += 1
                start_pos = self.position
                while self.position < len(self.source) and self.source[self.position] != '"':
                    self.position += 1
                if self.position >= len(self.source):
                    raise Exception("String not closed")
                value = self.source[start_pos:self.position]
                self.position += 1
                type = "STRING"

            elif self.source[self.position].isalpha():
                value += self.source[self.position]
                self.position += 1
                while (len(self.source) > self.position) and (self.source[self.position].isalnum()) or (self.source[self.position] == "_"):
                    value += self.source[self.position]
                    self.position += 1

                if value in palavras_reservadas:
                    type = value
                else:
                    type = "ID"

            elif self.source[self.position].isdigit():
                type = "INT"
                while len(self.source) > self.position and self.source[self.position].isdigit():
                    value += self.source[self.position]
                    self.position += 1
                if self.position < len(self.source) and self.source[self.position] == '.':
                    value += self.source[self.position]
                    type = 'FLOAT'
                    self.position += 1
                    while len(self.source) > self.position and self.source[self.position].isdigit():
                        value += self.source[self.position]
                        self.position += 1
                    value = float(value)
                else:
                    type = 'INT'
                    value = int(value)

            elif self.source[self.position] == "+":
                type = "PLUS"
                self.position += 1

            elif self.source[self.position] == "-":
                type = "MINUS"
                self.position += 1

            elif self.source[self.position] == "*":
                type = "MULT"
                self.position += 1

            elif self.source[self.position] == "/":
                type = "DIV"
                self.position += 1

            elif self.source[self.position] == "(":
                type = "LP"
                self.position += 1

            elif self.source[self.position] == ")":
                type = "RP"
                self.position += 1

            elif self.source[self.position] == "{":
                type = "LCB"
                self.position += 1

            elif self.source[self.position] == "}":
                type = "RCB"
                self.position += 1

            elif self.source[self.position] == "=":
                type = "ASSIGNMENT"
                self.position += 1
                if self.source[self.position] == "=":
                    type = "EQUAL"
                    self.position += 1
                elif self.source[self.position] == ">":
                    type = "ARROW"
                    self.position += 1

            elif self.source[self.position] == ";":
                type = "SC"
                self.position += 1

            elif self.source[self.position] == ":":
                type = "C"
                self.position += 1

            elif self.source[self.position] == ">":
                type = "GT"
                self.position += 1

            elif self.source[self.position] == "<":
                type = "LT"
                self.position += 1

            elif self.source[self.position] == ',':
                type = "COMMA"
                self.position += 1

            elif self.source[self.position] == "|":
                self.position += 1
                if self.source[self.position] == "|":
                    type = "OR"
                    self.position += 1
                else:
                    raise Exception("símbolo inválido faltou mais um '|'")

            elif self.source[self.position] == "&":
                self.position += 1
                if self.source[self.position] == "&":
                    type = "AND"
                    self.position += 1
                else:
                    raise Exception("símbolo inválido faltou mais um '&'")

            elif self.source[self.position] == "!":
                type = "NOT"
                self.position += 1

            else:
                raise Exception("símbolo inválido")

            self.next = Token(type, value)

        else:
            type = "EOF"
            self.next = Token(type, value)
            self.position += 1