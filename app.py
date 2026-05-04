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

# 🔥 IMPORTANTE: pagina ANTES de tudo
pagina = st.sidebar.selectbox(
    "📌 Menu",
    ["📚 Teoria", "🎹 Teste de Acordes", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA COMPLETA
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria dos Acordes")

    st.subheader("🎵 O que é um acorde?")
    st.write("Um acorde é a combinação de 3 ou mais notas tocadas ao mesmo tempo.")

    st.subheader("🎼 Como ele é formado?")
    st.write("Todo acorde maior segue a fórmula:")

    st.code("1 (tônica) + 3 (terça maior) + 5 (quinta justa)")

    st.write("Exemplo: C maior")

    st.code("C = C + E + G")

    st.write("Escala de C:")
    st.code("C D E F G A B")

    st.success("Resultado: C E G")

    st.divider()

    st.subheader("🎼 Acordes menores")

    st.write("No acorde menor, a terça é abaixada meio tom:")

    st.code("1 + b3 + 5")

    st.code("Cm = C + Eb + G")

    st.divider()

    st.subheader("🎼 Sustenidos e bemóis")

    st.write("🔼 # sobe meio tom")
    st.write("🔽 b desce meio tom")

    st.code("C# = C sobe meio tom")
    st.code("Eb = E desce meio tom")

    st.divider()

    st.subheader("🎼 Enarmonia")

    st.write("Mesma nota, nomes diferentes:")

    st.code("C# = Db")
    st.code("D# = Eb")
    st.code("F# = Gb")
    st.code("G# = Ab")
    st.code("A# = Bb")

    st.divider()

    st.subheader("🎼 Sétimas")

    st.code("C7 = C E G Bb")
    st.code("C7M = C E G B")

    st.success("Agora você entende como os acordes são construídos 🎹")

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
# 🎯 QUIZ PROFISSIONAL
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    banco_perguntas = [
        ("C = ?", ["C D E", "C E G", "C F G"], "C E G"),
        ("Cm = ?", ["C Eb G", "C E G", "C F G"], "C Eb G"),
        ("C# = ?", ["C# E# G#", "C# F G#", "C D G"], "C# E# G#"),
        ("Db = ?", ["Db F Ab", "Db E G", "Db F A"], "Db F Ab"),
        ("D# = ?", ["D# F# A#", "D E A", "D# G A#"], "D# F# A#"),
        ("Eb = ?", ["Eb G Bb", "Eb F Ab", "Eb G C"], "Eb G Bb"),
        ("F# = ?", ["F# A# C#", "F# A C#", "F# B D"], "F# A# C#"),
        ("Gb = ?", ["Gb Bb Db", "Gb A C#", "Gb B D"], "Gb Bb Db"),
        ("G# = ?", ["G# C D#", "G# B D#", "G# C E"], "G# C D#"),
        ("Ab = ?", ["Ab C Eb", "Ab D F", "Ab B Eb"], "Ab C Eb"),
        ("A# = ?", ["A# D F", "A# C F", "A# D G"], "A# D F"),
        ("Bb = ?", ["Bb D F", "Bb C F", "Bb E G"], "Bb D F"),
    ]

    if "quiz" not in st.session_state:
        st.session_state.quiz = random.sample(banco_perguntas, 4)
        st.session_state.finalizado = False

    perguntas = st.session_state.quiz

    respostas = []
    acertos = 0

    st.info("⚠️ Depois de enviar, não pode alterar respostas.")

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

        st.success(f"🎯 Você acertou {acertos}/4 perguntas!")

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = random.sample(banco_perguntas, 4)
        st.session_state.finalizado = False
        st.rerun()
