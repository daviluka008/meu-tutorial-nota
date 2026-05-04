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
# 📌 MENU
# =========================================

st.title("🎹 Sistema Completo de Acordes")

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
# 🎯 QUIZ (COM FEEDBACK)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    acertos = 0

    # Pergunta 1
    st.subheader("1. Qual é a formação do acorde C?")
    q1 = st.radio("", ["C D E", "C E G", "C F G"], key="q1")

    if q1 == "C E G":
        st.success("✔ Correto! C = 1 + 3 + 5")
        acertos += 1
    else:
        st.error("❌ Errado. Resposta correta: C E G")

    # Pergunta 2
    st.subheader("2. Qual é a formação do Cm?")
    q2 = st.radio("", ["C Eb G", "C E G", "C F G"], key="q2")

    if q2 == "C Eb G":
        st.success("✔ Correto!")
        acertos += 1
    else:
        st.error("❌ Errado. Resposta correta: C Eb G")

    # Pergunta 3
    st.subheader("3. O que significa C7?")
    q3 = st.radio("", ["C E G B", "C E G Bb", "C D G"], key="q3")

    if q3 == "C E G Bb":
        st.success("✔ Correto!")
        acertos += 1
    else:
        st.error("❌ Errado. Resposta correta: C E G Bb")

    # Pergunta 4
    st.subheader("4. Qual é Csus4?")
    q4 = st.radio("", ["C D G", "C F G", "C E G"], key="q4")

    if q4 == "C F G":
        st.success("✔ Correto!")
        acertos += 1
    else:
        st.error("❌ Errado. Resposta correta: C F G")

    # Pergunta 5
    st.subheader("5. O que é G/B?")
    q5 = st.radio("", ["G com baixo B", "G menor", "G aumentado"], key="q5")

    if q5 == "G com baixo B":
        st.success("✔ Correto!")
        acertos += 1
    else:
        st.error("❌ Errado. Resposta correta: G com baixo B")

    st.divider()

    if st.button("Ver resultado final"):
        st.success(f"🎯 Você acertou {acertos}/5 perguntas!")
