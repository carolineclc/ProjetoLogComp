# Spell Lang
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

## Exemplo 1: Definindo Variaveis
O seguinte exemplo monstra como corretanente definir as variaveis e como que tipar os valores correspondentes a que seria "strings", "int" e "booleanos". Tambem demonstra como fazer de forma correta a atribuicao de novos valores a variaveis ja pre definidas.

``` 
summon sorcery mana as 5. 
summon instant spell as "expeliamus".
summon artifact clock as True.

summon sorcery poison.
summon instant potion.

channel 7 to poison.
channel "recovery" to potion.

summon sorcery infection as mana drined poison. # infection = mana - poison
summon instant blink as spell infused potion. # blink = spell + potion

channel clock as False.
 

```

## Exemplo 2: Condicionais
O seguinte exemplo demonstra como que o programa trabalha com condicionais.

``` 
ward if mana greater than 5:
    reveal "mana is strong".
divert:
    reveal "mana is weak"

ward if clock:
    reveal clock.

    ward if clock is True:
        reveal "clock is True".
        channel False to clock.

```

## Exemplo 3: Loops
O seguinte exemplo demonstra como que o programa trabalha com loops:
``` 
chant until mana is 0:
    reveal mana.
    channel mana drained 1 to mana.

chant until clock:
    reveal clock.
    ward if mana is equal to 2:
        channel False to clock.
    divert:
        channel 2 to mana.

```


