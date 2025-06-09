# Spell Lang 🧙‍♂️🪄
## Introdução
A Spell lang tem como principal objetivo a ajudar pequenos aprendizes de magia a corretamente organizar suas magias para o proximo combate magico. Com o spell lang, aprendizes podem aprender de forma simplificada a logica da magia, e fazer o manegamento correto de feiticos, pocoes, transmutacoes e maldicoes com base na quantidade de mana, aftefatos e ingredientes a sua disposicao. Antes de colocar tudo em pratica, esses alunos tem a oportunidade de programar o seu proximo ataque ou feitico, garantindo sucesso na sua proxima empreentada.


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
SUMMON sorcery mana as 5. # Atribuindo o valor 5 a variavel mana
SUMMON instant spell as "expeliamus". # Atribuindo um valor tipo string para a variavel spell
SUMMON artifact clock as True. #Atribuindo um booleano a variavel clock

SUMMON sorcery poison. # Atribuindo a tipagem sorcery para a variavel poison
SUMMON instant potion. # Atribuindo a tipagem instant para a variavel potion

CHANNEL 7 to poison. # Atribuindo o valor 7 a variavel poision
CHANNEL "recovery" to potion. # Atribuindo a vatiavel "recovery" para a variavel potion

SUMMON sorcery infection as mana drined poison. # infection = mana - poison
SUMMON instant blink as spell infused potion. # blink = spell + potion

CHANNEL clock as False. # Atribuindo o valor Faslse a variavel clock
 

```

## Exemplo 2: Condicionais
O seguinte exemplo demonstra como que o programa trabalha com condicionais.

```
SUMMON mana as sorcery.
CHANNEL calling() to mana. # aqui um valor externo vai ser atribuido para a variavel mana.

WARD if mana greater than 5: 
reveal "mana is strong". 
divert:
reveal "mana is weak"

WARD if clock:
reveal clock.
-WARD if clock is True:
REVEAL "clock is True".
CHANNEL False to clock.

```

## Exemplo 3: Loops
O seguinte exemplo demonstra como que o programa trabalha com loops:
``` 
CHANT until mana is 0:
reveal mana.
channel mana drained 1 to mana.

CHANT until clock:
reveal clock.

WARD if mana is equal to 2:
CHANNEL False to clock.
DIVERT:
channel 2 to mana.

```




