import feedparser
import csv
import uuid
from datetime import datetime 


fuentes_rss = [
    {
        "url": "https://www.reforma.com/rss/ciencia.xml",
        "source": "Reforma",
        "category": "Ciencia"
    },
]

nombre_archivo = 'news_raw_corpus.csv'

with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_tsv:
    escritor_tsv = csv.writer(archivo_tsv, delimiter='\t')
    escritor_tsv.writerow(['id', 'title', 'description/body', 'source', 'category', 'date', 'url', 'retrieved_date '])
    
    for fuentes in fuentes_rss:
        print(f"Procesando: {fuentes['source']} - {fuentes['category']}")
        
        try: 
            feed = feedparser.parse(fuentes['url'])
            
            for entry in feed.entries:
                #1. Genera ID único para cada noticia
                doc_id = str(uuid.uuid4())
                
                #2. Extraer título
                raw_title = entry.get("title", "No title")
                
                #3. Extraer descripción
                raw_desc = entry.get ("description", entry.get("summary", "No description"))
                
                #4. Extraer fecha de publicación
                raw_date = entry.get("published", entry.get("updated", "No date"))
                
                #5. Extraer URL original
                raw_url =entry.get("link", "")
                
                #6. Fecha de recuperación (Timestamp actual)
                retrived_at =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                #7. Escribir la fila en el TSV
                escritor_tsv.writerow(
                    [
                        doc_id,
                        raw_title,
                        raw_desc,
                        fuentes['source'],
                        fuentes['category'],
                        raw_date,
                        raw_url,
                        retrived_at
                    ]
                )
        except Exception as e:
            print(f"Error procesando el feed {fuentes['url']}: {e}")
    print(f"Archivo {nombre_archivo} generado con éxito.")