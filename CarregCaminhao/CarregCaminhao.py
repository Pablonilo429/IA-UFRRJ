import random
import time

# parâmetros do problema
capacidade_maxima = 50
num_itens = 10
# definição dos itens (peso e valor)
itens = [
    {'peso': 10, 'valor': 60},
    {'peso': 20, 'valor': 100},
    {'peso': 30, 'valor': 120},
    {'peso': 40, 'valor': 140},
    {'peso': 50, 'valor': 160},
    {'peso': 10, 'valor': 50},
    {'peso': 20, 'valor': 90},
    {'peso': 30, 'valor': 110},
    {'peso': 40, 'valor': 130},
    {'peso': 50, 'valor': 150}
]

# explicação
print("\nO Problema de Carregamento de Caminhão\n")
print("Neste problema, temos um caminhão com uma capacidade máxima \ne um conjunto de itens, cada um com um peso e um valor associado.\nO objetivo é selecionar um subconjunto de itens para serem carregados \nno caminhão, de forma a maximizar o valor total dos itens transportados,\nrespeitando a restrição de capacidade do caminhão.")

print("\nCapacidade máxima:", capacidade_maxima)
print("Os itens com seus respectivos pesos e valores:\n")
for i, item in enumerate(itens):
    print(f"Item {i+1}: Peso = {item['peso']}, Valor = {item['valor']}")

# algoritmo genético
tamanho_populacao = int(input("\nDigite o tamanho da população: "))
taxa_mutacao = 0.2
num_geracoes = int(input("Digite o número de gerações: "))

# tamanho do cromossomo (um gene para cada item)
tamanho_cromossomo = num_itens

# função de fitness: calcula o valor total do carregamento
def fitness(cromossomo):
    valor_total = 0
    peso_total = 0

    for i in range(num_itens):
        if cromossomo[i] == 1:
            valor_total += itens[i]['valor']
            peso_total += itens[i]['peso']

    if peso_total > capacidade_maxima:
        valor_total = 0  # penalidade se exceder a capacidade

    return valor_total

# função de geração aleatória de um individuo (cromossomo)
def gerar_individuo():
    return [random.randint(0, 1) for _ in range(tamanho_cromossomo)]

# função de crossover de dois indivíduos para produzir um filho
def crossover(individuo1, individuo2):
    ponto_corte = random.randint(1, tamanho_cromossomo - 1)
    filho = individuo1[:ponto_corte] + individuo2[ponto_corte:]
    return filho

# função de mutação de um individuo
def mutacao(individuo, taxa_mutacao):
    for i in range(tamanho_cromossomo):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]  # inverte o bit (0 -> 1 ou 1 -> 0)
    return individuo

# geração inicial da população
populacao = [gerar_individuo() for _ in range(tamanho_populacao)]

for geracao in range(num_geracoes):
    # avaliar a aptidão (fitness) de cada indivíduo
    aptidoes = [fitness(individuo) for individuo in populacao]

    # aeleção dos pais por torneio
    pais = []
    for _ in range(tamanho_populacao):
        competidores = random.sample(range(tamanho_populacao), 2)
        indice_pai = max(competidores, key=lambda x: aptidoes[x])
        pais.append(populacao[indice_pai])

    # cruzamento (crossover) e mutação
    nova_populacao = []
    for i in range(0, tamanho_populacao, 2):
        filho1 = crossover(pais[i], pais[i+1])
        filho2 = crossover(pais[i+1], pais[i])
        filho1 = mutacao(filho1, taxa_mutacao)
        filho2 = mutacao(filho2, taxa_mutacao)
        nova_populacao.extend([filho1, filho2])

    populacao = nova_populacao

    # melhor individuo da geração atual
    melhor_individuo = max(populacao, key=fitness)
    melhor_valor = fitness(melhor_individuo)

    # exibir resultados da geração atual
    print(f"Geração {geracao + 1}:")
    print("Melhor carregamento encontrado:")
    print("Itens selecionados:", [i for i in range(num_itens) if melhor_individuo[i] == 1])
    print("Valor total:", melhor_valor)
    print("-----------------------------")

# resultado final
print("\nAlgoritmo genético concluído.")
print("Melhor carregamento encontrado:")
print("Itens selecionados:", [i for i in range(num_itens) if melhor_individuo[i] == 1])
print("Valor total:", melhor_valor)

time.sleep(5)