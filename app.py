import streamlit as st

# =========================================
# 🎹 LÓGICA DOS ACORDES (SEU CÓDIGO)
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
        "7M": [0,4,7,11],
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
# 🌐 INTERFACE STREAMLIT
# =========================================

st.title("🎹 Sistema de Acordes Completo")

# =========================
# 🎓 TUTORIAL (AGORA NO SITE)
# =========================

st.header("📚 Como funcionam os acordes")

st.write("👉 Um acorde é formado por várias notas tocadas juntas.")

st.subheader("🎼 Acorde maior")
st.write("C = C - E - G")

st.subheader("🎼 Acorde menor")
st.write("Cm = C - Eb - G")

st.subheader("🎼 Acorde com 7")
st.write("C7 = C - E - G - Bb")

st.write("---")

# =========================
# 🎹 TESTE INTERATIVO
# =========================

st.header("🎯 Teste seu acorde")

acorde = st.text_input("Digite um acorde (ex: C, Cm, C7, G/B)")

if st.button("Gerar acorde"):
    resultado = gerar_acorde(acorde)

    if resultado:
        st.success(f"Notas do acorde: {resultado['notas']}")

        if resultado["baixo"]:
            st.info(f"Baixo: {resultado['baixo']}")

        st.write("🎹 Visualização do teclado:")

        base = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

        teclado = ""
        for nota in base:
            if nota in resultado["notas"]:
                teclado += f"[{nota}] "
            else:
                teclado += f" {nota}  "

        st.text(teclado)

    else:
        st.error("Acorde não reconhecido!")
