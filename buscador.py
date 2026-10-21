import pandas as pd
import spacy
import re
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# 1. Cargar el modelo de NLP (el mismo que en la normalización)
print("Cargando modelo de lenguaje...")
nlp = spacy.load("es_core_news_sm")

# 2. Funciones de limpieza y normalización (EXACTAMENTE IGUALES al paso anterior)
def limpieza_texto(texto):
    if not isinstance(texto, str): return ""
    texto = re.sub(r'http[s]?://\S+', '', texto)
    texto = re.sub(r'[^\w\sáéíóúÁÉÍÓÚñÑüÜ]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def normalizacion_texto(texto):
    if not isinstance(texto, str) or texto == "": return ""
    texto = texto.lower()
    doc = nlp(texto)
    tokens_procesados = []
    pos_a_eliminar = {"DET", "ADP", "CCONJ", "SCONJ", "PRON"}
    for token in doc:
        if token.pos_ not in pos_a_eliminar:
            tokens_procesados.append(token.lemma_)
    return " ".join(tokens_procesados)

def procesar_consulta(consulta):
    texto_limpio = limpieza_texto(consulta)
    return normalizacion_texto(texto_limpio)

# 3. Cargar el corpus original (para mostrar los datos reales al usuario) y los modelos PKL
print("Cargando corpus y modelos vectoriales...")
df_corpus = pd.read_csv("news_raw_corpus.tsv", sep="\t") 

# Aquí indicamos qué modelo usar (Ejemplo: TF-IDF sobre la Descripción)
# Puedes cambiar estos archivos para probar Frecuencia o Binario sobre el Título
vectorizador = joblib.load('desc_tfidf_vectorizer.pkl')
matriz_documentos = joblib.load('desc_tfidf_matrix.pkl')

print("\n" + "="*50)
print(" SISTEMA DE RECUPERACIÓN DE NOTICIAS V1.0")
print("="*50)

# 4. Bucle principal del buscador
while True:
    consulta_usuario = input("\nIngresa tu búsqueda (o 'salir' para terminar): ")
    
    if consulta_usuario.lower() == 'salir':
        break
        
    # A) Aplicar el mismo proceso de normalización
    consulta_normalizada = procesar_consulta(consulta_usuario)
    print(f"Consulta normalizada: [{consulta_normalizada}]")
    
    # B) Representar la consulta en el espacio vectorial
    vector_consulta = vectorizador.transform([consulta_normalizada])
    
    # C) Calcular la similitud del coseno
    similitudes = cosine_similarity(vector_consulta, matriz_documentos).flatten()
    
    # D) Ordenar los resultados en orden descendente y obtener los 10 mejores
    indices_top10 = similitudes.argsort()[::-1][:10]
    
    # E) Mostrar los 10 documentos más similares, incluyendo su puntuación (score)
    print("\n--- TOP 10 RESULTADOS ---")
    for i, idx in enumerate(indices_top10):
        score = similitudes[idx]
        
        # Omitir resultados con score de 0 (ninguna similitud)
        if score == 0:
            if i == 0: print("No se encontraron documentos relevantes para esta búsqueda.")
            break
            
        doc_id = df_corpus.iloc[idx]['id']
        titulo = df_corpus.iloc[idx]['title']
        fuente = df_corpus.iloc[idx]['source']
        
        print(f"{i+1}. Score: {score:.4f} | {fuente}")
        print(f"   Título: {titulo}")
        print(f"   ID: {doc_id}\n")