import pandas as pd
import joblib
import spacy
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

print("Cargando modelos y datos para la evaluación...")
nlp = spacy.load("es_core_news_sm")
vectorizador = joblib.load('desc_tfidf_vectorizer.pkl')
matriz_documentos = joblib.load('desc_tfidf_matrix.pkl')

df_queries = pd.read_csv("queries.tsv", sep="\t")
df_qrels = pd.read_csv("qrels.tsv", sep="\t")
df_corpus = pd.read_csv("news_raw_corpus.tsv", sep="\t")

# Funciones de normalización idénticas a tu buscador
def limpiar_y_normalizar(texto):
    if not isinstance(texto, str): return ""
    texto = re.sub(r'http[s]?://\S+', '', texto)
    texto = re.sub(r'[^\w\sáéíóúÁÉÍÓÚñÑüÜ]', ' ', texto).lower()
    texto = re.sub(r'\s+', ' ', texto).strip()
    doc = nlp(texto)
    return " ".join([t.lemma_ for t in doc if t.pos_ not in {"DET", "ADP", "CCONJ", "SCONJ", "PRON"}])

rankings = []
metricas = []

print("\nEjecutando consultas y calculando métricas @10...\n")

for _, row in df_queries.iterrows():
    qid = row['query_id']
    consulta_texto = row['query']
    
    # 1. Ejecutar la búsqueda
    consulta_norm = limpiar_y_normalizar(consulta_texto)
    vec_consulta = vectorizador.transform([consulta_norm])
    similitudes = cosine_similarity(vec_consulta, matriz_documentos).flatten()
    
    # Obtener el Top 10
    top_10_indices = similitudes.argsort()[::-1][:10]
    top_10_docs = []
    
    for rank, idx in enumerate(top_10_indices):
        score = similitudes[idx]
        if score > 0:  # Solo contar si hay alguna similitud
            doc_id = df_corpus.iloc[idx]['id']
            top_10_docs.append(doc_id)
            # Guardar para rankings.tsv
            rankings.append({"query_id": qid, "document_id": doc_id, "score": score, "rank": rank + 1})
            
    # 2. Calcular Métricas @10 para esta consulta
    # Documentos que el sistema considera relevantes (Top 10)
    recuperados = set(top_10_docs)
    
    # Documentos que REALMENTE son relevantes (según qrels.tsv)
    relevantes_reales = set(df_qrels[df_qrels['query_id'] == qid]['document_id'])
    
    if len(relevantes_reales) > 0:
        # Intersección: Aciertos
        aciertos = recuperados.intersection(relevantes_reales)
        
        # Precision@10: ¿Cuántos de los 10 que traje son correctos?
        precision = len(aciertos) / 10.0
        
        # Recall@10: De todos los correctos que existen, ¿cuántos logré traer?
        recall = len(aciertos) / len(relevantes_reales)
        
        # F1@10: Media armónica
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        metricas.append({"query_id": qid, "Precision@10": precision, "Recall@10": recall, "F1@10": f1})
        print(f"{qid} | Precisión: {precision:.2f} | Recall: {recall:.2f} | F1: {f1:.2f}")

# 3. Guardar Rankings y mostrar el promedio
df_rankings = pd.DataFrame(rankings)
df_rankings.to_csv("rankings.tsv", sep="\t", index=False)
print("\n✅ Archivo rankings.tsv generado exitosamente.")

df_metricas = pd.DataFrame(metricas)
print("\n=== PROMEDIO GLOBAL DEL SISTEMA ===")
print(f"Mean Precision@10: {df_metricas['Precision@10'].mean():.4f}")
print(f"Mean Recall@10:    {df_metricas['Recall@10'].mean():.4f}")
print(f"Mean F1@10:        {df_metricas['F1@10'].mean():.4f}")