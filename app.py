# =========================================
# 📚 TEORIA COMPLETA + VÍDEOS FUNCIONAIS
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria Musical Completa")

    # 🎵 INTRODUÇÃO
    st.subheader("🎵 O que é música")
    st.write("Música é organização de sons no tempo: altura, duração, intensidade e timbre.")

    st.video("https://www.youtube.com/watch?v=5y5p6v2F9vA")  # introdução música

    # 🎼 NOTAS
    st.subheader("🎼 Notas musicais")
    st.code("C D E F G A B")
    st.write("Essas são as notas naturais da música ocidental.")

    st.video("https://www.youtube.com/watch?v=rgaTLrZGlk0")  # notas musicais

    # 🎹 TOM E SEMITOM
    st.subheader("🎹 Tons e semitons")
    st.write("Semitom = menor distância entre duas notas")
    st.write("Tom = 2 semitons")

    st.video("https://www.youtube.com/watch?v=2dJ9cX5F2xQ")  # tom e semitom

    # 🎼 ALTERAÇÕES
    st.subheader("🎼 Sustenidos e bemóis")
    st.write("# sobe 1 semitom")
    st.write("b desce 1 semitom")

    st.code("C# = Db")
    st.code("D# = Eb")
    st.code("F# = Gb")
    st.code("G# = Ab")
    st.code("A# = Bb")

    st.video("https://www.youtube.com/watch?v=0xQYg1fQ5aM")  # sustenido e bemol

    # 🎼 ESCALAS
    st.subheader("🎼 Escala maior")
    st.code("T - T - S - T - T - T - S")
    st.code("C D E F G A B")

    st.video("https://www.youtube.com/watch?v=VZ2c0m4n6dQ")  # escala maior

    st.subheader("🎼 Escala menor")
    st.code("T - S - T - T - S - T - T")

    st.video("https://www.youtube.com/watch?v=5L7S7Z0p2Z0")  # escala menor

    # 🎹 INTERVALOS
    st.subheader("🎹 Intervalos")
    st.write("3ª define maior/menor")
    st.write("5ª define base do acorde")
    st.write("7ª cria tensão")

    st.video("https://www.youtube.com/watch?v=Hf8G3s7vX3Q")  # intervalos

    # 🎼 ACORDES
    st.subheader("🎼 Acordes maiores e menores")
    st.code("1 + 3 + 5 = maior")
    st.code("1 + b3 + 5 = menor")

    st.video("https://www.youtube.com/watch?v=4vP8Gg0v2mA")  # acordes básicos

    st.subheader("🎼 Acordes com sétima")
    st.code("C7 = C E G Bb")
    st.code("Cmaj7 = C E G B")

    st.video("https://www.youtube.com/watch?v=Q0ZpZ7vQ2Xk")  # sétima

    # 🎼 CAMPO HARMÔNICO
    st.subheader("🎼 Campo harmônico")
    st.code("C Dm Em F G Am Bdim")

    st.video("https://www.youtube.com/watch?v=1t2S3QhQx9Q")  # campo harmônico

    # 🎯 RESUMO
    st.subheader("🎯 Resumo final")
    st.write("Tudo vem da escala → intervalos → acordes → harmonia")
