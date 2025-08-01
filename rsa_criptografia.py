import os
from math import gcd

# Codificação e decodificação
def encode_message(message):
    message = message.upper()
    alphabet = {chr(i + 65): i + 2 for i in range(26)}  
    alphabet[" "] = 28 
    return [alphabet[char] for char in message if char in alphabet]

def decode_message(codes):
    reverse_alphabet = {i + 2: chr(i + 65) for i in range(26)}
    reverse_alphabet[28] = " "
    return "".join(reverse_alphabet.get(code, "?") for code in codes)

# Funções matemáticas
def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def mod_inverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    raise Exception("Não foi possível encontrar inverso modular.")

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Geração de chaves
def gerar_chave_publica():
    p = int(input("Digite um número primo p: "))
    q = int(input("Digite um número primo q: "))

    if not is_prime(p) or not is_prime(q):
        print("Erro: p e q devem ser números primos.")
        return

    n = p * q
    phi = (p - 1) * (q - 1)

    e = int(input(f"Digite o expoente e (relativamente primo a {phi}): "))
    if gcd(e, phi) != 1:
        print("Erro: e não é relativamente primo a (p - 1)(q - 1).")
        return

    if n <= 28:
        print(f"Erro: n = {n} é muito pequeno. Deve ser maior que 28.")
        return

    # Salvar chave pública
    with open("chave_publica.txt", "w") as f:
        f.write(f"{e},{n}")
    print("✅ Chave pública salva em 'chave_publica.txt'")

    # Calcular chave privada 
    d = mod_inverse(e, phi)
    with open("chave_privada.txt", "w") as f:
        f.write(f"{d},{n}")
    print("🔐 Chave privada salva em 'chave_privada.txt'")
    print(f"Chave privada: d = {d}, n = {n}")

# Encriptação
def encriptar():
    mensagem = input("Digite a mensagem (A-Z e espaços): ")
    try:
        e, n = map(int, input("Digite a chave pública (formato: e,n): ").split(","))
    except ValueError:
        print("Erro: chave pública inválida.")
        return

    codigos = encode_message(mensagem)
    if any(c >= n for c in codigos):
        print(f"Erro: Algum caractere da mensagem tem valor >= n ({n}). Use um n maior.")
        return

    criptografada = [mod_exp(c, e, n) for c in codigos]
    with open("mensagem_encriptada.txt", "w") as f:
        f.write(",".join(map(str, criptografada)))
    print("✅ Mensagem encriptada salva em 'mensagem_encriptada.txt'")

# Desencriptação
def desencriptar():
    try:
        d, n = map(int, input("Digite a chave privada (formato: d,n): ").split(","))
    except ValueError:
        print("Erro: chave privada inválida.")
        return

    try:
        with open("mensagem_encriptada.txt", "r") as f:
            criptografada = list(map(int, f.read().strip().split(",")))
    except FileNotFoundError:
        print("Erro: Arquivo 'mensagem_encriptada.txt' não encontrado.")
        return

    decodificada = [mod_exp(c, d, n) for c in criptografada]
    mensagem = decode_message(decodificada)

    with open("mensagem_desencriptada.txt", "w") as f:
        f.write(mensagem)
    print("✅ Mensagem desencriptada salva em 'mensagem_desencriptada.txt'")
    print(f"📨 Mensagem original: {mensagem}")

# Menu principal
def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Gerar chave pública e privada")
        print("2 - Encriptar")
        print("3 - Desencriptar")
        print("4 - Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            gerar_chave_publica()
        elif opcao == "2":
            encriptar()
        elif opcao == "3":
            desencriptar()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

        voltar = input("\nDeseja voltar ao menu? (s/n): ").strip().lower()
        if voltar != "s":
            print("Encerrando o programa.")
            break

if __name__ == "__main__":
    menu()
