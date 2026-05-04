import streamlit as st
import random

# =========================================
# 🎹 LÓGICA DOS ACORDES
# =========================================

notas_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
notas_flat  = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

def usar_bemol(acorde):
    return "b" in acorde

def pegar_lista(acorde):
    return notas_flat if usar_bemol(acorde) else notas_sharp

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
    lista = pegar_lista(acorde_principal)

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
# 📚 TEORIA COMPLETA REAL
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.subheader("🎵 1. Som e música")
    st.write("Música é organização de ondas sonoras no tempo.")
    st.write("Propriedades: frequência, duração, intensidade e timbre.")

    st.subheader("🎼 2. Sistema temperado")
    st.write("A música ocidental divide o som em 12 semitons iguais.")

    st.code("C C# D D# E F F# G G# A A# B")

    st.subheader("🎹 3. Tons e semitons")
    st.write("Semitom = menor intervalo")
    st.write("Tom = 2 semitons")

    st.subheader("🎼 4. Acidentes musicais")
    st.write("# sobe 1 semitom")
    st.write("b desce 1 semitom")

    st.write("Enarmonia (mesma nota):")
    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.subheader("🎼 5. Intervalos (base de tudo)")
    st.write("1 = tônica")
    st.write("2 = segunda")
    st.write("3 = terça (define maior/menor)")
    st.write("4 = quarta")
    st.write("5 = quinta (base do acorde)")
    st.write("7 = sétima (tensão)")

    st.subheader("🎼 6. Escalas")

    st.write("Maior:")
    st.code("T - T - S - T - T - T - S")

    st.write("Menor natural:")
    st.code("T - S - T - T - S - T - T")

    st.subheader("🎼 7. Formação de acordes")

    st.write("Tríade maior:")
    st.code("1 + 3 + 5 → C E G")

    st.write("Tríade menor:")
    st.code("1 + b3 + 5 → C Eb G")

    st.write("Acordes com sétima:")
    st.code("C7 → C E G Bb")
    st.code("Cmaj7 → C E G B")

    st.subheader("🎼 8. Campo harmônico maior")

    st.code("C Dm Em F G Am Bdim")

    st.subheader("🎼 9. Funções harmônicas")

    st.write("Tônica = repouso")
    st.write("Subdominante = movimento")
    st.write("Dominante = tensão")

    st.code("C - F - G - C")

    st.subheader("🎼 10. Ciclo das quintas")

    st.code("C G D A E B F# C# Gb Db Ab Eb Bb F")

    st.subheader("🎼 11. Modos gregos (base)")
    st.write("Maior = Jônio")
    st.write("Dórico, Frígio, Lídio, Mixolídio, Eólio, Lócrio")

    st.subheader("🎯 Resumo final")
    st.write("Tudo na música vem de: ESCALA → INTERVALO → ACORDE → FUNÇÃO → HARMONIA")

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
# 🎯 QUIZ 100% CORRIGIDO
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    banco = [
        ("C = ?", ["C D E", "C E G", "C F G"], "C E G"),
        ("Cm = ?", ["C Eb G", "C E G", "C F G"], "C Eb G"),
        ("D = ?", ["D F# A", "D F A", "D E A"], "D F# A"),
        ("E = ?", ["E G# B", "E G B", "E A B"], "E G# B"),
        ("F = ?", ["F A C", "F G C", "F A D"], "F A C"),
    ]

    if "quiz" not in st.session_state:
        st.session_state.quiz = random.sample(banco, 5)
        st.session_state.finalizado = False
        st.session_state.respostas = {}

    perguntas = st.session_state.quiz

    # NÃO MARCA NADA ANTES
    if not st.session_state.finalizado:

        for i, (q, op, c) in enumerate(perguntas):

            escolha = st.radio(
                q,
                op,
                key=f"q{i}_{id(perguntas)}",
                index=None
            )

            st.session_state.respostas[i] = escolha

    else:

        acertos = 0
        st.divider()

        for i, (q, op, c) in enumerate(perguntas):

            r = st.session_state.respostas[i]

            st.write(f"**{q}**")
            st.write(f"Sua resposta: {r}")

            if r == c:
                st.success("✔ Correto")
                acertos += 1
            else:
                st.error("❌ Errado")
                st.info(f"✔ Correto: {c}")

        st.success(f"🎯 Acertos: {acertos}/5")

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = random.sample(banco, 5)
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.rerun()
