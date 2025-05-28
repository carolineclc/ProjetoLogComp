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
summon sorcery mana as 5. # Atribuindo o valor 5 a variavel mana
summon instant spell as "expeliamus". # Atribuindo um valor tipo string para a variavel spell
summon artifact clock as True. #Atribuindo um booleano a variavel clock

summon sorcery poison. # Atribuindo a tipagem sorcery para a variavel poison
summon instant potion. # Atribuindo a tipagem instant para a variavel potion

channel 7 to poison. # Atribuindo o valor 7 a variavel poision
channel "recovery" to potion. # Atribuindo a vatiavel "recovery" para a variavel potion

summon sorcery infection as mana drined poison. # infection = mana - poison
summon instant blink as spell infused potion. # blink = spell + potion

channel clock as False. # Atribuindo o valor Faslse a variavel clock
 

```

## Exemplo 2: Condicionais
O seguinte exemplo demonstra como que o programa trabalha com condicionais.

```
summon mana as sorcery.
channel calling() to mana. # aqui um valor externo vai ser atribuido para a variavel mana.

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




