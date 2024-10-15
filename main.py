import pyautogui
import time
import random
import threading
import keyboard
import json
import os

# Variável global para controle de execução
running = False
os.system('color 0B')

# Função para capturar pontos na tela ao pressionar uma tecla
def capture_points(num_points):
    points = []
    print(f"Para capturar um ponto, posicione o mouse e pressione 'Enter'. Total de pontos: {num_points}")
    
    for i in range(num_points):
        if i < 10:  # Primeiros 10 pontos (botões de 0 a 9)
            print(f"Posicione o mouse exatamente em cima do botão número {i} e pressione 'Enter'.")
        elif i == 10:
            print(f"Posicione o mouse no ACESSAR e pressione 'Enter'.")
        elif i == 11:
            print(f"Posicione o mouse no ENTENDI e pressione 'Enter'.")
        elif i == 12:
            print(f"Posicione o mouse no LIMPAR e pressione 'Enter'.")
        elif i == 13:
            print("Ponto 13 reservado para o botão de envio, mova o mouse para outro ponto.")
            continue
        else:
            print(f"Posicione o mouse no ponto {i + 1} e pressione 'Enter'.")
        
        # Espera o usuário pressionar 'Enter'
        keyboard.wait('enter')
        
        # Captura a posição do mouse
        x, y = pyautogui.position()
        points.append((i, x, y))

        print(points)
        print(f"Posição {i + 1} capturada: {x}, {y}")
    
    return points

# Função para carregar pontos de um arquivo
def load_points(filename="pontos.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            points = json.load(f)
        print(f"Pontos carregados do arquivo {filename}")
        return points
    else:
        print(f"Arquivo {filename} não encontrado!")
        return []

# Função para reordenar pontos aleatoriamente, exceto o ponto 13
import random

def reorder_points(points):
    if len(points) < 13:
        print("Número insuficiente de pontos para reordenar!")
        return points

    print("Reordenando os primeiros 10 pontos aleatoriamente (exceto os pontos 11, 12 e 13)")
    
    # Reordenar apenas os primeiros 10 pontos
    reorder = points[:10]  # Pegamos os primeiros 10 pontos
    random.shuffle(reorder)  # Reordenar aleatoriamente
    
    # Manter os pontos 11, 12 e 13 intactos
    reorder += points[10:13]  # Adicionar os pontos 11, 12 e 13 na ordem original
    
    # Adicionar o restante, caso haja mais pontos
    if len(points) > 13:
        reorder += points[13:]
    
    return reorder

# Função para salvar uma tentativa individualmente em tempo real
def save_attempt(attempt, filename="tentativas.txt"):
    with open(filename, 'a') as f:  # Usamos o modo 'a' para adicionar ao arquivo sem sobrescrever
        f.write(f"Tentativa: {attempt}\n")
    print(f"\nTentativa salva: {attempt}\n")

# Função para executar o auto clique
def auto_click(points, delay, click_speed, num_clicks, randomize, infinite_clicks, num_cycles):
    global running
    running = True
    cycle = 0

    while running:
       # Reordenar os primeiros 10 pontos no início de cada ciclo
        reordered_points = reorder_points(points)

        # Selecionar 8 pontos aleatórios dos primeiros 10, com repetição permitida
        random_8_points = random.choices(reordered_points[:10], k=8)

        # Manter os pontos 11, 12 e 13 sempre incluídos
        selected_points = random_8_points + reordered_points[10:13]

        # Criar a tentativa como uma string de valores `x` (segundo valor da tupla)
        attempt = ''.join(str(point[0]) for point in selected_points if point in reordered_points[:10])

        # Salvar a tentativa imediatamente
        save_attempt(attempt)  # Salvando após cada tentativa

        for i, point in enumerate(selected_points):
            if i == 13:  # Ponto 13 reservado, pular clique
                print("Ponto 13 é o botão de envio, não será clicado.")
                continue

            if randomize:
                x_offset = random.randint(-5, 5)
                y_offset = random.randint(-5, 5)
                pyautogui.moveTo(point[1] + x_offset, point[2] + y_offset, duration=click_speed)
            else:
                pyautogui.moveTo(point[1], point[2], duration=click_speed)

            for _ in range(num_clicks):  # Número de cliques por ponto
                pyautogui.click()
            time.sleep(delay)

        cycle += 1
        if not infinite_clicks and cycle >= num_cycles:
            break

    print("Encerrando Ciclos.")



# Função para parar o auto clicker
def stop_auto_click():
    global running
    running = False
    print("Auto clicker parado.")

# Menu de opções
def menu():
    print("\n--- MENU ---")
    print("1. Iniciar Auto-Clicker")
    print("2. Capturar Posições")
    print("3. Sair")

# Função principal
def main():
    global num_cycles
    points = []
    num_cycles = 2;
    while True:
        menu()
        choice = input("Escolha uma opção: ")

        if choice == '1':  # Iniciar Auto-Clicker
            if not points:
                print("Nenhuma posição capturada! Por favor, capture pontos antes de iniciar o auto-clicker.")
                continue

            # Tempo de atraso entre cliques
            delay = float(input("Digite o tempo de atraso entre cliques (segundos): "))

            # Velocidade dos cliques
            click_speed = float(input("Digite a velocidade do clique (segundos para mover): "))

            # Número de cliques por ponto
            num_clicks = int(input("Digite o número de cliques por ponto: "))

            # Ciclos infinitos ou finitos
            infinite_clicks = input("Deseja ciclos infinitos? (s/n): ").lower() == 's'
            if not infinite_clicks:
                num_cycles = int(input("Digite o número de ciclos de cliques: "))

            # Clique aleatório ao redor dos pontos
            randomize = 'n'

            # Iniciar o auto clicker em uma thread separada
            threading.Thread(target=auto_click, args=(points, delay, click_speed, num_clicks, randomize, infinite_clicks, num_cycles)).start()

            # Comando para parar o auto clicker
            input("Pressione Enter para parar o auto clicker...")
            stop_auto_click()

        elif choice == '2': 
             # Capturar Posições
            num_points = int(input("Número de botões clicáveis (13): "))
            if num_points > 13:
                num_points = 13
            
            points = capture_points(num_points)

            # Perguntar se deseja reordenar os pontos
            reorder_choice = input("Deseja que sejam em ordem aleatoria? (s/n): ").lower()
            if reorder_choice == 's':
                points = reorder_points(points)

        elif choice == '3':  # Sair
            confirm_exit = input("Tem certeza que deseja sair? (s/n): ").lower()
            if confirm_exit == 's':
                print("Saindo do programa.")
                break

        else:
            print("Opção inválida! Tente novamente.")

# Iniciar o programa
if __name__ == "__main__":
    main()