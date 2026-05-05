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

notas_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
notas_flat  = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

def separar_acorde(acorde):
    if len(acorde) > 1 and acorde[1] in ["#", "b"]:
        return acorde[:2], acorde[2:].lower()
    return acorde[0], acorde[1:].lower()

def gerar_acorde(acorde):
    acorde = acorde.strip()

    if "/" in acorde:
        acorde_principal, baixo = acorde.split("/")
        baixo = baixo.strip()
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

    notas = [lista[(i + x) % 12] for x in tipos[tipo]]

    return {"notas": notas, "baixo": baixo}

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
# 📚 TEORIA (EBOOK COMPLETO)
# =========================================

if pagina == "📚 Teoria":

    st.header("📘 Curso Completo de Música (Do Zero ao Avançado)")

    # =========================
    # 🟢 INICIANTE
    # =========================
    st.subheader("🟢 1. Iniciante — Fundamentos")

    st.write("""
🎵 Música é a organização de sons.

Ela é formada por 4 pilares:

- Melodia (notas em sequência)
- Harmonia (notas juntas)
- Ritmo (tempo)
- Timbre (identidade do som)
""")

    st.code("C D E F G A B")

    st.write("""
Essas são as 7 notas básicas.

Elas se repetem em várias oitavas.
""")

    st.subheader("🎹 Semitom e Tom")

    st.write("""
- Semitom = menor distância (C → C#)
- Tom = dois semitons (C → D)
""")

    st.subheader("🎼 Enarmonia")

    st.write("""
Mesma nota, nomes diferentes:

C# = Db  
D# = Eb  
F# = Gb  
G# = Ab  
A# = Bb
""")

    # =========================
    # 🟡 INTERMEDIÁRIO
    # =========================
    st.subheader("🟡 2. Intermediário — Escalas e Acordes")

    st.write("""
🎼 Escala maior segue padrão:

T – T – S – T – T – T – S
""")

    st.code("C D E F G A B")

    st.write("""
🎼 Escala menor:

T – S – T – T – S – T – T
""")

    st.code("A B C D E F G")

    st.subheader("🎹 Formação de acordes")

    st.write("""
- Acorde maior: 1 + 3 + 5
- Acorde menor: 1 + b3 + 5
""")

    st.code("C = C E G")
    st.code("Cm = C Eb G")

    st.subheader("🎼 Intervalos")

    st.write("""
- 3ª maior = som alegre
- 3ª menor = som triste
- 5ª justa = estabilidade
- 7ª = tensão
""")

    # =========================
    # 🔵 AVANÇADO
    # =========================
    st.subheader("🔵 3. Avançado — Harmonia Completa")

    st.write("""
🎹 Acordes com sétima:

- C7 = dominante
- Cmaj7 = suave / jazz
- Cm7 = emocional
""")

    st.code("C7 = C E G Bb")
    st.code("Cmaj7 = C E G B")

    st.subheader("🎼 Campo harmônico")

    st.write("""
É o conjunto de acordes dentro de uma tonalidade.

Exemplo: Campo de Dó maior
""")

    st.code("C Dm Em F G Am B°")

    st.subheader("🎼 Progressões")

    st.write("""
Progressões comuns:

- I – IV – V
- I – V – vi – IV
""")

    st.subheader("🎹 Modos musicais (nível avançado)")

    st.write("""
- Jônio (maior)
- Dórico
- Frígio
- Lídio
- Mixolídio
- Eólio (menor)
- Lócrio
""")

    st.subheader("🎯 Resumo final")

    st.write("""
Dominar música é entender:

Escalas → Acordes → Harmonia → Emoção
""")

# =========================================
# 🎹 PRÁTICA
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
# 🎯 QUIZ (INALTERADO)
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
                acertos += 1
                st.success(f"{q} ✔")
            else:
                st.error(f"{q} ❌ correta: {correta}")

        st.success(f"🎯 Você acertou {acertos}/6")

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()
