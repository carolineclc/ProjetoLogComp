# parser.py
from lexer.tokenizer import Tokenizer

from ast.ast import *

class PrePro:
    @staticmethod
    def filter(string):
        resultado = ""
        i = 0
        length = len(string)
        while i < length:
            if i < length - 1 and string[i] == '/' and string[i + 1] == '*':
                i += 2
                while i < length - 1 and not (string[i] == '*' and string[i + 1] == '/'):
                    i += 1
                    if i == length - 1:
                        raise RuntimeError("Erro: Comentário aberto não fechado corretamente.")
                i += 2
            else:
                resultado += string[i]
                i += 1
        return resultado

class Parser:
    tokenizer = None

    @staticmethod
    def parseBlock():
        if Parser.tokenizer.next.type == "LCB":
            Parser.tokenizer.selectNext()
            node = Block(None, [])
            while Parser.tokenizer.next.type != "RCB":
                child = Parser.parseStatement()
                node.children.append(child)
            Parser.tokenizer.selectNext()
        else:
            raise Exception("TOKEN INVÁLIDO")
        return node

    @staticmethod
    def parseStatement():
        # ... (copie o conteúdo do método parseStatement do seu código original)
        pass

    @staticmethod
    def parseRelativeExpression():
        # ... (copie o conteúdo do método parseRelativeExpression do seu código original)
        pass

    @staticmethod
    def parseExpression():
        # ... (copie o conteúdo do método parseExpression do seu código original)
        pass

    @staticmethod
    def parseTerm():
        # ... (copie o conteúdo do método parseTerm do seu código original)
        pass

    @staticmethod
    def parseFactor():
        # ... (copie o conteúdo do método parseFactor do seu código original)
        pass

    @staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        result = Parser.parseBlock()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception("Sobrou Token")
        else:
            return result

# main
import sys
if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        Parser.run(PrePro.filter(f.read())).Evaluate()