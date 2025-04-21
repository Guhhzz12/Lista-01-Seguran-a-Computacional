from collections import Counter
from unidecode import unidecode
import math

FREQ_PT = {
    'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57, 'f': 1.02,
    'g': 1.30, 'h': 1.28, 'i': 6.18, 'j': 0.40, 'k': 0.02, 'l': 2.78,
    'm': 4.74, 'n': 5.05, 'o': 10.73, 'p': 2.52, 'q': 1.20, 'r': 6.53,
    's': 7.81, 't': 4.34, 'u': 4.63, 'v': 1.67, 'w': 0.01, 'x': 0.21,
    'y': 0.01, 'z': 0.47
}


def cifra_transposicao(mensagem, chave):
    mensagem = unidecode(mensagem)  
    colunas = [''] * chave
    for i in range(len(mensagem)):
        col = i % chave
        colunas[col] += mensagem[i]
    return ''.join(colunas)

def decifra_transposicao(mensagem, chave):
    mensagem = unidecode(mensagem)  
    num_colunas = chave
    num_linhas = len(mensagem) // chave
    if len(mensagem) % chave != 0:
        num_linhas += 1

    colunas = []
    tamanho_coluna_base = len(mensagem) // chave
    num_colunas_maiores = len(mensagem) % chave

    idx = 0
    for i in range(chave):
        tamanho_coluna = tamanho_coluna_base + (1 if i < num_colunas_maiores else 0)
        colunas.append(mensagem[idx:idx + tamanho_coluna])
        idx += tamanho_coluna

    resultado = ''
    for i in range(num_linhas):
        for col in colunas:
            if i < len(col):
                resultado += col[i]
    return resultado

def calcula_frequencia(texto):
    texto = unidecode(texto.lower())
    letras = [c for c in texto if c.isalpha()]
    total = len(letras)
    contagem = Counter(letras)
    freq = {letra: (contagem.get(letra, 0) / total) * 100 if total > 0 else 0 for letra in FREQ_PT}
    return freq

def erro_absoluto_medio(freq1, freq2):
    return sum(abs(freq1[letra] - freq2[letra]) for letra in FREQ_PT) / len(FREQ_PT)

def descriptografar_por_frequencia(mensagem, top_n=5):
    print("\nDescriptografando por frequência de letras...\n")
    tentativas = []

    for chave in range(2, min(len(mensagem), 40)): 
        tentativa = decifra_transposicao(mensagem, chave)
        freq_tentativa = calcula_frequencia(tentativa)
        erro = erro_absoluto_medio(freq_tentativa, FREQ_PT)
        tentativas.append((erro, chave, tentativa))

    tentativas.sort(key=lambda x: x[0]) 

    print(f"\nTop {top_n} melhores tentativas:")
    for erro, chave, texto in tentativas[:top_n]:
        print(f"\n🔑 Chave {chave:2} | Erro médio: {erro:.4f}")
        print(f"📜 Texto: {texto[:300]}{'...' if len(texto) > 300 else ''}")

def forca_bruta(mensagem):
    print("\nTentativas de descriptografia por força bruta:\n")
    for chave in range(2, len(mensagem) + 1):
        tentativa = decifra_transposicao(mensagem, chave)
        print(f"Chave {chave:2}: {tentativa}")

def main():
    print("1 - Criptografar mensagem")
    print("2 - Descriptografar com chave")
    print("3 - Descriptografar por força bruta")
    print("4 - Descriptografar por distribuição de frequência (sem RMSE)")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        mensagem = input("Digite a mensagem: ")
        chave = int(input("Digite a chave (número de colunas): "))
        criptografada = cifra_transposicao(mensagem, chave)
        print(f"\nCriptografado: {criptografada}")

    elif opcao == "2":
        mensagem = input("Digite a mensagem criptografada: ")
        chave = int(input("Digite a chave usada na criptografia: "))
        descriptografada = decifra_transposicao(mensagem, chave)
        print(f"\nDescriptografado: {descriptografada}")

    elif opcao == "3":
        mensagem = input("Digite a mensagem criptografada: ")
        forca_bruta(mensagem)

    elif opcao == "4":
        mensagem = input("Digite a mensagem criptografada: ")
        descriptografar_por_frequencia(mensagem)

    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
