import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="Monitor Financiero Pro 360", page_icon="📈", layout="wide")

# 2. Estilos CSS para diseño limpio
st.markdown("""
    <style>
    .fecha-noticia { font-size: 0.7rem !important; font-weight: bold; color: #6b7280; margin-bottom: 5px; }
    .card-noticia { 
        background-color: #ffffff; padding: 12px; border-radius: 8px; border: 1px solid #e9ecef; 
        height: 100%; display: flex; flex-direction: column; justify-content: space-between;
    }
    .titulo-seccion { color: #1f1f1f; border-bottom: 2px solid #007bff; padding-bottom: 5px; margin-top: 25px; margin-bottom: 15px; }
    .ticker-header { background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #007bff; }
    .catalizador-pos { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 5px solid #28a745; margin-bottom: 8px; font-size: 0.85rem; }
    .catalizador-neg { color: #721c24; background-color: #f8d7da; padding: 10px; border-radius: 5px; border-left: 5px solid #dc3545; margin-bottom: 8px; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. Diccionario de Sectores y Catalizadores
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

# 4. Funciones de obtención de datos
def obtener_noticias(query, limite=10, argentina=False):
    try:
        query_codificada = urllib.parse.quote(query)
        region = "AR" if argentina else "US"
        url = f"https://news.google.com/rss/search?q={query_codificada}&hl=es-419&gl={region}&ceid={region}:es-419"
        feed = feedparser.parse(url)
        return feed.entries[:limite]
    except:
        return []

def filtrar_catalizadores(noticias, keywords_pos, keywords_neg):
    p_enc, n_enc = [], []
    for n in noticias:
        tit = n.title.lower()
        if any(k.lower() in tit for k in keywords_pos): p_enc.append(n)
        elif any(k.lower() in tit for k in keywords_neg): n_enc.append(n)
    return p_enc[:4], n_enc[:4]

# 5. Barra Lateral (Sidebar)
with st.sidebar:
    st.title("⚙️ Configuración")
    tickers_input = st.text_input("Mis Tickers:", "AAPL, GGAL, YPF")
    st.divider()
    sector_elegido = st.selectbox("Elegir Sector para Análisis:", list(SECTORES.keys()))

# 6. Cuerpo Principal - Panorama General
st.title("📊 Monitor Financiero Estratégico")

col_g, col_n = st.columns(2)
with col_g:
    st.markdown("<h3 class='titulo-seccion'>🌐 Panorama Global</h3>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Mundial", limite=2, argentina=False):
        st.write(f"**{n.title}** ([Link]({n.link}))")
with col_n:
    st.markdown("<h3 class='titulo-seccion'>🇦🇷 Panorama Nacional</h3>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Argentina", limite=2, argentina=True):
        st.write(f"**{n.title}** ([Link]({n.link}))")

# 7. Cuerpo Principal - Análisis de Tickers
st.markdown("<h2 class='titulo-seccion'>📈 Análisis de Acciones Elegidas</h2>", unsafe_allow_html=True)

if tickers_input:
    lista_tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    for ticker in lista_tickers:
        try:
            stock = yf.Ticker(ticker)
            nombre = stock.info.get('longName', ticker)
            st.markdown(f"<div class='ticker-header'><strong>Acción: {nombre} ({ticker})</strong></div>", unsafe_allow_html=True)
            
            c_met, c_n1, c_n2, c_n3 = st.columns([1, 1.5, 1.5, 1.5])
            
            with c_met:
                hist = stock.history(period="2d")
                if not hist.empty and len(hist) >= 2:
                    precio = hist['Close'].iloc[-1]
                    delta = precio - hist['Close'].iloc[0]
                    st.metric("Precio Actual", f"${precio:.2f}", f"{delta:.2f}")
                else:
                    st.write("Datos de precio no disponibles")
            
            noticias_t = obtener_noticias(f"{ticker} acciones", 3)
            cols_noticias = [c_n1, c_n2, c_n3]
            for idx, nt in enumerate(noticias_t):
                if idx < len(cols_noticias):
                    with cols_noticias[idx]:
                        st.markdown(f"""<div class='card-noticia'>
                            <div><p class='fecha-noticia'>{nt.published[:16]}</p>
                            <p style='font-size: 0.8rem;'><strong>{nt.title}</strong></p></div>
                            <a href='{nt.link}' target='_blank' style='font-size: 0.7rem; color: #007bff;'>Fuente →</a>
                        </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"No se pudieron cargar datos para {ticker}")

# 8. Cuerpo Principal - Catalizadores Sectoriales
st.markdown(f"<h2 class='titulo-seccion'>🏢 Catalizadores del Sector: {sector_elegido}</h2>", unsafe_allow_html=True)

conf = SECTORES[sector_elegido]
noticias_sector = obtener_noticias(conf["query"], limite=20)
pos, neg = filtrar_catalizadores(noticias_sector, conf["pos"], conf["neg"])

col_pos, col_neg = st.columns(2)
with col_pos:
    st.markdown("#### ✅ Catalizadores Positivos")
    if pos:
        for p in pos:
            st.markdown(f"<div class='catalizador-pos'><strong>{p.title}</strong><br><a href='{p.link}' target='_blank' style='color:#155724; font-size:0.7rem;'>Ver noticia →</a></div>", unsafe_allow_html=True)
    else:
        st.info("No hay información reciente.")

with col_neg:
    st.markdown("#### ❌ Catalizadores Negativos")
    if neg:
        for n in neg:
            st.markdown(f"<div class='catalizador-neg'><strong>{n.title}</strong><br><a href='{n.link}' target='_blank' style='color:#721c24; font-size:0.7rem;'>Ver noticia →</a></div>", unsafe_allow_html=True)
    else:
        st.info("No hay información reciente.")

st.divider()
st.caption("Dashboard Pro 360 | Fuentes: Google News AR/US, Yahoo Finance")
