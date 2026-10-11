import feedparser
import csv
import uuid
import requests
from datetime import datetime 

fuentes_rss = [
    {
        "url": "https://www.reforma.com/rss/ciencia.xml",
        "source": "Reforma",
        "category": "Ciencia"
    }
]

nombre_archivo = 'news_raw_corpus.tsv'

# Configuramos los Headers para simular un navegador web real y evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_tsv:
    escritor_tsv = csv.writer(archivo_tsv, delimiter='\t')
    escritor_tsv.writerow(['id', 'title', 'description', 'source', 'category', 'date', 'url', 'retrieved_date'])
    
    for fuentes in fuentes_rss:
        try: 
            # 1. Hacemos la petición HTTP disfrazada de navegador
            respuesta = requests.get(fuentes['url'], headers=headers, timeout=15)
            
            # 2. Le pasamos el contenido descargado a feedparser
            feed = feedparser.parse(respuesta.content)
            
            # Imprimimos cuántos artículos encontró
            print(f"Procesando: {fuentes['source']} - {fuentes['category']} (Artículos encontrados: {len(feed.entries)})")
            
            for entry in feed.entries:
                doc_id = str(uuid.uuid4())
                
                # Limpiamos saltos de línea y tabulaciones para no romper el TSV
                raw_title = entry.get("title", "No title").replace('\n', ' ').replace('\t', ' ')
                raw_desc = entry.get("description", entry.get("summary", "No description")).replace('\n', ' ').replace('\t', ' ')
                
                raw_date = entry.get("published", entry.get("updated", "No date"))
                raw_url = entry.get("link", "")
                retrived_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                escritor_tsv.writerow([doc_id, raw_title, raw_desc, fuentes['source'], fuentes['category'], raw_date, raw_url, retrived_at])
                
        except Exception as e:
            print(f"Error procesando el feed {fuentes['url']}: {e}")
            
    print(f"Archivo {nombre_archivo} generado con éxito.")