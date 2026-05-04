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

# =========================================
# 🔥 ACORDES CORRIGIDO (EbM, Ebm etc)
# =========================================
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
# 🌐 CONFIG
# =========================================

st.set_page_config(page_title="🎹 Acordes App", page_icon="🎹")

st.title("🎹 Sistema Completo de Acordes + Teoria")

pagina = st.sidebar.selectbox(
    "📌 Menu",
    ["📚 Teoria", "🎹 Prática", "🎯 Quiz"]
)


# =========================================
# 📚 TEORIA (SEM ALTERAÇÃO)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.subheader("🎵 O que é música?")
    st.write("""
Música é organização de sons no tempo: melodia, harmonia, ritmo e timbre.
""")

    st.subheader("🎼 Notas musicais")
    st.code("C D E F G A B")

    st.subheader("🎹 Tom e semitom")
    st.write("Semitom = 1 passo | Tom = 2 passos")

    st.subheader("🎼 Sustenidos e bemóis")
    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.subheader("🎼 Acordes básicos")
    st.code("""
Maior: C E G
Menor: C Eb G
""")

    st.subheader("🎼 Sétimas")
    st.code("""
C7 = C E G Bb
Cmaj7 = C E G B
""")

    st.subheader("🎯 Resumo")
    st.write("Escala → Intervalos → Acordes → Música")


# =========================================
# 🎹 PRÁTICA (SEM ALTERAÇÃO)
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
# 🎯 QUIZ NOVO (CORRIGIDO E ESTÁVEL)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

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

    def gerar():
        pool = []
        for n in notas:
            pool.append((f"{n} = ?", montar(n,"maior")))
            pool.append((f"{n}m = ?", montar(n,"menor")))
        random.shuffle(pool)
        return pool

    # RESET LIMPO
    if "quiz" not in st.session_state:
        st.session_state.quiz = gerar()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = gerar()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}
        st.rerun()

    perguntas = st.session_state.quiz[:6]

    # =========================================
    # OPÇÕES FIXAS (SEM MUDAR ORDEM OU BUG)
    # =========================================
    def gerar_opcoes(qid, correta):

        if qid in st.session_state.opcoes:
            return st.session_state.opcoes[qid]

        opcoes = {correta}

        partes = correta.split()

        if len(partes) == 3:
            c, e, g = partes

            opcoes.update([
                f"{c} Eb {g}",
                f"{c} D# {g}",
                f"{c} E G",
                f"{c} D G"
            ])

        while len(opcoes) < 4:
            n = random.choice(notas)
            opcoes.add(montar(n,"maior"))

        lista = list(opcoes)

        # trava ordem após criar
        lista.sort()

        st.session_state.opcoes[qid] = lista[:4]
        return lista[:4]

    # =========================================
    # RESPOSTAS TRAVADAS
    # =========================================
    if not st.session_state.finalizado:

        for i, (q, correta) in enumerate(perguntas):

            st.session_state.respostas[i] = st.radio(
                q,
                options=gerar_opcoes(i, correta),
                key=f"q_{i}",
                index=None
            )

    # =========================================
    # RESULTADO FINAL
    # =========================================
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

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()
