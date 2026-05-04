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
# 📚 TEORIA MUSICAL COMPLETA (EXPANDIDA DE VERDADE)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.subheader("🎵 O que é música?")
    st.write("""
Música é a organização consciente dos sons no tempo.

Ela não é apenas “som bonito”, mas um sistema estruturado que combina:
- Altura (grave ou agudo)
- Duração (tempo das notas)
- Intensidade (volume)
- Timbre (identidade sonora)

Tudo isso trabalha junto para criar emoção e harmonia.
""")

    st.subheader("🎼 O que são notas musicais?")
    st.write("""
As notas musicais são os sons básicos usados para formar toda a música ocidental.

Elas são 7:

C - D - E - F - G - A - B

Essas notas se repetem em diferentes alturas (oitavas).
""")

    st.subheader("🎹 O que é tom e semitom?")
    st.write("""
- Semitom = menor distância possível entre duas notas
- Tom = dois semitons

Exemplo no teclado:
- C → C# = 1 semitom
- C → D = 1 tom
""")

    st.subheader("🎼 Sustenidos (#) e bemóis (b)")
    st.write("""
Eles servem para alterar a altura das notas:

- # (sustenido) → sobe meio tom
- b (bemol) → desce meio tom

Exemplos reais:

C# = Db  
D# = Eb  
F# = Gb  
G# = Ab  
A# = Bb  

Isso é chamado de ENARMONIA (mesma nota com nomes diferentes).
""")

    st.subheader("🎼 Enarmonia (explicação simples)")
    st.write("""
Enarmonia significa que duas notas diferentes no nome podem ser a mesma no som.

Exemplo:
- C# e Db soam iguais
- D# e Eb soam iguais

A diferença é apenas teórica (notação musical).
""")

    st.subheader("🎼 Escala maior (base da música)")
    st.write("""
A escala maior é a estrutura principal da música ocidental.

Fórmula:
T - T - S - T - T - T - S

Exemplo em C:
C D E F G A B
""")

    st.subheader("🎼 Escala menor (som emocional)")
    st.write("""
A escala menor tem som mais triste ou emocional.

Fórmula:
T - S - T - T - S - T - T

Exemplo:
A B C D E F G
""")

    st.subheader("🎼 Como acordes são formados")
    st.write("""
Acordes são combinações de notas da escala.

🎹 Acorde maior:
1 + 3 + 5 → C E G

🎹 Acorde menor:
1 + b3 + 5 → C Eb G
""")

    st.subheader("🎼 Por que acordes funcionam?")
    st.write("""
Porque eles seguem relações matemáticas entre frequências.

- 3ª define se é maior ou menor
- 5ª dá estabilidade
- 7ª cria tensão emocional
""")

    st.subheader("🎼 Sétimas")
    st.write("""
A sétima adiciona profundidade emocional ao acorde.

Exemplo:
C7 = C E G Bb  
Cmaj7 = C E G B
""")

    st.subheader("🎼 Campo harmônico")
    st.write("""
É o conjunto de acordes que pertencem a uma tonalidade.

Exemplo em C:

C Dm Em F G Am Bdim
""")

    st.subheader("🎯 Conclusão")
    st.write("""
Toda música funciona assim:

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
# 🎯 QUIZ
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    notas = ["C","C#","Db","D","D#","Eb","E","F","F#","Gb","G","G#","Ab","A","A#","Bb","B"]

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
        pool = []
        for n in notas:
            pool.append((f"{n} = ?", montar(n,"maior")))
            pool.append((f"{n}m = ?", montar(n,"menor")))
        random.shuffle(pool)
        return pool

    # =========================
    # INIT QUIZ
    # =========================

    if "quiz" not in st.session_state:
        st.session_state.quiz = gerar_quiz()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = gerar_quiz()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}
        st.rerun()

    perguntas = st.session_state.quiz[:6]

    # =========================================
    # 🎯 OPÇÕES FIXAS (NÃO MUDAM MAIS)
    # =========================================

    def gerar_opcoes_estaveis(qid, correta):

        if qid in st.session_state.opcoes:
            return st.session_state.opcoes[qid]

        partes = correta.split()

        opts = [correta]

        if len(partes) == 3:
            c, e, g = partes

            opts.append(f"{c} D {g}")
            opts.append(f"{c} Eb {g}")
            opts.append(f"{c} E A")
            opts.append(f"{c} E Gb")

        extras = [
            "C E G",
            "C Eb G",
            "D F A",
            "E G B",
            "F A C",
            "G B D",
            "A C E",
            "B D F"
        ]

        while len(opts) < 5:
            op = random.choice(extras)
            if op not in opts:
                opts.append(op)

        random.shuffle(opts)
        opts = opts[:5]

        st.session_state.opcoes[qid] = opts
        return opts

    # =========================
    # RESPOSTAS
    # =========================

    if not st.session_state.finalizado:

        for i, (q, correta) in enumerate(perguntas):

            st.session_state.respostas[i] = st.radio(
                q,
                options=gerar_opcoes_estaveis(i, correta),
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
