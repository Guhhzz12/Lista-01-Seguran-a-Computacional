from unidecode import unidecode

letras_para_numeros = {chr(i + ord('A')): i for i in range(26)}
numeros_para_letras = {i: chr(i + ord('A')) for i in range(26)}

def shift_cipher(texto, chave):
    resultado = ""
    for char in texto:
        if char.isalpha():
            base_char = unidecode(char)
            base = ord('A') if char.isupper() else ord('a')
            deslocado = (ord(base_char.lower()) - ord('a') + chave) % 26
            novo_char = chr(base + deslocado)
            resultado += novo_char.upper() if char.isupper() else novo_char
        else:
            resultado += char
    return resultado

def forca_bruta(mensagem_criptografada):
    print("\nTentativas de descriptografia por força bruta:\n")
    for chave in range(1, 27):
        tentativa = shift_cipher(mensagem_criptografada, -chave)
        print(f"Deslocamento {chave:2}: {tentativa}")

def substituicao_por_frequencia_simples(mensagem_criptografada):
    print("\nTentativas de descriptografia por substituição simples (letras mais frequentes do português):\n")
    texto_sem_espacos = ''.join(c for c in mensagem_criptografada if c.isalpha())
    if not texto_sem_espacos:
        print("Mensagem inválida ou vazia.")
        return

    letra_mais_frequente = max(set(unidecode(texto_sem_espacos.upper())), key=unidecode(texto_sem_espacos.upper()).count)
    letras_comuns_pt = ['E', 'A', 'O', 'S', 'R']

    for letra_pt in letras_comuns_pt:
        desloc = (letras_para_numeros[letra_mais_frequente] - letras_para_numeros[letra_pt]) % 26
        tentativa = shift_cipher(mensagem_criptografada, -desloc)
        print(f"Assumindo que '{letra_mais_frequente}' = '{letra_pt}' → Deslocamento {desloc:2}: {tentativa}")

def main():
    print("1 - Criptografar mensagem")
    print("2 - Descriptografar por força bruta")
    print("3 - Descriptografar por substituição (frequência simples)")
    print("4 - Descriptografar mensagem com chave")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        mensagem = input("Digite a mensagem: ")
        while True:
            try:
                chave = int(input("Digite o deslocamento (0 a 26): "))
                if 0 <= chave <= 26:
                    break
                else:
                    print("Por favor, escolha um número entre 0 e 26.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
        criptografado = shift_cipher(mensagem, chave)
        print(f"\nCriptografado: {criptografado}")

    elif opcao == "2":
        mensagem = input("Digite a mensagem criptografada: ")
        forca_bruta(mensagem)

    elif opcao == "3":
        mensagem = input("Digite a mensagem criptografada: ")
        substituicao_por_frequencia_simples(mensagem)

    elif opcao == "4":
        mensagem = input("Digite a mensagem criptografada: ")
        while True:
            try:
                chave = int(input("Digite a chave de descriptografia (0 a 26): "))
                if 0 <= chave <= 26:
                    break
                else:
                    print("Por favor, escolha um número entre 0 e 26.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
        descriptografado = shift_cipher(mensagem, -chave)
        print(f"\nTexto descriptografado: {descriptografado}")
    
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
