Librerias
pip install feedparser pandas spacy scikit-learn joblib
Modelo de lenguaje en español para spacy
-m spacy download es_core_news_sm

Flujo de ejecución
1 rss_feedparser_v2
2 limpiar_duplicados
3 normalizacion
4 vsm
5 buscador (se puede omitir)
6 generar_benchmark
7 evalucion
