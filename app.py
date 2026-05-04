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
# 📚 TEORIA COMPLETA (SEM CORTES)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.subheader("🎵 O que é música")
    st.write("""
Música é a organização dos sons no tempo.

Ela possui 4 elementos principais:
- Altura (grave/agudo)
- Duração
- Intensidade
- Timbre
""")

    st.subheader("🎼 Notas musicais")
    st.code("C D E F G A B")

    st.subheader("🎹 Semitom e Tom")
    st.write("Semitom = menor distância entre notas")
    st.write("Tom = 2 semitons")

    st.subheader("🎼 Sustenidos e bemóis")
    st.write("# = sobe meio tom")
    st.write("b = desce meio tom")

    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.subheader("🎼 Enarmonia")
    st.write("Mesma nota, nomes diferentes:")
    st.code("C# = Db | D# = Eb | F# = Gb | G# = Ab | A# = Bb")

    st.subheader("🎼 Escala maior")
    st.code("T - T - S - T - T - T - S")
    st.code("C D E F G A B")

    st.subheader("🎼 Escala menor")
    st.code("T - S - T - T - S - T - T")
    st.code("A B C D E F G")

    st.subheader("🎼 Formação de acordes")
    st.code("Maior = 1 + 3 + 5 → C E G")
    st.code("Menor = 1 + b3 + 5 → C Eb G")

    st.subheader("🎼 Sétimas")
    st.code("C7 = C E G Bb")
    st.code("Cmaj7 = C E G B")

    st.subheader("🎼 Campo harmônico")
    st.code("C Dm Em F G Am Bdim")

    st.subheader("🎯 Resumo")
    st.write("Escala → Intervalos → Acordes → Harmonia")

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
# 🎯 QUIZ (100% CORRIGIDO)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    notas = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

    intervalos = {
        "maior": [0,4,7],
        "menor": [0,3,7]
    }

    def montar(nota, tipo):
        i = notas.index(nota)
        return " ".join([notas[(i+x)%12] for x in intervalos[tipo]])

    def gerar_quiz():
        pool = []

        for n in notas:
            pool.append((f"{n} = ?", montar(n,"maior")))
            pool.append((f"{n}m = ?", montar(n,"menor")))

        random.shuffle(pool)
        return pool

    # inicializa
    if "quiz" not in st.session_state:
        st.session_state.quiz = gerar_quiz()
        st.session_state.finalizado = False
        st.session_state.respostas = {}

    # novo quiz
    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = gerar_quiz()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.rerun()

    perguntas = st.session_state.quiz[:6]

    # =========================
    # RESPONDER (SEM PRÉ-MARCAR)
    # =========================

    if not st.session_state.finalizado:

        for i, (q, correta) in enumerate(perguntas):

            st.session_state.respostas[i] = st.radio(
                q,
                options=[correta, "C E G", "D F A", "E G B", "F A C", "G B D"],
                key=f"q_{i}",
                index=None
            )

    # =========================
    # RESULTADO TRAVADO
    # =========================

    else:

        acertos = 0
        st.divider()

        for i, (q, correta) in enumerate(perguntas):

            r = st.session_state.respostas.get(i)

            st.write(f"**{q}**")
            st.write(f"Sua resposta: {r}")

            if r == correta:
                st.success("✔ Correta")
                acertos += 1
            else:
                st.error("❌ Errada")
                st.info(f"✔ Correta: {correta}")

        st.success(f"🎯 Você acertou {acertos}/6")

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()
       
