import streamlit as st
import yfinance as yf
import feedparser
from bs4 import BeautifulSoup # Para limpiar el texto

st.set_page_config(page_title="Monitor Financiero Pro", page_icon="📈", layout="wide")

# Estilo para la fecha pequeña
st.markdown("""
    <style>
    .fecha-noticia {
        font-size: 0.75rem !important;
        font-weight: bold;
        color: #6b7280;
        margin-bottom: -15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Monitor de Noticias y Resúmenes")

tickers_input = st.text_input("Tickers (separados por coma):", "AAPL, TSLA, NVDA")

def limpiar_resumen(html_text):
    # Google News envía HTML. Esto extrae solo el texto.
    soup = BeautifulSoup(html_text, "html.parser")
    texto = soup.get_text()
    # Limitar a 100 palabras
    palabras = texto.split()
    if len(palabras) > 100:
        return " ".join(palabras[:100]) + "..."
    return texto

def obtener_noticias(ticker):
    url = f"https://news.google.com/rss/search?q={ticker}+acciones+finanzas&hl=es-419&gl=US&ceid=US:es-419"
    return feedparser.parse(url).entries

if tickers_input:
    tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    for ticker in tickers_list:
        st.header(f"🏢 {ticker}")
        noticias = obtener_noticias(ticker)
        
        if not noticias:
            st.info(f"No hay noticias recientes para {ticker}")
        else:
            for entry in noticias[:5]:
                # 1. Fecha (Arriba, Izquierda, Negrita, Chica)
                # Usamos HTML para el estilo personalizado
                fecha = entry.published
                st.markdown(f'<p class="fecha-noticia">{fecha}</p>', unsafe_allow_html=True)
                
                # 2. Titular y Contenido
                with st.expander(entry.title):
                    resumen = limpiar_resumen(entry.summary)
                    st.write(f"**Resumen:** {resumen}")
                    
                    st.write(f"**Fuente:** {entry.source.title if 'source' in entry else 'N/A'}")
                    st.write(f"[Ver noticia original]({entry.link})")
        st.divider()
