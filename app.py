import streamlit as st

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

st.title("🎹 Sistema Completo de Acordes + Teoria")

pagina = st.sidebar.selectbox(
    "📌 Menu",
    ["📚 Teoria", "🎹 Teste de Acordes", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Tutorial Completo")

    st.subheader("🎵 O que é um acorde?")
    st.write("Acorde é quando tocamos várias notas ao mesmo tempo.")

    st.write("MAIOR: 1 + 3 + 5")
    st.code("C → C E G")

    st.write("MENOR: 1 + b3 + 5")
    st.code("Cm → C Eb G")

    st.write("COM 7:")
    st.code("C7 → C E G Bb")
    st.code("C7M → C E G B")

    st.write("ADD9:")
    st.code("Cadd9 → C E G D")

    st.write("SUS:")
    st.code("Csus2 → C D G")
    st.code("Csus4 → C F G")

    st.write("BAIXO DIFERENTE:")
    st.code("G/B → acorde G com baixo B")

    st.write("SUSTENIDO (#) sobe meio tom")
    st.write("BEMOL (b) desce meio tom")

# =========================================
# 🎹 TESTE DE ACORDES
# =========================================

elif pagina == "🎹 Teste de Acordes":

    st.header("🎯 Teste seus acordes")

    acorde = st.text_input("Digite um acorde")

    if st.button("Gerar"):
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
# 🎯 QUIZ (CORRIGIDO SEM ERRO)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")
    st.write("Responda e clique para ver seu resultado.")

    q1 = st.radio("1. C = ?", ["C D E", "C E G", "C F G"], key="q1")
    q2 = st.radio("2. Cm = ?", ["C Eb G", "C E G", "C F G"], key="q2")
    q3 = st.radio("3. C7 = ?", ["C E G B", "C E G Bb", "C D G"], key="q3")
    q4 = st.radio("4. Csus4 = ?", ["C D G", "C F G", "C E G"], key="q4")
    q5 = st.radio("5. G/B = ?", ["G com baixo B", "G menor", "G aumentado"], key="q5")

    if st.button("Ver resultado final"):

        acertos = 0

        if q1 == "C E G":
            st.success("✔ Q1 correta")
            acertos += 1
        else:
            st.error("❌ Q1 errada (C E G)")

        if q2 == "C Eb G":
            st.success("✔ Q2 correta")
            acertos += 1
        else:
            st.error("❌ Q2 errada (C Eb G)")

        if q3 == "C E G Bb":
            st.success("✔ Q3 correta")
            acertos += 1
        else:
            st.error("❌ Q3 errada (C E G Bb)")

        if q4 == "C F G":
            st.success("✔ Q4 correta")
            acertos += 1
        else:
            st.error("❌ Q4 errada (C F G)")

        if q5 == "G com baixo B":
            st.success("✔ Q5 correta")
            acertos += 1
        else:
            st.error("❌ Q5 errada (G com baixo B)")

        st.divider()
        st.success(f"🎯 Você acertou {acertos}/5 perguntas!")
