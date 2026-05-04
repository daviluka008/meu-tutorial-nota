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
# 🌐 INTERFACE
# =========================================

st.set_page_config(page_title="🎹 Acordes App", page_icon="🎹")

st.title("🎹 Sistema Completo de Acordes")

pagina = st.sidebar.selectbox(
    "📌 Menu",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria dos Acordes")

    st.write("Acorde é quando tocamos várias notas ao mesmo tempo.")

    st.code("MAIOR → C = C E G")
    st.code("MENOR → Cm = C Eb G")
    st.code("7 → C7 = C E G Bb")
    st.code("7M → C7M = C E G B")
    st.code("add9 → Cadd9 = C E G D")
    st.code("sus2 → Csus2 = C D G")
    st.code("sus4 → Csus4 = C F G")

    st.write("G/B = acorde com baixo diferente")

    st.success("👉 Vá para PRÁTICA depois")

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
            st.error("❌ Acorde não reconhecido")

# =========================================
# 🎯 QUIZ DINÂMICO (NOVO)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    banco_perguntas = [
        ("C = ?", ["C D E", "C E G", "C F G"], "C E G"),
        ("Cm = ?", ["C Eb G", "C E G", "C F G"], "C Eb G"),
        ("C7 = ?", ["C E G B", "C E G Bb", "C D G"], "C E G Bb"),
        ("Csus4 = ?", ["C D G", "C F G", "C E G"], "C F G"),
        ("G/B = ?", ["G com baixo B", "G menor", "G aumentado"], "G com baixo B"),
        ("Cadd9 = ?", ["C E G D", "C E G", "C D G"], "C E G D"),
        ("Cm7 = ?", ["C Eb G Bb", "C E G Bb", "C D G"], "C Eb G Bb"),
    ]

    perguntas = random.sample(banco_perguntas, 3)

    acertos = 0

    for i, (enunciado, opcoes, resposta) in enumerate(perguntas):

        escolha = st.radio(enunciado, opcoes, key=f"q{i}")

        if escolha == resposta:
            acertos += 1

    if st.button("Ver resultado final"):

        st.divider()
        st.success(f"🎯 Você acertou {acertos}/3 perguntas!")
        st.info("🔄 Atualize a página para novas perguntas")
