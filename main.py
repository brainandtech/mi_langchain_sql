import mysql.connector
#from langchain.embeddings import EmbeddingFactory
#from langchain.matchers import EmbeddingMatcher

# Establecer la conexión con la base de datos MySQL
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Telcosa92",
    database="general"
)
cursor = cnx.cursor()

# Consulta para obtener los datos de la tabla MENSAJES
query = "SELECT TITULO, RESPUESTA, VERACIDAD FROM noticias"
cursor.execute(query)
results = cursor.fetchall()

# Crear una lista de documentos para el embedding
documents = []
for row in results:
    titulo = row[0]
    respuesta = row[1]
    veracidad = row[2]
    # Concatenar los campos relevantes en un solo documento
    document = f"{titulo} {respuesta} {veracidad}"
    documents.append(document)

# Crear el objeto EmbeddingFactory y cargar el modelo pre-entrenado
embedding_factory = EmbeddingFactory()
embedding_factory.load_model('modelo_embedding_preentrenado')

# Calcular los embeddings para los documentos
embeddings = embedding_factory.encode(documents)

# Bucle de preguntas
while True:
    pregunta = input("Haz tu pregunta (o escribe 'salir' para terminar): ")
    if pregunta.lower() == "salir":
        break

    # Calcular el embedding para la pregunta
    pregunta_embedding = embedding_factory.encode([pregunta])[0]

    # Utilizar el matcher de embeddings para encontrar la respuesta más cercana
    matcher = EmbeddingMatcher(embeddings)
    best_match_index = matcher.get_best_match_index(pregunta_embedding)

    # Obtener la respuesta correspondiente al mejor match
    best_match_document = documents[best_match_index]
    # Aquí puedes realizar el procesamiento necesario para extraer la información relevante
    # de la respuesta y mostrarla al usuario



# Cerrar la conexión con la base de datos
cursor.close()
cnx.close()
