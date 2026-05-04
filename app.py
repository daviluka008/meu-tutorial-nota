# =========================================
# 🎹 SISTEMA COMPLETO DE ACORDES + TECLADO
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

    # baixo
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

    return {
        "notas": notas,
        "baixo": baixo
    }

# =========================================
# 🎹 TECLADO SIMPLES
# =========================================

def mostrar_teclado(notas_acorde):
    base = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    teclado = ""
    for nota in base:
        if nota in notas_acorde:
            teclado += f"[{nota}] "
        else:
            teclado += f" {nota}  "

    print("\n🎹 Teclado:")
    print(teclado)
    print("👉 Toque as notas entre []\n")

# =========================================
# 🎓 TUTORIAL
# =========================================

def tutorial():
    print("\n🎓 ===== TUTORIAL =====\n")

    print("👉 Acorde = várias notas tocadas juntas\n")

    print("MAIOR: 1 + 3 + 5")
    print("C → C E G\n")

    print("MENOR: 1 + b3 + 5")
    print("Cm → C Eb G\n")

    print("COM 7:")
    print("C7 → C E G Bb")
    print("C7M → C E G B\n")

    print("ADD9:")
    print("Cadd9 → C E G D\n")

    print("SUS:")
    print("Csus2 → C D G")
    print("Csus4 → C F G\n")

    print("BAIXO DIFERENTE:")
    print("G/B → acorde G com baixo B\n")

    print("SUSTENIDO (#) sobe meio tom")
    print("BEMOL (b) desce meio tom\n")

    print("👉 Teste: C, Cm, Cadd9, G/B, F#, Bb\n")

# =========================================
# 🤖 MENU
# =========================================

def menu():
    while True:
        print("\n🤖 ===== MENU =====")
        print("1 - Aprender")
        print("2 - Testar acorde")
        print("3 - Sair")

        op = input("Escolha: ")

        if op == "1":
            tutorial()

        elif op == "2":
            acorde = input("\nDigite o acorde: ")
            resultado = gerar_acorde(acorde)

            if resultado:
                print("\nNotas:", resultado["notas"])

                if resultado["baixo"]:
                    print("Baixo:", resultado["baixo"])

                mostrar_teclado(resultado["notas"])

            else:
                print("\n❌ Acorde não reconhecido!\n")

        elif op == "3":
            print("Encerrando...")
            break

        else:
            print("Opção inválida!")

# INICIAR
menu()
