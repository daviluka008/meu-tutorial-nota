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

Cada som que ouvimos possui 4 elementos:

✔ Altura → grave ou agudo  
✔ Duração → tempo do som  
✔ Intensidade → volume  
✔ Timbre → identidade do som  

É a combinação disso que cria música.
""")

    st.subheader("🎼 Notas musicais")
    st.write("""
O sistema musical ocidental usa 7 notas:

C D E F G A B

Essas notas se repetem em ciclos no teclado.
""")

    st.subheader("🎹 Semitom e Tom")

    st.write("""
Semitom = menor distância entre duas teclas  
Tom = 2 semitons
""")

    st.code("""
Exemplo:
C → C# = 1 semitom
C → D = 1 tom
""")

    st.subheader("🎼 Sustenidos e bemóis")

    st.write("""
✔ # (sustenido) sobe meio tom  
✔ b (bemol) desce meio tom
""")

    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.subheader("🎼 Por que isso existe? (ENARMONIA)")

    st.write("""
Uma mesma nota pode ter nomes diferentes dependendo do contexto musical.

Exemplo:
- C# e Db são a mesma tecla
- F# e Gb são a mesma tecla

Isso é chamado de ENARMONIA.
""")

    st.subheader("🎼 Escala maior (base de tudo)")

    st.write("""
A escala maior segue um padrão fixo:

T - T - S - T - T - T - S

(T = tom | S = semitom)
""")

    st.code("""
Exemplo em C:
C D E F G A B
""")

    st.subheader("🎼 Escala menor natural")

    st.code("""
T - S - T - T - S - T - T

Exemplo em A:
A B C D E F G
""")

    st.subheader("🎼 Como nasce um acorde")

    st.write("""
Um acorde nasce da escala.

Pegamos notas específicas:

✔ 1 = nota principal (tônica)  
✔ 3 = define maior ou menor  
✔ 5 = estabilidade do som  
✔ 7 = tensão (emocionalidade)
""")

    st.subheader("🎼 Acorde maior")

    st.code("""
1 + 3 + 5

Exemplo:
C = C E G
""")

    st.subheader("🎼 Acorde menor")

    st.code("""
1 + b3 + 5

Exemplo:
Cm = C Eb G
""")

    st.subheader("🎼 Acordes com sétima")

    st.code("""
C7 = C E G Bb
Cmaj7 = C E G B
""")

    st.subheader("🎼 Campo harmônico")

    st.write("""
É o conjunto de acordes que nascem de uma escala.
""")

    st.code("""
C maior:
C Dm Em F G Am Bdim
""")

    st.subheader("🎯 Conclusão")

    st.write("""
Tudo na música segue uma lógica:

Escala → Intervalos → Acordes → Harmonia
""")

# =========================================
# 🎹 PRÁTICA
# =========================================

elif pagina == "🎹 Prática":

    st.header("🎹 Pratique Acordes")

    acorde = st.text_input("Digite um acorde (ex: C, Cm, D, Dm, F#, Bb)")

    if st.button("Analisar"):
        resultado = gerar_acorde(acorde)

        if resultado:
            st.success(f"🎵 Notas: {resultado['notas']}")
        else:
            st.error("❌ Acorde inválido")

# =========================================
# 🎯 QUIZ REAL (SIGLAS CORRETAS)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    base = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

    def gerar_perguntas():

        perguntas = []
        usadas = set()

        while len(perguntas) < 6:

            nota = random.choice(base)
            if nota in usadas:
                continue
            usadas.add(nota)

            tipo = random.choice(["maior", "menor"])

            if tipo == "maior":
                resposta = gerar_acorde(nota)["notas"]
                resposta = " ".join(resposta)
                pergunta = f"{nota} = ?"

            else:
                menor_map = {
                    "C":"C Eb G","C#":"C# E G#","D":"D F A","D#":"D# F# A#",
                    "E":"E G B","F":"F Ab C","F#":"F# A C#",
                    "G":"G Bb D","G#":"G# B D#","A":"A C E",
                    "A#":"A# C# E#","B":"B D F#"
                }

                resposta = menor_map.get(nota)
                pergunta = f"{nota}m = ?"

            if resposta:
                perguntas.append((pergunta, resposta))

        return perguntas

    if "quiz" not in st.session_state or st.button("🔄 Novo quiz"):
        st.session_state.quiz = gerar_perguntas()
        st.session_state.finalizado = False
        st.session_state.respostas = {}

    perguntas = st.session_state.quiz

    if not st.session_state.finalizado:

        for i, (q, correta) in enumerate(perguntas):

            escolha = st.radio(
                q,
                [correta, "C E G", "D F A", "E G B", "F A C"],
                key=f"q{i}_{id(perguntas)}",
                index=None
            )

            st.session_state.respostas[i] = escolha

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

        st.success(f"🎯 Acertos: {acertos}/6")

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()
