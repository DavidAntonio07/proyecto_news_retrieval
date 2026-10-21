import feedparser
import csv
import uuid
from datetime import datetime
import os
import logging

# Configurar el registro de errores (log)
logging.basicConfig(
    filename='scraping_errors.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

fuentes_rss = [
    {"url": "https://www.jornada.com.mx/rss/cultura.xml?v=1", "source": "La Jornada", "category": "Cultura"},
    {"url": "https://www.jornada.com.mx/rss/ciencias.xml?v=1", "source": "La Jornada", "category": "Ciencias"},
    {"url": "https://www.jornada.com.mx/rss/economia.xml?v=1", "source": "La Jornada", "category": "Economía"},
    {"url": "https://www.reforma.com/rss/ciencia.xml", "source": "Reforma", "category": "Ciencia"},
    {"url": "https://www.reforma.com/rss/cultura.xml", "source": "Reforma", "category": "Cultura"},
    {"url": "https://www.reforma.com/rss/negocios.xml", "source": "Reforma", "category": "Negocios"},
    {"url": "https://www.eluniversal.com.mx/rss/ciencia.xml", "source": "El Universal", "category": "Ciencia"},
    {"url": "https://www.eluniversal.com.mx/rss/cultura.xml", "source": "El Universal", "category": "Cultura"},
    {"url": "https://www.eluniversal.com.mx/rss/economia.xml", "source": "El Universal", "category": "Economía"},
    {"url": "https://www.eluniversal.com.mx/rss/negocios.xml", "source": "El Universal", "category": "Negocios"},
    {"url": "https://www.milenio.com/rss/ciencia.xml", "source": "Milenio", "category": "Ciencia"},
    {"url": "https://www.milenio.com/rss/cultura.xml", "source": "Milenio", "category": "Cultura"},
    {"url": "https://www.milenio.com/rss/economia.xml", "source": "Milenio", "category": "Economía"},
    {"url": "https://www.milenio.com/rss/negocios.xml", "source": "Milenio", "category": "Negocios"},
    {"url": "https://www.elfinanciero.com.mx/rss/ciencia.xml", "source": "El Financiero", "category": "Ciencia"},
    {"url": "https://www.elfinanciero.com.mx/rss/cultura.xml", "source": "El Financiero", "category": "Cultura"},
    {"url": "https://www.elfinanciero.com.mx/rss/economia.xml", "source": "El Financiero", "category": "Economía"},
    {"url": "https://www.elfinanciero.com.mx/rss/negocios.xml", "source": "El Financiero", "category": "Negocios"},
    {"url": "https://www.20minutos.com.mx/rss/ciencia.xml", "source": "20 Minutos", "category": "Ciencia"},
    {"url": "https://www.20minutos.com.mx/rss/cultura.xml", "source": "20 Minutos", "category": "Cultura"},
    {"url": "https://www.20minutos.com.mx/rss/economia.xml", "source": "20 Minutos", "category": "Economía"},
    {"url": "https://www.20minutos.com.mx/rss/negocios.xml", "source": "20 Minutos", "category": "Negocios"},
    {"url": "https://www.elsoldemexico.com.mx/rss/ciencia.xml", "source": "El Sol de México", "category": "Ciencia"},
    {"url": "https://www.elsoldemexico.com.mx/rss/cultura.xml", "source": "El Sol de México", "category": "Cultura"},
    {"url": "https://www.elsoldemexico.com.mx/rss/economia.xml", "source": "El Sol de México", "category": "Economía"},
    {"url": "https://www.elsoldemexico.com.mx/rss/negocios.xml", "source": "El Sol de México", "category": "Negocios"},
    {"url": "https://www.mural.com.mx/rss/ciencia.xml", "source": "Mural", "category": "Ciencia"},
    {"url": "https://www.mural.com.mx/rss/cultura.xml", "source": "Mural", "category": "Cultura"},
    {"url": "https://www.mural.com.mx/rss/economia.xml", "source": "Mural", "category": "Economía"},
    {"url": "https://www.mural.com.mx/rss/negocios.xml", "source": "Mural", "category": "Negocios"},
    {"url": "https://www.altonivel.com.mx/rss/ciencia.xml", "source": "Alto Nivel", "category": "Ciencia"},
    {"url": "https://www.altonivel.com.mx/rss/cultura.xml", "source": "Alto Nivel", "category": "Cultura"},
    {"url": "https://www.altonivel.com.mx/rss/economia.xml", "source": "Alto Nivel", "category": "Economía"},
    {"url": "https://www.altonivel.com.mx/rss/negocios.xml", "source": "Alto Nivel", "category": "Negocios"}
]

nombre_archivo = "news_raw_corpus.tsv"
archivo_existe = os.path.exists(nombre_archivo)

with open(nombre_archivo, mode="a", newline="", encoding="utf-8") as archivo_tsv:
    escritor_tsv = csv.writer(archivo_tsv, delimiter="\t")
    
    # Escribir encabezados solo si el archivo no existe previamente
    if not archivo_existe:
        escritor_tsv.writerow(["id", "title", "description", "source", "category", "date", "url", "retrieved_at"])

    for fuente in fuentes_rss:
        print(f"Consultando: {fuente['source']} - {fuente['category']}...")
        
        try:
            feed = feedparser.parse(fuente['url'])
            
            # Verificar si feedparser detectó un error a nivel HTTP o de parseo
            if getattr(feed, 'bozo', 0) == 1 or ('status' in feed and getattr(feed, 'status', 200) >= 400):
                logging.error(f"Error al acceder o parsear {fuente['url']}")
                continue

            for entry in feed.entries:
                doc_id = str(uuid.uuid4())
                
                title = entry.get("title", "No title").replace("\n", " ").replace("\t", " ")
                content = entry.get("description", entry.get("summary", "No content")).replace("\n", " ").replace("\t", " ")
                
                date = entry.get("published", entry.get("updated", "No date"))
                url = entry.get("link", "No url")
                retrieved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                escritor_tsv.writerow([doc_id, title, content, fuente['source'], fuente['category'], date, url, retrieved_at])
                
        except Exception as e:
            logging.error(f"Excepción procesando {fuente['url']}: {e}")

print(f"\nExtracción finalizada. Los datos crudos se guardaron en: {nombre_archivo}")