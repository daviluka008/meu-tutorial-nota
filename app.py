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

    return {"notas": notas, "baixo": baixo}

# =========================================
# 🌐 CONFIG
# =========================================

st.set_page_config(page_title="🎹 Acordes App", page_icon="🎹")
st.title("🎹 Sistema Completo de Acordes + Teoria")

pagina = st.sidebar.selectbox(
    "📌 Menu",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA COMPLETA (APOSTILA)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.subheader("🎵 O que é música")
    st.write("""
Música é a organização de sons no tempo.  
Ela possui 4 elementos principais:
- altura (grave/agudo)
- duração
- intensidade
- timbre
""")

    st.subheader("🎼 Notas musicais")
    st.code("C D E F G A B")

    st.write("Essas são as 7 notas naturais da música ocidental.")

    st.subheader("🎹 Semitom e Tom")
    st.write("""
- Semitom = menor distância entre duas notas  
- Tom = 2 semitons  
""")

    st.subheader("🎼 Sustenidos e bemóis")
    st.write("""
# sobe meio tom  
b desce meio tom  
""")

    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.subheader("🎼 Escala maior")
    st.write("Fórmula:")
    st.code("T - T - S - T - T - T - S")

    st.write("Exemplo em C:")
    st.code("C D E F G A B")

    st.subheader("🎼 Escala menor")
    st.code("T - S - T - T - S - T - T")

    st.subheader("🎼 Acordes")

    st.write("✔ Maior:")
    st.code("1 + 3 + 5 → C E G")

    st.write("✔ Menor:")
    st.code("1 + b3 + 5 → C Eb G")

    st.write("✔ Sétima:")
    st.code("C7 → C E G Bb")

    st.write("✔ Maj7:")
    st.code("Cmaj7 → C E G B")

    st.subheader("🎼 Campo harmônico")
    st.code("C Dm Em F G Am Bdim")

    st.subheader("🎯 Resumo")
    st.write("""
Tudo na música vem de:
Escala → Intervalos → Acordes → Harmonia
""")

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
                teclado += f"[{nota}] " if nota in resultado["notas"] else f" {nota}  "

            st.text(teclado)

        else:
            st.error("❌ Acorde não reconhecido")

# =========================================
# 🎯 QUIZ DINÂMICO
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    banco = [
        ("C = ?", ["C D E", "C E G", "C F G"], "C E G"),
        ("Cm = ?", ["C Eb G", "C E G", "C F G"], "C Eb G"),
        ("D = ?", ["D F# A", "D F A", "D E A"], "D F# A"),
        ("E = ?", ["E G# B", "E G B", "E A B"], "E G# B"),
        ("F = ?", ["F A C", "F G C", "F A D"], "F A C"),
        ("G = ?", ["G B D", "G A D", "G B E"], "G B D"),
        ("A = ?", ["A C# E", "A C E", "A D E"], "A C# E"),
        ("B = ?", ["B D# F#", "B D F#", "B E G"], "B D# F#"),
        ("C# = ?", ["C# E# G#", "C# E G#", "C D G#"], "C# E# G#"),
        ("Eb = ?", ["Eb G Bb", "Eb F Ab", "Eb G C"], "Eb G Bb"),
    ]

    if "quiz" not in st.session_state:
        st.session_state.quiz = random.sample(banco, 5)
        st.session_state.finalizado = False

    perguntas = st.session_state.quiz
    respostas = []
    acertos = 0

    for i, (q, op, c) in enumerate(perguntas):

        escolha = st.radio(
            q,
            op,
            key=f"q{i}",
            disabled=st.session_state.finalizado
        )

        respostas.append((escolha, c))

    if st.button("Ver resultado"):

        st.session_state.finalizado = True

        for i, (e, c) in enumerate(respostas):

            if e == c:
                st.success(f"✔ Pergunta {i+1} correta")
                acertos += 1
            else:
                st.error(f"❌ Pergunta {i+1} errada")
                st.info(f"✔ Resposta certa: {c}")

        st.success(f"🎯 Você acertou {acertos}/5")
    
    if st.button("Novo quiz"):
        st.session_state.quiz = random.sample(banco, 5)
        st.session_state.finalizado = False
        st.rerun()
