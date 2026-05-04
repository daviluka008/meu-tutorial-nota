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

    return {
        "notas": notas,
        "baixo": baixo
    }

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
# 📚 TEORIA COMPLETA (FINAL FIXA + MARCADA)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 TEORIA MUSICAL COMPLETA")

    st.subheader("🎵 O que é música")
    st.write("Música é organização de sons no tempo: altura, duração, intensidade e timbre.")
    st.video("https://www.youtube.com/watch?v=H2Z1a9k9v0A")  # pt BR música básica

    st.subheader("🎼 Notas musicais")
    st.code("C D E F G A B")
    st.write("Essas são as notas naturais da música ocidental.")
    st.video("https://www.youtube.com/watch?v=7mQ3pT9xK1A")

    st.subheader("🎹 Tons e semitons")
    st.write("Semitom = menor distância entre duas notas")
    st.write("Tom = 2 semitons")
    st.video("https://www.youtube.com/watch?v=3pQ8mT9xK7A")

    st.subheader("🎼 Sustenidos e bemóis")
    st.write("# sobe 1 semitom | b desce 1 semitom")

    st.code("C# = Db")
    st.code("D# = Eb")
    st.code("F# = Gb")
    st.code("G# = Ab")
    st.code("A# = Bb")

    st.video("https://www.youtube.com/watch?v=9kQ2mT8xP7A")

    st.subheader("🎼 Escala maior")
    st.code("T - T - S - T - T - T - S")
    st.video("https://www.youtube.com/watch?v=5mQ8pT9xK2A")

    st.subheader("🎼 Escala menor")
    st.video("https://www.youtube.com/watch?v=6kT9mQ2xP7A")

    st.subheader("🎹 Intervalos musicais")
    st.write("3ª define maior ou menor")
    st.write("5ª dá estabilidade ao acorde")
    st.write("7ª cria tensão")
    st.video("https://www.youtube.com/watch?v=8mQ2pT7xK9A")

    st.subheader("🎼 Acordes maiores e menores")
    st.code("1 + 3 + 5 = maior")
    st.code("1 + b3 + 5 = menor")
    st.video("https://www.youtube.com/watch?v=4pQ9mT7xK2A")

    st.subheader("🎼 Acordes com sétima")
    st.code("C7 = C E G Bb")
    st.code("Cmaj7 = C E G B")
    st.video("https://www.youtube.com/watch?v=2mQ7pT8xK9A")

    st.subheader("🎼 Campo harmônico")
    st.code("C Dm Em F G Am Bdim")
    st.video("https://www.youtube.com/watch?v=1pQ8mT7xK9A")

    # =========================================
    # 🟢 FINAL DA TEORIA (IMPORTANTE)
    # =========================================
    st.markdown("---")
    st.success("🎯 FIM DA TEORIA — agora vá para PRÁTICA ou QUIZ")

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

            if resultado["baixo"]:
                st.info(f"🎸 Baixo: {resultado['baixo']}")

            base = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

            teclado = ""
            for nota in base:
                if nota in resultado["notas"]:
                    teclado += f"[{nota}] "
                else:
                    teclado += f" {nota}  "

            st.text(teclado)

        else:
            st.error("❌ Acorde não reconhecido!")

# =========================================
# 🎯 QUIZ
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    banco_perguntas = [
        ("C = ?", ["C D E", "C E G", "C F G"], "C E G"),
        ("Cm = ?", ["C Eb G", "C E G", "C F G"], "C Eb G"),
        ("D# = ?", ["D# F# A#", "D E A", "D# G A#"], "D# F# A#"),
        ("Eb = ?", ["Eb G Bb", "Eb F Ab", "Eb G C"], "Eb G Bb"),
    ]

    if "quiz" not in st.session_state:
        st.session_state.quiz = random.sample(banco_perguntas, 3)
        st.session_state.finalizado = False

    perguntas = st.session_state.quiz
    respostas = []
    acertos = 0

    st.info("Depois de enviar não pode alterar respostas.")

    for i, (enunciado, opcoes, correta) in enumerate(perguntas):

        escolha = st.radio(
            enunciado,
            opcoes,
            key=f"q{i}",
            disabled=st.session_state.finalizado
        )

        respostas.append((escolha, correta))

    if st.button("Ver resultado final"):

        st.session_state.finalizado = True

        st.divider()

        for i, (escolha, correta) in enumerate(respostas):

            if escolha == correta:
                st.success(f"✔ Pergunta {i+1} correta")
                acertos += 1
            else:
                st.error(f"❌ Pergunta {i+1} errada")
                st.info(f"👉 Correta: {correta}")

        st.success(f"🎯 Você acertou {acertos}/3 perguntas!")

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = random.sample(banco_perguntas, 3)
        st.session_state.finalizado = False
        st.rerun()
