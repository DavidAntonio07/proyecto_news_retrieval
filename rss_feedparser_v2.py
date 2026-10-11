# Script para extraer noticias de múltiples fuentes RSS y guardarlas en un archivo TSV.
import feedparser
import csv
import uuid
from datetime import datetime

fuentes_rss = [
    {
        "url": "https://www.jornada.com.mx/rss/cultura.xml?v=1",
        "source": "La Jornada",
        "category": "Cultura"
    },
    {
        "url": "https://www.jornada.com.mx/rss/ciencias.xml?v=1",
        "source": "La Jornada",
        "category": "Ciencias"
    },
    {
        "url": "https://www.jornada.com.mx/rss/economia.xml?v=1",
        "source": "La Jornada",
        "category": "Economía"
    },
    {
        "url": "https://www.reforma.com/rss/ciencia.xml",
        "source": "Reforma",
        "category": "Ciencia"
    },
    {
        "url": "https://www.reforma.com/rss/cultura.xml",
        "source": "Reforma",
        "category": "Cultura"
    },
    {
        "url": "https://www.reforma.com/rss/negocios.xml",
        "source": "Reforma",
        "category": "Negocios"
    },
    {
        "url": "https://www.eluniversal.com.mx/rss/ciencia.xml",
        "source": "El Universal",
        "category": "Ciencia"
    },
    {
        "url": "https://www.eluniversal.com.mx/rss/cultura.xml",
        "source": "El Universal",
        "category": "Cultura"
    },
    {
        "url": "https://www.eluniversal.com.mx/rss/economia.xml",
        "source": "El Universal",
        "category": "Economía"
    },
    {
        "url": "https://www.eluniversal.com.mx/rss/negocios.xml",
        "source": "El Universal",
        "category": "Negocios"
    },
    {
        "url": "https://www.excelsior.com.mx/rss/ciencia.xml",
        "source": "Excélsior",
        "category": "Ciencia"
    },
    {
        "url": "https://www.excelsior.com.mx/rss/cultura.xml",
        "source": "Excélsior",
        "category": "Cultura"
    },
    {
        "url": "https://www.excelsior.com.mx/rss/economia.xml",
        "source": "Excélsior",
        "category": "Economía"
    },
    {
        "url": "https://www.excelsior.com.mx/rss/negocios.xml",
        "source": "Excélsior",
        "category": "Negocios"
    },
    {
        "url": "https://www.milenio.com/rss/ciencia.xml",
        "source": "Milenio",
        "category": "Ciencia"
    },
    {
        "url": "https://www.milenio.com/rss/cultura.xml",
        "source": "Milenio",
        "category": "Cultura"
    },
    {
        "url": "https://www.milenio.com/rss/economia.xml",
        "source": "Milenio",
        "category": "Economía"
    },
    {
        "url": "https://www.milenio.com/rss/negocios.xml",
        "source": "Milenio",
        "category": "Negocios"
    },
    {
        "url": "https://www.elfinanciero.com.mx/rss/ciencia.xml",
        "source": "El Financiero",
        "category": "Ciencia"
    },
    {
        "url": "https://www.elfinanciero.com.mx/rss/cultura.xml",
        "source": "El Financiero",
        "category": "Cultura"
    },
    {
        "url": "https://www.elfinanciero.com.mx/rss/economia.xml",
        "source": "El Financiero",
        "category": "Economía"
    },
    {
        "url": "https://www.elfinanciero.com.mx/rss/negocios.xml",
        "source": "El Financiero",
        "category": "Negocios"
    },
    {
        "url": "https://www.20minutos.com.mx/rss/ciencia.xml",
        "source": "20 Minutos",
        "category": "Ciencia"
    },
    {
        "url": "https://www.20minutos.com.mx/rss/cultura.xml",
        "source": "20 Minutos",
        "category": "Cultura"
    },
    {
        "url": "https://www.20minutos.com.mx/rss/economia.xml",
        "source": "20 Minutos",
        "category": "Economía"
    },
    {
        "url": "https://www.20minutos.com.mx/rss/negocios.xml",
        "source": "20 Minutos",
        "category": "Negocios"
    },
    {
        "url": "https://www.elsoldemexico.com.mx/rss/ciencia.xml",
        "source": "El Sol de México",
        "category": "Ciencia"
    },
    {
        "url": "https://www.elsoldemexico.com.mx/rss/cultura.xml",
        "source": "El Sol de México",
        "category": "Cultura"
    },
    {
        "url": "https://www.elsoldemexico.com.mx/rss/economia.xml",
        "source": "El Sol de México",
        "category": "Economía"
    },
    {
        "url": "https://www.elsoldemexico.com.mx/rss/negocios.xml",
        "source": "El Sol de México",
        "category": "Negocios"
    },
    {
        "url": "https://www.mural.com.mx/rss/ciencia.xml",
        "source": "Mural",
        "category": "Ciencia"
    },
    {
        "url": "https://www.mural.com.mx/rss/cultura.xml",
        "source": "Mural",
        "category": "Cultura"
    },
    {
        "url": "https://www.mural.com.mx/rss/economia.xml",
        "source": "Mural",
        "category": "Economía"
    },
    {
        "url": "https://www.mural.com.mx/rss/negocios.xml",
        "source": "Mural",
        "category": "Negocios"
    },
    {
        "url": "https://www.altonivel.com.mx/rss/ciencia.xml",
        "source": "Alto Nivel",
        "category": "Ciencia"
    },
    {
        "url": "https://www.altonivel.com.mx/rss/cultura.xml",
        "source": "Alto Nivel",
        "category": "Cultura"
    },
    {
        "url": "https://www.altonivel.com.mx/rss/economia.xml",
        "source": "Alto Nivel",
        "category": "Economía"
    },
    {
        "url": "https://www.altonivel.com.mx/rss/negocios.xml",
        "source": "Alto Nivel",
        "category": "Negocios"
    }
]

nombre_archivo = "news_raw_corpus.tsv"

# 2. Abrir el archivo TSV una sola vez al principio
with open(nombre_archivo, mode="a", newline="", encoding="utf-8") as archivo_tsv:
    escritor_tsv = csv.writer(archivo_tsv, delimiter="\t")
    escritor_tsv.writerow(["id", "title", "description", "source", "category", "date", "url", "retrieved_at"])

    # 3. Ciclo exterior: Recorrer cada enlace de nuestra lista
    for fuente in fuentes_rss:
        print(f"Consultando: {fuente['source']} - {fuente['category']}...")
        
        # Parsear el XML de la URL actual
        feed = feedparser.parse(fuente['url'])
        
        # 4. Ciclo interior: Extraer las noticias de ese feed
        for entry in feed.entries:
            doc_id = str(uuid.uuid4())
            
            title = entry.get("title", "No title").replace("\n", " ").replace("\t", " ")
            content = entry.get("description", entry.get("summary", "No content")).replace("\n", " ").replace("\t", " ")
            
            date = entry.get("published", entry.get("updated", "No date"))
            url = entry.get("link", "No url")
            retrieved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Escribir la fila usando los datos dinámicos del diccionario actual
            escritor_tsv.writerow([doc_id, title, content, fuente['source'], fuente['category'], date, url, retrieved_at])

print(f"\nExtracción finalizada. Los datos crudos se guardaron en: {nombre_archivo}")