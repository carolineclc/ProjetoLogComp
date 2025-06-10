CC = g++
CFLAGS = -std=c++11 -Wall
LEX = flex
YACC = bison
LEX_SRC = src/lexer.l
YACC_SRC = src/parser.y
OBJ = lexer.cpp parser.cpp main.o
TARGET = my_program

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJ)

lexer.cpp: $(LEX_SRC)
	$(LEX) -o lexer.cpp $(LEX_SRC)

parser.cpp: $(YACC_SRC)
	$(YACC) -o parser.cpp $(YACC_SRC)

clean:
	rm -f $(OBJ) $(TARGET) lexer.cpp parser.cpp
