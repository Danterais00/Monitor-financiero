import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse

st.set_page_config(page_title="Dashboard Financiero 360", page_icon="📈", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .fecha-noticia { font-size: 0.75rem !important; font-weight: bold; color: #6b7280; margin-bottom: 5px; }
    .card-noticia { 
        background-color: #f8f9fa; 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid #e9ecef; 
        height: 100%;
        transition: 0.3s;
    }
    .card-noticia:hover { border-color: #007bff; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); }
    .titulo-seccion { color: #1f1f1f; border-bottom: 2px solid #007bff; padding-bottom: 5px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES ---
def obtener_noticias(query, limite=4):
    query_codificada = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_codificada}&hl=es-419&gl=US&ceid=US:es-419"
    return feedparser.parse(url).entries[:limite]

def detectar_impacto(titular_macro):
    keywords = {
        "FED": "Tecnología y Crecimiento (AAPL, MSFT, NVDA)",
        "TASAS": "Sector Bancario y Real Estate",
        "PETROLEO": "Energía (XOM, CVX, YPF)",
        "INFLACION": "Consumo Masivo y Retail",
        "CHIPS": "Semiconductores (NVDA, AMD)",
        "FMI": "Mercados Emergentes (Argentina)"
    }
    titular_upper = titular_macro.upper()
    for key, desc in keywords.items():
        if key in titular_upper:
            return f"🔔 **Relación con:** {desc}"
    return None

# --- SIDEBAR (Solo para Tickers) ---
with st.sidebar:
    st.title("⚙️ Panel de Control")
    tickers_input = st.text_input("Ingresa tus Tickers:", "AAPL, NVDA, GGAL")
    st.info("Escribe los tickers separados por coma.")

# --- CUERPO PRINCIPAL ---
st.title("📊 Monitor Financiero Estratégico")

# --- SECCIÓN 1: PANORAMA GLOBAL ---
st.markdown("<h2 class='titulo-seccion'>🌐 Panorama Global (Economía Mundial)</h2>", unsafe_allow_html=True)
noticias_global = obtener_noticias("Economía Mundial")

cols_global = st.columns(4)
for i, noticia in enumerate(noticias_global):
    with cols_global[i]:
        impacto = detectar_impacto(noticia.title)
        st.markdown(f"""<div class='card-noticia'>
            <p class='fecha-noticia'>{noticia.published[:16]}</p>
            <p><strong>{noticia.title}</strong></p>
            <a href="{noticia.link}" target="_blank" style="font-size: 0.8rem;">Leer noticia</a>
        </div>""", unsafe_allow_html=True)
        if impacto:
            st.caption(impacto)

# --- SECCIÓN 2: PANORAMA NACIONAL ---
st.markdown("<h2 class='titulo-seccion'>🇦🇷 Panorama Nacional (Argentina/Región)</h2>", unsafe_allow_html=True)
noticias_nacional = obtener_noticias("Economía Argentina") # Puedes cambiar esto por tu país

cols_nac = st.columns(4)
for i, noticia in enumerate(noticias_nacional):
    with cols_nac[i]:
        st.markdown(f"""<div class='card-noticia'>
            <p class='fecha-noticia'>{noticia.published[:16]}</p>
            <p><strong>{noticia.title}</strong></p>
            <a href="{noticia.link}" target="_blank" style="font-size: 0.8rem;">Leer noticia</a>
        </div>""", unsafe_allow_html=True)

# --- SECCIÓN 3: SEGUIMIENTO DE TICKERS ---
st.markdown("<h2 class='titulo-seccion'>📈 Análisis de Tickers Elegidos</h2>", unsafe_allow_html=True)

if tickers_input:
    tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    for ticker in tickers_list:
        with st.container():
            col_met, col_news = st.columns([1, 3])
            
            # Datos Financieros
            with col_met:
                try:
                    datos = yf.Ticker(ticker)
                    info = datos.info
                    precio = datos.history(period="1d")['Close'].iloc[-1]
                    cambio = precio - datos.history(period="2d")['Close'].iloc[0]
                    
                    st.metric(label=info.get('longName', ticker), 
                              value=f"${precio:.2f}", 
                              delta=f"{cambio:.2f}")
                except:
                    st.subheader(ticker)
                    st.write("Datos no disponibles")

            # Noticias del Ticker
            with col_news:
                noticias_t = obtener_noticias(f"{ticker} acciones", limite=3)
                cols_t = st.columns(3)
                for j, nt in enumerate(noticias_t):
                    with cols_t[j]:
                        with st.expander(f"Noticia {j+1}"):
                            st.write(f"**{nt.title}**")
                            st.caption(nt.published)
                            st.write(f"[Ir a fuente]({nt.link})")
            st.divider()

st.caption("Actualizado en tiempo real | Fuentes: Google News RSS & Yahoo Finance")
