import streamlit as st
import yfinance as yf
import feedparser

st.set_page_config(page_title="Monitor Financiero LATAM", page_icon="📊")

st.title("🚀 Buscador de Noticias Financieras")
st.write("Noticias en español de fuentes como Yahoo Finanzas, Investing.com, y más.")

# Entrada de usuario
tickers_input = st.text_input("Introduce Tickers (ej: AAPL, TSLA, NVDA):", "AAPL, TSLA")

def obtener_noticias_google(ticker):
    # Parámetros ajustados: 
    # hl=es-419 (Español Latinoamericano)
    # gl=US (Mantiene enfoque en mercado de EE.UU. pero en español)
    # ceid=US:es-419 (Identificador de edición)
    url = f"https://news.google.com/rss/search?q={ticker}+acciones+finanzas&hl=es-419&gl=US&ceid=US:es-419"
    feed = feedparser.parse(url)
    return feed.entries

if tickers_input:
    # Limpiamos los tickers
    tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    for ticker in tickers_list:
        st.divider()
        
        # --- BLOQUE DE PRECIO ---
        col1, col2 = st.columns([1, 3])
        try:
            datos = yf.Ticker(ticker)
            # Intentamos obtener el nombre real de la empresa y su precio
            nombre_empresa = datos.info.get('longName', ticker)
            precio = datos.history(period="1d")['Close'].iloc[-1]
            col1.metric(label=nombre_empresa, value=f"${precio:.2f}")
        except:
            col1.write(f"**{ticker}**")

        # --- BLOQUE DE NOTICIAS ---
        with col2:
            st.subheader(f"Noticias recientes de {ticker}")
            noticias = obtener_noticias_google(ticker)
            
            if not noticias:
                st.warning(f"No se encontraron noticias en español para {ticker}.")
            else:
                # Mostramos las 5 más recientes
                for entry in noticias[:5]:
                    with st.expander(entry.title):
                        # Intentamos formatear un poco la fuente
                        fuente = entry.source.title if 'source' in entry else 'Fuente de noticias'
                        st.write(f"**Publicado:** {entry.published}")
                        st.write(f"**Fuente:** {fuente}")
                        st.write(f"[Leer noticia completa]({entry.link})")

st.divider()
st.caption("Configurado para Español Latinoamericano (es-419)")
