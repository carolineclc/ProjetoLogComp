# MetroScript

## Introdução
A Linguagem MetroScript foi desenvolvida com o objetivo de facilitar a criação e execução de rotas e instruções para trens de metro. Ela oferece uma sintaxe simples e intuitiva, permitindo que usuarios definam trens, suas rotas, suas paradas e outras aplicações como velocidade e rotação de rodas para os trens.

## Desenvolvedor
Caroline Chaim de Lima Carneiro

## Como executar
python main.py [arquivos de teste]

### Arquivo de teste
exemplo1.m

exemplo2.m

exemplo3.m

exemplo4.m
## EBNF

``` lua
BLOCK = '{' , STATEMENT , '}';

STATEMENT = ";" | ASSIGMENT | PRINT | IF | WHILE | START | STOP | FINISH;

ASSIGNMENT = IDENTIFIER,( CREATE | SET);

CREATE = "=>", TYPE, ["=", (RELEXP | MATH_FUNC)], ";";

SET = "=", (RELEXP | MATH_FUNC),";";

PRINT = 'printLog','(',RELEXP,')';

WHILE = "while","(", RELEXP,")",BLOCK, ";";

IF = "if","(", RELEXP,")",BLOCK,["else",BLOCK], ";";

MATH_FUNC = MATHFUNC_N, "(", RELEXP, ")", ";";

MATH_FUNC_N = "sqrt" |"sin" | "cos" | "tan"| "log" | "exp" | "pow" | "pi";

START = "START","(","id",":", IDENTIFIER , "," , "station", ":" , IDENTIFIER , ",", "region" , IDENTIFIER, ")",";";

STOP = "STOP" , "(","name", ":" , IDENTIFIER, ",", "speed", ":", NUMBER, "," , "rotation", ":", NUMBER,")",";";

FINISH= "FINISH","(","id",":", IDENTIFIER , "," , "station", ":" , IDENTIFIER , ",", "region" , IDENTIFIER, ")",";";

RELEXPR = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION };

EXPRESSION = TERM, { ("+" | "-" | "||" | "."), TERM };

TERM = FACTOR, { ("*" | "/" | "&&"), FACTOR };

FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | "(", RELEXPR, ")" | IDENTIFIER, ["(", RELEXPR, {",", RELEXPR} ,")"] | ("READLN", "(", ")");

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" };

NUMBER = DIGIT, { DIGIT };

LETTER = ( a | ... | z | A | ... | Z );

DIGIT = ( 1* | 2* | 3* | 4* | 5* | 6* | 7* | 8* | 9* | 0* );

```

## Exemplo 1: Definindo rota

O seguinte exemplo demonstra como usar a linguagem para definir uma rota com tres paradas. A rota comeca o lugar que o trem estiver estacionado pela noite anterior e passar pelas paradas 1,2,3 e termina no lugar onde ele vai parar pelo dia. Note que neste exemplo o trem passa pelas estacoes sem parar, e no final faz sua parada na estacao do hospital depois de concluir o seu percurso de novo na estacao Santa Rosa.

``` lua

{
START (id : "abc_123", station : "Santa Rosa", region : "Norte");

STOP (name : "Pinheiros", speed: 50, rotation: 100);
STOP (name : "Parque", speed : 20, rotation : 50);
STOP (name : "Hospital", speed : 0, rotation : 0);

FINISH (id :  "abc_123", station : "Santa Rosa", region : "Norte); 
}
```

## Exemplo 2: Mudando a velocidade 
O seguinte exemplo demonstra como que o programa captura a mudanca de velocidade ao passar em um ponto, ou de um ponto a outro. E importante ressaltar que a velocidade vai estar sempre em km/h.

``` lua
{
float => init_speed = 0.0;
float => target_speed = 50.0;
float => time = 0.0;
float => aceletation = 3.5;

float => time_to_reach_target_speed = (target_speed - init_speed) / aceletation;

START (id : "abc_123", station : "Santa Rosa", region : "Norte");

while (time < time_to_reach_target_speed ) {
    init_speed = init_speed + aceletation;
    time = time + 1.0;
    STOP (name : "GOING TO Pinheiros", speed: init_speed, rotation: 100);
}

STOP (name : "Pinheiros", speed: init_speed, rotation: 100);

}
```

## Exemplo 3: Alterando a rotação da roda
O seguinte exemplo demonstra como que o programa consegue alterar a velocidade da rotacao da roda dependendo do seu diametro. E como essa rotacao influencia na velocidade do trem dentro de um trecho do percurso.

``` lua
{

float => diameter;
float => radius;
float => circumferance;
int => km = 1;
float => rpm;


diameter = 4.0;
radius = diameter * 2.0;
circumferance = pi() * diameter;

float => init_speed = 0.0;
float => target_speed = 50.0;
float => time = 0.0;
float => aceletation = 3.5;
float => time_to_reach_target_speed = (target_speed - init_speed) / aceletation;


START (id : "abc_123", station : "Santa Rosa", region : "Norte");
while (time < time_to_reach_target_speed ) {

    init_speed = init_speed + aceletation;
    time = time + 1.0;
    rpm = init_speed * 60.0 / circumferance;
    STOP (name : "GOING TO Pinheiros", speed: init_speed, rotation: rpm);
    }
}

```

## Exemplo 4: Fazendo uso dos simbolos matematicos
``` lua
{
printlog(sqrt(2.0));
printlog(sin(90));
printlog(cos(60));
printlog(tan(45));
printlog(log(1.3));
printlog(exp(5));
printlog(pi());
}

```
