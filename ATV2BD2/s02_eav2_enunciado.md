# [S02] EAV2 — Sistema de Guildas (Neo4j)

Poles expandiu seu universo de RPG e agora precisa de um sistema para gerenciar as **guildas de aventureiros** do mundo de Granjaran. Ele quer registrar as guildas existentes, os aventureiros que fazem parte delas e as missões disponíveis em cada região — e precisa da sua ajuda para modelar e popular esse banco de dados em **Neo4j**.

## Contexto

O sistema possui três entidades principais:

- **Guild (Guilda):** cada guilda possui nome, descrição, cidade-sede e uma lista de especializações (ex.: "Combate", "Magia", "Furtividade", "Exploração", "Comércio").
- **Adventurer (Aventureiro):** cada aventureiro possui nome, idade, lista de habilidades, rank ("Novato", "Aprendiz", "Veterano", "Mestre" ou "Lendário"), cidade de origem, data de registro e pode ser membro de uma ou mais guildas.
- **Quest (Missão):** cada missão possui título, descrição, recompensa em moedas de ouro, nível de perigo (1 a 5), lista de especializações requeridas e lista de ranks aceitos.

## Configuração

Coloque todos os arquivos em uma mesma pasta.

Crie um ambiente virtual (Python 3.11) se achar necessário e instale as dependências:

```bash
pip install neo4j pytest
```

Edite as credenciais Neo4j no topo de `s02_eav2_base.py` antes de executar.

Para rodar os testes:

```bash
pytest s02_eav2_base.py
```

---

## Questão 1 — `GuildDAO.add_guild` e `QuestDAO.add_quest` (25 pts)

Implemente os dois métodos de inserção:

**`GuildDAO.add_guild(guild: Guild)`**
Insira a guilda no Neo4j com os atributos `name`, `description` e `headquarters`. Para cada especialização da guilda, crie (ou reutilize) um nó `:Specialization` e estabeleça o relacionamento:

```
(:Guild)-[:HAS_SPECIALIZATION]->(:Specialization)
```

> Use `MERGE` tanto para a guilda quanto para cada especialização, evitando duplicatas quando guildas diferentes compartilharem a mesma especialização.

**`QuestDAO.add_quest(quest: Quest)`**
Insira a missão no Neo4j com todos os seus atributos. Armazene `required_specializations` e `required_ranks` diretamente como propriedades de lista no nó `:Quest` — não é necessário criar nós separados para esses valores.

---

## Questão 2 — `GuildDAO.get_guilds_by_specialization` (15 pts)

Implemente a busca que, dada uma especialização, retorna todas as guildas que a possuem.

O retorno deve ser uma **lista de dicionários** com as chaves `"name"` e `"headquarters"`, ordenada **alfabeticamente** pelo nome da guilda.

---

## Questão 3 — `AdventurerDAO.add_adventurer` (25 pts)

Implemente a inserção de um aventureiro no Neo4j com todos os seus atributos. O campo `registration_date` deve ser armazenado como o tipo `DATE` nativo do Neo4j.

Para cada guilda em `guild_memberships`, crie o relacionamento:

```
(:Adventurer)-[:MEMBER_OF]->(:Guild)
```

> Use `MERGE` na guilda para não duplicar nós de guildas já existentes.

---

## Questão 4 — `AdventurerDAO.get_available_quests` (35 pts)

Implemente a busca que retorna todas as missões disponíveis para um aventureiro.

Uma missão está **disponível** se as duas condições forem satisfeitas:
1. O **rank** do aventureiro está na lista `required_ranks` da missão.
2. Pelo menos uma das **especializações** das guildas do aventureiro aparece na lista `required_specializations` da missão.

O retorno deve ser uma **lista de dicionários** com as chaves `"title"`, `"reward"` e `"danger_level"`, **sem duplicatas**, ordenada do **maior reward para o menor** (em caso de empate, ordenar pelo título em ordem alfabética crescente).

---

## Questão 5 — `AdventurerDAO.promote_adventurer` (20 pts)

Implemente a atualização que promove um aventureiro: recebe o nome do aventureiro, um novo rank (`new_rank`) e uma nova habilidade (`new_skill`).

A operação deve:
- Substituir o valor de `rank` pelo novo rank informado.
- **Acrescentar** `new_skill` à lista `skills` já existente, **sem apagar as habilidades anteriores**.

---

## Questão 6 — `QuestDAO.delete_quest` (20 pts)

Implemente a remoção de uma missão pelo seu título. A operação deve excluir permanentemente o nó `:Quest` e todos os seus relacionamentos do grafo (use `DETACH DELETE`). Se não existir nenhuma missão com o título informado, a operação não deve gerar erro.

