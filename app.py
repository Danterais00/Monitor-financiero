import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse  # <--- Nueva importación para arreglar las URLs

st.set_page_config(page_title="Monitor Financiero Inteligente", page_icon="🌐", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .fecha-noticia { font-size: 0.8rem !important; font-weight: bold; color: #6b7280; margin-bottom: -10px; }
    .noticia-contexto { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #d1d5db; min-height: 150px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE BÚSQUEDA ---
def obtener_noticias(query, limite=5):
    # IMPORTANTE: Esto codifica los espacios y acentos para que la URL sea válida
    query_codificada = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_codificada}&hl=es-419&gl=US&ceid=US:es-419"
    return feedparser.parse(url).entries[:limite]

def detectar_impacto(titular_macro, ticker):
    keywords_impacto = {
        "FED": ["AAPL", "MSFT", "TSLA", "TECH"],
        "TASAS": ["BANCOS", "CRECIMIENTO", "AAPL"],
        "PETROLEO": ["XOM", "CVX", "ENERGIA"],
        "INFLACION": ["CONSUMO", "RETAIL", "WMT"],
        "GUERRA": ["DEFENSA", "ORO", "LMT"],
        "CHIP": ["NVDA", "AMD", "INTC"]
    }
    
    titular_upper = titular_macro.upper()
    for key, tickers_relacionados in keywords_impacto.items():
        if key in titular_upper:
            return f"⚠️ **Impacto Sectorial ({key}):** Relacionado con {', '.join(tickers_relacionados)}."
    return None

# --- INTERFAZ ---
st.title("🌐 Monitor de Mercado: Tickers + Contexto Global")

with st.sidebar:
    st.header("Configuración")
    paises = {
        "Mundo": "Economía Mundial", 
        "Argentina": "Economía Argentina", 
        "México": "Economía México", 
        "España": "Economía España"
    }
    seleccion_pais = st.selectbox("Región de contexto:", list(paises.keys()))
    tickers_input = st.text_input("Tus Tickers (ej: AAPL, NVDA):", "AAPL, TSLA")

# --- SECCIÓN 1: CONTEXTO MACRO ---
st.subheader(f"🌍 Contexto Económico: {seleccion_pais}")
noticias_macro = obtener_noticias(paises[seleccion_pais], limite=3)

if noticias_macro:
    cols_macro = st.columns(3)
    for i, noticia in enumerate(noticias_macro):
        with cols_macro[i]:
            st.markdown(f"""<div class="noticia-contexto">
                <p class="fecha-noticia">{noticia.published[:16]}</p>
                <p><strong>{noticia.title}</strong></p>
                <a href="{noticia.link}" target="_blank">Leer más</a>
            </div>""", unsafe_allow_html=True)
else:
    st.warning("No se pudieron cargar las noticias de contexto.")

# --- SECCIÓN 2: ANÁLISIS DE TICKERS ---
st.divider()
if tickers_input:
    tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    for ticker in tickers_list:
        col_info, col_news = st.columns([1, 2])
        
        with col_info:
            try:
                datos = yf.Ticker(ticker)
                nombre = datos.info.get('longName', ticker)
                precio = datos.history(period="1d")['Close'].iloc[-1]
                st.metric(label=nombre, value=f"${precio:.2f}")
                
                # Match con noticias macro
                for nm in noticias_macro:
                    alerta = detectar_impacto(nm.title, ticker)
                    if alerta:
                        st.info(alerta)
            except Exception as e:
                st.write(f"**{ticker}** (Datos no disponibles)")

        with col_news:
            st.write(f"**Últimas de {ticker}:**")
            # También codificamos la búsqueda del ticker por seguridad
            noticias_ticker = obtener_noticias(f"{ticker} acciones", limite=3)
            for nt in noticias_ticker:
                with st.expander(nt.title):
                    st.caption(nt.published)
                    st.write(f"🔗 [Ir a la fuente]({nt.link})")
        st.divider()
