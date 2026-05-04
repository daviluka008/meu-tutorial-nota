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
# 🌐 CONFIGURAÇÃO VISUAL
# =========================================

st.set_page_config(page_title="Acordes App", page_icon="🎹")

st.title("🎹 Aprenda Acordes de Forma Simples")

st.sidebar.title("📌 Menu de Estudo")

pagina = st.sidebar.radio(
    "Navegação",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz"]
)

st.sidebar.markdown("---")
st.sidebar.info("📌 Siga a ordem: Teoria → Prática → Quiz")

# =========================================
# 📚 TEORIA
# =========================================

if pagina == "📚 Teoria":

    st.header("📚 Teoria dos Acordes")

    st.markdown("### 🎵 O que é um acorde?")
    st.write("É quando tocamos várias notas ao mesmo tempo.")

    st.markdown("### 📌 Fórmulas principais")

    st.code("MAIOR → 1 + 3 + 5 (C = C E G)")
    st.code("MENOR → 1 + b3 + 5 (Cm = C Eb G)")
    st.code("7 → C7 = C E G Bb")
    st.code("7M → C7M = C E G B")
    st.code("add9 → Cadd9 = C E G D")
    st.code("sus2 → Csus2 = C D G")
    st.code("sus4 → Csus4 = C F G")

    st.markdown("### 🎸 Extras")
    st.write("G/B = acorde com baixo diferente")
    st.write("# sobe meio tom | b desce meio tom")

    st.success("👉 Agora vá para a aba PRÁTICA")

# =========================================
# 🎹 PRÁTICA
# =========================================

elif pagina == "🎹 Prática":

    st.header("🎹 Pratique Acordes")

    acorde = st.text_input("Digite um acorde (ex: C7, Cm, G/B)")

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
# 🎯 QUIZ
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    st.write("Responda e veja seu resultado no final.")

    q1 = st.radio("1. C = ?", ["C D E", "C E G", "C F G"], key="q1")
    q2 = st.radio("2. Cm = ?", ["C Eb G", "C E G", "C F G"], key="q2")
    q3 = st.radio("3. C7 = ?", ["C E G B", "C E G Bb", "C D G"], key="q3")
    q4 = st.radio("4. Csus4 = ?", ["C D G", "C F G", "C E G"], key="q4")
    q5 = st.radio("5. G/B = ?", ["G com baixo B", "G menor", "G aumentado"], key="q5")

    if st.button("Ver resultado final"):

        acertos = 0

        def check(resp, correta, msg):
            nonlocal acertos
            if resp == correta:
                st.success("✔ " + msg)
                acertos += 1
            else:
                st.error("❌ Errado. " + msg)

        check(q1, "C E G", "C = 1 + 3 + 5")
        check(q2, "C Eb G", "Cm correto")
        check(q3, "C E G Bb", "C7 correto")
        check(q4, "C F G", "Csus4 correto")
        check(q5, "G com baixo B", "G/B correto")

        st.divider()
        st.success(f"🎯 Você acertou {acertos}/5")
