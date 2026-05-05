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
# 🎹 ACORDES (INALTERADO)
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
# 🌐 MENU
# =========================================

st.set_page_config(page_title="🎹 Curso Musical", page_icon="🎹")

st.title("🎹 Sistema Completo de Música")

pagina = st.sidebar.selectbox(
    "Menu",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Curso Completo de Música")

    prog = get_progress()
    st.write(f"📊 Nível atual: {prog['nivel']}")

    st.subheader("🔰 Fundamentos")
    st.write("Música = som organizado no tempo")

    st.subheader("🎹 Escalas")
    st.write("Maior: T T S T T T S")

    st.subheader("🎼 Acordes")
    st.write("Maior = 1 3 5 | Menor = 1 b3 5")

    st.subheader("🔥 Harmonia")
    st.write("C Dm Em F G Am Bdim")

    st.subheader("🚀 Avançado")
    st.write("Extensões, modulação e produção")

# =========================================
# 🎹 PRÁTICA (INTACTA)
# =========================================

elif pagina == "🎹 Prática":

    st.header("🎹 Prática de Acordes")

    acorde = st.text_input("Digite um acorde")

    if st.button("Analisar"):

        resultado = gerar_acorde(acorde)

        if resultado:
            st.success("🎵 Notas:")
            st.write(resultado["notas"])

            st.write("🎸 Baixo:")
            st.write(resultado["baixo"] if resultado["baixo"] else "Sem baixo")

        else:
            st.error("❌ Acorde inválido")

# =========================================
# 🎯 QUIZ (ORIGINAL RESTAURADO 100%)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    escala = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

    mapa = {nota: i for i, nota in enumerate(escala)}

    maior = [0,4,7]
    menor = [0,3,7]

    def montar_acorde(nota, tipo):
        i = mapa[nota]
        intervalos = maior if tipo == "maior" else menor
        return " ".join([escala[(i + x) % 12] for x in intervalos])

    def gerar_perguntas():
        pool = []
        for n in escala:
            pool.append((f"{n} = ?", montar_acorde(n, "maior"), "maior"))
            pool.append((f"{n}m = ?", montar_acorde(n, "menor"), "menor"))
        random.shuffle(pool)
        return pool

    if "quiz" not in st.session_state:
        st.session_state.quiz = gerar_perguntas()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = gerar_perguntas()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}
        st.rerun()

    perguntas = st.session_state.quiz[:6]

    def gerar_opcoes(qid, correta):

        if qid in st.session_state.opcoes:
            return st.session_state.opcoes[qid]

        opcoes = {correta}

        falsas = [
            "C Eb G","C D G","C E G#",
            "D F A","D F# A","E G B",
            "F A C","F Ab C","G B D",
            "G Bb D","A C E","A C# E",
            "B D F","B D# F#"
        ]

        while len(opcoes) < 4:
            opcoes.add(random.choice(falsas))

        lista = list(opcoes)
        random.shuffle(lista)

        st.session_state.opcoes[qid] = lista[:4]
        return lista[:4]

    if not st.session_state.finalizado:

        for i, (q, correta, tipo) in enumerate(perguntas):

            st.session_state.respostas[i] = st.radio(
                q,
                options=gerar_opcoes(i, correta),
                key=f"q_{i}",
                index=None
            )

    else:

        acertos = 0

        for i, (q, correta, tipo) in enumerate(perguntas):

            if st.session_state.respostas[i] == correta:
                acertos += 1

        st.success(f"🎯 Você acertou {acertos}/6")

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()
