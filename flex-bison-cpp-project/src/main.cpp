#include <iostream>
#include "ast.h" 
#include "parser.tab.h"


extern FILE *yyin;

int main(int argc, char **argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            std::cerr << "Error opening file: " << argv[1] << std::endl;
            return 1;
        }
    } else {
        std::cerr << "Usage: " << argv[0] << " <input_file>" << std::endl;
        return 1;
    }

    yyparse();

    fclose(yyin);
    return 0;
}