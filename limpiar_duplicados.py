import pandas as pd

# 1. Limpiar el corpus crudo
archivo_crudo = "news_raw_corpus.tsv"
df_raw = pd.read_csv(archivo_crudo, sep="\t")
df_raw_limpio = df_raw.drop_duplicates(subset=['title', 'source'])
df_raw_limpio.to_csv(archivo_crudo, sep="\t", index=False)
print(f"Corpus crudo actualizado: de {len(df_raw)} bajó a {len(df_raw_limpio)} noticias únicas.")

# 2. Limpiar el corpus normalizado
archivo_norm = "news_normalized_corpus.tsv"
df_norm = pd.read_csv(archivo_norm, sep="\t")
df_norm_limpio = df_norm.drop_duplicates(subset=['title', 'source'])
df_norm_limpio.to_csv(archivo_norm, sep="\t", index=False)
print(f"Corpus normalizado actualizado: de {len(df_norm)} bajó a {len(df_norm_limpio)} noticias únicas.")