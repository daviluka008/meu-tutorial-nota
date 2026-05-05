import streamlit as st
import random
import json
import os

# =========================================
# 🔐 LOGIN + PROGRESSO
# =========================================

ARQ_USUARIOS = "usuarios.json"
ARQ_PROGRESSO = "progresso.json"

def carregar_usuarios():
    if os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "r") as f:
            return json.load(f)
    return {}

def salvar_usuarios(data):
    with open(ARQ_USUARIOS, "w") as f:
        json.dump(data, f)

def carregar_progresso():
    if os.path.exists(ARQ_PROGRESSO):
        with open(ARQ_PROGRESSO, "r") as f:
            return json.load(f)
    return {}

def salvar_progresso(data):
    with open(ARQ_PROGRESSO, "w") as f:
        json.dump(data, f)

if "usuarios" not in st.session_state:
    st.session_state.usuarios = carregar_usuarios()

if "progresso" not in st.session_state:
    st.session_state.progresso = carregar_progresso()

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# =========================================
# 🔐 LOGIN
# =========================================

def login():

    st.title("🔐 Login")

    modo = st.radio("Escolha", ["Entrar", "Criar conta"])

    if modo == "Criar conta":

        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Criar conta"):

            if email == "" or senha == "":
                st.error("Preencha tudo")
                return

            if email in st.session_state.usuarios:
                st.error("Usuário já existe")
                return

            st.session_state.usuarios[email] = senha
            salvar_usuarios(st.session_state.usuarios)

            st.success("Conta criada!")

    else:

        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):

            if email in st.session_state.usuarios and st.session_state.usuarios[email] == senha:
                st.session_state.logado = True
                st.session_state.usuario = email
                st.rerun()
            else:
                st.error("Login inválido")

if not st.session_state.logado:
    login()
    st.stop()

# =========================================
# 📊 PROGRESSO
# =========================================

def get_progress():
    u = st.session_state.usuario
    if u not in st.session_state.progresso:
        st.session_state.progresso[u] = {"nivel": 1}
    return st.session_state.progresso[u]

# =========================================
# 🎹 ACORDES (CORRIGIDO)
# =========================================

notas = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

def separar_acorde(a):
    if len(a) > 1 and a[1] in ["#","b"]:
        return a[:2], a[2:].lower()
    return a[0], a[1:].lower()

def gerar_acorde(acorde):

    acorde = acorde.strip()

    if "/" in acorde:
        base, baixo = acorde.split("/")
    else:
        base = acorde
        baixo = None

    raiz, tipo = separar_acorde(base)

    if raiz not in notas:
        return None

    i = notas.index(raiz)

    tipos = {
        "": [0,4,7],
        "m": [0,3,7],
        "7": [0,4,7,10],
        "m7": [0,3,7,10],
        "7M": [0,4,7,11],
        "dim": [0,3,6],
        "aug": [0,4,8],
        "sus2": [0,2,7],
        "sus4": [0,5,7]
    }

    if tipo not in tipos:
        return None

    notas_acorde = [notas[(i+x)%12] for x in tipos[tipo]]

    return {"notas": notas_acorde, "baixo": baixo}

# =========================================
# 🌐 CONFIG
# =========================================

st.set_page_config(page_title="🎹 Curso Musical", page_icon="🎹")

st.title("🎹 Plataforma Completa de Música")

pagina = st.sidebar.selectbox(
    "Menu",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA (VERSÃO CURSO REAL)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Curso Completo de Música (Do Zero ao Avançado)")

    prog = get_progress()
    nivel = prog["nivel"]

    st.write(f"📊 Nível atual: {nivel}")

    # =========================
    # 🔰 FUNDAMENTOS
    # =========================
    st.subheader("🔰 1. Fundamentos da Música")

    st.write("""
🎵 Música é som organizado no tempo.

Elementos:
- Melodia
- Harmonia
- Ritmo
- Timbre

🎼 Sistema musical:
C D E F G A B

🎹 Semitom = menor distância  
🎹 Tom = 2 semitons
""")

    st.info("Exemplo: C → C# = semitom | C → D = tom")

    # =========================
    # 🎹 ESCALAS
    # =========================
    st.subheader("🎹 2. Escalas Musicais")

    st.write("""
🎼 Escala maior:
T - T - S - T - T - T - S

Exemplo:
C D E F G A B

🎼 Escala menor:
T - S - T - T - S - T - T

Exemplo:
A B C D E F G
""")

    # =========================
    # 🎼 ACORDES
    # =========================
    st.subheader("🎼 3. Formação de Acordes")

    st.write("""
✔ Maior = 1 + 3 + 5  
✔ Menor = 1 + b3 + 5  

Exemplo:
C = C E G  
Cm = C Eb G  

✔ Diminuto = 1 b3 b5  
✔ Aumentado = 1 3 #5
""")

    # =========================
    # 🔥 HARMONIA
    # =========================
    st.subheader("🔥 4. Harmonia Funcional")

    st.write("""
Campo harmônico de C:

C Dm Em F G Am Bdim

Funções:
- Tônica (repouso)
- Subdominante (movimento)
- Dominante (tensão)

Progressões:
I–IV–V  
II–V–I  
I–V–VI–IV
""")

    # =========================
    # 🚀 AVANÇADO
    # =========================
    st.subheader("🚀 5. Avançado")

    st.write("""
🎹 Acordes com extensão:
7ª, 9ª, 11ª, 13ª

🎼 Modulação:
Mudança de tonalidade

🎧 Reharmonização:
Trocar acordes mantendo sentido

🎛 Produção musical:
EQ, compressão, reverb
""")

# =========================================
# 🎹 PRÁTICA (INTACTA)
# =========================================

elif pagina == "🎹 Prática":

    st.header("🎹 Prática de Acordes")

    acorde = st.text_input("Digite um acorde")

    if st.button("Analisar"):

        r = gerar_acorde(acorde)

        if r:

            st.success("🎵 Notas:")
            st.write(r["notas"])

            st.write("🎸 Baixo:")
            st.write(r["baixo"] if r["baixo"] else "Sem baixo")

        else:
            st.error("Inválido")

# =========================================
# 🎯 QUIZ (INTACTO)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz")

    escala = notas
    mapa = {n:i for i,n in enumerate(escala)}

    maior = [0,4,7]
    menor = [0,3,7]

    def montar(n,t):
        i = mapa[n]
        ints = maior if t=="maior" else menor
        return " ".join([escala[(i+x)%12] for x in ints])

    def gerar():
        pool=[]
        for n in escala:
            pool.append((f"{n}=",montar(n,"maior")))
            pool.append((f"{n}m=",montar(n,"menor")))
        random.shuffle(pool)
        return pool

    if "q" not in st.session_state:
        st.session_state.q = gerar()
        st.session_state.res = {}
        st.session_state.done = False

    perguntas = st.session_state.q[:6]

    if not st.session_state.done:

        for i,(q,c) in enumerate(perguntas):
            st.session_state.res[i] = st.radio(q,[c],key=i)

    else:

        acertos = 0
        for i,(q,c) in enumerate(perguntas):
            if st.session_state.res[i] == c:
                acertos += 1

        st.success(f"Você acertou {acertos}/6")
