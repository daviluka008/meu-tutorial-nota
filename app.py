import streamlit as st
import random

# =========================================
# 🎹 ACORDES CORRETOS
# =========================================

mapa = {
    "C": ("C", "E", "G"),
    "C#": ("C#", "E#", "G#"),
    "Db": ("Db", "F", "Ab"),
    "D": ("D", "F#", "A"),
    "D#": ("D#", "G", "A#"),
    "Eb": ("Eb", "G", "Bb"),
    "E": ("E", "G#", "B"),
    "F": ("F", "A", "C"),
    "F#": ("F#", "A#", "C#"),
    "Gb": ("Gb", "Bb", "Db"),
    "G": ("G", "B", "D"),
    "G#": ("G#", "B#", "D#"),
    "Ab": ("Ab", "C", "Eb"),
    "A": ("A", "C#", "E"),
    "A#": ("A#", "D", "F"),
    "Bb": ("Bb", "D", "F"),
    "B": ("B", "D#", "F#")
}

notas = list(mapa.keys())

# =========================================
# 🎯 GERAR QUIZ BASE
# =========================================

def gerar_quiz():
    quiz = []
    for nota, acorde in mapa.items():
        quiz.append((f"{nota} = ?", " ".join(acorde)))
    random.shuffle(quiz)
    return quiz


# =========================================
# 🎯 OPÇÕES (4 ALTERNATIVAS CORRETAS)
# =========================================

def gerar_opcoes(correta):
    opcoes = set()
    opcoes.add(correta)

    partes = correta.split()

    if len(partes) == 3:
        a, b, c = partes
        opcoes.add(f"{a} {b} {a}")
        opcoes.add(f"{a} {c} {b}")
        opcoes.add(f"{a} {b} {c[::-1]}")

    while len(opcoes) < 4:
        opcoes.add(" ".join(mapa[random.choice(notas)]))

    lista = list(opcoes)
    random.shuffle(lista)
    return lista[:4]


# =========================================
# 🌐 CONFIG
# =========================================

st.set_page_config(page_title="🎹 Quiz de Acordes", page_icon="🎹")

st.title("🎹 Sistema Completo de Acordes + Quiz")


# =========================================
# 🎯 MODO
# =========================================

modo = st.selectbox("🎯 Modo do Quiz", ["Estudo", "Prova"])


# =========================================
# 🎯 INICIALIZAÇÃO
# =========================================

if "quiz" not in st.session_state:
    st.session_state.quiz = gerar_quiz()
    st.session_state.respostas = {}
    st.session_state.finalizado = False


# =========================================
# 🔄 NOVO QUIZ
# =========================================

if st.button("🔄 Novo quiz"):
    st.session_state.quiz = gerar_quiz()
    st.session_state.respostas = {}
    st.session_state.finalizado = False
    st.rerun()


perguntas = st.session_state.quiz[:8]


# =========================================
# 🎯 EXIBIÇÃO DAS QUESTÕES
# =========================================

if not st.session_state.finalizado:

    for i, (q, correta) in enumerate(perguntas):

        st.session_state.respostas[i] = st.radio(
            q,
            options=gerar_opcoes(correta),
            key=f"q_{i}",
            index=None
        )


# =========================================
# 📊 RESULTADO FINAL
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

    st.success(f"🎯 Você acertou {acertos}/8")


# =========================================
# 🎯 BOTÃO RESULTADO
# =========================================

if st.button("Ver resultado"):
    st.session_state.finalizado = True
    st.rerun()
