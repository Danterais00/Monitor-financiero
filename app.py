import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

st.set_page_config(page_title="Monitor Financiero Pro", page_icon="📊")

st.title("🚀 Buscador de Noticias Financieras")
st.write("Agregando noticias de Google News, Reuters, Yahoo Finance y más.")

# Entrada de usuario
tickers_input = st.text_input("Introduce Tickers (ej: AAPL, TSLA, NVDA):", "AAPL, MSFT")

def obtener_noticias_google(ticker):
    # Creamos una búsqueda avanzada para Google News
    # hl=es (idioma español), gl=ES (región), q=ticker + stock + news
    url = f"https://news.google.com/rss/search?q={ticker}+stock+news&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    return feed.entries

if tickers_input:
    tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    for ticker in tickers_list:
        st.divider()
        
        # --- BLOQUE DE PRECIO (Bonus) ---
        col1, col2 = st.columns([1, 3])
        try:
            datos = yf.Ticker(ticker)
            precio = datos.history(period="1d")['Close'].iloc[-1]
            col1.metric(label=f"Precio {ticker}", value=f"${precio:.2f}")
        except:
            col1.write(f"**{ticker}**")

        # --- BLOQUE DE NOTICIAS ---
        with col2:
            st.subheader(f"Últimas noticias de {ticker}")
            noticias = obtener_noticias_google(ticker)
            
            if not noticias:
                st.warning("No se encontraron noticias en Google News.")
            else:
                # Mostramos las 5 más recientes
                for entry in noticias[:5]:
                    with st.expander(entry.title):
                        st.write(f"**Publicado:** {entry.published}")
                        st.write(f"**Fuente:** {entry.source.title if 'source' in entry else 'Desconocida'}")
                        st.write(f"[Leer noticia completa en el sitio original]({entry.link})")

st.divider()
st.caption("Fuente: Google News RSS & Yahoo Finance API")
