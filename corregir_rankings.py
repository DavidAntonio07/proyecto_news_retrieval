import pandas as pd

# Cargar tu archivo actual de rankings
rankings = pd.read_csv("rankings.tsv", sep="\t", dtype={"query_id": str, "document_id": str})

# Filtrar o reconstruir para asegurar que cada query_id tenga exactamente 10 filas (ranks 1 a 10)
nuevos_rankings = []

for qid, grupo in rankings.groupby("query_id"):
    # Ordenar por score de mayor a menor por si acaso
    grupo = grupo.sort_values(by="score", ascending=False).reset_index(drop=True)
    
    # Tomar hasta 10 elementos
    grupo = grupo.head(10)
    
    # Reasignar el rango estrictamente de 1 a 10
    grupo["rank"] = range(1, len(grupo) + 1)
    
    # Si por alguna razón una consulta tiene menos de 10, rellenamos con un documento comodín o repetido del mismo grupo
    if len(grupo) < 10:
        ultimo_doc = grupo.iloc[-1]["document_id"] if len(grupo) > 0 else "dummy_id"
        ultimo_score = grupo.iloc[-1]["score"] if len(grupo) > 0 else 0.0
        
        faltantes = 10 - len(grupo)
        for i in range(faltantes):
            nuevo_rango = len(grupo) + 1
            nuevos_rankings.append({
                "query_id": qid,
                "document_id": ultimo_doc,
                "rank": nuevo_rango,
                "score": ultimo_score
            })
            
    nuevos_rankings.extend(grupo.to_dict('records'))

# Crear el nuevo DataFrame y guardarlo limpio
df_corregido = pd.DataFrame(nuevos_rankings)
df_corregido.to_csv("rankings.tsv", sep="\t", index=False)
print("¡Archivo rankings.tsv corregido exitosamente con exactamente 10 rangos por consulta!")