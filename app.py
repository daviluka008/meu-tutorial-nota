import streamlit as st

# =========================
# 🎹 TÍTULO
# =========================
st.title("🎹 Tutorial de Música + Acordes Interativo")

# =========================
# 🎓 TUTORIAL
# =========================
st.header("📚 Como funcionam escalas e acordes")

st.write("👉 Escala é uma sequência de notas em ordem.")

st.write("🎼 Exemplo de escala de Dó maior:")
st.code("C - D - E - F - G - A - B - C")

st.write("👉 Acorde é quando tocamos várias notas ao mesmo tempo.")

st.write("🎸 Acorde de Dó maior:")
st.code("C - E - G")

st.write("👉 Acorde menor:")
st.code("C - Eb - G")

st.write("---")

# =========================
# 🎹 SISTEMA DE ACORDES
# =========================

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

# =========================
# 🎯 INTERAÇÃO
# =========================

st.header("🎯 Teste seus acordes")

acorde = st.text_input("Digite um acorde (ex: C, Cm, C7, G/B)")

if st.button("Gerar acorde"):
    resultado = gerar_acorde(acorde)

    if resultado:
        st.success(f"Notas: {resultado['notas']}")

        if resultado["baixo"]:
            st.info(f"Baixo: {resultado['baixo']}")

    else:
        st.error("Acorde não reconhecido")
