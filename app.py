# =========================================
# 📚 TEORIA (EXPANDIDA E EXPLICATIVA)
# =========================================

if pagina == "📚 Teoria":

    st.header("🎓 Teoria dos Acordes")

    st.subheader("🎵 O que é um acorde?")
    st.write(
        "Um acorde é a combinação de 3 ou mais notas tocadas ao mesmo tempo. "
        "Essas notas são organizadas a partir de uma escala musical."
    )

    st.subheader("🎼 Como um acorde é formado?")

    st.write("Todo acorde básico maior segue essa estrutura:")

    st.code("1 (tônica) + 3 (terça maior) + 5 (quinta justa)")

    st.write("Exemplo no acorde de C maior:")

    st.code("C = C (tônica) + E (terça maior) + G (quinta justa)")

    st.write("👉 Isso significa que começamos na nota C e pulamos notas na escala:")

    st.write("C → D → E → F → G")

    st.success("Resultado: C E G")

    st.divider()

    st.subheader("🎼 Acordes menores")

    st.write("No acorde menor, a única mudança é a terça:")

    st.code("1 + b3 + 5")

    st.write("A terça é abaixada meio tom (fica mais ‘triste’ no som).")

    st.write("Exemplo:")

    st.code("Cm = C + Eb + G")

    st.write("C → D → Eb → F → G")

    st.success("Resultado: C Eb G")

    st.divider()

    st.subheader("🎼 Acordes com sétima")

    st.write("A sétima adiciona mais tensão e cor ao som.")

    st.write("Existem dois principais tipos:")

    st.code("C7 = 1 + 3 + 5 + b7")
    st.code("C7M = 1 + 3 + 5 + 7")

    st.write("Exemplo C7:")

    st.code("C E G Bb")

    st.write("Exemplo C7M:")

    st.code("C E G B")

    st.divider()

    st.subheader("🎼 Sustenidos (#) e bemóis (b)")

    st.write("Esses símbolos alteram a altura da nota:")

    st.write("🔼 Sustenido (#) sobe meio tom")
    st.write("🔽 Bemol (b) desce meio tom")

    st.code("C# = C sobe meio tom")
    st.code("Eb = E desce meio tom")

    st.divider()

    st.subheader("🎼 Enarmonia (mesma nota com nomes diferentes)")

    st.write("Algumas notas têm dois nomes diferentes, mas soam igual:")

    st.code("C# = Db")
    st.code("D# = Eb")
    st.code("F# = Gb")
    st.code("G# = Ab")
    st.code("A# = Bb")

    st.info("Isso depende do contexto musical.")

    st.divider()

    st.subheader("🎯 Resumo")

    st.write("""
    - Acorde maior = som mais aberto e feliz  
    - Acorde menor = som mais triste  
    - Sustenido/bemol = ajusta meio tom  
    - Sétima = adiciona tensão e emoção  
    """)

    st.success("Agora você já entende como os acordes são construídos 🎹")
