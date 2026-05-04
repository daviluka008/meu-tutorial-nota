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

st.set_page_config(page_title="🎹 Curso Completo de Música", page_icon="🎹")

st.title("🎹 Curso Completo de Música e Piano")

pagina = st.sidebar.selectbox(
    "📌 Menu",
    ["📚 Teoria Completa", "🎹 Prática", "🎯 Quiz"]
)

# =========================================
# 📚 TEORIA (CURSO COMPLETO REAL)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa (Curso Real)")

    st.subheader("🎵 1. O que é música")
    st.write("""
Música é a organização intencional dos sons no tempo.

Ela depende de 4 pilares:

✔ Melodia → sequência de notas  
✔ Harmonia → notas tocadas juntas  
✔ Ritmo → organização do tempo  
✔ Timbre → característica do som  
""")

    st.subheader("🎼 2. Sistema de notas (padrão ocidental)")

    st.code("C D E F G A B")

    st.write("""
Esse sistema é chamado de escala natural.

Ele se repete infinitamente em oitavas.
""")

    st.subheader("🎹 3. Teclado completo")

    st.write("""
O piano funciona com 12 sons repetidos:

C C# D D# E F F# G G# A A# B
""")

    st.subheader("🎼 4. Enarmonia (essencial)")

    st.write("""
Mesma nota, nomes diferentes:

C# = Db  
D# = Eb  
F# = Gb  
G# = Ab  
A# = Bb  
""")

    st.subheader("🎹 5. Tom e semitom")

    st.write("""
Semitom = menor distância no piano  
Tom = 2 semitons  

Exemplo:
C → C# = 1 semitom  
C → D = 1 tom  
""")

    st.subheader("🎼 6. Escala maior (base de tudo)")

    st.code("T - T - S - T - T - T - S")

    st.write("Exemplo C:")
    st.code("C D E F G A B")

    st.subheader("🎼 7. Escala menor")

    st.code("T - S - T - T - S - T - T")

    st.code("A B C D E F G")

    st.subheader("🎹 8. Formação de acordes")

    st.write("""
Acordes são construídos por intervalos:

✔ Maior = 1 + 3 + 5 → C E G  
✔ Menor = 1 + b3 + 5 → C Eb G  
✔ Diminuto = 1 + b3 + b5  
✔ Aumentado = 1 + 3 + #5  
""")

    st.subheader("🎼 9. Acordes com sétima")

    st.code("""
C7 = C E G Bb
Cmaj7 = C E G B
""")

    st.subheader("🎹 10. Campo harmônico")

    st.code("C Dm Em F G Am Bdim")

    st.subheader("🎯 Conclusão")

    st.write("""
Tudo na música vem de:

ESCALA → INTERVALOS → ACORDES → HARMONIA → EMOÇÃO
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
# 🎯 QUIZ BASE (PRONTO PARA EXPANSÃO TOTAL)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    notas = notas_sharp + notas_flat

    def gerar_perguntas():
        perguntas = []
        for n in notas:
            perguntas.append((f"{n} = ?", f"{n} maior"))
            perguntas.append((f"{n}m = ?", f"{n} menor"))
        random.shuffle(perguntas)
        return perguntas[:6]

    if "quiz" not in st.session_state:
        st.session_state.quiz = gerar_perguntas()
        st.session_state.finalizado = False

    perguntas = st.session_state.quiz

    respostas = []

    for i, (q, correta) in enumerate(perguntas):

        escolha = st.radio(
            q,
            ["maior", "menor", "dim", "aug"],
            key=f"q{i}",
            disabled=st.session_state.finalizado
        )

        respostas.append((escolha, correta))

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()
