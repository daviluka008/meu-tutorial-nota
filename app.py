import streamlit as st
import random
import json
import os

# =========================================
# 🔐 USUÁRIOS + PROGRESSO
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

    st.title("🔐 Login do Sistema")

    modo = st.radio("Escolha", ["Entrar", "Criar conta"])

    if modo == "Criar conta":

        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Criar conta"):

            if email == "" or senha == "":
                st.error("Preencha todos os campos")
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
# 🎹 LÓGICA DOS ACORDES (SEU ORIGINAL)
# =========================================

notas_sharp = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
notas_flat = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]

def separar_acorde(acorde):
    if len(acorde) > 1 and acorde[1] in ["#","b"]:
        return acorde[:2], acorde[2:].lower()
    return acorde[0], acorde[1:].lower()

def gerar_acorde(acorde):

    acorde = acorde.strip()

    if "/" in acorde:
        acorde_principal, baixo = acorde.split("/")
    else:
        acorde_principal = acorde
        baixo = None

    raiz, tipo = separar_acorde(acorde_principal)

    lista = notas_sharp if raiz in notas_sharp else notas_flat

    if raiz not in lista:
        return None

    i = lista.index(raiz)

    tipos = {
        "": [0,4,7],
        "m": [0,3,7],
        "7": [0,4,7,10],
        "m7": [0,3,7,10],
        "7M": [0,4,7,11],
        "M7": [0,4,7,11],
        "9": [0,4,7,10,14],
        "sus2": [0,2,7],
        "sus4": [0,5,7],
        "dim": [0,3,6],
        "aug": [0,4,8],
    }

    if tipo not in tipos:
        return None

    notas = [lista[(i+x)%12] for x in tipos[tipo]]

    return {"notas": notas}

# =========================================
# 🌐 CONFIG
# =========================================

st.set_page_config(page_title="🎹 Acordes App", page_icon="🎹")

st.title("🎹 Sistema Completo de Música")

pagina = st.sidebar.selectbox(
    "Menu",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA (CURSO COMPLETO)
# =========================================

if pagina == "📚 Teoria":

    st.header("📘 Curso Completo de Música")

    prog = get_progress()
    nivel = prog["nivel"]

    st.write(f"📊 Seu nível: {nivel}")

    # =========================
    # 🔰 NÍVEL 1
    # =========================
    st.subheader("🔰 Nível 1 - Fundamentos")

    st.write("""
- Notas musicais (C D E F G A B)
- Semitom e Tom
- Escala cromática
""")

    if nivel >= 1:
        if st.button("Concluir Nível 1"):
            prog["nivel"] = 2
            salvar_progresso(st.session_state.progresso)
            st.rerun()
    else:
        st.warning("Bloqueado")

    # =========================
    # 🎹 NÍVEL 2
    # =========================
    st.subheader("🎹 Nível 2 - Acordes")

    if nivel >= 2:
        st.write("""
- Tríades (maior e menor)
- Formação de acordes
- Intervalos básicos
""")

        if st.button("Concluir Nível 2"):
            prog["nivel"] = 3
            salvar_progresso(st.session_state.progresso)
            st.rerun()
    else:
        st.warning("Bloqueado")

    # =========================
    # 🔥 NÍVEL 3
    # =========================
    st.subheader("🔥 Nível 3 - Harmonia")

    if nivel >= 3:
        st.write("""
- Campo harmônico
- Funções harmônicas
- Progressões II–V–I
""")

        if st.button("Concluir Nível 3"):
            prog["nivel"] = 4
            salvar_progresso(st.session_state.progresso)
            st.rerun()
    else:
        st.warning("Bloqueado")

    # =========================
    # 🚀 NÍVEL 4
    # =========================
    st.subheader("🚀 Nível 4 - Avançado")

    if nivel >= 4:
        st.write("""
- Acordes com extensão (9, 11, 13)
- Substituições harmônicas
- Modulação
""")

        if st.button("Finalizar Curso"):
            prog["nivel"] = 5
            salvar_progresso(st.session_state.progresso)
            st.success("Curso completo!")
            st.balloons()
    else:
        st.warning("Bloqueado")

# =========================================
# 🎹 PRÁTICA (INALTERADA)
# =========================================

elif pagina == "🎹 Prática":

    st.header("🎹 Prática de Acordes")

    acorde = st.text_input("Digite um acorde")

    if st.button("Analisar"):
        r = gerar_acorde(acorde)
        if r:
            st.success(r["notas"])
        else:
            st.error("Inválido")

# =========================================
# 🎯 QUIZ (INALTERADO)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    escala = notas_sharp
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
