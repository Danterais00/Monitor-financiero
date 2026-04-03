import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="Monitor Financiero Pro 360", page_icon="📈", layout="wide")

# 2. Estilos CSS
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

# 3. Diccionario Completo de Sectores (Los 14 sectores solicitados)
SECTORES = {
    "Comercio Minorista (Retail)": {
        "query": "sector retail comercio minorista noticias",
        "pos": ["ventas al alza", "navidad", "black friday", "expansión rentable", "consumo favorable", "logística"],
        "neg": ["caída ventas", "inventarios altos", "inflación", "suministro", "hábitos consumo"]
    },
    "Energía": {
        "query": "sector energía petróleo gas noticias",
        "pos": ["precios petróleo", "precios gas", "reservas", "exportación", "tecnología extracción"],
        "neg": ["caída commodities", "regulación ambiental", "derrame", "exceso oferta", "baja demanda"]
    },
    "Materiales Básicos": {
        "query": "sector minería acero químicos noticias",
        "pos": ["precios commodities", "yacimientos", "demanda industrial", "innovación procesos"],
        "neg": ["caída precios", "regulación ambiental", "costos energéticos", "conflictos laborales"]
    },
    "Industriales": {
        "query": "sector industrial manufactura construcción noticias",
        "pos": ["crecimiento pedidos", "contratos", "expansión mercados", "innovación productiva", "automotriz"],
        "neg": ["caída pedidos", "materias primas", "huelgas", "recesión global", "suministro"]
    },
    "Consumo Masivo": {
        "query": "sector consumo masivo alimentos bebidas noticias",
        "pos": ["ventas constantes", "expansión mercados", "innovación productos", "presencia marca"],
        "neg": ["costos insumos", "reputación", "cuota mercado", "regulaciones azúcar", "alcohol"]
    },
    "Salud y Farmacéuticas": {
        "query": "sector salud farmacéutica biotecnología noticias",
        "pos": ["resultados clínicos", "aprobación regulatoria", "patentes", "cambios demográficos"],
        "neg": ["ensayos fallidos", "pérdida exclusividad", "problemas regulatorios", "litigios"]
    },
    "Financiero": {
        "query": "sector bancos aseguradoras fintech noticias",
        "pos": ["suba tasas", "baja morosidad", "digitalización", "dividendos", "fusiones"],
        "neg": ["alta morosidad", "baja tasas", "fraude", "crisis financiera", "regulaciones"]
    },
    "Tecnológicas": {
        "query": "sector tecnología software chips noticias",
        "pos": ["resultados superiores", "lanzamiento innovador", "usuarios", "alianza estratégica", "guidance"],
        "neg": ["guidance a la baja", "fallos productos", "regulación tech", "cuota mercado", "tasas altas"]
    },
    "Bienes Raíces / Real Estate": {
        "query": "sector inmobiliario real estate noticias",
        "pos": ["demanda inmobiliaria", "tasas hipotecarias", "zonas premium", "ocupación"],
        "neg": ["tasas altas", "sobreoferta", "caída precios", "desaceleración", "impuestos"]
    },
    "Medios y Entretenimiento": {
        "query": "sector medios entretenimiento streaming noticias",
        "pos": ["suscriptores", "contenidos virales", "expansión internacional", "diversificación"],
        "neg": ["caída ratings", "costos producción", "conflictos licencias", "hábitos consumo"]
    },
    "Telecomunicaciones": {
        "query": "sector telecomunicaciones 5G telefonía noticias",
        "pos": ["suscriptores", "5G", "diversificación servicios", "planes corporativos"],
        "neg": ["competencia precios", "regulaciones", "caída ingresos", "infraestructura"]
    },
    "Transporte y Logística": {
        "query": "sector transporte logística carga noticias",
        "pos": ["demanda transporte", "costos combustible", "contratos largo plazo", "optimización"],
        "neg": ["precios combustible", "disminución comercio", "huelgas", "bloqueos", "seguridad"]
    },
    "Energías Renovables": {
        "query": "sector energías renovables solar eólica noticias",
        "pos": ["subsidios", "avances tecnológicos", "contratos suministro", "conciencia ambiental"],
        "neg": ["reducción subsidios", "competencia barata", "problemas técnicos", "regulatorios"]
    },
    "Turismo y Hotelería": {
        "query": "sector turismo hoteles viajes noticias",
        "pos": ["alta ocupación", "temporadas récord", "expansión destinos", "fidelización"],
        "neg": ["crisis sanitaria", "geopolítica", "costos operativos", "clima adverso"]
    }
}

# 4. Funciones de ayuda
def obtener_noticias(query, limite=10, argentina=False):
    try:
        q_cod = urllib.parse.quote(query)
        reg = "AR" if argentina else "US"
        url = f"https://news.google.com/rss/search?q={q_cod}&hl=es-419&gl={reg}&ceid={reg}:es-419"
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

# 5. Sidebar
with st.sidebar:
    st.title("⚙️ Configuración")
    tickers_input = st.text_input("Mis Tickers:", "AAPL, GGAL, YPF")
    st.divider()
    sector_elegido = st.selectbox("Elegir Sector para Análisis:", list(SECTORES.keys()))

# 6. Panorama General
st.title("📊 Monitor Financiero Estratégico")
c_g, c_n = st.columns(2)
with c_g:
    st.markdown("<h3 class='titulo-seccion'>🌐 Panorama Global</h3>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Mundial", 2):
        st.write(f"**{n.title}** ([Link]({n.link}))")
with c_n:
    st.markdown("<h3 class='titulo-seccion'>🇦🇷 Panorama Nacional</h3>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Argentina", 2, True):
        st.write(f"**{n.title}** ([Link]({n.link}))")

# 7. Análisis de Acciones
st.markdown("<h2 class='titulo-seccion'>📈 Análisis de Acciones Elegidas</h2>", unsafe_allow_html=True)
if tickers_input:
    lista_t = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    for ticker in lista_t:
        try:
            stock = yf.Ticker(ticker)
            nombre = stock.info.get('longName', ticker)
            st.markdown(f"<div class='ticker-header'><strong>Acción: {nombre} ({ticker})</strong></div>", unsafe_allow_html=True)
            
            c_met, c_n1, c_n2, c_n3 = st.columns([1, 1.5, 1.5, 1.5])
            with c_met:
                h = stock.history(period="2d")
                if not h.empty and len(h) >= 2:
                    p = h['Close'].iloc[-1]
                    d = p - h['Close'].iloc[0]
                    st.metric("Precio Actual", f"${p:.2f}", f"{d:.2f}")
                else: st.write("Datos N/D")
            
            noticias_t = obtener_noticias(f"{ticker} acciones", 3)
            cols = [c_n1, c_n2, c_n3]
            for idx, nt in enumerate(noticias_t):
                if idx < len(cols):
                    with cols[idx]:
                        st.markdown(f"<div class='card-noticia'><div><p class='fecha-noticia'>{nt.published[:16]}</p><p style='font-size: 0.8rem;'><strong>{nt.title}</strong></p></div><a href='{nt.link}' target='_blank' style='font-size: 0.7rem; color: #007bff;'>Fuente →</a></div>", unsafe_allow_html=True)
        except: st.warning(f"No se pudo cargar {ticker}")

# 8. Catalizadores Sectoriales
st.markdown(f"<h2 class='titulo-seccion'>🏢 Catalizadores del Sector: {sector_elegido}</h2>", unsafe_allow_html=True)
conf = SECTORES[sector_elegido]
noticias_s = obtener_noticias(conf["query"], 20)
pos, neg = filtrar_catalizadores(noticias_s, conf["pos"], conf["neg"])

cp, cn = st.columns(2)
with cp:
    st.markdown("#### ✅ Catalizadores Positivos")
    if pos:
        for p in pos: st.markdown(f"
