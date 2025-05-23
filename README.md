# Script Programming The
## Introdução
A Script Programming The, ou The Programing Script invertido tem como principal objetivo dificultar a vida de qualquer programador experiente ou inexperiente na sua jornada de desenvolvimento de código. Essa linguagem requer que o programador tenha paciencia e calma em pensar no codigo, pois a primeira linha vai ser sempre reservada para o que normalmente seria a última! Como eu sempre digo: A melhor forma de progredir é sonhar no que voce pode conquistar...e agora voce pode fazer isso de forma prática! Começando (eu acho) com o seu Print! Então com forma de dar um gostinho do que vem por vir: !game the hate, player the hate dont.

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
STATEMENT = (|DECLARATION|("infuse","iden","with",BEXP)|("reveal","{",BEXP,"}")|
("ward","if",BEXP,":","\n",STATEMENT,["diverge",":","\n",STATEMENT])),".","\n";

DECLARATION =  'summon',('sorcery'|'instant'|'artifact'),'iden','as', BEXP;

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
