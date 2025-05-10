import sys
import math


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

                # verifica palavras reservadas ao invés de strings
                if value in palavras_reservadas:
                    type = value  # os types serão: printlog, if, while, scanf, else, int, str, bool

                else:
                    type = "ID"

            elif self.source[self.position].isdigit():
                type = "INT"  # se começar com número é um int
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
                type = "LCB"  # left curly bracket
                self.position += 1

            elif self.source[self.position] == "}":
                type = "RCB"  # right curly bracket
                self.position += 1

            elif self.source[self.position] == "=":
                type = "ASSIGNMENT"  # identificator
                self.position += 1
                if self.source[self.position] == "=":
                    type = "EQUAL"
                    self.position += 1
                elif self.source[self.position] == ">":
                    type = "ARROW"
                    self.position += 1

            elif self.source[self.position] == ";":
                type = "SC"  # semicolon
                self.position += 1

            elif self.source[self.position] == ":":
                type = "C"  # colon
                self.position += 1

            elif self.source[self.position] == ">":
                type = "GT"  # greater than
                self.position += 1

            elif self.source[self.position] == "<":
                type = "LT"  # less than
                self.position += 1
            
            elif self.source[self.position] == ',':
                type = "COMMA" # vírgula
                self.position += 1

            # lógica do or
            elif self.source[self.position] == "|":
                self.position += 1
                if self.source[self.position] == "|":
                    type = "OR"
                    self.position += 1

                else:
                    raise Exception("símbolo inválido faltou mais um '|'")

            # lógica do and
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

            # se não for nenhum, símbolo inválido
            else:
                raise Exception("símbolo inválido")

            self.next = Token(type, value)

        else:
            type = "EOF"
            self.next = Token(type, value)
            self.position += 1


class Parser:
    tokenizer = None

    @staticmethod
    def parseBlock():
        if Parser.tokenizer.next.type == "LCB":
            Parser.tokenizer.selectNext()
            node = Block(None, [])

            while Parser.tokenizer.next.type != "RCB":
                child = Parser.parseStatement()  # guardar no node
                node.children.append(child)
            Parser.tokenizer.selectNext()

        else:
            raise Exception("TOKEN INVÁLIDO")

        return node

    @staticmethod
    def parseStatement():
        if Parser.tokenizer.next.type == "SC":  # caminho do semicolon
            Parser.tokenizer.selectNext()
            resultado = NoOp("", "")

        elif Parser.tokenizer.next.type == "BREAK":
            Parser.tokenizer.selectNext()
            print("break")
            return NoOp("", "")

        
        elif Parser.tokenizer.next.type in ["int", "str", "bool","float"]:  # caminho do tipo
            var_type = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()

            declarations = []
            assignments = []

            while True:
                if Parser.tokenizer.next.type == "ARROW":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "ID":
                        identifier = Identifier(Parser.tokenizer.next.value, [])
                        declarations.append(identifier)
                        Parser.tokenizer.selectNext()

                        if Parser.tokenizer.next.type == "ASSIGNMENT":
                            Parser.tokenizer.selectNext()
                            expression = Parser.parseExpression()
                            assignments.append(Assignment("", [identifier, expression]))

                        if Parser.tokenizer.next.type == "COMMA":
                            Parser.tokenizer.selectNext()
                        else:
                            break
                    else:
                        raise Exception("TOKEN INVÁLIDO")
                else:
                    raise Exception("FALTOU ARROW")

            resultado = VarDec(var_type, declarations + [Block("", assignments)])

            if Parser.tokenizer.next.type == "SC":
                Parser.tokenizer.selectNext()
            else:
                raise Exception("FALTOU SEMICOLON")

        elif Parser.tokenizer.next.type == "ID":  # caminho do identifier para atribuição
            identifier = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "ASSIGNMENT":
                Parser.tokenizer.selectNext()
                expression = Parser.parseExpression()
                resultado = Assignment("", [identifier, expression])

                if Parser.tokenizer.next.type == "SC":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("FALTOU SEMICOLON")
            else:
                raise Exception("TOKEN INVÁLIDO")
            
        elif Parser.tokenizer.next.type == "START":  # caminho do START
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type != "LP":
                raise Exception("FALTOU '('")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "id":
                raise Exception('erro')
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "C":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            id = Parser.parseRelativeExpression()
            if Parser.tokenizer.next.type != "COMMA":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "station":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "C":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            station = Parser.parseRelativeExpression()
            if Parser.tokenizer.next.type != "COMMA":
                raise Exception("erro") 
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "region":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "C":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            region = Parser.parseRelativeExpression()
            if Parser.tokenizer.next.type != "RP":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "SC":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            resultado = START("", [id,station,region])

        elif Parser.tokenizer.next.type == "STOP":  # caminho do START
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type != "LP":
                raise Exception("FALTOU '('")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "name":
                raise Exception('erro')
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "C":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            name = Parser.parseRelativeExpression()
            if Parser.tokenizer.next.type != "COMMA":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "speed":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "C":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            speed = Parser.parseRelativeExpression()
            if Parser.tokenizer.next.type != "COMMA":
                raise Exception("erro") 
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "rotation":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "C":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            rotation = Parser.parseRelativeExpression()
            if Parser.tokenizer.next.type != "RP":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "SC":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            resultado = STOP("", [name,speed,rotation])

        elif Parser.tokenizer.next.type == "FINISH":  # caminho do START
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type != "LP":
                raise Exception("FALTOU '('")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "id":
                raise Exception('erro')
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "C":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            id = Parser.parseRelativeExpression()
            if Parser.tokenizer.next.type != "COMMA":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "station":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "C":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            station = Parser.parseRelativeExpression()
            if Parser.tokenizer.next.type != "COMMA":
                raise Exception("erro") 
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "region":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "C":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            region = Parser.parseRelativeExpression()
            if Parser.tokenizer.next.type != "RP":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "SC":
                raise Exception("erro")
            Parser.tokenizer.selectNext()
            resultado = FINISH("", [id,station,region])

        elif Parser.tokenizer.next.type == "printlog":  # caminho do Print
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = Print("", [Parser.parseRelativeExpression()])

                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()

                    if Parser.tokenizer.next.type == "SC":
                        Parser.tokenizer.selectNext()

                    else:
                        raise Exception("FALTOU SEMICOLON")

                else:
                    raise Exception("FALTOU ')'")

            else:
                raise Exception("TOKEN INVÁLIDO")

        elif Parser.tokenizer.next.type == "while":  # caminho do while
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                condicao = Parser.parseRelativeExpression()

                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                    # primeiro filho condicao do while/ segundo o que o while faz
                    resultado = While('', [condicao, Parser.parseStatement()])

                else:
                    raise Exception("FALTOU ')'")
            else:
                raise Exception("FALTOU '('")

        elif Parser.tokenizer.next.type == "if":  # camimho do if
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                condicao = Parser.parseRelativeExpression()

                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                    acao = Parser.parseStatement()

                    if Parser.tokenizer.next.type == "else":
                        Parser.tokenizer.selectNext()
                        resultado = If(
                            '', [condicao, acao, Parser.parseStatement()])

                    else:
                        resultado = If('', [condicao, acao])

                else:
                    raise Exception("FALTOU ')'")

            else:
                raise Exception("FALTOU '('")

        else:
            resultado = Parser.parseBlock()

        return resultado

    @staticmethod
    def parseRelativeExpression():
        resultado = Parser.parseExpression()
        while Parser.tokenizer.next.type == "EQUAL" or Parser.tokenizer.next.type == "GT" or Parser.tokenizer.next.type == "LT":

            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()
                resultado = BinOp("==", [resultado, Parser.parseExpression()])

            if Parser.tokenizer.next.type == "GT":
                Parser.tokenizer.selectNext()
                resultado = BinOp(">", [resultado, Parser.parseExpression()])

            if Parser.tokenizer.next.type == "LT":
                Parser.tokenizer.selectNext()
                resultado = BinOp("<", [resultado, Parser.parseExpression()])

        return resultado

    @staticmethod
    def parseExpression():
        resultado = Parser.parseTerm()
        while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS" or Parser.tokenizer.next.type == "OR":

            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("+", [resultado, Parser.parseTerm()])

            if Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("-", [resultado, Parser.parseTerm()])

            if Parser.tokenizer.next.type == "OR":
                Parser.tokenizer.selectNext()
                resultado = BinOp("||", [resultado, Parser.parseTerm()])

        return resultado

    @staticmethod
    def parseTerm():
        resultado = Parser.parseFactor()
        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV" or Parser.tokenizer.next.type == "AND":

            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.selectNext()
                resultado = BinOp("*", [resultado, Parser.parseFactor()])

            if Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.selectNext()
                resultado = BinOp("/", [resultado, Parser.parseFactor()])

            if Parser.tokenizer.next.type == "AND":
                Parser.tokenizer.selectNext()
                resultado = BinOp("&&", [resultado, Parser.parseFactor()])

        return resultado

    @staticmethod
    def parseFactor():
        if Parser.tokenizer.next.type == "INT":
            resultado = IntVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.next.type == "FLOAT":
            resultado = FloatVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.next.type == "STRING":
            resultado = StringVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.selectNext()
            resultado = UnOp("+", [Parser.parseFactor()])

        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.selectNext()
            resultado = UnOp("-", [Parser.parseFactor()])

        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.selectNext()
            resultado = UnOp("!", [Parser.parseFactor()])

        elif Parser.tokenizer.next.type == "LP":
            Parser.tokenizer.selectNext()
            resultado = Parser.parseRelativeExpression()

            if Parser.tokenizer.next.type == "RP":
                Parser.tokenizer.selectNext()

            else:
                raise Exception("FALTOU ')'")
            
        elif Parser.tokenizer.next.type == "sqrt":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = MathFunc("sqrt", [Parser.parseExpression()])
                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("FALTOU ')'")
            else:
                raise Exception("FALTOU '('")
            
        elif Parser.tokenizer.next.type == "sin":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = MathFunc("sin", [Parser.parseExpression()])
                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("FALTOU ')'")
            else:
                raise Exception("FALTOU '('")
            
        elif Parser.tokenizer.next.type == "cos":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = MathFunc("cos", [Parser.parseExpression()])
                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("FALTOU ')'")
            else:
                raise Exception("FALTOU '('")       

        elif Parser.tokenizer.next.type == "tan":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = MathFunc("tan", [Parser.parseExpression()])
                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("FALTOU ')'")
            else:
                raise Exception("FALTOU '('")
            
        elif Parser.tokenizer.next.type == "log":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = MathFunc("log", [Parser.parseExpression()])
                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("FALTOU ')'")
            else:
                raise Exception("FALTOU '('")
            
        elif Parser.tokenizer.next.type == "exp":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = MathFunc("exp", [Parser.parseExpression()])
                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("FALTOU ')'")
            else:
                raise Exception("FALTOU '('")
            
        elif Parser.tokenizer.next.type == "pow":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = MathFunc("pow", [Parser.parseExpression()])
                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("FALTOU ')'")
            else:
                raise Exception("FALTOU '('")
            

        elif Parser.tokenizer.next.type == "pi":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()
                resultado = MathFunc("pi", [])
                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception("FALTOU ')'")
            else:
                raise Exception("FALTOU '('")          

        elif Parser.tokenizer.next.type == "scanf":
            Parser.tokenizer.selectNext()
            resultado = Read('', [])

            if Parser.tokenizer.next.type == "LP":
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type == "RP":
                    Parser.tokenizer.selectNext()

                else:
                    raise Exception("FALTOU ')'")

            else:
                raise Exception("FALTOU '('")

        elif Parser.tokenizer.next.type == "ID":
            resultado = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()

        else:
            raise Exception("TOKEN INVÁLIDO")

        return resultado

    @staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        result = Parser.parseBlock()

        if Parser.tokenizer.next.type != "EOF":
            raise Exception("Sobrou Token")
        else:
            return result


class PrePro:
    @staticmethod
    def filter(string):
        resultado = ""
        i = 0
        length = len(string)
        
        while i < length:
            if i < length - 1 and string[i] == '/' and string[i + 1] == '*':
                # Encontrou o início de um comentário /*, então pula para o fim do comentário
                i += 2  # Pular os caracteres /*
                while i < length - 1 and not (string[i] == '*' and string[i + 1] == '/'):
                    i += 1
                    if i == length - 1:
                        # Se chegar ao final da string sem encontrar o fechamento do comentário
                        raise RuntimeError("Erro: Comentário aberto não fechado corretamente.")
                i += 2  # Pular os caracteres */
            else:
                resultado += string[i]
                i += 1

        return resultado


class Node:
    def __init__(self, value, children):
        self.value = value  # variant
        self.children = children  # list of nodes

    def Evaluate(self):  # variant
        pass


class BinOp(Node):  # Binary Operation. Contem dois filhos
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        val_f1, type_f1 = self.children[0].Evaluate()
        val_f2, type_f2 = self.children[1].Evaluate()

        # Mapeamento de bool para int
        if type_f1 == 'bool':
            val_f1 = 1 if val_f1 else 0
            type_f1 = 'int'
        if type_f2 == 'bool':
            val_f2 = 1 if val_f2 else 0
            type_f2 = 'int'

        if self.value == "+":
            if type_f1 == 'str' or type_f2 == 'str':
                return str(val_f1) + str(val_f2), 'str'
            elif type_f1 == 'int' and type_f2 == 'int':
                return val_f1 + val_f2, 'int'
            elif type_f1 == 'float' and type_f2 == 'float':
                return val_f1 + val_f2, 'float'
            else:
                raise Exception(f"Type mismatch: Add operation requires 'int', 'bool', or 'str' operands, got '{type_f1}' and '{type_f2}'")

        elif self.value == "-":
            if type_f1 == 'int' and type_f2 == 'int':
                return val_f1 - val_f2, 'int'
            elif type_f1 == 'float' and type_f2 == 'float':
                return val_f1 - val_f2, 'float'
            else:
                raise Exception(f"Type mismatch: Sub operation requires 'int' or 'bool' operands, got '{type_f1}' and '{type_f2}'")

        elif self.value == "*":
            if type_f1 == 'int' and type_f2 == 'int':
                return val_f1 * val_f2, 'int'
            elif type_f1 == 'float' and type_f2 == 'float':
                return val_f1 * val_f2, 'float'
            else:
                raise Exception(f"Type mismatch: Mul operation requires 'int' or 'bool' operands, got '{type_f1}' and '{type_f2}'")

        elif self.value == "/":
            if type_f1 == 'int' and type_f2 == 'int':
                if val_f2 == 0:
                    raise Exception("Division by zero")
                return val_f1 // val_f2, 'int'
            elif type_f1 == 'float' and type_f2 == 'float':
                return val_f1 // val_f2, 'float'
            else:
                raise Exception(f"Type mismatch: Div operation requires 'int' or 'bool' operands, got '{type_f1}' and '{type_f2}'")

        elif self.value == "==":
            if type_f1 == type_f2:
                return int(val_f1 == val_f2), 'bool'
            else:
                raise Exception(f"Type mismatch: Equal operation requires operands of the same type, got '{type_f1}' and '{type_f2}'")

        elif self.value == ">":
            if type_f1 == type_f2:
                return int(val_f1 > val_f2), 'bool'
            else:
                raise Exception(f"Type mismatch: Greater than operation requires operands of the same type, got '{type_f1}' and '{type_f2}'")

        elif self.value == "<":
            if type_f1 == type_f2:
                return int(val_f1 < val_f2), 'bool'
            else:
                raise Exception(f"Type mismatch: Less than operation requires operands of the same type, got '{type_f1}' and '{type_f2}'")

        elif self.value == "&&":
            if type_f1 == ('int'or"float") and type_f2 == ('int' or "float"):
                return int(bool(val_f1) and bool(val_f2)), 'bool'
            else:
                raise Exception(f"Type mismatch: And operation requires 'int' or 'bool' operands, got '{type_f1}' and '{type_f2}'")

        elif self.value == "||":
            if type_f1 == ('int'or"float")and type_f2 == ('int'or"float"):
                return int(bool(val_f1) or bool(val_f2)), 'bool'
            else:
                raise Exception(f"Type mismatch: Or operation requires 'int' or 'bool' operands, got '{type_f1}' and '{type_f2}'")

        else:
            raise Exception("TOKEN INVÁLIDO")


class UnOp(Node):  # Unary Operation. Contem um filho
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        val, type_val = self.children[0].Evaluate()

        # Mapeamento de bool para int
        if type_val == 'bool':
            val = 1 if val else 0
            type_val = 'int'

        if self.value == "-":
            if type_val == 'int':
                return -val, 'int'
            if type_val == 'float':
                return -val, 'float'
            else:
                raise Exception(f"Type mismatch: Unary minus operation requires 'int' or 'bool' operand, got '{type_val}'")
        
        elif self.value == "!":
            if type_val == 'int':
                return int(not bool(val)), 'bool'
            if type_val == 'float':
                return int(not bool(val)), 'bool'
            else:
                raise Exception(f"Type mismatch: Not operation requires 'int' or 'bool' operand, got '{type_val}'")

        else:
            return val, type_val


class IntVal(Node):  # Integer value. Não contem filhos
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        return self.value, 'int'  # Retorna o valor e o tipo
    
class FloatVal(Node):  # Integer value. Não contem filhos
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        return self.value, 'float'  # Retorna o valor e o tipo

class StringVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        return self.value, 'str'  # Retorna o valor e o tipo


class NoOp(Node):  # No Operation (Dummy). Não contem filhos
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        return super().Evaluate()

class Block(Node):  # tem vários filhos
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        identifier = self.children[0].value
        value, value_type = self.children[1].Evaluate()
        if identifier in SymbolTable.table:
            var_type = SymbolTable.table[identifier][1]
            if (var_type == value_type) or (var_type in ['int', 'bool',"float"] and value_type in ['int', 'bool',"float"]):
                SymbolTable.table[identifier][0] = value  # Atualiza o valor da variável na tabela de símbolos
            else:
                raise Exception(f"Type mismatch: Variable '{identifier}' is of type '{var_type}' but got '{value_type}'")
        else:
            raise Exception(f"Variable '{identifier}' not declared")

class Identifier(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        if self.value in SymbolTable.table:
            value, var_type = SymbolTable.table[self.value]
            if var_type == "str":
                n_type = str
            elif var_type == "int":
                n_type = int
            elif var_type == "float":
                n_type = float
            if type(value) is not n_type:
                raise Exception(f"Type mismatch: Variable '{self.value}' is of type '{var_type}' but got '{type(value)}'")
            
            return value, var_type  # Retorna o valor e o tipo da variável
        else:
            raise Exception(f"Variable '{self.value}' not declared")


class Print(Node):  # só tem um child
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        value, _ = self.children[0].Evaluate()
        print(value)


class Read(Node):  # não tem children e nem value, seu evaluate que retorna o valor de um input
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        user_input = input()
        if user_input.isdigit():
            return int(user_input), 'int'
        else:
            raise Exception("Invalid input: Expected an integer")


class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        while self.children[0].Evaluate()[0]:
            self.children[1].Evaluate()


class START(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):

        print("------------- Starting track ----------------")
        print(" - Train ID: " + self.children[0].value)
        print(" - Station: " + self.children[1].value)
        print(" - Region: " + self.children[2].value)
        print("---------------------------------------------")

class STOP(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        val_speed,_ = self.children[1].Evaluate()
        val_rotation,_ = self.children[2].Evaluate()
        print("------------- STOPPING track ----------------")
        print(" - STATION NAME: " + self.children[0].value)
        print(" - TRAIN SPEED: " + str(val_speed))
        print(" - WHEEL ROTATION: " + str(val_rotation))
        print("---------------------------------------------")

class FINISH(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        print("------------- FINISHING track ----------------")
        print(" - Train ID: " + self.children[0].value)
        print(" - Station: " + self.children[1].value)
        print(" - Region: " + self.children[2].value)
        print("---------------------------------------------")

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        if self.children[0].Evaluate():
            self.children[1].Evaluate()

        elif len(self.children) > 2:
            self.children[2].Evaluate()

class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        var_type = self.value  # O tipo da variável está no value do nó VarDec
        for child in self.children[:-1]:  # Itera sobre todos os filhos, exceto o último (bloco de assignments)
            if var_type == 'int':
                initial_value = 0
            elif var_type == 'float':
                initial_value = 0.0
            elif var_type == 'str':
                initial_value = ""
            elif var_type == 'bool':
                initial_value = False
            else:
                raise Exception(f"Unsupported type '{var_type}'")
            SymbolTable.set_table(child.value, initial_value, var_type)  # Declara as variáveis com valor inicial e tipo especificado
        self.children[-1].Evaluate()  # Evaluate no bloco de assignments

class MathFunc(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        if self.value == "sqrt":
            val,type= self.children[0].Evaluate()
            return float(math.sqrt(val)), 'float'
            
        elif self.value == "sin":
            val,type= self.children[0].Evaluate()
            return float(math.sin(val)), 'float'
        elif self.value == "cos":
            val,type= self.children[0].Evaluate()
            return float(math.cos(val)), 'float'
        elif self.value == "tan":
            val,type= self.children[0].Evaluate()
            return float(math.tan(val)), 'float'
        elif self.value == "log":
            val,type= self.children[0].Evaluate()
            return float(math.log(val)), 'float'
        elif self.value == "exp":
            val,type= self.children[0].Evaluate()
            return float(math.exp(val)), 'float'

        elif self.value == "pi":
            return float(math.pi), 'float'
class SymbolTable:
    table = dict()

    @staticmethod
    def get_table(key):
        return SymbolTable.table[key]

    @staticmethod
    def set_table(key, value, type):
        if key in SymbolTable.table:
            raise Exception(f"Variable '{key}' is already declared and cannot be redeclared")
        SymbolTable.table[key] = [value, type]


# main
with open(sys.argv[1], "r") as f:
    Parser.run(PrePro.filter(f.read())).Evaluate()

# debug
# with open("test.c", "r") as f:
#     Parser.run(PrePro.filter(f.read())).Evaluate()