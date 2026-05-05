import streamlit as st
import random
import smtplib
from email.message import EmailMessage

# =========================================
# 🔐 LOGIN SYSTEM
# =========================================

if "usuarios" not in st.session_state:
    st.session_state.usuarios = {}

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = ""

if "codigo_verificacao" not in st.session_state:
    st.session_state.codigo_verificacao = None

if "email_temp" not in st.session_state:
    st.session_state.email_temp = ""

if "senha_temp" not in st.session_state:
    st.session_state.senha_temp = ""

# =========================================
# 🔐 EMAIL (SECRETS OPCIONAL, NÃO QUEBRA)
# =========================================

EMAIL_ORIGEM = None
SENHA_APP = None

if hasattr(st, "secrets"):
    if "EMAIL_ORIGEM" in st.secrets and "SENHA_APP" in st.secrets:
        EMAIL_ORIGEM = st.secrets["EMAIL_ORIGEM"]
        SENHA_APP = st.secrets["SENHA_APP"]

# =========================================
# 📩 ENVIAR CÓDIGO
# =========================================

def enviar_codigo(email, codigo):

    if EMAIL_ORIGEM is None or SENHA_APP is None:
        st.warning("E-mail não configurado. Conta será criada sem verificação.")
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = "Código de verificação"
        msg["From"] = EMAIL_ORIGEM
        msg["To"] = email
        msg.set_content(f"Seu código de verificação é: {codigo}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ORIGEM, SENHA_APP)
            smtp.send_message(msg)

    except:
        st.error("Erro ao enviar e-mail")

# =========================================
# 🔐 TELA LOGIN
# =========================================

def tela_login():

    st.title("🔐 Login")

    opcao = st.radio("Escolha", ["Entrar", "Criar conta"])

    if opcao == "Criar conta":

        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Criar conta"):

            if email == "" or senha == "":
                st.error("Preencha tudo")
                return

            if email in st.session_state.usuarios:
                st.error("Usuário já existe")
                return

            codigo = str(random.randint(100000, 999999))

            st.session_state.codigo_verificacao = codigo
            st.session_state.email_temp = email
            st.session_state.senha_temp = senha

            enviar_codigo(email, codigo)
            st.success("Código enviado")

        if st.session_state.codigo_verificacao:

            codigo_input = st.text_input("Código de verificação")

            if st.button("Validar"):

                if codigo_input == st.session_state.codigo_verificacao:

                    st.session_state.usuarios[st.session_state.email_temp] = st.session_state.senha_temp
                    st.success("Conta criada!")
                    st.session_state.codigo_verificacao = None

                else:
                    st.error("Código errado")

    else:

        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):

            if email in st.session_state.usuarios and st.session_state.usuarios[email] == senha:

                st.session_state.logado = True
                st.session_state.usuario_atual = email
                st.rerun()

            else:
                st.error("Login inválido")

# =========================================
# 🚪 BLOQUEIO DO APP
# =========================================

if not st.session_state.logado:
    tela_login()
    st.stop()

# =========================================
# 🎹 LÓGICA DOS ACORDES (SEU ORIGINAL)
# =========================================

notas_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
notas_flat = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

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
# 📚 TEORIA (SEU ORIGINAL INTACTO)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.subheader("🎵 O que é música?")
    st.write("""
Música é a organização dos sons no tempo, combinando:
- Melodia
- Harmonia
- Ritmo
- Timbre
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
# 🎹 PRÁTICA (SEU ORIGINAL INTACTO)
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
# 🎯 QUIZ (SEU ORIGINAL INTACTO)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    escala = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

    mapa = {nota: i for i, nota in enumerate(escala)}

    maior = [0,4,7]
    menor = [0,3,7]

    def montar_acorde(nota, tipo):
        i = mapa[nota]
        intervalos = maior if tipo == "maior" else menor
        return " ".join([escala[(i+x)%12] for x in intervalos])

    def gerar_perguntas():
        pool = []
        for n in escala:
            pool.append((f"{n} = ?", montar_acorde(n,"maior"), "maior"))
            pool.append((f"{n}m = ?", montar_acorde(n,"menor"), "menor"))
        random.shuffle(pool)
        return pool

    if "quiz" not in st.session_state:
        st.session_state.quiz = gerar_perguntas()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}

    if st.button("🔄 Novo quiz"):
        st.session_state.quiz = gerar_perguntas()
        st.session_state.finalizado = False
        st.session_state.respostas = {}
        st.session_state.opcoes = {}
        st.rerun()

    perguntas = st.session_state.quiz[:6]

    def gerar_opcoes(qid, correta, tipo):

        if qid in st.session_state.opcoes:
            return st.session_state.opcoes[qid]

        opcoes = {correta}

        falsas = [
            "C Eb G","C D G","C E G#","D F A","D F# A",
            "E G B","F A C","F Ab C","G B D","G Bb D",
            "A C E","A C# E","B D F","B D# F#"
        ]

        while len(opcoes) < 4:
            opcoes.add(random.choice(falsas))

        lista = list(opcoes)
        lista.sort()

        st.session_state.opcoes[qid] = lista[:4]
        return lista[:4]

    if not st.session_state.finalizado:

        for i,(q,correta,tipo) in enumerate(perguntas):

            st.session_state.respostas[i] = st.radio(
                q,
                options=gerar_opcoes(i,correta,tipo),
                key=f"q_{i}",
                index=None
            )

    else:

        acertos = 0
        st.divider()

        for i,(q,correta,tipo) in enumerate(perguntas):

            r = st.session_state.respostas.get(i)

            if r == correta:
                st.success(f"{q} ✔")
                acertos += 1
            else:
                st.error(f"{q} ❌ correta: {correta}")

        st.success(f"🎯 Você acertou {acertos}/6")

    if st.button("Ver resultado"):
        st.session_state.finalizado = True
        st.rerun()
