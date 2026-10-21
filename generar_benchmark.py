import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# 1. Definir las 15 consultas del benchmark
consultas = [
    {"query_id": "Q01", "difficulty_level": 1, "query": "inflación y tasas de interés en méxico"},
    {"query_id": "Q02", "difficulty_level": 1, "query": "nueva misión espacial de la nasa"},
    {"query_id": "Q03", "difficulty_level": 1, "query": "exposición de arte en el museo"},
    {"query_id": "Q04", "difficulty_level": 1, "query": "crecimiento del producto interno bruto"},
    {"query_id": "Q05", "difficulty_level": 1, "query": "descubrimiento de nueva especie de dinosaurio"},
    {"query_id": "Q06", "difficulty_level": 2, "query": "aumento en el costo de los alimentos"},
    {"query_id": "Q07", "difficulty_level": 2, "query": "nuevos tratamientos médicos para el cáncer"},
    {"query_id": "Q08", "difficulty_level": 2, "query": "festival internacional de cine y cultura"},
    {"query_id": "Q09", "difficulty_level": 2, "query": "inversiones extranjeras en empresas de tecnología"},
    {"query_id": "Q10", "difficulty_level": 2, "query": "avances en energía renovable solar"},
    {"query_id": "Q11", "difficulty_level": 3, "query": "impacto económico por el clima extremo en cosechas"},
    {"query_id": "Q12", "difficulty_level": 3, "query": "reemplazo de trabajadores por inteligencia artificial"},
    {"query_id": "Q13", "difficulty_level": 3, "query": "políticas gubernamentales para proteger el patrimonio histórico"},
    {"query_id": "Q14", "difficulty_level": 3, "query": "empresas al borde de la quiebra por mala gestión"},
    {"query_id": "Q15", "difficulty_level": 3, "query": "ética en la manipulación genética humana"}
]

# 2. Generar el archivo queries.tsv
df_queries = pd.DataFrame(consultas)
df_queries.to_csv("queries.tsv", sep="\t", index=False)
print("✅ Archivo queries.tsv generado exitosamente.")

# 3. Leer tu corpus más reciente para generar el qrels.tsv automáticamente
try:
    df_corpus = pd.read_csv("news_raw_corpus.tsv", sep="\t")
    
    # Combinamos título y descripción para buscar mejor
    df_corpus['texto_completo'] = df_corpus['title'].fillna('') + ' ' + df_corpus['description'].fillna('')
    
    # Vectorizar rápidamente para encontrar similitudes
    vectorizador = TfidfVectorizer()
    matriz_tfidf = vectorizador.fit_transform(df_corpus['texto_completo'])
    
    qrels = []
    
    for q in consultas:
        # Transformar la consulta al mismo espacio
        vector_q = vectorizador.transform([q['query']])
        similitudes = cosine_similarity(vector_q, matriz_tfidf).flatten()
        
        # Obtener los top 5 documentos para esta consulta
        indices_top = similitudes.argsort()[::-1][:5]
        
        for i, idx in enumerate(indices_top):
            score = similitudes[idx]
            # Solo guardamos si hay una similitud real (evita guardar basura en consultas como "dinosaurios")
            if score > 0.05:
                # Asignamos relevancia 2 a los dos primeros lugares, y 1 a los siguientes
                relevancia = 2 if i < 2 else 1
                doc_id = df_corpus.iloc[idx]['id']
                qrels.append({"query_id": q['query_id'], "document_id": doc_id, "relevance": relevancia})
                
    # Generar el archivo qrels.tsv
    df_qrels = pd.DataFrame(qrels)
    df_qrels.to_csv("qrels.tsv", sep="\t", index=False)
    print(f"✅ Archivo qrels.tsv generado exitosamente con {len(df_qrels)} juicios de relevancia adaptados a tu corpus.")

except FileNotFoundError:
    print("❌ Error: No se encontró 'news_raw_corpus.tsv'. Asegúrate de que el nombre sea correcto.")