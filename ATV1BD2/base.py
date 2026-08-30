from pymongo import MongoClient
from pymongo.server_api import ServerApi

class MongoDBDatabase:
    mongo_uri = "mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/" # TODO <<alterar valor>>
    database = None

    @staticmethod
    def get_database():
        if MongoDBDatabase.database is None:
            client = MongoClient(MongoDBDatabase.mongo_uri, server_api=ServerApi('1'))
            MongoDBDatabase.database = client.get_database('personagens_db') # TODO <<alterar valor>>
            MongoDBDatabase.database.get_collection('characters').delete_many({})
            MongoDBDatabase.database.get_collection('guilds').delete_many({})
            MongoDBDatabase.database.get_collection('items').delete_many({})
        return MongoDBDatabase.database

class Character:
    def __init__(self, name, char_class, level, region, guild):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.region = region
        self.guild = guild

    def to_dict(self):
        return {
            "name": self.name,
            "char_class": self.char_class,
            "level": self.level,
            "region": self.region,
            "guild": self.guild,
        }

class Guild:
    def __init__(self, name, region, specialty):
        self.name = name
        self.region = region
        self.specialty = specialty

    def to_dict(self):
        return {
            "name": self.name,
            "region": self.region,
            "specialty": self.specialty,
        }

class Item:
    def __init__(self, name, type, rarity, required_specialty = []):
        self.name = name
        self.type = type
        self.rarity = rarity
        self.required_specialty = required_specialty

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "rarity": self.rarity,
            "required_specialty": self.required_specialty,
        }

class CharacterDAO:

    def __init__(self) -> None:
        self.characters = MongoDBDatabase.get_database().get_collection('characters')

    def add_character(self, character : Character):
        #---------------------------------------------------------------------Questão 1
         self.characters.insert_one(character.to_dict())

    def get_characters_by_region(self, region):
        #---------------------------------------------------------------------Questão 1
         cursor = self.characters.find({"region": region},{"_id": 0, "name": 1, "level": 1}).sort([("level", -1), ("name", 1)])
         return list(cursor)

     

class GuildDAO:

    def __init__(self) -> None:
        self.guilds = MongoDBDatabase.get_database().get_collection('guilds')

    def add_guild(self, guild : Guild):
        #---------------------------------------------------------------------Questão 2
        self.guilds.insert_one(guild.to_dict())
        pass

class ItemDAO:

    def __init__(self) -> None:
        self.items = MongoDBDatabase.get_database().get_collection('items')
        self.guilds = MongoDBDatabase.get_database().get_collection('guilds')

    def add_item(self, item : Item):
        #---------------------------------------------------------------------Questão 2
        self.items.insert_one(item.to_dict())
        pass 

    def get_items_by_guild_specialty(self, guild_name):
        #---------------------------------------------------------------------Questão 2
        guild = self.guilds.find_one({"name": guild_name})
        if not guild: return []

        speciality = guild.get("specialty")

        cursor = self.items.find({"required_specialty": speciality}, {"_id": 0, "name": 1, "type": 1}).sort("name", 1)
        return list(cursor) #lista de dicionarios pelo q eu entendi

character_dao = CharacterDAO()
guild_dao = GuildDAO()
item_dao = ItemDAO()

# Questão 1
def test_questao_1():

    characters_data = [
        {"name": "Draven Ashford",      "char_class": "Guerreiro", "level": 12, "region": "Costa Ocidental",       "guild": "Companhia do Horizonte"},
        {"name": "Callum Driftwood",    "char_class": "Ladino",    "level": 5,  "region": "Costa Ocidental",       "guild": "Companhia do Horizonte"},
        {"name": "Lyra Nightwhisper",   "char_class": "Ladino",    "level": 15, "region": "Terras Sombrias",       "guild": "Irmandade das Sombras"},
        {"name": "Seraphina Voss",      "char_class": "Mago",      "level": 20, "region": "Reino Central",         "guild": "Ordem da Chama"},
        {"name": "Theron Brightblade",  "char_class": "Clérigo",   "level": 18, "region": "Reino Central",         "guild": "Ordem da Chama"},
        {"name": "Mira Stoneforge",     "char_class": "Guerreiro", "level": 16, "region": "Cordilheira do Norte",  "guild": "Forjadores de Ferro"},
        {"name": "Elena Marsh",         "char_class": "Arqueiro",  "level": 9,  "region": "Costa Ocidental",       "guild": "Companhia do Horizonte"},
        {"name": "Grom Ironfist",       "char_class": "Guerreiro", "level": 12, "region": "Cordilheira do Norte",  "guild": "Forjadores de Ferro"},
        {"name": "Nyx Shadowmere",      "char_class": "Ladino",    "level": 11, "region": "Terras Sombrias",       "guild": "Irmandade das Sombras"},
        {"name": "Alaric Frost",        "char_class": "Mago",      "level": 14, "region": "Vale da Morte",         "guild": "Caçadores do Vale"},
        {"name": "Bianca Thornwood",    "char_class": "Clérigo",   "level": 7,  "region": "Vale da Morte",         "guild": "Caçadores do Vale"},
        {"name": "Finn Rivera",         "char_class": "Arqueiro",  "level": 12, "region": "Costa Ocidental",       "guild": "Companhia do Horizonte"},
        {"name": "Vesper Nightingale",  "char_class": "Ladino",    "level": 19, "region": "Reino Central",         "guild": "Ordem da Chama"},
        {"name": "Roran Anvil",         "char_class": "Guerreiro", "level": 6,  "region": "Cordilheira do Norte",  "guild": "Forjadores de Ferro"},
        {"name": "Isolde Emberheart",   "char_class": "Mago",      "level": 17, "region": "Terras Sombrias",       "guild": "Irmandade das Sombras"},
    ]

    input_region = "Costa Ocidental"

    expected = [
        {"name": "Draven Ashford", "level": 12},
        {"name": "Finn Rivera", "level": 12},
        {"name": "Elena Marsh", "level": 9},
        {"name": "Callum Driftwood", "level": 5}
    ]

    for character_data in characters_data:
        character = Character(character_data['name'], character_data['char_class'], character_data['level'], character_data['region'], character_data['guild'])
        character_dao.add_character(character=character)

    output = character_dao.get_characters_by_region(region=input_region)

    assert expected == output

# Questão 2
def test_questao_2():

    guilds_data = [
        {"name": "Ordem da Chama",         "region": "Reino Central",         "specialty": "Magia"},
        {"name": "Irmandade das Sombras",  "region": "Terras Sombrias",       "specialty": "Furtividade"},
        {"name": "Companhia do Horizonte", "region": "Costa Ocidental",       "specialty": "Exploração"},
        {"name": "Forjadores de Ferro",    "region": "Cordilheira do Norte",  "specialty": "Combate"},
        {"name": "Caçadores do Vale",      "region": "Vale da Morte",         "specialty": "Rastreamento"},
    ]

    items_data = [
        {"name": "Cajado Arcano",     "type": "Arma",      "rarity": "Raro",    "required_specialty": ["Magia"]},
        {"name": "Grimório Antigo",   "type": "Artefato",  "rarity": "Épico",   "required_specialty": ["Magia"]},
        {"name": "Adaga Envenenada",  "type": "Arma",      "rarity": "Raro",    "required_specialty": ["Furtividade"]},
        {"name": "Capa das Sombras",  "type": "Armadura",  "rarity": "Épico",   "required_specialty": ["Furtividade"]},
        {"name": "Bússola Encantada", "type": "Artefato",  "rarity": "Incomum", "required_specialty": ["Exploração"]},
        {"name": "Mapa do Tesouro",   "type": "Artefato",  "rarity": "Raro",    "required_specialty": ["Exploração", "Rastreamento"]},
        {"name": "Martelo de Guerra", "type": "Arma",      "rarity": "Raro",    "required_specialty": ["Combate"]},
        {"name": "Escudo Rúnico",     "type": "Armadura",  "rarity": "Épico",   "required_specialty": ["Combate"]},
        {"name": "Arco Longo",        "type": "Arma",      "rarity": "Comum",   "required_specialty": ["Rastreamento", "Exploração"]},
        {"name": "Poção de Cura",     "type": "Poção",     "rarity": "Comum",   "required_specialty": ["Magia", "Combate", "Furtividade", "Exploração", "Rastreamento"]},
    ]

    input_guild_name = "Companhia do Horizonte"

    expected = [
        {"name": "Arco Longo", "type": "Arma"},
        {"name": "Bússola Encantada", "type": "Artefato"},
        {"name": "Mapa do Tesouro", "type": "Artefato"},
        {"name": "Poção de Cura", "type": "Poção"}
    ]

    for guild_data in guilds_data:
        guild = Guild(guild_data['name'], guild_data['region'], guild_data['specialty'])
        guild_dao.add_guild(guild=guild)

    for item_data in items_data:
        item = Item(item_data['name'], item_data['type'], item_data['rarity'], item_data['required_specialty'])
        item_dao.add_item(item=item)

    output = item_dao.get_items_by_guild_specialty(guild_name=input_guild_name)

    assert expected == output
