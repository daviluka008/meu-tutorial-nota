import streamlit as st
import random
import json
import os

# =========================================
# 💾 ARQUIVO DE USUÁRIOS (PERSISTENTE)
# =========================================

ARQ_USUARIOS = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "r") as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    with open(ARQ_USUARIOS, "w") as f:
        json.dump(usuarios, f)

# =========================================
# 🔐 LOGIN
# =========================================

if "usuarios" not in st.session_state:
    st.session_state.usuarios = carregar_usuarios()

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = ""

def tela_login():

    st.title("🔐 Login")

    opcao = st.radio("Escolha", ["Entrar", "Criar conta"])

    if opcao == "Criar conta":

        email = st.text_input("E-mail")
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

            st.success("Conta criada com sucesso!")

    else:

        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):

            if email in st.session_state.usuarios and st.session_state.usuarios[email] == senha:
                st.session_state.logado = True
                st.session_state.usuario_atual = email
                st.rerun()
            else:
                st.error("Login inválido")

if not st.session_state.logado:
    tela_login()
    st.stop()

# =========================================
# 🎹 LÓGICA DOS ACORDES
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

    lista = notas_flat if "b" in raiz else notas_sharp

    if raiz not in lista:
        return None

    i = lista.index(raiz)

    tipos = {
        "": [0,4,7],
        "m": [0,3,7],
        "7": [0,4,7,10],
        "m7": [0,3,7,10],
        "7m": [0,3,7,10],
        "7M": [0,4,7,11],
        "M7": [0,4,7,11],
        "9": [0,4,7,10,14],
        "m9": [0,3,7,10,14],
        "add9": [0,4,7,14],
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

st.title("🎹 Sistema Completo de Acordes + Teoria")

st.write(f"👤 Logado: {st.session_state.usuario_atual}")

pagina = st.sidebar.selectbox(
    "Menu",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA (CURSO COMPLETO)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Curso Completo de Teoria Musical (Iniciante → Avançado)")

    st.subheader("🟢 Iniciante")
    st.write("Música é organização de sons no tempo.")

    st.subheader("Notas musicais")
    st.code("C D E F G A B")

    st.subheader("Tom e semitom")
    st.write("Semitom = 1 passo | Tom = 2 passos")

    st.subheader("Escala maior")
    st.code("C D E F G A B")

    st.subheader("🟡 Intermediário")
    st.write("C# = Db | D# = Eb | F# = Gb | G# = Ab | A# = Bb")

    st.subheader("Acordes básicos")
    st.code("Maior: C E G\nMenor: C Eb G")

    st.subheader("Intervalos")
    st.write("3ª maior = feliz | 3ª menor = triste")

    st.subheader("🔴 Avançado")
    st.subheader("Acordes com sétima")
    st.code("C7 = C E G Bb\nCmaj7 = C E G B")

    st.subheader("Campo harmônico")
    st.code("C - Dm - Em - F - G - Am - Bdim")

    st.subheader("Harmonia")
    st.write("Progressões criam emoção na música.")

    st.subheader("🎯 Resumo")
    st.write("Notas → Escalas → Acordes → Harmonia → Música")

# =========================================
# 🎹 PRÁTICA (SEM ALTERAÇÃO)
# =========================================

elif pagina == "🎹 Prática":

    st.header("🎹 Pratique Acordes")

    acorde = st.text_input("Digite um acorde")

    if st.button("Analisar"):
        resultado = gerar_acorde(acorde)

        if resultado:
            st.success(f"🎵 Notas: {resultado['notas']}")
        else:
            st.error("❌ Acorde inválido")

# =========================================
# 🎯 QUIZ (SEM ALTERAÇÃO)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    escala = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

    mapa = {n:i for i,n in enumerate(escala)}

    maior = [0,4,7]
    menor = [0,3,7]

    def montar(n,tipo):
        i = mapa[n]
        seq = maior if tipo=="maior" else menor
        return " ".join([escala[(i+x)%12] for x in seq])

    def gerar():
        p=[]
        for n in escala:
            p.append((f"{n} = ?", montar(n,"maior"), "maior"))
            p.append((f"{n}m = ?", montar(n,"menor"), "menor"))
        random.shuffle(p)
        return p

    if "quiz" not in st.session_state:
        st.session_state.quiz = gerar()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}

    if st.button("Novo quiz"):
        st.session_state.quiz = gerar()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}
        st.rerun()

    perguntas = st.session_state.quiz[:6]

    def opcoes(qid, correta):

        if qid in st.session_state.opcoes:
            return st.session_state.opcoes[qid]

        opts = {correta}
        falsas = ["C Eb G","C D G","D F A","E G B","F A C","G B D","A C E"]

        while len(opts) < 4:
            opts.add(random.choice(falsas))

        lista = list(opts)
        random.shuffle(lista)

        st.session_state.opcoes[qid] = lista
        return lista

    if not st.session_state.finalizado:

        for i,(q,correta,t) in enumerate(perguntas):
            st.session_state.respostas[i] = st.radio(
                q,
                options=opcoes(i,correta),
                key=f"q{i}",
                index=None
            )

    else:

        acertos = 0

        for i,(q,correta,t) in enumerate(perguntas):
            r = st.session_state.respostas.get(i)

            if r == correta:
                st.success(f"{q} ✔")
                acertos += 1
            else:
                st.error(f"{q} ❌ correta: {correta}")

        st.success(f"🎯 Você acertou {acertos}/6")

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()
