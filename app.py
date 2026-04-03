import streamlit as st
import yfinance as yf
import feedparser

# Configuración de página ancha
st.set_page_config(page_title="Monitor Financiero", page_icon="📈", layout="wide")

# Estilo CSS para la fecha (Chica, Negrita, arriba a la izquierda)
st.markdown("""
    <style>
    .fecha-noticia {
        font-size: 0.8rem !important;
        font-weight: bold;
        color: #6b7280;
        margin-bottom: -10px;
        text-align: left;
    }
    .stExpander {
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🗞️ Monitor de Noticias Financieras")
st.write("Selecciona tus tickers para ver las últimas novedades del mercado en español.")

# Entrada de usuario
tickers_input = st.text_input("Introduce Tickers (ej: AAPL, TSLA, NVDA, MSFT):", "AAPL, TSLA")

def obtener_noticias(ticker):
    # RSS de Google News en español latinoamericano
    url = f"https://news.google.com/rss/search?q={ticker}+acciones+finanzas&hl=es-419&gl=US&ceid=US:es-419"
    return feedparser.parse(url).entries

if tickers_input:
    # Procesar lista de tickers
    tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    for ticker in tickers_list:
        st.divider()
        
        # --- ENCABEZADO Y PRECIO ---
        col_tit, col_met = st.columns([3, 1])
        try:
            datos = yf.Ticker(ticker)
            nombre = datos.info.get('longName', ticker)
            precio = datos.history(period="1d")['Close'].iloc[-1]
            
            col_tit.subheader(f"🏢 {nombre} ({ticker})")
            col_met.metric(label="Precio Actual", value=f"${precio:.2f}")
        except:
            col_tit.subheader(f"🏢 Ticker: {ticker}")

        # --- LISTA DE NOTICIAS ---
        noticias = obtener_noticias(ticker)
        
        if not noticias:
            st.info(f"No se encontraron noticias recientes en español para {ticker}.")
        else:
            # Mostramos las 5 noticias más relevantes
            for entry in noticias[:5]:
                # 1. Fecha (Chica y Negrita arriba)
                st.markdown(f'<p class="fecha-noticia">{entry.published}</p>', unsafe_allow_html=True)
                
                # 2. Expander con el Título
                with st.expander(entry.title):
                    fuente = entry.source.title if 'source' in entry else "Fuente no especificada"
                    st.write(f"**Fuente:** {fuente}")
                    st.write(f"🔗 [Leer noticia completa en el sitio original]({entry.link})")

st.divider()
st.caption("Datos: Yahoo Finance | Noticias: Google News RSS (LATAM)")
