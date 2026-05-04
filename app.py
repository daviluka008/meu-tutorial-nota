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
    ["📚 Teoria", "🎹 Teste de Acordes", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA + VÍDEOS (DENTRO DO SITE)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 TEORIA MUSICAL COMPLETA")

    st.subheader("🎵 O que é música")
    st.write("Música é organização de sons no tempo: altura, duração, intensidade e timbre.")

    st.components.v1.html("""
    <iframe width="100%" height="350"
    src="https://www.youtube.com/embed/7Yc6m2kQ0XQ"
    frameborder="0"
    allowfullscreen></iframe>
    """, height=350)

    st.subheader("🎼 Notas musicais")
    st.code("C D E F G A B")

    st.components.v1.html("""
    <iframe width="100%" height="350"
    src="https://www.youtube.com/embed/5rX0q7mK9sA"
    frameborder="0"
    allowfullscreen></iframe>
    """, height=350)

    st.subheader("🎹 Tons e semitons")
    st.write("Semitom = menor distância | Tom = 2 semitons")

    st.components.v1.html("""
    <iframe width="100%" height="350"
    src="https://www.youtube.com/embed/3mQ8pT7xK9A"
    frameborder="0"
    allowfullscreen></iframe>
    """, height=350)

    st.subheader("🎼 Sustenidos e bemóis")

    st.code("C# = Db")
    st.code("D# = Eb")
    st.code("F# = Gb")
    st.code("G# = Ab")
    st.code("A# = Bb")

    st.components.v1.html("""
    <iframe width="100%" height="350"
    src="https://www.youtube.com/embed/9kQ3mT8xP7A"
    frameborder="0"
    allowfullscreen></iframe>
    """, height=350)

    st.subheader("🎼 Escala maior")
    st.code("T - T - S - T - T - T - S")

    st.components.v1.html("""
    <iframe width="100%" height="350"
    src="https://www.youtube.com/embed/6kT9mQ2xP7A"
    frameborder="0"
    allowfullscreen></iframe>
    """, height=350)

    st.subheader("🎼 Acordes maiores e menores")
    st.code("1 + 3 + 5 = maior")
    st.code("1 + b3 + 5 = menor")

    st.components.v1.html("""
    <iframe width="100%" height="350"
    src="https://www.youtube.com/embed/4pQ9mT7xK2A"
    frameborder="0"
    allowfullscreen></iframe>
    """, height=350)

    st.markdown("---")
    st.success("🎯 FIM DA TEORIA — vá para prática ou quiz")

# =========================================
# 🎹 PRÁTICA
# =========================================

elif pagina == "🎹 Teste de Acordes":

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
            st.error("❌ Acorde inválido")

# =========================================
# 🎯 QUIZ
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    banco = [
        ("C = ?", ["C D E", "C E G", "C F G"], "C E G"),
        ("Cm = ?", ["C Eb G", "C E G", "C F G"], "C Eb G"),
        ("D# = ?", ["D# F# A#", "D E A", "D# G A#"], "D# F# A#"),
        ("Eb = ?", ["Eb G Bb", "Eb F Ab", "Eb G C"], "Eb G Bb"),
    ]

    if "quiz" not in st.session_state:
        st.session_state.quiz = random.sample(banco, 3)
        st.session_state.finalizado = False

    perguntas = st.session_state.quiz
    respostas = []
    acertos = 0

    for i, (q, op, c) in enumerate(perguntas):

        escolha = st.radio(
            q,
            op,
            key=f"q{i}",
            disabled=st.session_state.finalizado
        )

        respostas.append((escolha, c))

    if st.button("Ver resultado"):

        st.session_state.finalizado = True

        for i, (e, c) in enumerate(respostas):

            if e == c:
                st.success(f"✔ Q{i+1} correta")
                acertos += 1
            else:
                st.error(f"❌ Q{i+1} errada")
                st.info(f"Resposta certa: {c}")

        st.success(f"🎯 Acertos: {acertos}/3")

    if st.button("Novo quiz"):
        st.session_state.quiz = random.sample(banco, 3)
        st.session_state.finalizado = False
        st.rerun()
