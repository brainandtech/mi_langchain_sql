import mysql.connector
#from langchain import LangChain
#from openaiembeddings import OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
#from openai_chat import ChatOpenAI
from langchain.chat_models import ChatOpenAI
import requests.exceptions

'''
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone, Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
'''


# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': 'Telcosa92',
    'host': '127.0.0.1',
    'database': 'general',
    'raise_on_warnings': True
}

try:
    # Establecer conexión con la base de datos
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Consulta SQL para obtener los datos de la tabla MENSAJES
    query = "SELECT TITULO, RESPUESTA, VERACIDAD FROM noticias"

    # Ejecutar la consulta
    cursor.execute(query)

    # Crear una instancia de LangChain
    
    #lc = LangChain()

    # Crear una instancia de OpenAIEmbeddings
    embeddings = OpenAIEmbeddings()

    # Recorrer los resultados y agregar los textos a LangChain
    for (titulo, codigo, veracidad) in cursor:
        # Obtener los embeddings de los textos utilizando OpenAIEmbeddings
        titulo_embedding = embeddings.encode(titulo)
        codigo_embedding = embeddings.encode(codigo)
        veracidad_embedding = embeddings.encode(veracidad)

        # Agregar los embeddings a LangChain
        lc.add_embedding(titulo_embedding)
        lc.add_embedding(codigo_embedding)
        lc.add_embedding(veracidad_embedding)

    # Cerrar la conexión con la base de datos
    cursor.close()
    cnx.close()

    # Tu clave de API de OpenAI
    api_key = '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'

    # Crear una instancia de ChatOpenAI con tu clave de API
    chat_openai = ChatOpenAI(api_key)

    # Bucle para hacer preguntas
    while True:
        question = input("Ingrese su pregunta (o escriba 'salir' para terminar): ")
        if question.lower() == 'salir':
            break

        try:
            # Obtener la respuesta de ChatOpenAI
            answer = chat_openai.ask(question)

            print("Respuesta: " + answer)
        except requests.exceptions.RequestException as e:
            print("Error al conectarse a la API de OpenAI:", e)

except mysql.connector.Error as err:
    print("Error al conectar a la base de datos:", err)
