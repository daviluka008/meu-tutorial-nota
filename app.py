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
        "7M": [0,4,7,11],
        "dim": [0,3,6],
        "aug": [0,4,8],
        "sus2": [0,2,7],
        "sus4": [0,5,7],
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
# 📚 TEORIA (MANTIDA)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.write("""
Música é organização de sons no tempo.

Elementos:
✔ Melodia
✔ Harmonia
✔ Ritmo
✔ Timbre
""")

    st.code("C D E F G A B")

    st.write("Sustenido sobe meio tom (#) e bemol desce (b).")

    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.write("Acorde maior: 1 + 3 + 5")
    st.write("Acorde menor: 1 + b3 + 5")

    st.code("""
C = C E G
Cm = C Eb G
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
        else:
            st.error("❌ Acorde inválido")


# =========================================
# 🎯 QUIZ COMPLETO (FIXADO + TODAS NOTAS)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes Completo")

    notas = [
        "C","C#","Db","D","D#","Eb","E","F","F#","Gb",
        "G","G#","Ab","A","A#","Bb","B"
    ]

    base = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

    mapa = {
        "C":0,"C#":1,"Db":1,"D":2,"D#":3,"Eb":3,
        "E":4,"F":5,"F#":6,"Gb":6,"G":7,"G#":8,"Ab":8,
        "A":9,"A#":10,"Bb":10,"B":11
    }

    maior = [0,4,7]
    menor = [0,3,7]

    def montar(nota, tipo):
        i = mapa[nota]
        intervalos = maior if tipo == "maior" else menor
        return " ".join([base[(i+x)%12] for x in intervalos])

    def gerar_quiz():
        perguntas = []
        for n in notas:
            perguntas.append((f"{n} = ?", montar(n,"maior")))
            perguntas.append((f"{n}m = ?", montar(n,"menor")))
        random.shuffle(perguntas)
        return perguntas

    if "quiz" not in st.session_state:
        st.session_state.quiz = gerar_quiz()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}

    def gerar_opcoes(qid, correta):

        if qid in st.session_state.opcoes:
            return st.session_state.opcoes[qid]

        base = set()
        base.add(correta)

        partes = correta.split()

        if len(partes) == 3:
            c, e, g = partes

            base.add(f"{c} Eb {g}")
            base.add(f"{c} D {g}")
            base.add(f"{c} E Gb")
            base.add(f"{c} E F#")

        extras = [
            "C E G","C Eb G","D F A","D F# A",
            "E G B","F A C","F Ab C",
            "G B D","G Bb D","A C E",
            "A C# E","B D F","B D# F#"
        ]

        while len(base) < 5:
            base.add(random.choice(extras))

        lista = list(base)
        random.shuffle(lista)

        st.session_state.opcoes[qid] = lista[:5]
        return lista[:5]

    perguntas = st.session_state.quiz[:6]

    st.info("Depois de enviar não pode alterar respostas.")

    if not st.session_state.finalizado:

        for i, (q, correta) in enumerate(perguntas):

            if i not in st.session_state.respostas:
                st.session_state.respostas[i] = st.radio(
                    q,
                    gerar_opcoes(i, correta),
                    key=f"q_{i}",
                    index=None
                )

    else:

        acertos = 0
        st.divider()

        for i, (q, correta) in enumerate(perguntas):

            r = st.session_state.respostas.get(i)

            st.write(f"**{q}**")

            if r == correta:
                st.success("✔ Correta")
                acertos += 1
            else:
                st.error(f"❌ Errada → correta: {correta}")

        st.success(f"🎯 Você acertou {acertos}/6")

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = gerar_quiz()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}
        st.rerun()

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()
