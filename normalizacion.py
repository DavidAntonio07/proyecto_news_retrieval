import pandas as pd
import spacy
import re

# Cargar el modelo de NLP en español
nlp = spacy.load("es_core_news_sm")

# Leer el corpus crudo
df = pd.read_csv("news_raw_corpus.tsv", sep="\t")

# ==========================================
# 1. HOMOLOGACIÓN
# ==========================================
# Damos un significado único a datos que vienen de diferentes criterios.
print("Aplicando Homologación...")
df['category'] = df['category'].replace({
    'Ciencias': 'Ciencia',
    'Economia': 'Economía',
    'Negocios': 'Economía' # (Opcional) Si el profesor pidiera reducir categorías similares
})

# ==========================================
# 2. LIMPIEZA
# ==========================================
# Eliminar URLs, caracteres especiales, símbolos extraños y espacios innecesarios.
def limpieza_texto(texto):
    if not isinstance(texto, str):
        return ""
    
    # Eliminar URLs (http:// o https://)
    texto = re.sub(r'http[s]?://\S+', '', texto)
    
    # Eliminar caracteres especiales y símbolos (dejamos solo letras, números y espacios)
    # El rango incluye letras acentuadas y la ñ
    texto = re.sub(r'[^\w\sáéíóúÁÉÍÓÚñÑüÜ]', ' ', texto)
    
    # Eliminar espacios en blanco innecesarios o múltiples
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

print("Aplicando Limpieza...")
df['title_clean'] = df['title'].apply(limpieza_texto)
df['description_clean'] = df['description'].apply(limpieza_texto)

# ==========================================
# 3. NORMALIZACIÓN
# ==========================================
# Convertir a minúsculas, lematizar y eliminar stopwords por categoría gramatical.
def normalizacion_texto(texto):
    if not isinstance(texto, str) or texto == "":
        return ""
    
    # Convertir todo el texto a minúsculas
    texto = texto.lower()
    
    # Procesar con spaCy
    doc = nlp(texto)
    tokens_procesados = []
    
    # Categorías gramaticales a eliminar según el documento:
    # DET (artículos), ADP (preposiciones), CCONJ/SCONJ (conjunciones), PRON (pronombres)
    pos_a_eliminar = {"DET", "ADP", "CCONJ", "SCONJ", "PRON"}
    
    for token in doc:
        if token.pos_ not in pos_a_eliminar:
            # Aplicar lematización (reducir palabras a su raíz)
            tokens_procesados.append(token.lemma_)
            
    return " ".join(tokens_procesados)

print("Aplicando Normalización...")
df['title'] = df['title_clean'].apply(normalizacion_texto)
df['description'] = df['description_clean'].apply(normalizacion_texto)

# Eliminar las columnas temporales de limpieza
df = df.drop(columns=['title_clean', 'description_clean'])

# ==========================================
# GUARDADO
# ==========================================
archivo_salida = "news_normalized_corpus.tsv"
df.to_csv(archivo_salida, sep="\t", index=False)

print(f"\nProceso completado con éxito. Archivo guardado como: {archivo_salida}")