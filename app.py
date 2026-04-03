import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse

# Configuración de página
st.set_page_config(page_title="Monitor Financiero Pro 360", page_icon="📈", layout="wide")

# --- ESTILOS CSS ---
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

# --- DICCIONARIO DE SECTORES Y CATALIZADORES (Base completa) ---
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
    "Materiales Básicos": {
        "query": "sector minería acero químicos noticias",
        "pos": ["precios commodities", "yacimientos", "demanda industrial", "innovación extracción"],
        "neg": ["caída precios", "costos energéticos", "conflictos laborales", "regulación ambiental"]
    },
    "Industriales": {
        "query": "sector industria manufactura noticias",
        "pos": ["crecimiento pedidos", "contratos", "expansión mercados", "recuperación construcción"],
        "neg": ["caída pedidos", "materias primas", "huelgas", "recesión global", "suministro"]
    },
    "Consumo Masivo": {
        "query": "sector consumo masivo alimentos bebidas noticias",
        "pos": ["ventas constantes", "expansión mercados", "innovación productos", "presencia marca"],
        "neg": ["costos insumos", "reputación", "cuota mercado", "regulaciones azúcar"]
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
        "query": "sector salud farmacéutica biotecnología noticias",
        "pos": ["ensayo clínico positivo", "aprobación regulatoria", "patentes", "demanda"],
        "neg": ["clínico fallido", "pérdida exclusividad", "litigio", "efectos adversos"]
    },
    "Bienes Raíces / Real Estate": {
        "query": "sector inmobiliario real estate noticias",
        "pos": ["demanda inmobiliaria", "tasas bajas", "alquileres", "ocupación"],
        "neg": ["tasas altas", "sobreoferta", "caída precios", "desaceleración"]
    },
    "Turismo y Hotelería": {
        "query": "sector turismo hoteles viajes noticias",
        "pos": ["alta ocupación", "temporada récord", "expansión destinos", "fidelización"],
        "neg": ["crisis sanitaria", "geopolítica", "costos operativos", "clima adverso"]
    }
}

# --- FUNCIONES ---
def obtener_noticias(query, limite=10):
    query_codificada = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_codificada}&hl=es-419&gl=US&ceid=US:es-419"
    return feedparser.parse(url).entries[:limite]

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
    tickers_input = st.text_input("Mis Tickers:", "AAPL, GGAL, TSLA, YPF")
    st.divider()
    st.markdown("### Análisis Sectorial")
    sector_elegido = st.selectbox("Elegir Sector:", list(SECTORES.keys()))

# --- CUERPO PRINCIPAL ---
st.title("📊 Monitor Financiero Estratégico")

# --- SECCIÓN 1: PANORAMA GENERAL (GLOBAL Y NACIONAL) ---
col_g, col_n = st.columns(2)
with col_g:
    st.markdown("<h3 class='titulo-seccion'>🌐 Panorama Global</h3>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Mundial", 2):
        st.write(f"**{n.title}** ([Link]({n.link}))")
with col_n:
    st.markdown("<h3 class='titulo-seccion'>🇦🇷 Panorama Nacional</h3>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Argentina", 2):
        st.write(f"**{n.title}** ([Link]({n.link}))")

# --- SECCIÓN 2: ANÁLISIS DE TICKERS ELEGIDOS (Prioridad Alta) ---
st.markdown("<h2 class='titulo-seccion'>📈 Análisis de Acciones Elegidas</h2>", unsafe_allow_html=True)

if tickers_input:
    for ticker in [t.strip().upper() for t in tickers_input.split(",") if t.strip()]:
        try:
            stock = yf.Ticker(ticker)
            nombre = stock.info.get('longName', ticker)
            st.markdown(f"<div class='ticker-header'><strong>Acción: {nombre} ({ticker})</strong></div>", unsafe_allow_html=True)
            
            c_m, c_1, c_2, c_3 = st.columns([1, 1.5, 1.5, 1.5])
            with c_m:
                precio = stock.history(period="1d")['Close'].iloc[-1]
                delta = precio - stock.history(period="2d")['Close'].iloc[0]
                st.metric("Precio", f"${precio:.2f}", f"{delta:.2f}")
            
            noticias_t = obtener_noticias(f"{ticker} acciones", 3)
            for idx, nt in enumerate(noticias_t):
                with [c_1, c_2, c_3][idx]:
                    st.markdown(f"<div class='card-noticia'><p class='fecha-noticia'>{nt.published[:16]}</p><p style='font-size: 0.8rem;'>{nt.title}</p><a href='{nt.link}' style='font-size: 0.7rem;'>Fuente</a></div>", unsafe_allow_html=True)
        except:
            st.error(f"Error cargando {ticker}")

# --- SECCIÓN 3: ANÁLISIS DE CATALIZADORES POR SECTOR (Al final) ---
st.markdown(f"<h2 class='titulo-seccion'>🏢 Análisis de Catalizadores: {sector_elegido}</h2>", unsafe_allow_html=True)

conf = SECTORES[sector_elegido]
noticias_sector = obtener_noticias(conf["query"], limite=20)
pos, neg = filtrar_catalizadores(noticias_sector, conf["pos"], conf["neg"])

c_pos, c_neg = st.columns(2)

with c_pos:
    st.markdown("#### ✅ Catalizadores Positivos")
    if pos:
        for p in pos:
            st.markdown(f"<div class='catalizador-pos'><strong>{p.title}</strong><br><a href='{p.link}' target='_blank' style='color: #155724; font-size: 0.7rem;'>Ver noticia →</a></div>", unsafe_allow_html=True)
    else:
        st.info("No hay información reciente sobre catalizadores positivos.")

with c_neg:
    st.markdown("#### ❌ Catalizadores Negativos")
    if neg:
        for n in neg:
            st.markdown(f"<div class='catalizador-neg'><strong>{n.title}</strong><br><a href='{n.link}' target='_blank' style='color: #721c24; font-size: 0.7rem;'>Ver noticia →</a></div>", unsafe_allow_html=True)
    else:
        st.info("No hay información reciente sobre catalizadores negativos.")

st.divider()
st.caption("Dashboard Automatizado | Desarrollado con Streamlit")
