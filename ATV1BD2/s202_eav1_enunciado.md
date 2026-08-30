# [S202] Fichas de Personagem (MongoDB)

Poles está desenvolvendo um sistema de fichas de personagem para as guildas de aventureiros do mundo de Granjaran. O sistema precisa de dois subsistemas simples para funcionar.

O primeiro subsistema é uma ficha de personagens. Neste sistema, os personagens possuem nome, classe (Guerreiro, Ladino, Mago, Clérigo ou Arqueiro), nível, região onde atuam e guilda à qual pertencem.

O segundo subsistema é um catálogo de guildas e itens. Neste sistema existem guildas e itens. As guildas possuem nome, região e especialidade (Magia, Furtividade, Exploração, Combate ou Rastreamento). Os itens possuem nome, tipo (Arma, Armadura, Artefato ou Poção), raridade e uma lista de especialidades que podem utilizá-los.

Considere os casos de teste e as informações dadas em cada teste para registrar os dados dos personagens, guildas e itens. Para cada questão um conjunto de dados diferente será usado, contendo a entrada necessária e a saída esperada para resolver cada um dos problemas.

## Configuração

Coloque todos os arquivos em uma mesma pasta.

Crie um ambiente virtual (python 3.11) se achar necessário e execute o seguinte comando para instalar as bibliotecas necessárias:

`pip install -r requirements.txt`

Para executar os testes use o comando:

`pytest s202_personagens_base.py`

## Questão 1 (classe CharacterDAO)

(20 pontos) Desenvolva a função `add_character` para inserir as informações dos personagens no MongoDB.

(10 pontos) Desenvolva a função `get_characters_by_region` para buscar no MongoDB os nomes e níveis de todos os personagens de uma determinada região, ordenados por nível (do maior para o menor). Em caso de empate no nível, ordene por nome em ordem alfabética.

## Questão 2 (classes GuildDAO e ItemDAO)

(20 pontos) Desenvolva a função `add_guild` para inserir as guildas no MongoDB.

(10 pontos) Desenvolva a função `add_item` para inserir os itens no MongoDB, incluindo a lista de especialidades que podem utilizá-los.

(10 pontos) Desenvolva a função `get_items_by_guild_specialty` que, dado o nome de uma guilda, retorna o nome e o tipo de todos os itens que podem ser utilizados pela especialidade daquela guilda, ordenados por nome em ordem alfabética.
