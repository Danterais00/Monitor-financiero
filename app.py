# --- FUNCIÓN MEJORADA ---
def obtener_noticias(query, limite=10, argentina=False):
    query_codificada = urllib.parse.quote(query)
    
    # Si es nacional, usamos la edición de Argentina (gl=AR)
    if argentina:
        url = f"https://news.google.com/rss/search?q={query_codificada}&hl=es-419&gl=AR&ceid=AR:es-419"
    else:
        # Para internacional/tickers, usamos la edición global/US
        url = f"https://news.google.com/rss/search?q={query_codificada}&hl=es-419&gl=US&ceid=US:es-419"
        
    return feedparser.parse(url).entries[:limite]

# --- ASÍ DEBERÍAS LLAMARLAS EN EL CUERPO ---

# 1. Para Global (Mundo):
noticias_global = obtener_noticias("Economía Mundial", limite=2, argentina=False)

# 2. Para Nacional (Argentina):
# Al poner True, Google buscará en Clarín, La Nación, Ámbito, El Cronista, etc.
noticias_nacional = obtener_noticias("Economía Argentina", limite=2, argentina=True)

# 3. Para Tickers y Sectores:
# Generalmente conviene dejarlo en False para tener visión global del mercado
noticias_t = obtener_noticias(f"{ticker} acciones", 3, argentina=False)
