# =========================================
# 📚 TEORIA (MELHORADA E MAIS COMPLETA)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    st.subheader("🎵 O que é música?")
    st.write("""
Música é a organização dos sons no tempo.

Ela é formada por 4 elementos principais:

✔ Melodia (sequência de notas)  
✔ Harmonia (notas tocadas ao mesmo tempo)  
✔ Ritmo (organização do tempo e batidas)  
✔ Timbre (característica do som de cada instrumento)  
""")

    st.subheader("🎼 Notas musicais")
    st.write("""
As notas são a base da música:

C D E F G A B

Elas se repetem em diferentes alturas chamadas oitavas.
""")

    st.code("C D E F G A B")

    st.subheader("🎹 Tom e semitom")
    st.write("""
- Semitom = menor distância entre duas notas
- Tom = dois semitons

Exemplos:
C → C# = 1 semitom  
C → D = 1 tom
""")

    st.subheader("🎼 Sustenidos e bemóis")
    st.write("""
# = sobe meio tom  
b = desce meio tom
""")

    st.code("""
C# = Db
D# = Eb
F# = Gb
G# = Ab
A# = Bb
""")

    st.subheader("🎼 Enarmonia")
    st.write("""
Enarmonia significa a mesma nota com nomes diferentes.

Exemplo:
C# = Db (mesmo som, nome diferente)
""")

    st.subheader("🎼 Escala maior")
    st.write("""
Fórmula:
T - T - S - T - T - T - S
""")

    st.code("C D E F G A B")

    st.write("""
A escala maior é a base da maioria das músicas ocidentais.
""")

    st.subheader("🎼 Escala menor")
    st.write("""
Fórmula:
T - S - T - T - S - T - T
""")

    st.code("A B C D E F G")

    st.write("""
A escala menor tem um som mais triste ou emocional.
""")

    st.subheader("🎹 Formação de acordes")
    st.write("""
Acordes são formados por notas da escala.

✔ Acorde maior: 1 + 3 + 5  
✔ Acorde menor: 1 + b3 + 5
""")

    st.code("""
C maior = C E G
C menor = C Eb G
""")

    st.subheader("🎼 Intervalos")
    st.write("""
Intervalos são as distâncias entre as notas:

- 3ª maior → som feliz  
- 3ª menor → som triste  
- 5ª → estabilidade do acorde  
- 7ª → tensão e emoção
""")

    st.subheader("🎼 Acordes com sétima")
    st.code("""
C7 = C E G Bb
Cmaj7 = C E G B
""")

    st.subheader("🎼 Campo harmônico")
    st.write("""
É o conjunto de acordes de uma escala.

Exemplo em Dó maior:

C Dm Em F G Am Bdim
""")

    st.subheader("🎯 Resumo final")
    st.write("""
ESCALA → INTERVALOS → ACORDES → HARMONIA → MÚSICA

Tudo na música começa pelas notas.
""")
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

# =========================================
# 🎯 QUIZ NOVO (CORRIGIDO 100% MUSICAL)
# =========================================

elif pagina == "🎯 Quiz":

    st.header("🎯 Quiz de Acordes")

    # escala cromática completa (base correta)
    escala = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # mapa de posições
    mapa = {nota: i for i, nota in enumerate(escala)}

    # intervalos reais
    maior = [0, 4, 7]
    menor = [0, 3, 7]

    def montar_acorde(nota, tipo):
        i = mapa[nota]
        intervalos = maior if tipo == "maior" else menor
        return " ".join([escala[(i + x) % 12] for x in intervalos])

    # gerar perguntas fixas na sessão
    def gerar_perguntas():
        pool = []
        for n in escala:
            pool.append((f"{n} = ?", montar_acorde(n, "maior"), "maior"))
            pool.append((f"{n}m = ?", montar_acorde(n, "menor"), "menor"))
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

    # =========================================
    # 🎯 OPÇÕES 100% CORRETAS (SEM BUG)
    # =========================================
    def gerar_opcoes(qid, correta, tipo):

        if qid in st.session_state.opcoes:
            return st.session_state.opcoes[qid]

        opcoes = {correta}

        notas_erradas = [
            "C Eb G", "C D G", "C E G#",
            "D F A", "D F# A", "E G B",
            "F A C", "F Ab C", "G B D",
            "G Bb D", "A C E", "A C# E",
            "B D F", "B D# F#"
        ]

        # garante alternativas falsas plausíveis
        while len(opcoes) < 4:
            opcoes.add(random.choice(notas_erradas))

        lista = list(opcoes)

        # FIXA ORDEM (não muda ao clicar)
        lista.sort()

        st.session_state.opcoes[qid] = lista[:4]
        return lista[:4]

    # =========================================
    # BLOQUEIO DE RESPOSTA
    # =========================================
    if not st.session_state.finalizado:

        for i, (q, correta, tipo) in enumerate(perguntas):

            st.session_state.respostas[i] = st.radio(
                q,
                options=gerar_opcoes(i, correta, tipo),
                key=f"q_{i}",
                index=None
            )

    # =========================================
    # RESULTADO FINAL
    # =========================================
    else:

        acertos = 0
        st.divider()

        for i, (q, correta, tipo) in enumerate(perguntas):

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
