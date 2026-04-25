"""
EpisiaAgent · Streamlit UI
Epidemiology AI powered by LangChain + Groq + Episia
"""

import os
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

#  Page config 
st.set_page_config(
    page_title="EpisiaAgent · AI Epidemiologist",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

#  Theme 
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

T = st.session_state.theme

if T == "dark":
    BG0 = "#020912"; BG1 = "#060e1b"; BG2 = "#0a1628"
    CARD = "#0d1c35"; BORDER = "rgba(41,151,255,0.14)"
    T_PRI = "#e8f0f9"; T_SEC = "#7a9dc0"; T_MUT = "#3d5e7d"
    ACC = "#2997ff"; ACC2 = "#00c8b4"; ACC3 = "#e05c5c"; ACC4 = "#f5a623"
    PLT_BG = "#060e1b"; PLT_FONT = "#e8f0f9"
    SIDEBAR = "#030b17"; INPUT = "#0a1628"
    USER_BG = "#0a1628"; USER_BD = "rgba(41,151,255,0.30)"
    BOT_BG  = "#0d1c35"; BOT_BD  = "rgba(0,200,180,0.25)"
else:
    BG0 = "#f0f4fa"; BG1 = "#f8fafd"; BG2 = "#ffffff"
    CARD = "#ffffff"; BORDER = "rgba(15,80,180,0.15)"
    T_PRI = "#0d1f33"; T_SEC = "#2a4a6e"; T_MUT = "#6a8aaa"
    ACC = "#0a6fd8"; ACC2 = "#008f80"; ACC3 = "#c0392b"; ACC4 = "#b06800"
    PLT_BG = "#ffffff"; PLT_FONT = "#0d1f33"
    SIDEBAR = "#e6edf7"; INPUT = "#f0f4fa"
    USER_BG = "#e8f0fa"; USER_BD = "rgba(10,111,216,0.30)"
    BOT_BG  = "#e8f7f4"; BOT_BD  = "rgba(0,143,128,0.30)"

#  CSS (inclut le style pour les composants natifs st.chat_message) 
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=Sora:wght@400;500;600;700&display=swap');

:root {{
  --bg0:{BG0}; --bg1:{BG1}; --bg2:{BG2}; --card:{CARD};
  --border:{BORDER}; --t-pri:{T_PRI}; --t-sec:{T_SEC}; --t-mut:{T_MUT};
  --acc:{ACC}; --acc2:{ACC2}; --acc3:{ACC3}; --acc4:{ACC4};
  --sidebar:{SIDEBAR}; --input:{INPUT}; --user-bg:{USER_BG}; --user-bd:{USER_BD};
  --bot-bg:{BOT_BG}; --bot-bd:{BOT_BD};
}}
html,body,[class*="css"],.stApp {{
  font-family:'Sora',sans-serif !important;
  background-color:var(--bg0) !important;
  color:var(--t-pri) !important;
}}
section[data-testid="stSidebar"] {{
  background-color:var(--sidebar) !important;
  border-right:1px solid var(--border) !important;
}}
section[data-testid="stSidebar"] * {{ color:var(--t-pri) !important; }}

.stTextInput > div > div, .stSelectbox > div > div {{
  background-color:var(--input) !important;
  border-color:var(--border) !important;
  color:var(--t-pri) !important;
}}
.stTextInput input {{ color:var(--t-pri) !important; background:var(--input) !important; }}
.stButton > button {{
  background:var(--card) !important; color:var(--acc) !important;
  border:1px solid var(--border) !important;
  font-family:'IBM Plex Mono',monospace !important; font-size:.72rem !important;
}}
.stButton > button:hover {{ border-color:var(--acc) !important; }}

/* Styles pour les messages natifs Streamlit (st.chat_message) */
[data-testid="stChatMessage"] {{
  background: transparent !important;
}}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {{
  background: var(--card) !important;
  border-radius: 18px !important;
  padding: 0.6rem 1rem !important;
  border: 1px solid var(--border) !important;
  margin: 0.2rem 0 !important;
}}
/* Message utilisateur */
[data-testid="stChatMessage"][data-testid="user"] [data-testid="stMarkdownContainer"] {{
  background: var(--user-bg) !important;
  border-color: var(--user-bd) !important;
  border-top-right-radius: 4px !important;
}}
/* Message assistant */
[data-testid="stChatMessage"][data-testid="assistant"] [data-testid="stMarkdownContainer"] {{
  background: var(--bot-bg) !important;
  border-color: var(--bot-bd) !important;
  border-top-left-radius: 4px !important;
}}
/* Avatar personnalisé (optionnel) */
[data-testid="stChatMessageAvatar"] {{
  background: transparent !important;
}}
[data-testid="stChatMessageAvatar"] svg {{
  stroke: var(--acc) !important;
  fill: var(--acc) !important;
}}
.tool-badge {{
  display: inline-block;
  background: rgba(41,151,255,.08);
  color: var(--acc);
  border: 1px solid rgba(41,151,255,.2);
  border-radius: 4px;
  padding: .1rem .4rem;
  font-family: 'IBM Plex Mono', monospace;
  font-size: .6rem;
  margin: .1rem .15rem;
}}
.tool-bar {{
  margin-top: .5rem;
  padding-top: .4rem;
  border-top: 1px solid var(--border);
  font-size: .62rem;
  color: var(--t-mut);
  font-family: 'IBM Plex Mono', monospace;
}}
.status-ok  {{ color: var(--acc2); font-family: 'IBM Plex Mono', monospace; font-size: .7rem; }}
.status-err {{ color: var(--acc3); font-family: 'IBM Plex Mono', monospace; font-size: .7rem; }}
.logo-wrap  {{ font-family: 'Sora', sans-serif; font-size: 1.3rem; font-weight: 700; }}
.logo-epi   {{ color: var(--acc); }}
.logo-sia   {{ color: var(--t-pri); }}
.logo-agent {{ color: var(--acc2); font-size: .9rem; }}
.sec-hdr {{
  font-size: .72rem; font-weight: 600; color: var(--t-sec);
  letter-spacing: .1em; text-transform: uppercase;
  border-bottom: 1px solid var(--border); padding-bottom: .3rem;
  margin-bottom: .6rem; margin-top: 1rem;
}}
hr {{ border-color: var(--border) !important; }}
div[data-testid="stSuccess"] {{ background: var(--bg1) !important; border: 1px solid var(--acc2) !important; }}
div[data-testid="stError"]   {{ background: var(--bg1) !important; border: 1px solid var(--acc3) !important; }}
div[data-testid="stInfo"]    {{ background: var(--bg1) !important; border: 1px solid var(--acc) !important; }}
div[data-testid="stSuccess"] p, div[data-testid="stError"] p, div[data-testid="stInfo"] p {{
  color: var(--t-pri) !important;
}}
</style>
""", unsafe_allow_html=True)

#  Session state 
if "agent"        not in st.session_state: st.session_state.agent     = None
if "messages"     not in st.session_state: st.session_state.messages  = []
if "api_ready"    not in st.session_state: st.session_state.api_ready = False
if "lang"         not in st.session_state: st.session_state.lang      = "en"
if "processing"   not in st.session_state: st.session_state.processing = False
if "temp_message" not in st.session_state: st.session_state.temp_message = None

#  Sidebar 
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <span class="logo-epi">Epi</span><span class="logo-sia">sia</span>
      <span class="logo-agent">Agent</span>
    </div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;
    color:var(--t-mut);letter-spacing:.08em;text-transform:uppercase;margin-bottom:.3rem">
    AI Epidemiologist · Groq LPU</div>
    """, unsafe_allow_html=True)

    st.divider()


    #  Configuration 
    st.markdown('<div class="sec-hdr">Configuration</div>', unsafe_allow_html=True)

    from agent.agent import GROQ_MODELS
    model_choice = st.selectbox(
        "Model",
        list(GROQ_MODELS.keys()),
        format_func=lambda x: GROQ_MODELS[x],
        label_visibility="collapsed",
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.05)

    groq_key = os.getenv("GROQ_API_KEY", "")

    prev_model = st.session_state.get("_model", None)
    prev_temp  = st.session_state.get("_temp",  None)
    model_changed = (prev_model != model_choice) or (prev_temp != temperature)

    if not st.session_state.api_ready or model_changed:
        if not groq_key:
            st.markdown(
                f'<div style="background:#1e0505;border:1px solid var(--acc3);border-radius:6px;'
                f'padding:.5rem .7rem;font-size:.7rem;color:var(--acc3);font-family:IBM Plex Mono,monospace">'
                f'⚠ GROQ_API_KEY manquant dans .env<br>'
                f'Ajoutez: GROQ_API_KEY=gsk_...</div>',
                unsafe_allow_html=True
            )
        else:
            with st.spinner("Initialisation agent..."):
                try:
                    from agent.agent import EpisiaAgent
                    st.session_state.agent     = EpisiaAgent(model=model_choice, temperature=temperature, verbose=False)
                    st.session_state.api_ready = True
                    st.session_state._model    = model_choice
                    st.session_state._temp     = temperature
                except Exception as e:
                    st.session_state.api_ready = False
                    st.markdown(f'<div style="font-size:.7rem;color:var(--acc3)">Erreur: {e}</div>', unsafe_allow_html=True)

    if st.session_state.api_ready:
        st.markdown(
            f'<div class="status-ok">● Agent actif · {model_choice.split("-")[0].upper()}</div>'
            f'<div style="font-size:.6rem;color:var(--t-mut);font-family:IBM Plex Mono,monospace;margin-top:.2rem">',
            unsafe_allow_html=True
        )
    else:
        st.markdown(f'<div class="status-err">● Agent hors ligne</div>', unsafe_allow_html=True)

    st.divider()

    #  Tools info 
    st.markdown('<div class="sec-hdr">Available tools</div>', unsafe_allow_html=True)
    tools_info = [
        ("sample_size_rr",    "Cohort · Risk Ratio"),
        ("sample_size_or",    "Case-Control · OR"),
        ("sample_size_diag",  "Diagnostic test n"),
        ("sample_size_prop",  "Single proportion"),
        ("vaccine_efficacy",  "Vaccine Efficacy (VE)"),
        ("diagnostic_test",   "RDT / Test evaluation"),
        ("seir_simulation",   "SEIR outbreak model"),
        ("hiv_cascade",       "HIV 90-90-90 cascade"),
        ("muac_analysis",     "MUAC malnutrition"),
        ("epidemic_alert",    "Epidemic alert detection"),
    ]
    for tool_id, tool_label in tools_info:
        st.markdown(
            f'<div style="font-size:.68rem;color:var(--t-sec);font-family:IBM Plex Mono,monospace;'
            f'padding:.15rem 0">◈ {tool_label}</div>',
            unsafe_allow_html=True
        )

    st.divider()

    #  Language 
    lang = st.radio(
        "Response language",
        ["English 🇬🇧", "Français 🇫🇷"],
        label_visibility="collapsed",
        horizontal=True,
    )
    st.session_state.lang = "fr" if "rançais" in lang else "en"

    st.divider()

    if st.button("🗑 Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.temp_message = None
        if st.session_state.agent:
            st.session_state.agent.reset()
        st.rerun()

    st.markdown(
        f'<div style="font-size:.6rem;color:var(--t-mut);margin-top:.5rem;'
        f'font-family:IBM Plex Mono,monospace">'
        f'Episia v0.1.1<br>'
        f'<a href="https://github.com/Xcept-Health/episia" '
        f'style="color:var(--acc)">github.com/Xcept-Health/episia</a></div>',
        unsafe_allow_html=True
    )


# 
# Main area – Chat interface (scrollable history + fixed input)
# 

st.markdown(
    f'<h1 style="font-family:Sora,sans-serif;font-size:1.5rem;font-weight:700;'
    f'color:var(--t-pri);margin-bottom:.1rem">'
    f'<span style="color:var(--acc)">Epi</span>siaAgent '
    f'<span style="font-size:1rem;color:var(--t-mut);font-weight:400">· AI Epidemiologist for Africa</span></h1>',
    unsafe_allow_html=True
)

#  Exemples (uniquement si aucun message) 
examples_en = [
    "Sample size for a cohort study: baseline risk 10%, expected RR=2.5, 80% power",
    "Vaccine efficacy: 12 cases among 3000 vaccinated, 87 cases among 3000 unvaccinated",
    "SEIR meningitis Kaya district, population 350000, beta=0.42, 35% vaccination coverage",
    "HIV cascade Burkina Faso: 110000 PLHIV, 66% know status, 79% on ART, 88% suppressed",
    "MUAC results: 8125 screened, 450 SAM, 820 MAM, OTP capacity 120 slots",
    "Epidemic alert analysis: weekly cases [2,3,5,12,28,45,60,42,18,8,3], threshold 15",
    "Malaria RDT evaluation: 142 TP, 18 FP, 23 FN, 317 TN. Local prevalence 20%",
    "Survey sample size: expected vaccination coverage 70%, precision ±5%, cluster DEFF=1.5",
]
examples_fr = [
    "Taille d'échantillon étude de cohorte : risque basal 10%, RR attendu 2.5, puissance 80%",
    "Efficacité vaccinale MenAfriVac : 12 cas sur 3000 vaccinés, 87 cas sur 3000 non vaccinés",
    "Modèle SEIR méningite district Kaya, population 350000, couverture vaccinale 35%",
    "Cascade VIH Burkina Faso : 110000 PVVIH, 66% connaissent statut, 79% sous ARV, 88% supprimés",
    "Résultats MUAC Titao : 8125 dépistés, 450 MAS, 820 MAM, capacité OTP 120 places",
    "Détection alerte épidémique : cas hebdomadaires [2,3,5,12,28,45,60,42,18,8,3], seuil 15",
    "Évaluation TDR paludisme : 142 VP, 18 FP, 23 FN, 317 VN. Prévalence locale 20%",
    "Taille d'échantillon enquête couverture vaccinale attendue 70%, précision ±5%, DEFF=1.5",
]
examples = examples_fr if st.session_state.lang == "fr" else examples_en

if not st.session_state.messages and not st.session_state.temp_message:
    st.markdown(
        f'<div style="font-size:.78rem;color:var(--t-sec);margin-bottom:.8rem">'
        f'{"Exemples de questions — cliquez pour l’utiliser :" if st.session_state.lang == "fr" else "Example queries — click to use:"}'
        f'</div>',
        unsafe_allow_html=True
    )
    cols = st.columns(2)
    for i, ex in enumerate(examples):
        with cols[i % 2]:
            if st.button(ex, key=f"ex_{i}", use_container_width=True):
                st.session_state._pending_input = ex
                st.rerun()

#  Affichage de l’historique des messages (chat scrollable) 
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    tools_used = msg.get("tools_used", [])
    with st.chat_message(role):
        st.markdown(content)
        if tools_used:
            badges = "".join([f'<span class="tool-badge">⚙ {t}</span>' for t in tools_used])
            st.markdown(
                f'<div class="tool-bar">'
                f'{"Outils utilisés" if st.session_state.lang == "fr" else "Tools used"}: {badges}</div>',
                unsafe_allow_html=True
            )
        if role == "assistant" and "elapsed" in msg:
            st.caption(f" {msg['elapsed']}")

#  Message temporaire « réfléchit... » 
if st.session_state.temp_message:
    with st.chat_message("assistant"):
        st.markdown(st.session_state.temp_message)

#  Zone de saisie fixe (st.chat_input) 
prompt = st.chat_input(
    placeholder="Posez votre question épidémiologique..." if st.session_state.lang == "fr"
    else "Ask your epidemiological question..."
)

#  Traitement de la requête 
# On utilise un flag "processing" pour éviter les doubles appels (due aux reruns)
if prompt and not st.session_state.processing:
    st.session_state.processing = True

    # Récupérer la requête (depuis le prompt ou depuis un clic sur exemple)
    query = prompt
    if st.session_state.get("_pending_input"):
        query = st.session_state.pop("_pending_input")

    # Vérifier que l’agent est prêt
    if not st.session_state.api_ready or st.session_state.agent is None:
        st.error(
            "Agent not ready. Check that GROQ_API_KEY is set in your .env file."
            if st.session_state.lang == "en"
            else "Agent non prêt. Vérifiez que GROQ_API_KEY est défini dans votre fichier .env."
        )
        st.session_state.processing = False
        st.rerun()
    else:
        # Ajouter le message utilisateur à l’historique
        st.session_state.messages.append({"role": "user", "content": query})

        # Ajouter un message temporaire de réflexion
        thinking_text = "*EpisiaAgent réfléchit...*" if st.session_state.lang == "fr" else "*EpisiaAgent is thinking...*"
        st.session_state.temp_message = thinking_text

        # Forcer un rerun pour afficher immédiatement l’UI avec le message temporaire
        st.rerun()

# Si on est en train de traiter (processing=True) mais qu’on a déjà affiché le message temporaire,
# on exécute l’agent et on remplace le message temporaire par la réponse finale.
# Ce bloc s’exécute après le rerun déclenché ci-dessus.
if st.session_state.processing and st.session_state.temp_message:
    # Récupérer la dernière requête de l’utilisateur (le dernier message)
    last_user_msg = next((m for m in reversed(st.session_state.messages) if m["role"] == "user"), None)
    if last_user_msg is None:
        st.session_state.processing = False
        st.session_state.temp_message = None
        st.rerun()

    query = last_user_msg["content"]

    # Ajouter l’indication de langue si nécessaire
    if st.session_state.lang == "fr" and not any(w in query.lower() for w in ["réponds", "en français", "français"]):
        query_processed = query + "\n\n(Réponds en français)"
    else:
        query_processed = query

    # Appel à l’agent
    t0 = time.time()
    try:
        result = st.session_state.agent.run(query_processed)
        elapsed = time.time() - t0

        # Remplacer le message temporaire par la vraie réponse
        st.session_state.temp_message = None
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "tools_used": result["tools_used"],
            "model": model_choice.split("-")[0].upper(),
            "elapsed": f"{elapsed:.1f}s",
        })
    except Exception as e:
        st.session_state.temp_message = None
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Error: {str(e)}\n\nPlease check your API key and try again.",
            "tools_used": [],
            "model": "Error",
        })
    finally:
        st.session_state.processing = False
        st.rerun()

#  Petit pied de page (optionnel) 
if st.session_state.messages:
    last_bot = [m for m in st.session_state.messages if m["role"] == "assistant"]
    if last_bot:
        last = last_bot[-1]
        elapsed = last.get("elapsed", "")
        tools_count = len(last.get("tools_used", []))
        st.markdown(
            f'<div style="font-size:.62rem;color:var(--t-mut);font-family:IBM Plex Mono,monospace;'
            f'text-align:right;margin-top:.3rem">'
            f'Last response: {elapsed} · {tools_count} tool(s) called'
            f'</div>',
            unsafe_allow_html=True
        )