#pragma once
#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <unordered_map>
#include <variant>
#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif


class Node;
using NodePtr = std::shared_ptr<Node>;
using NodeList = std::vector<NodePtr>;

// Variant for value types
using Value = std::variant<int, float, std::string, bool>;

struct EvalResult {
    Value value;
    std::string type;
    EvalResult(const Value& v, const std::string& t) : value(v), type(t) {}
    EvalResult() : value(0), type("float") {}
};

class SymbolTable {
public:
    static std::unordered_map<std::string, std::pair<Value, std::string>> table;

    static void set(const std::string& key, Value value, const std::string& type) {
        if (table.count(key))
            throw std::runtime_error("Variable '" + key + "' already declared");
        table[key] = {value, type};
    }
    static std::pair<Value, std::string> get(const std::string& key) {
        if (!table.count(key))
            throw std::runtime_error("Variable '" + key + "' not declared");
        return table[key];
    }
    static void assign(const std::string& key, Value value, const std::string& type) {
        if (!table.count(key))
            throw std::runtime_error("Variable '" + key + "' not declared");
        auto& [old_val, old_type] = table[key];
        if (old_type == type || (old_type == "int" && type == "bool") || (old_type == "float" && (type == "int" || type == "bool")))
            old_val = value;
        else
            throw std::runtime_error("Type mismatch on assignment to '" + key + "'");
    }
};

inline std::unordered_map<std::string, std::pair<Value, std::string>> SymbolTable::table;

class Node {
public:
    virtual ~Node() = default;
    virtual EvalResult Evaluate() { return {0, "int"}; }
};

class IntVal : public Node {
public:
    int value;
    IntVal(int v) : value(v) {}
    EvalResult Evaluate() override { return {value, "int"}; }
};

class FloatVal : public Node {
public:
    float value;
    FloatVal(float v) : value(v) {}
    EvalResult Evaluate() override { return {value, "float"}; }
};

class StringVal : public Node {
public:
    std::string value;
    StringVal(const std::string& v) : value(v) {}
    EvalResult Evaluate() override { return {value, "str"}; }
};

class Identifier : public Node {
public:
    std::string name;
    Identifier(const std::string& n) : name(n) {}
    EvalResult Evaluate() override {
        auto [val, type] = SymbolTable::get(name);
        return {val, type};
    }
};

class Assignment : public Node {
public:
    NodePtr id;
    NodePtr expr;
    Assignment(NodePtr id_, NodePtr expr_) : id(id_), expr(expr_) {}
    EvalResult Evaluate() override {
        auto id_eval = std::dynamic_pointer_cast<Identifier>(id);
        if (!id_eval) throw std::runtime_error("Assignment to non-identifier");
        auto res = expr->Evaluate();
        SymbolTable::assign(id_eval->name, res.value, res.type);
        return res;
    }
};

class BinOp : public Node {
public:
    std::string op;
    NodePtr left, right;
    BinOp(const std::string& o, NodePtr l, NodePtr r) : op(o), left(l), right(r) {}
    EvalResult Evaluate() override {
        auto l = left->Evaluate();
        auto r = right->Evaluate();
        // Convert bool to int for arithmetic
        if (l.type == "bool") l = {std::get<bool>(l.value) ? 1 : 0, "int"};
        if (r.type == "bool") r = {std::get<bool>(r.value) ? 1 : 0, "int"};
        if (op == "+") {
            if (l.type == "str" || r.type == "str")
                return {std::get<std::string>(l.value) + std::get<std::string>(r.value), "str"};
            if (l.type == "int" && r.type == "int")
                return {std::get<int>(l.value) + std::get<int>(r.value), "int"};
            if (l.type == "float" && r.type == "float")
                return {std::get<float>(l.value) + std::get<float>(r.value), "float"};
        } else if (op == "-") {
            if (l.type == "int" && r.type == "int")
                return {std::get<int>(l.value) - std::get<int>(r.value), "int"};
            if (l.type == "float" && r.type == "float")
                return {std::get<float>(l.value) - std::get<float>(r.value), "float"};
        } else if (op == "*") {
            if (l.type == "int" && r.type == "int")
                return {std::get<int>(l.value) * std::get<int>(r.value), "int"};
            if (l.type == "float" && r.type == "float")
                return {std::get<float>(l.value) * std::get<float>(r.value), "float"};
        } else if (op == "/") {
            if (l.type == "int" && r.type == "int") {
                if (std::get<int>(r.value) == 0) throw std::runtime_error("Division by zero");
                return {std::get<int>(l.value) / std::get<int>(r.value), "int"};
            }
            if (l.type == "float" && r.type == "float") {
                if (std::get<float>(r.value) == 0.0f) throw std::runtime_error("Division by zero");
                return {std::get<float>(l.value) / std::get<float>(r.value), "float"};
            }
        } else if (op == "==") {
            if (l.type == r.type) {
                if (l.type == "int")
                    return {std::get<int>(l.value) == std::get<int>(r.value), "bool"};
                if (l.type == "float")
                    return {std::get<float>(l.value) == std::get<float>(r.value), "bool"};
                if (l.type == "str")
                    return {std::get<std::string>(l.value) == std::get<std::string>(r.value), "bool"};
            }
        } else if (op == ">") {
            if (l.type == r.type) {
                if (l.type == "int")
                    return {std::get<int>(l.value) > std::get<int>(r.value), "bool"};
                if (l.type == "float")
                    return {std::get<float>(l.value) > std::get<float>(r.value), "bool"};
            }
        } else if (op == "<") {
            if (l.type == r.type) {
                if (l.type == "int")
                    return {std::get<int>(l.value) < std::get<int>(r.value), "bool"};
                if (l.type == "float")
                    return {std::get<float>(l.value) < std::get<float>(r.value), "bool"};
            }
        } else if (op == "&&") {
            return {boolify(l) && boolify(r), "bool"};
        } else if (op == "||") {
            return {boolify(l) || boolify(r), "bool"};
        }
        throw std::runtime_error("Invalid binary operation or type mismatch");
    }
private:
    static bool boolify(const EvalResult& e) {
        if (e.type == "int") return std::get<int>(e.value) != 0;
        if (e.type == "float") return std::get<float>(e.value) != 0.0f;
        if (e.type == "bool") return std::get<bool>(e.value);
        return false;
    }
};

class UnOp : public Node {
public:
    std::string op;
    NodePtr child;
    UnOp(const std::string& o, NodePtr c) : op(o), child(c) {}
    EvalResult Evaluate() override {
        auto v = child->Evaluate();
        if (v.type == "bool") v = {std::get<bool>(v.value) ? 1 : 0, "int"};
        if (op == "-") {
            if (v.type == "int") return {-std::get<int>(v.value), "int"};
            if (v.type == "float") return {-std::get<float>(v.value), "float"};
        } else if (op == "!") {
            if (v.type == "int") return {!std::get<int>(v.value), "bool"};
            if (v.type == "float") return {!std::get<float>(v.value), "bool"};
        }
        return v;
    }
};

class NoOp : public Node {
public:
    EvalResult Evaluate() override { return {0, "int"}; }
};

class Block : public Node {
public:
    NodeList children;
    Block(const NodeList& c) : children(c) {}
    EvalResult Evaluate() override {
        for (auto& child : children)
            if (child) child->Evaluate();
        return {0, "int"};
    }
};

class Print : public Node {
public:
    NodePtr expr;
    Print(NodePtr e) : expr(e) {}
    EvalResult Evaluate() override {
        auto res = expr->Evaluate();
        if (res.type == "int") std::cout << std::get<int>(res.value) << std::endl;
        else if (res.type == "float") std::cout << std::get<float>(res.value) << std::endl;
        else if (res.type == "str") std::cout << std::get<std::string>(res.value) << std::endl;
        else if (res.type == "bool") std::cout << (std::get<bool>(res.value) ? "true" : "false") << std::endl;
        return {0, "int"};
    }
};

class Read : public Node {
public:
    EvalResult Evaluate() override {
        int val;
        std::cin >> val;
        return {val, "int"};
    }
};

class While : public Node {
public:
    NodePtr cond, body;
    While(NodePtr c, NodePtr b) : cond(c), body(b) {}
    EvalResult Evaluate() override {
        while (boolify(cond->Evaluate()))
            body->Evaluate();
        return {0, "int"};
    }
private:
    static bool boolify(const EvalResult& e) {
        if (e.type == "int") return std::get<int>(e.value) != 0;
        if (e.type == "float") return std::get<float>(e.value) != 0.0f;
        if (e.type == "bool") return std::get<bool>(e.value);
        return false;
    }
};

class START : public Node {
public:
    NodePtr id, station, region;
    START(NodePtr i, NodePtr s, NodePtr r) : id(i), station(s), region(r) {}
    EvalResult Evaluate() override {
        std::cout << "------------- Starting track ----------------\n";
        std::cout << " - Train ID: " << std::get<std::string>(id->Evaluate().value) << "\n";
        std::cout << " - Station: " << std::get<std::string>(station->Evaluate().value) << "\n";
        std::cout << " - Region: " << std::get<std::string>(region->Evaluate().value) << "\n";
        std::cout << "---------------------------------------------\n";
        return {0, "int"};
    }
};

class STOP : public Node {
public:
    NodePtr name, speed, rotation;
    STOP(NodePtr n, NodePtr s, NodePtr r) : name(n), speed(s), rotation(r) {}
    EvalResult Evaluate() override {
        std::cout << "------------- STOPPING track ----------------\n";
        std::cout << " - STATION NAME: " << std::get<std::string>(name->Evaluate().value) << "\n";
        std::cout << " - TRAIN SPEED: " << std::get<int>(speed->Evaluate().value) << "\n";
        std::cout << " - WHEEL ROTATION: " << std::get<int>(rotation->Evaluate().value) << "\n";
        std::cout << "---------------------------------------------\n";
        return {0, "int"};
    }
};

class FINISH : public Node {
public:
    NodePtr id, station, region;
    FINISH(NodePtr i, NodePtr s, NodePtr r) : id(i), station(s), region(r) {}
    EvalResult Evaluate() override {
        std::cout << "------------- FINISHING track ----------------\n";
        std::cout << " - Train ID: " << std::get<std::string>(id->Evaluate().value) << "\n";
        std::cout << " - Station: " << std::get<std::string>(station->Evaluate().value) << "\n";
        std::cout << " - Region: " << std::get<std::string>(region->Evaluate().value) << "\n";
        std::cout << "---------------------------------------------\n";
        return {0, "int"};
    }
};

class If : public Node {
public:
    NodePtr cond, then_branch, else_branch;
    If(NodePtr c, NodePtr t, NodePtr e = nullptr) : cond(c), then_branch(t), else_branch(e) {}
    EvalResult Evaluate() override {
        if (boolify(cond->Evaluate()))
            then_branch->Evaluate();
        else if (else_branch)
            else_branch->Evaluate();
        return {0, "int"};
    }
private:
    static bool boolify(const EvalResult& e) {
        if (e.type == "int") return std::get<int>(e.value) != 0;
        if (e.type == "float") return std::get<float>(e.value) != 0.0f;
        if (e.type == "bool") return std::get<bool>(e.value);
        return false;
    }
};

class VarDec : public Node {
public:
    std::string var_type;
    NodeList decls;
    NodePtr assignments;
    VarDec(const std::string& t, const NodeList& d, NodePtr a) : var_type(t), decls(d), assignments(a) {}
    EvalResult Evaluate() override {
        for (auto& decl : decls) {
            auto id = std::dynamic_pointer_cast<Identifier>(decl);
            if (!id) throw std::runtime_error("VarDec expects identifiers");
            if (var_type == "int")
                SymbolTable::set(id->name, 0, "int");
            else if (var_type == "float")
                SymbolTable::set(id->name, 0.0f, "float");
            else if (var_type == "str")
                SymbolTable::set(id->name, std::string(""), "str");
            else if (var_type == "bool")
                SymbolTable::set(id->name, false, "bool");
            else
                throw std::runtime_error("Unsupported type in VarDec");
        }
        if (assignments) assignments->Evaluate();
        return {0, "int"};
    }
};

class MathFunc : public Node {
public:
    std::string func;
    NodeList args;
    MathFunc(const std::string& f, const NodeList& a) : func(f), args(a) {}
    EvalResult Evaluate() override {
        if (func == "sqrt") return EvalResult(std::sqrt(std::get<float>((args[0]->Evaluate()).value)), "float");
        if (func == "sin")  return EvalResult(std::sin(std::get<float>((args[0]->Evaluate()).value)), "float");
        if (func == "cos")  return EvalResult(std::cos(std::get<float>((args[0]->Evaluate()).value)), "float");
        if (func == "tan")  return EvalResult(std::tan(std::get<float>((args[0]->Evaluate()).value)), "float");
        if (func == "log")  return EvalResult(std::log(std::get<float>((args[0]->Evaluate()).value)), "float");
        if (func == "exp")  return EvalResult(std::exp(std::get<float>((args[0]->Evaluate()).value)), "float");
        if (func == "pow")  return EvalResult(
            std::pow(
                std::get<float>((args[0]->Evaluate()).value),
                std::get<float>((args[1]->Evaluate()).value)
            ), "float");
        if (func == "pi")   return EvalResult(static_cast<float>(M_PI), "float");
        throw std::runtime_error("Unknown math function: " + func);
}
};