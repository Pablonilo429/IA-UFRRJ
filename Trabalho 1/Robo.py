from tkinter import * # biblioteca para o uso de interfaces
from random import random, choice # biblioteca para definir de forma aleatoria os obstaculos e a direção
import heapq # biblioteca para o uso de fila de prioridades
import time

class Estado: # a classe Estado representa um estado do robô
    def __init__(self, pos, direcao, custo_acumulado, estado_anterior=None):
        # a posição, a direção, o custo acumulado e o estado anterior
        self.pos = pos
        self.direcao = direcao
        self.custo_acumulado = custo_acumulado
        self.estado_anterior = estado_anterior

    def __lt__(self, other): # implementa o método __lt__ para que os objetos Estado possam ser comparados com base no custo acumulado.
        return self.custo_acumulado < other.custo_acumulado

    def obter_posicao(self):
        return self.pos

    def obter_direcao(self):
        return self.direcao

    def obter_custo_acumulado(self):
        return self.custo_acumulado

    def obter_estado_anterior(self):
        return self.estado_anterior

class Tabuleiro: # a classe Tabuleiro é responsável por criar e controlar a interface gráfica do tabuleiro

    def __init__(self, janela):
        self.janela = janela
        self.tabuleiro = self.criar_tabuleiro()

    def criar_tabuleiro(self): #  cria uma matriz de quadrados que representam as células do tabuleiro.
        tabuleiro = [[None for _ in range(15)] for _ in range(15)]

        for i in range(15):
            for j in range(15):
                quadrado = Label(self.janela, width=2, height=1, relief="solid", bg="white")
                quadrado.grid(row=i, column=j, padx=2, pady=2)
                tabuleiro[i][j] = quadrado

                if random() < 0.3: # se o resultado da função random() for menor que 0.3, o quadrado é colorido de azul, criando os obstaculos
                    quadrado.config(bg="red")

        #definindo posição de inicio e final da matriz
        inicio = (0, 0)
        final = (14, 14)
        tabuleiro[inicio[0]][inicio[1]].config(bg="purple")
        tabuleiro[final[0]][final[1]].config(bg="orange")

        return tabuleiro

    def mostrar_caminho_vermelho(self, caminho):
        for posicao in caminho:
            x, y = posicao
            if self.obter_cor_quadrado(x, y) != "red":
                self.atualizar_quadrado(x, y, "yellow")
            janela.update()

    def atualizar_quadrado(self, x, y, cor):
        self.tabuleiro[x][y].config(bg=cor)

    def obter_cor_quadrado(self, x, y):
        return self.tabuleiro[x][y].cget("bg")

    def obter_heuristica(self, pos, final):
        x1, y1 = pos
        x2, y2 = final
        return abs(x1 - x2) + abs(y1 - y2)  # Distância de Manhattan

class Robo:
    def __init__(self, tabuleiro, inicio, final):
        self.tabuleiro = tabuleiro
        self.inicio = inicio
        self.final = final
        # norte, leste, noroeste, nordeste = revisar logica tá dando problema
        self.direcoes = ["Norte", "Leste", "Sul", "Oeste", "Noroeste", "Nordeste", "Sudoeste", "Sudeste"]
        self.direcao = choice(self.direcoes)
        self.posX = inicio[0]
        self.posY = inicio[1]
        self.custos_movimentos = {
            "ficar_parado": 1000,
            "girar_45": 1,
            "bater_obstaculo": 1000,
            "seguir_direcao_atual": 0
        }

        self.estado_tabuleiro = [[False for _ in range(15)] for _ in range(15)]

    # lógica para encontrar o caminho usando o algoritmo A*
    def encontrar_caminho_astar(self):

        x, y = self.posX, self.posY
        # movimentos possiveis
        movimentos = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        # matriz estados para armazenar os estados visitados durante a busca
        estados = [[None for _ in range(len(self.tabuleiro.tabuleiro[0]))] for _ in range(len(self.tabuleiro.tabuleiro))]
        print(self.direcao)

        # cria um objeto estado com informações da posição inicial, d
        # ireção, custo acumulado (0) e estado anterior (none)
        estado_inicial = Estado((x, y), self.direcao, 0, None)

        # inicializando toda matriz com none
        estados[x][y] = estado_inicial

        # lista de prioridade armazenando os estados que vão ser explorados,
        #  iniciando o estado inicial com prioridade 0
        heap = [(0, estado_inicial)]
        print(heap)

        while heap:
            # usa o _ pra ignorar o primeiro elemento da tupla,
            # logo apos remove e retorna o menor elemento da lista, com base nas prioridades definidas.
            _, estado_atual = heapq.heappop(heap)

            # extrai coordenadas atraves do metodo
            x, y = estado_atual.obter_posicao()

            # verifica se o estado é igual a posição final
            if estado_atual.obter_posicao() == self.final:
                caminho = []
                while estado_atual:
                    caminho.append(estado_atual.obter_posicao())
                    estado_atual = estado_atual.obter_estado_anterior()
                caminho.reverse()
                self.mostrar_caminho(caminho)
                break

            for movimento in movimentos:
                # somando o deslocamento do movimento atual ao x e y atuais.
                novo_x = x + movimento[0]
                novo_y = y + movimento[1]

                # verificamos se as novas coordenadas estão dentro dos limites do tabuleiro
                # e se o estado correspondente ainda não foi visitado
                if novo_x >= 0 and novo_x < len(self.tabuleiro.tabuleiro) and novo_y >= 0 and novo_y < len(self.tabuleiro.tabuleiro[0]) and estados[novo_x][novo_y] is None:

                    # se as coordenadas são válidas e o estado ainda não foi visitado, 
                    # atribuimos um custo de movimento com base no tipo de movimento e direção atual
                    if movimento == (0, 0):
                        custo_movimento = self.custos_movimentos["ficar_parado"]
                    elif movimento == (1, 0) and self.direcao == "Norte":
                        custo_movimento = self.custos_movimentos["seguir_direcao_atual"]
                    elif movimento == (0, 1) and self.direcao == "Leste":
                        custo_movimento = self.custos_movimentos["seguir_direcao_atual"]
                    elif movimento == (-1, 0) and self.direcao == "Sul":
                        custo_movimento = self.custos_movimentos["seguir_direcao_atual"]
                    elif movimento == (0, -1) and self.direcao == "Oeste":
                        custo_movimento = self.custos_movimentos["seguir_direcao_atual"]
                    elif movimento == (1, 1) and self.direcao == "Nordeste":
                        custo_movimento = self.custos_movimentos["seguir_direcao_atual"]
                    elif movimento == (-1, 1) and self.direcao == "Noroeste":
                        custo_movimento = self.custos_movimentos["seguir_direcao_atual"]
                    elif movimento == (1, -1) and self.direcao == "Sudeste":
                        custo_movimento = self.custos_movimentos["seguir_direcao_atual"]
                    elif movimento == (-1, -1) and self.direcao == "Sudoeste":
                        custo_movimento = self.custos_movimentos["seguir_direcao_atual"]
                    elif abs(movimento[0]) == abs(movimento[1]):

                        # verificando movimentos na diagonal
                        novo_x = x + movimento[0]
                        novo_y = y + movimento[1]

                        if self.tabuleiro.obter_cor_quadrado(novo_x, novo_y) == "red":
                            custo_movimento = self.custos_movimentos["bater_obstaculo"]
                        else:
                            custo_movimento = self.custos_movimentos["girar_45"]

                        # atualizando informações sobre o estado atual, isso vai permitir rastrear o caminho percorrido até o momento
                        novo_estado = Estado((novo_x, novo_y), self.direcao, estado_atual.obter_custo_acumulado() + custo_movimento, estado_atual)

                        #armazena na matriz estados e marca o novo estado como visitado
                        estados[novo_x][novo_y] = novo_estado

                        # adicionando o novo estado na fila de prioridade
                        # a prioridade é definida pela soma do custo acumulado até o momento 
                        # e a heurística estimada do novo estado até o destino final
                        heapq.heappush(heap, (novo_estado.obter_custo_acumulado() + self.tabuleiro.obter_heuristica(novo_estado.obter_posicao(), self.final), novo_estado))

                        #  as etapas vão ser realizados para cada nó vizinho válido, 
                        # permitindo que o algoritmo A* continue a busca pelo caminho mais curto até o destino final.

                    elif self.tabuleiro.obter_cor_quadrado(novo_x, novo_y) == "red":
                        continue

                    else:
                        custo_movimento = self.custos_movimentos["seguir_direcao_atual"]

                        # segue a mesma logica
                        novo_estado = Estado((novo_x, novo_y), self.direcao, estado_atual.obter_custo_acumulado() + custo_movimento, estado_atual)
                        estados[novo_x][novo_y] = novo_estado
                        heapq.heappush(heap, (novo_estado.obter_custo_acumulado() + self.tabuleiro.obter_heuristica(novo_estado.obter_posicao(), self.final), novo_estado))
        if caminho:
            self.tabuleiro.mostrar_caminho_vermelho(caminho)

        # corrigir, tá dando erro!
        if not caminho:
            self.tabuleiro.mostrar_caminho_vermelho(caminho)
            print("Não há uma saida possivel!")




    def busca_largura(self):
        # estado inicial
        x, y = self.posX, self.posY
        fila = [(x, y)]  # fila de estados para explorar
        visitados = set()  # conjunto de estados visitados

        while fila:
            x, y = fila.pop(0)  # pegar o primeiro estado na fila

            if (x, y) == self.final:
                # objetivo alcançado, retornar o caminho
                caminho = [(x, y)]

                #self.mostrar_caminho(caminho)
                while (x, y) != self.inicio:
                    x, y = self.estado_tabuleiro[x][y]
                    caminho.append((x, y))
                caminho.reverse()
                self.mostrar_caminho(caminho)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                novo_x, novo_y = x + dx, y + dy

                if 0 <= novo_x < 15 and 0 <= novo_y < 15 and self.tabuleiro.obter_cor_quadrado(novo_x,novo_y) != "red" and (novo_x, novo_y) not in visitados:

                    visitados.add((novo_x, novo_y))
                    self.estado_tabuleiro[novo_x][novo_y] = (x, y)  # armazenar o estado anterior para cada novo estado
                    fila.append((novo_x, novo_y))

            # objetivo não alcançável
        if caminho:
            self.tabuleiro.mostrar_caminho_vermelho(caminho)
        return None



    # atualiza a interface gráfica do tabuleiro para mostrar o caminho percorrido pelo robô
    def atualizar_interface(self, caminho):
        for posicao in caminho:
            x, y = posicao
            if self.tabuleiro.obter_cor_quadrado(x, y) != "red":
                self.tabuleiro.atualizar_quadrado(x, y, "purple")
            janela.update()
            time.sleep(0.3)

    # Mostra o caminho percorrido pelo robô no tabuleiro
    def mostrar_caminho(self, caminho):
        self.atualizar_interface(caminho)

# Código principal
janela = Tk()
janela.title("Trajeto de um Robô usando A*")    #Abre a janela mostrando o algoritmo A*
tabuleiro = Tabuleiro(janela)
robo = Robo(tabuleiro, (0, 0), (14, 14))
robo.encontrar_caminho_astar()
janela.mainloop()                               #Fechando a tela executa o proximo


janelaLarg = Tk()                               #Abre a janela mostrando o algoritmo A*
janelaLarg.title("Trajeto deBusca por Largura")
tabuleiroLarg = Tabuleiro(janelaLarg)
robo2 = Robo(tabuleiroLarg, (0, 0), (14, 14))
robo2.busca_largura()
janelaLarg.mainloop()