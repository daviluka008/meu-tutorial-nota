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
# 📚 TEORIA
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.subheader("🎵 O que é música")
    st.write("Música é organização de sons no tempo: altura, duração, intensidade e timbre.")

    st.subheader("🎼 Notas musicais")
    st.code("C D E F G A B")

    st.subheader("🎹 Semitom e Tom")
    st.write("Semitom = menor distância | Tom = 2 semitons")

    st.subheader("🎼 Sustenidos e bemóis")
    st.write("# sobe meio tom | b desce meio tom")

    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.subheader("🎼 Escala maior")
    st.code("T - T - S - T - T - T - S")

    st.subheader("🎼 Acordes básicos")

    st.code("Maior: 1 + 3 + 5 → C E G")
    st.code("Menor: 1 + b3 + 5 → C Eb G")
    st.code("7: C7 → C E G Bb")

    st.subheader("🎼 Campo harmônico")
    st.code("C Dm Em F G Am Bdim")

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

            base = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

            teclado = ""
            for nota in base:
                teclado += f"[{nota}] " if nota in resultado["notas"] else f" {nota}  "

            st.text(teclado)

        else:
            st.error("❌ Acorde não reconhecido")

# =========================================
# 🎯 QUIZ (CORRIGIDO COMPLETO)
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

    st.info("Responda e veja seu resultado ao final.")

    # RESET visual correto (sem pré-marcação)
    for i, (q, op, correta) in enumerate(perguntas):

        if not st.session_state.finalizado:

            escolha = st.radio(
                q,
                op,
                key=f"q{i}",
                index=None  # 🔥 impede resposta pré-marcada
            )

            if escolha:
                st.session_state.respostas[i] = escolha

        else:

            st.radio(
                q,
                op,
                index=op.index(st.session_state.respostas[i]),
                key=f"q{i}",
                disabled=True
            )

    if st.button("Ver resultado"):

        st.session_state.finalizado = True

        acertos = 0

        st.divider()

        for i, (q, op, correta) in enumerate(perguntas):

            resposta = st.session_state.respostas.get(i)

            if resposta == correta:
                st.success(f"✔ Pergunta {i+1} correta")
                acertos += 1
            else:
                st.error(f"❌ Pergunta {i+1} errada")
                st.info(f"✔ Resposta certa: {correta}")

        st.success(f"🎯 Você acertou {acertos}/5")

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = random.sample(banco, 5)
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.rerun()
