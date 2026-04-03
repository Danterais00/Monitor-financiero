import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse

# Configuración de página
st.set_page_config(page_title="Monitor Financiero 360", page_icon="📈", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .fecha-noticia { font-size: 0.7rem !important; font-weight: bold; color: #6b7280; margin-bottom: 5px; }
    .card-noticia { 
        background-color: #ffffff; 
        padding: 12px; 
        border-radius: 8px; 
        border: 1px solid #e9ecef; 
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card-noticia:hover { border-color: #007bff; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); }
    .titulo-seccion { color: #1f1f1f; border-bottom: 2px solid #007bff; padding-bottom: 5px; margin-top: 30px; margin-bottom: 15px; }
    .ticker-header { background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES ---
def obtener_noticias(query, limite=4):
    query_codificada = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_codificada}&hl=es-419&gl=US&ceid=US:es-419"
    return feedparser.parse(url).entries[:limite]

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configuración")
    tickers_input = st.text_input("Mis Tickers (ej: AAPL, GGAL, NVDA):", "AAPL, GGAL")
    st.caption("Separa los símbolos por comas.")

# --- CUERPO PRINCIPAL ---
st.title("📊 Monitor Financiero Estratégico")

# --- SECCIÓN 1: PANORAMA GLOBAL ---
st.markdown("<h2 class='titulo-seccion'>🌐 Panorama Global</h2>", unsafe_allow_html=True)
noticias_global = obtener_noticias("Economía Mundial")

cols_global = st.columns(4)
for i, noticia in enumerate(noticias_global):
    with cols_global[i]:
        st.markdown(f"""<div class='card-noticia'>
            <div>
                <p class='fecha-noticia'>{noticia.published[:16]}</p>
                <p style='font-size: 0.9rem;'><strong>{noticia.title}</strong></p>
            </div>
            <a href="{noticia.link}" target="_blank" style="font-size: 0.8rem; color: #007bff; text-decoration: none;">Leer más →</a>
        </div>""", unsafe_allow_html=True)

# --- SECCIÓN 2: PANORAMA NACIONAL ---
st.markdown("<h2 class='titulo-seccion'>🇦🇷 Panorama Nacional</h2>", unsafe_allow_html=True)
noticias_nacional = obtener_noticias("Economía Argentina")

cols_nac = st.columns(4)
for i, noticia in enumerate(noticias_nacional):
    with cols_nac[i]:
        st.markdown(f"""<div class='card-noticia'>
            <div>
                <p class='fecha-noticia'>{noticia.published[:16]}</p>
                <p style='font-size: 0.9rem;'><strong>{noticia.title}</strong></p>
            </div>
            <a href="{noticia.link}" target="_blank" style="font-size: 0.8rem; color: #007bff; text-decoration: none;">Leer más →</a>
        </div>""", unsafe_allow_html=True)

# --- SECCIÓN 3: TICKERS ELEGIDOS ---
st.markdown("<h2 class='titulo-seccion'>📈 Análisis de Tickers Elegidos</h2>", unsafe_allow_html=True)

if tickers_input:
    tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    for ticker in tickers_list:
        # Intentamos obtener el nombre largo de la empresa
        try:
            stock_data = yf.Ticker(ticker)
            nombre_largo = stock_data.info.get('longName', ticker) # Si no hay nombre largo, usa el ticker
        except:
            nombre_largo = ticker

        # Cabecera de la sección de Ticker
        st.markdown(f"<div class='ticker-header'><strong>Acción: {nombre_largo} ({ticker})</strong></div>", unsafe_allow_html=True)
        
        col_met, col_n1, col_n2, col_n3 = st.columns([1, 1.5, 1.5, 1.5])
        
        # Columna de Precio
        with col_met:
            try:
                precio = stock_data.history(period="1d")['Close'].iloc[-1]
                cambio = precio - stock_data.history(period="2d")['Close'].iloc[0]
                st.metric(label="Precio Actual", value=f"${precio:.2f}", delta=f"{cambio:.2f}")
            except:
                st.write("Precio N/D")

        # Columnas de Noticias
        noticias_t = obtener_noticias(f"{ticker} acciones", limite=3)
        cols_noticias = [col_n1, col_n2, col_n3]
        
        for j, nt in enumerate(noticias_t):
            if j < len(cols_noticias):
                with cols_noticias[j]:
                    st.markdown(f"""<div class='card-noticia'>
                        <div>
                            <p class='fecha-noticia'>{nt.published[:16]}</p>
                            <p style='font-size: 0.85rem;'><strong>{nt.title}</strong></p>
                        </div>
                        <a href="{nt.link}" target="_blank" style="font-size: 0.75rem; color: #007bff; text-decoration: none;">Fuente →</a>
                    </div>""", unsafe_allow_html=True)
        
        st.write("") # Espacio entre tickers

st.divider()
st.caption("Dashboard Automatizado | Desarrollado con Streamlit")
