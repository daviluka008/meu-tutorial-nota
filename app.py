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

st.title("🎹 Sistema Completo de Acordes + Teoria")

pagina = st.sidebar.selectbox(
    "📌 Menu",
    ["📚 Teoria", "🎹 Teste de Acordes", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria dos Acordes")

    st.write("Acorde é quando tocamos várias notas ao mesmo tempo.")

    st.code("C = C E G")
    st.code("Cm = C Eb G")
    st.code("D = D F# A")
    st.code("Dm = D F A")
    st.code("E = E G# B")
    st.code("Em = E G B")
    st.code("F = F A C")
    st.code("F# = F# A# C#")
    st.code("G = G B D")
    st.code("Gm = G Bb D")
    st.code("A = A C# E")
    st.code("Am = A C E")
    st.code("B = B D# F#")
    st.code("Bm = B D F#")

    st.write("Extras:")
    st.code("C7 = C E G Bb")
    st.code("Cm7 = C Eb G Bb")
    st.code("G/B = G com baixo B")

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
# 🎯 QUIZ COMPLETO (AMPLIADO)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz Completo de Acordes")

    banco_perguntas = [
        ("C = ?", ["C D E", "C E G", "C F G"], "C E G"),
        ("Cm = ?", ["C Eb G", "C E G", "C F G"], "C Eb G"),
        ("D = ?", ["D F A", "D F# A", "D G A"], "D F# A"),
        ("Dm = ?", ["D F A", "D F# A", "D A C"], "D F A"),
        ("E = ?", ["E G B", "E G# B", "E A B"], "E G# B"),
        ("Em = ?", ["E G B", "E G# B", "E A B"], "E G B"),
        ("F = ?", ["F A C", "F A# C", "F G C"], "F A C"),
        ("F# = ?", ["F# A# C#", "F# A C#", "F# B C#"], "F# A# C#"),
        ("G = ?", ["G B D", "G Bb D", "G C D"], "G B D"),
        ("Gm = ?", ["G Bb D", "G B D", "G A D"], "G Bb D"),
        ("A = ?", ["A C E", "A C# E", "A D E"], "A C# E"),
        ("Am = ?", ["A C E", "A C# E", "A D F"], "A C E"),
        ("B = ?", ["B D F#", "B D# F#", "B E G#"], "B D# F#"),
        ("Bm = ?", ["B D F#", "B D# F#", "B F A"], "B D F#"),
        ("C7 = ?", ["C E G B", "C E G Bb", "C D G"], "C E G Bb"),
        ("Cm7 = ?", ["C Eb G Bb", "C E G Bb", "C D G"], "C Eb G Bb"),
        ("G/B = ?", ["G com baixo B", "G menor", "G aumentado"], "G com baixo B"),
    ]

    if "quiz_perguntas" not in st.session_state:
        st.session_state.quiz_perguntas = random.sample(banco_perguntas, 4)

    perguntas = st.session_state.quiz_perguntas

    acertos = 0
    respostas = []

    for i, (enunciado, opcoes, resposta) in enumerate(perguntas):

        escolha = st.radio(enunciado, opcoes, key=f"q{i}")
        respostas.append((escolha, resposta))

    if st.button("Ver resultado final"):

        st.divider()

        for i, (escolha, correta) in enumerate(respostas):

            if escolha == correta:
                st.success(f"✔ Pergunta {i+1} correta")
                acertos += 1
            else:
                st.error(f"❌ Pergunta {i+1} errada")

        st.success(f"🎯 Você acertou {acertos}/4 perguntas!")

    if st.button("🔄 Novo quiz"):
        del st.session_state.quiz_perguntas
        st.rerun()
