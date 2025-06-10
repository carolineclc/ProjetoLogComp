# Flex and Bison C++ Project

This project demonstrates the use of Flex and Bison to create a simple parser and lexer in C++. 

## Project Structure

```
flex-bison-cpp-project
├── src
│   ├── lexer.l        # Flex lexer definitions
│   ├── parser.y       # Bison parser definitions
│   └── main.cpp       # Entry point for the application
├── Makefile           # Build instructions
└── README.md          # Project documentation
```

## Files Description

- **src/lexer.l**: Contains the Flex lexer definitions. It defines the tokens and the rules for tokenizing the input source code.

- **src/parser.y**: Contains the Bison parser definitions. It defines the grammar rules and the actions to be taken when those rules are matched.

- **src/main.cpp**: Serves as the entry point for the application. It includes the necessary headers and initializes the lexer and parser.

- **Makefile**: Contains the build instructions for compiling the project. It specifies how to generate the C++ files from the Flex and Bison definitions and how to link them together.

## Build Instructions

To build the project, navigate to the project directory and run the following command:

```
make
```

This will generate the necessary C++ files from the Flex and Bison definitions and compile the project.

## Running the Project

After building the project, you can run the application using:

```
./main
```

Make sure to provide the necessary input files as required by your lexer and parser. 

## License

This project is licensed under the MIT License.