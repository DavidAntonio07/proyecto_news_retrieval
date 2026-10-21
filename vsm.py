import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# 1. Cargar el corpus normalizado más reciente
nombre_archivo = "news_normalized_corpus.tsv"
df = pd.read_csv(nombre_archivo, sep="\t")

# Manejar posibles valores nulos que puedan romper el vectorizador
df['title'] = df['title'].fillna("")
df['description'] = df['description'].fillna("")

# 2. Vectorización del Título
print("Generando representaciones para Títulos...")
titulo_text = df['title']

# Frecuencia (Unigramas y Bigramas)
freq_vec_title = CountVectorizer(ngram_range=(1, 2))
matriz_freq_title = freq_vec_title.fit_transform(titulo_text)

# Binario (Unigramas y Bigramas)
bin_vec_title = CountVectorizer(ngram_range=(1, 2), binary=True)
matriz_bin_title = bin_vec_title.fit_transform(titulo_text)

# TF-IDF (Unigramas y Bigramas)
tfidf_vec_title = TfidfVectorizer(ngram_range=(1, 2))
matriz_tfidf_title = tfidf_vec_title.fit_transform(titulo_text)

# 3. Vectorización de la Descripción/Cuerpo
print("Generando representaciones para Descripciones...")
desc_text = df['description']

# Frecuencia (Unigramas y Bigramas)
freq_vec_desc = CountVectorizer(ngram_range=(1, 2))
matriz_freq_desc = freq_vec_desc.fit_transform(desc_text)

# Binario (Unigramas y Bigramas)
bin_vec_desc = CountVectorizer(ngram_range=(1, 2), binary=True)
matriz_bin_desc = bin_vec_desc.fit_transform(desc_text)

# TF-IDF (Unigramas y Bigramas)
tfidf_vec_desc = TfidfVectorizer(ngram_range=(1, 2))
matriz_tfidf_desc = tfidf_vec_desc.fit_transform(desc_text)

# 4. Guardar los vectorizadores y las matrices en archivos PKL
print("Guardando archivos PKL...")

# Modelos de Título
joblib.dump(freq_vec_title, 'title_freq_vectorizer.pkl')
joblib.dump(matriz_freq_title, 'title_freq_matrix.pkl')
joblib.dump(bin_vec_title, 'title_bin_vectorizer.pkl')
joblib.dump(matriz_bin_title, 'title_bin_matrix.pkl')
joblib.dump(tfidf_vec_title, 'title_tfidf_vectorizer.pkl')
joblib.dump(matriz_tfidf_title, 'title_tfidf_matrix.pkl')

# Modelos de Descripción
joblib.dump(freq_vec_desc, 'desc_freq_vectorizer.pkl')
joblib.dump(matriz_freq_desc, 'desc_freq_matrix.pkl')
joblib.dump(bin_vec_desc, 'desc_bin_vectorizer.pkl')
joblib.dump(matriz_bin_desc, 'desc_bin_matrix.pkl')
joblib.dump(tfidf_vec_desc, 'desc_tfidf_vectorizer.pkl')
joblib.dump(matriz_tfidf_desc, 'desc_tfidf_matrix.pkl')

print("Proceso completado. Modelos y matrices guardados con éxito.")