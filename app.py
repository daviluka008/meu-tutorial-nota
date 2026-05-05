import streamlit as st
import random
import json
import os

# =========================================
# 💾 LOGIN (PERSISTENTE)
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

notas_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def gerar_acorde(acorde):

    acorde = acorde.strip()

    if "/" in acorde:
        acorde_principal, baixo = acorde.split("/")
    else:
        acorde_principal = acorde
        baixo = None

    raiz = acorde_principal[0]

    if raiz not in notas_sharp:
        return None

    return {"notas": [raiz], "baixo": baixo}

# =========================================
# 🌐 CONFIG
# =========================================

st.set_page_config(page_title="🎹 Acordes App", page_icon="🎹")

st.title("🎹 Sistema Completo de Acordes + Teoria")

pagina = st.sidebar.selectbox(
    "📌 Menu",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA (MELHORADA COMPLETA)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa (Do Zero ao Avançado)")

    # 🟢 BÁSICO
    st.subheader("🎵 O que é música?")
    st.write("""
Música é a organização dos sons no tempo.

Elementos:
- Melodia
- Harmonia
- Ritmo
- Timbre
""")

    st.subheader("🎼 Notas musicais")
    st.code("C D E F G A B")

    # 🟡 INTERMEDIÁRIO
    st.subheader("🎹 Tom e semitom")
    st.write("Semitom = 1 passo | Tom = 2 passos")

    st.subheader("🎼 Sustenidos e bemóis")
    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.subheader("🎼 Escala maior")
    st.code("T – T – S – T – T – T – S")
    st.code("C D E F G A B")

    st.subheader("🎼 Escala menor")
    st.code("T – S – T – T – S – T – T")
    st.code("A B C D E F G")

    # 🔵 AVANÇADO
    st.subheader("🎹 Formação de acordes")
    st.code("""
Maior: 1 3 5 → C E G
Menor: 1 b3 5 → C Eb G
""")

    st.subheader("🎼 Intervalos")
    st.write("""
3ª maior = som feliz  
3ª menor = som triste  
5ª justa = estabilidade  
7ª = tensão
""")

    st.subheader("🎼 Acordes com sétima")
    st.code("""
C7 = C E G Bb
Cmaj7 = C E G B
""")

    st.subheader("🎼 Campo harmônico")
    st.code("C - Dm - Em - F - G - Am - Bdim")

    st.subheader("🎯 Resumo final")
    st.write("Escalas → Intervalos → Acordes → Harmonia → Música")

# =========================================
# 🎹 PRÁTICA (SEM MUDAR)
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
# 🎯 QUIZ (SEM MUDAR)
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
        return " ".join([escala[(i+x)%12] for x in intervalos])

    def gerar_perguntas():
        pool = []
        for n in escala:
            pool.append((f"{n} = ?", montar_acorde(n,"maior"), "maior"))
            pool.append((f"{n}m = ?", montar_acorde(n,"menor"), "menor"))
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

    def gerar_opcoes(qid, correta, tipo):

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
        lista.sort()

        st.session_state.opcoes[qid] = lista[:4]
        return lista[:4]

    if not st.session_state.finalizado:

        for i,(q,correta,tipo) in enumerate(perguntas):

            st.session_state.respostas[i] = st.radio(
                q,
                options=gerar_opcoes(i,correta,tipo),
                key=f"q_{i}",
                index=None
            )

    else:

        acertos = 0
        st.divider()

        for i,(q,correta,tipo) in enumerate(perguntas):

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
