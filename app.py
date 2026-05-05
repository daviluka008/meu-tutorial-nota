import streamlit as st
import random
import numpy as np
import wave
import io

# =========================================
# 🎹 LÓGICA DOS ACORDES
# =========================================

notas_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
notas_flat = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

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
# 🔊 SOM DAS NOTAS
# =========================================

frequencias = {
    "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13,
    "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00,
    "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88
}

def gerar_som(freq, duracao=0.5):
    taxa = 44100
    t = np.linspace(0, duracao, int(taxa * duracao), False)
    onda = np.sin(freq * t * 2 * np.pi)
    audio = (onda * 32767).astype(np.int16)

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(taxa)
        wf.writeframes(audio.tobytes())

    buffer.seek(0)
    return buffer


# =========================================
# 🌐 CONFIG
# =========================================

st.set_page_config(page_title="🎹 Acordes App", page_icon="🎹")

st.title("🎹 Sistema Completo de Acordes + Teoria")

pagina = st.sidebar.selectbox(
    "📌 Menu",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz", "🎹 Teclado Interativo"]
)

# =========================================
# 📚 TEORIA
# =========================================

if pagina == "📚 Teoria":
    st.header("🎓 Teoria Musical Completa")

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
# 🎯 QUIZ
# =========================================

elif pagina == "🎯 Quiz":
    st.header("🎯 Quiz de Acordes")

    escala = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    mapa = {nota: i for i, nota in enumerate(escala)}

    maior = [0, 4, 7]
    menor = [0, 3, 7]

    def montar_acorde(nota, tipo):
        i = mapa[nota]
        intervalos = maior if tipo == "maior" else menor
        return " ".join([escala[(i + x) % 12] for x in intervalos])

# =========================================
# 🎹 TECLADO INTERATIVO COM SOM
# =========================================

elif pagina == "🎹 Teclado Interativo":

    st.header("🎹 Teclado Interativo com Som")

    acordes = {
        "C": ["C", "E", "G"],
        "G": ["G", "B", "D"],
        "Am": ["A", "C", "E"],
        "F": ["F", "A", "C"],
        "Dm": ["D", "F", "A"]
    }

    acorde = st.selectbox("Escolha um acorde:", list(acordes.keys()))
    notas = acordes[acorde]

    st.subheader(f"Notas do acorde {acorde}")
    st.write(notas)

    teclas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    st.subheader("🎹 Clique nas teclas")

    for nota in teclas:
        if st.button(nota):
            if nota in frequencias:
                som = gerar_som(frequencias[nota])
                st.audio(som, format="audio/wav")
