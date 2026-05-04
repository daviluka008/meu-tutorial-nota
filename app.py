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
# 📚 TEORIA COMPLETA (EXPLICADA DE VERDADE)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.subheader("🎵 O que é música?")
    st.write("""
Música é a organização de sons no tempo.

Ela possui 4 elementos principais:
✔ altura (grave ou agudo)
✔ duração (tempo)
✔ intensidade (forte ou fraco)
✔ timbre (identidade do som)
""")

    st.subheader("🎼 Notas musicais")
    st.write("O sistema musical ocidental usa 7 notas:")
    st.code("C D E F G A B")

    st.write("Essas notas se repetem em diferentes alturas no teclado.")

    st.subheader("🎹 Semitom e Tom")
    st.write("Semitom = menor distância entre duas teclas")
    st.write("Tom = 2 semitons")

    st.write("Exemplo:")
    st.code("C → C# = 1 semitom")
    st.code("C → D = 1 tom")

    st.subheader("🎼 Sustenidos e bemóis")

    st.write("""
✔ # sobe meio tom  
✔ b desce meio tom
""")

    st.write("Exemplos reais:")
    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.subheader("🎼 Escala maior (base de tudo)")
    st.write("Fórmula:")
    st.code("T - T - S - T - T - T - S")

    st.write("Exemplo em C:")
    st.code("C D E F G A B")

    st.subheader("🎼 Escala menor natural")
    st.code("T - S - T - T - S - T - T")

    st.write("Exemplo:")
    st.code("A B C D E F G")

    st.subheader("🎼 Intervalos (fundação dos acordes)")

    st.write("""
✔ 1 = nota base (tônica)  
✔ 3 = define maior ou menor  
✔ 5 = estabilidade  
✔ 7 = tensão harmônica
""")

    st.subheader("🎼 Formação de acordes")

    st.write("🎹 Acorde maior:")
    st.code("1 + 3 + 5 → C E G")

    st.write("🎹 Acorde menor:")
    st.code("1 + b3 + 5 → C Eb G")

    st.write("🎹 Acorde com sétima:")
    st.code("C7 → C E G Bb")

    st.subheader("🎼 Campo harmônico maior")

    st.code("C Dm Em F G Am Bdim")

    st.subheader("🎼 Funções harmônicas")

    st.write("""
✔ Tônica = descanso  
✔ Subdominante = movimento  
✔ Dominante = tensão
""")

    st.code("C → F → G → C")

    st.subheader("🎯 Conclusão")
    st.write("Tudo na música vem de escala → intervalos → acordes → harmonia")

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
# 🎯 QUIZ COMPLETO DINÂMICO
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    banco = [
        ("C = ?", ["C D E", "C E G", "C F G"], "C E G"),
        ("Cm = ?", ["C Eb G", "C E G", "C F G"], "C Eb G"),
        ("D = ?", ["D F# A", "D F A", "D E A"], "D F# A"),
        ("D# = ?", ["D# F# A#", "D D# A#", "D# G A#"], "D# F# A#"),
        ("Eb = ?", ["Eb G Bb", "Eb F Ab", "Eb G C"], "Eb G Bb"),
        ("F# = ?", ["F# A# C#", "F# A C#", "F# B D"], "F# A# C#"),
        ("Gb = ?", ["Gb Bb Db", "Gb A C#", "Gb B D"], "Gb Bb Db"),
        ("G# = ?", ["G# C D#", "G# B D#", "G# C E"], "G# C D#"),
        ("Ab = ?", ["Ab C Eb", "Ab D F", "Ab B Eb"], "Ab C Eb"),
        ("Bb = ?", ["Bb D F", "Bb C F", "Bb E G"], "Bb D F"),
    ]

    if "quiz" not in st.session_state:
        st.session_state.quiz = random.sample(banco, 5)
        st.session_state.finalizado = False
        st.session_state.respostas = {}

    perguntas = st.session_state.quiz

    # NÃO MARCA NADA AO ENTRAR
    if not st.session_state.finalizado:

        for i, (q, op, c) in enumerate(perguntas):

            escolha = st.radio(
                q,
                op,
                key=f"q{i}_{id(perguntas)}",
                index=None
            )

            st.session_state.respostas[i] = escolha

    # RESULTADO TRAVADO
    else:

        acertos = 0
        st.divider()

        for i, (q, op, c) in enumerate(perguntas):

            r = st.session_state.respostas[i]

            st.write(f"**{q}**")
            st.write(f"Sua resposta: {r}")

            if r == c:
                st.success("✔ Correta")
                acertos += 1
            else:
                st.error("❌ Errada")
                st.info(f"✔ Correta: {c}")

        st.success(f"🎯 Acertos: {acertos}/5")

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = random.sample(banco, 5)
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.rerun()
