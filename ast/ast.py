# ast.py
import math

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        pass

class BinOp(Node):
    def Evaluate(self):
        val_f1, type_f1 = self.children[0].Evaluate()
        val_f2, type_f2 = self.children[1].Evaluate()
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
            if type_f1 in ['int', 'float'] and type_f2 in ['int', 'float']:
                return int(bool(val_f1) and bool(val_f2)), 'bool'
            else:
                raise Exception(f"Type mismatch: And operation requires 'int' or 'bool' operands, got '{type_f1}' and '{type_f2}'")
        elif self.value == "||":
            if type_f1 in ['int', 'float'] and type_f2 in ['int', 'float']:
                return int(bool(val_f1) or bool(val_f2)), 'bool'
            else:
                raise Exception(f"Type mismatch: Or operation requires 'int' or 'bool' operands, got '{type_f1}' and '{type_f2}'")
        else:
            raise Exception("TOKEN INVÁLIDO")

class UnOp(Node):
    def Evaluate(self):
        val, type_val = self.children[0].Evaluate()
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

class IntVal(Node):
    def Evaluate(self):
        return self.value, 'int'

class FloatVal(Node):
    def Evaluate(self):
        return self.value, 'float'

class StringVal(Node):
    def Evaluate(self):
        return self.value, 'str'

class NoOp(Node):
    def Evaluate(self):
        return super().Evaluate()

class Block(Node):
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class Assignment(Node):
    def Evaluate(self):
        identifier = self.children[0].value
        value, value_type = self.children[1].Evaluate()
        if identifier in SymbolTable.table:
            var_type = SymbolTable.table[identifier][1]
            if (var_type == value_type) or (var_type in ['int', 'bool', "float"] and value_type in ['int', 'bool', "float"]):
                SymbolTable.table[identifier][0] = value
            else:
                raise Exception(f"Type mismatch: Variable '{identifier}' is of type '{var_type}' but got '{value_type}'")
        else:
            raise Exception(f"Variable '{identifier}' not declared")

class Identifier(Node):
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
            return value, var_type
        else:
            raise Exception(f"Variable '{self.value}' not declared")

class Print(Node):
    def Evaluate(self):
        value, _ = self.children[0].Evaluate()
        print(value)

class Read(Node):
    def Evaluate(self):
        user_input = input()
        if user_input.isdigit():
            return int(user_input), 'int'
        else:
            raise Exception("Invalid input: Expected an integer")

class While(Node):
    def Evaluate(self):
        while self.children[0].Evaluate()[0]:
            self.children[1].Evaluate()

class START(Node):
    def Evaluate(self):
        print("------------- Starting track ----------------")
        print(" - Train ID: " + self.children[0].value)
        print(" - Station: " + self.children[1].value)
        print(" - Region: " + self.children[2].value)
        print("---------------------------------------------")

class STOP(Node):
    def Evaluate(self):
        val_speed, _ = self.children[1].Evaluate()
        val_rotation, _ = self.children[2].Evaluate()
        print("------------- STOPPING track ----------------")
        print(" - STATION NAME: " + self.children[0].value)
        print(" - TRAIN SPEED: " + str(val_speed))
        print(" - WHEEL ROTATION: " + str(val_rotation))
        print("---------------------------------------------")

class FINISH(Node):
    def Evaluate(self):
        print("------------- FINISHING track ----------------")
        print(" - Train ID: " + self.children[0].value)
        print(" - Station: " + self.children[1].value)
        print(" - Region: " + self.children[2].value)
        print("---------------------------------------------")

class If(Node):
    def Evaluate(self):
        if self.children[0].Evaluate():
            self.children[1].Evaluate()
        elif len(self.children) > 2:
            self.children[2].Evaluate()

class VarDec(Node):
    def Evaluate(self):
        var_type = self.value
        for child in self.children[:-1]:
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
            SymbolTable.set_table(child.value, initial_value, var_type)
        self.children[-1].Evaluate()

class MathFunc(Node):
    def Evaluate(self):
        if self.value == "sqrt":
            val, type = self.children[0].Evaluate()
            return float(math.sqrt(val)), 'float'
        elif self.value == "sin":
            val, type = self.children[0].Evaluate()
            return float(math.sin(val)), 'float'
        elif self.value == "cos":
            val, type = self.children[0].Evaluate()
            return float(math.cos(val)), 'float'
        elif self.value == "tan":
            val, type = self.children[0].Evaluate()
            return float(math.tan(val)), 'float'
        elif self.value == "log":
            val, type = self.children[0].Evaluate()
            return float(math.log(val)), 'float'
        elif self.value == "exp":
            val, type = self.children[0].Evaluate()
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