import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Monitor Financiero Pro 360", page_icon="📈", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .fecha-noticia { font-size: 0.7rem !important; font-weight: bold; color: #6b7280; margin-bottom: 5px; }
    .card-noticia { 
        background-color: #ffffff; padding: 12px; border-radius: 8px; border: 1px solid #e9ecef; 
        height: 100%; display: flex; flex-direction: column; justify-content: space-between;
    }
    .card-noticia:hover { border-color: #007bff; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); }
    .titulo-seccion { color: #1f1f1f; border-bottom: 2px solid #007bff; padding-bottom: 5px; margin-top: 25px; margin-bottom: 15px; }
    .ticker-header { background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #007bff; }
    .catalizador-pos { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 5px solid #28a745; margin-bottom: 8px; font-size: 0.85rem; }
    .catalizador-neg { color: #721c24; background-color: #f8d7da; padding: 10px; border-radius: 5px; border-left: 5px solid #dc3545; margin-bottom: 8px; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

# --- DICCIONARIO DE SECTORES ---
SECTORES = {
    "Comercio Minorista (Retail)": {
        "query": "sector retail comercio minorista noticias",
        "pos": ["ventas al alza", "navidad", "black friday", "expansión", "consumo favorable", "logística"],
        "neg": ["caída ventas", "inventarios altos", "inflación", "suministro", "hábitos consumo"]
    },
    "Energía": {
        "query": "sector energía petróleo gas noticias",
        "pos": ["precios petróleo", "precios gas", "reservas", "exportación", "tecnología extracción"],
        "neg": ["caída commodities", "regulación ambiental", "derrame", "exceso oferta", "baja demanda"]
    },
    "Tecnológicas": {
        "query": "sector tecnología software chips noticias",
        "pos": ["resultados superiores", "lanzamiento innovador", "usuarios", "alianza", "guidance"],
        "neg": ["guidance a la baja", "retraso producto", "regulación tech", "tasas interés altas"]
    },
    "Financiero": {
        "query": "sector bancos fintech finanzas noticias",
        "pos": ["suba tasas", "baja morosidad", "digitalización", "dividendos", "fusión"],
        "neg": ["alta morosidad", "baja tasas", "fraude", "crisis financiera", "regulación"]
    },
    "Salud y Farmacéuticas": {
        "query": "sector salud farmacéutica noticias",
        "pos": ["resultados clínicos", "aprobación regulatoria", "patentes", "demanda"],
        "neg": ["ensayos fallidos", "pérdida exclusividad", "regulatorio", "litigios"]
    }
}

# --- FUNCIÓN DE NOTICIAS ---
def obtener_noticias(query, limite=10, argentina=False):
    try:
        query_codificada = urllib.parse.quote(query)
        region = "AR" if argentina else "US"
        url = f"https://news.google.com/rss/search?q={query_codificada}&hl=es-419&gl={region}&ceid={region}:es-419"
        return feedparser.parse(url).entries[:limite]
    except:
        return []

def filtrar_catalizadores(noticias, keywords_pos, keywords_neg):
    pos_encontradas = []
    neg_encontradas = []
    for n in noticias:
        titular = n.title.lower()
        if any(k.lower() in titular for k in keywords_pos):
            pos_encontradas.append(n)
        if any(k.lower() in titular for k in keywords_neg):
            neg_encontradas.append(n)
    return pos_encontradas[:4], neg_encontradas[:4]

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configuración")
    tickers_input = st.text_input("Mis Tickers:", "AAPL, GGAL, YPF")
    st.divider()
    sector_elegido = st.selectbox("Elegir Sector para Análisis:", list(SECTORES.keys()))

# --- CUERPO PRINCIPAL ---
st.title("📊 Monitor Financiero Estratégico")

# --- SECCIÓN 1: PANORAMA GENERAL ---
col_g, col_n = st.columns(2)
with col_g:
    st.markdown("<h3 class='titulo-seccion'>🌐 Panorama Global (Bloomberg, Reuters)</h3>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Mundial", limite=2, argentina=False):
        st.write(f"**{n.title}** ([Link]({n.link}))")
with col_n:
    st.markdown("<h3 class='titulo-seccion'>🇦🇷 Panorama Nacional (Ámbito, Cronista)</h3>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Argentina", limite=2, argentina=True):
        st.write(f"**{n.title}** ([Link]({n.link}))")

# --- SECCIÓN 2: ANÁLISIS DE ACCIONES ELEGIDAS ---
st.markdown("<h2 class='titulo-seccion'>📈 Análisis de Acciones Elegidas</h2>", unsafe_allow_html=True)

if tickers_input:
    for ticker in [t.strip().upper() for t in tickers_input.split(",") if t.strip()]:
        try:
            stock = yf.Ticker(ticker)
            nombre = stock.info.get('longName', ticker)
            st.markdown(f"<div class='ticker-header'><strong>Acción: {nombre} ({ticker})</strong></div>", unsafe_allow_html=True)
            
            c_m, c_1, c_2, c_3 = st.columns([1, 1.5, 1.5, 1.5])
            with c_m:
                hist = stock.history(period="2d")
                if not hist.empty:
                    precio = hist['Close'].iloc[-1]
                    delta = precio - hist['Close'].iloc[0]
                    st.metric("Precio Actual", f"${precio:.2f}", f"{delta:.2f}")
                else:
                    st.write("Precio N/D")
            
            noticias_t = obtener_noticias(f"{ticker} acciones", 3)
            cols_noticias = [c_1, c_2, c_3]
            for idx, nt in enumerate(noticias_t):
                if idx < len(cols_noticias):
                    with cols_noticias[idx]:
                        st
