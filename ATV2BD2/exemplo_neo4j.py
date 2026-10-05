from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

def clean(tx):
    try:
        tx.run("MATCH(n) DETACH DELETE n;")
    except:
        print("Erro ao excluir...")
        raise

def get_movies(tx):
    query = """
        MATCH (n) RETURN DISTINCT(n.title) AS title;
    """
    try:
        result = tx.run(query)
        return [{
            'title':row['title']
        } for row in result]

    except ServiceUnavailable as exception:

        print("{query} raised an error: \n {exception}".format(query=query, exception=exception))
        raise

def create_movie(tx, par_title, par_duration):
    query = """
        CREATE (n:Movie{
            title: $title_query,
            duration: $duration_query
        })
        RETURN 
            n.title AS title;
    """
    try:
        result = tx.run(
            query, 
            title_query = par_title,
            duration_query = par_duration
        )
        return [{
            'title':row['title']
        } for row in result]

    except ServiceUnavailable as exception:

        print("{query} raised an error: \n {exception}".format(query=query, exception=exception))
        raise


def main():
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "neo4jtest"

    driver = GraphDatabase.driver(uri, auth=(user, password))

    # print("Limpando dados...")
    # with driver.session() as session:
    #     session.execute_write(clean)

    # print("Criando o banco de dados...")
    # with driver.session() as session:
    #     result = session.execute_write(
    #         create_movie, 
    #         "Teste4",
    #         200
    #     )
    #     if len(result):
    #         for row in result:
    #             print(f"Filme {row['title']} criado.")
    #     else:
    #         print("Erro ao criar banco de dados.")
    #         driver.close()
    #         return

    with driver.session() as session:
        result = session.execute_read(get_movies)
        quantidade = len(result)
        if quantidade > 0:
            print(f"Quantidade de filmes: {quantidade}")
            for row in result:
                print(row['title'])
        else:
            print(quantidade)
            print("Nenhum filme encontrado.")

if __name__ == "__main__":
    main()