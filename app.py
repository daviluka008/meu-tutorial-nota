import streamlit as st
import random
import json
import os

# =========================================
# 🔐 USUÁRIOS
# =========================================

ARQ_USUARIOS = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "r") as f:
            return json.load(f)
    return {}

def salvar_usuarios(data):
    with open(ARQ_USUARIOS, "w") as f:
        json.dump(data, f)

if "usuarios" not in st.session_state:
    st.session_state.usuarios = carregar_usuarios()

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

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if modo == "Criar conta":

        if st.button("Criar conta"):

            if email in st.session_state.usuarios:
                st.error("Usuário já existe")
            else:
                st.session_state.usuarios[email] = senha
                salvar_usuarios(st.session_state.usuarios)
                st.success("Conta criada!")

    else:

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
# 🎹 ACORDES
# =========================================

notas = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

def separar_acorde(a):
    if len(a) > 1 and a[1] in ["#","b"]:
        return a[:2], a[2:].lower()
    return a[0], a[1:].lower()

def gerar_acorde(acorde):

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

pagina = st.sidebar.selectbox("Menu", ["📚 Teoria", "🎹 Prática", "🎯 Quiz"])

# =========================================
# 📚 TEORIA (VERSÃO PROFISSIONAL)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Curso Completo de Música (Do Zero ao Avançado)")

    st.subheader("🔰 MÓDULO 1 — FUNDAMENTOS ABSOLUTOS")

    st.write("""
Música é a organização do som no tempo.

Ela tem:

• Melodia  
• Harmonia  
• Ritmo  
• Timbre  

Sistema musical:
C D E F G A B
""")

    st.subheader("🎼 MÓDULO 2 — INTERVALOS")

    st.write("""
C → D = tom  
C → C# = semitom  

• 3ª maior = alegria  
• 3ª menor = tristeza  
• 5ª justa = estabilidade  
• 7ª = tensão
""")

    st.subheader("🎹 MÓDULO 3 — ESCALAS")

    st.write("""
Maior: T T S T T T S  
Menor: T S T T S T T  

C maior:
C D E F G A B
""")

    st.subheader("🎸 MÓDULO 4 — ACORDES")

    st.write("""
Maior = 1 3 5  
Menor = 1 b3 5  
Dim = 1 b3 b5  
Aug = 1 3 #5
""")

    st.subheader("🔥 MÓDULO 5 — CAMPO HARMÔNICO")

    st.write("""
C: C Dm Em F G Am Bdim

Funções:
Tônica / Subdominante / Dominante
""")

    st.subheader("🚀 MÓDULO 6 — AVANÇADO")

    st.write("""
Acordes 7, 9, 11, 13  
Substituição  
Modulação  
Reharmonização
""")

    st.subheader("🎯 MÓDULO 7 — APLICAÇÃO")

    st.write("""
C → Am → F → G

Base de milhares de músicas reais.
""")

# =========================================
# 🎹 PRÁTICA
# =========================================

elif pagina == "🎹 Prática":

    st.header("🎹 Prática de Acordes")

    acorde = st.text_input("Digite um acorde")

    if st.button("Analisar"):

        r = gerar_acorde(acorde)

        if r:
            st.success(r["notas"])
            st.write("Baixo:", r["baixo"] if r["baixo"] else "sem baixo")
        else:
            st.error("Inválido")

# =========================================
# 🎯 QUIZ (INTACTO)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

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

            resposta = st.session_state.res[i]

            if resposta == c:
                st.success(f"{q} ✔ Correto: {c}")
                acertos += 1
            else:
                st.error(f"{q} ❌ Sua resposta: {resposta} | Correto: {c}")

        st.success(f"🎯 Você acertou {acertos}/6")

    if st.button("Ver resultado"):
        st.session_state.done = True
        st.rerun()
