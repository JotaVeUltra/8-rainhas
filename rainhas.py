"""
Problema 8 Rainhas
•Solução utilizando um algoritmo evolucionário:
•Representação
•População inicial: 20 indivíduos
•Função de avaliação
•Seleção elitista: 10 indivíduos
•Recombinação (crossover): cut-and-crossfill
"""
from random import randint, shuffle


def cruzar(individuo_a, individuo_b, corte, mutação):
    filho_a = individuo_a[:corte] + crossover(individuo_a[:corte], individuo_b[:])
    filho_b = individuo_b[:corte] + crossover(individuo_b[:corte], individuo_a[:])
    if mutação:  # inserção
        mutar(filho_a)
        mutar(filho_b)
    return [filho_a, filho_b]


def crossover(corte_individuo_a, copia_individuo_b):
    for gene in corte_individuo_a:
        if gene in copia_individuo_b:
            copia_individuo_b.remove(gene)
    return copia_individuo_b


def mutar(filho):
    posição_1 = randint(0, 7)
    posição_2 = randint(0, 7)
    gene = filho.pop(posição_1)
    filho.insert(posição_2, gene)


def gerar_individuo(n):
    gene = list(range(n))
    shuffle(gene)
    return gene


def gerar_população(tamanho_população, n):
    return [gerar_individuo(n) for _ in range(tamanho_população)]


def avaliar_adaptação(individuo):
    colisões = 0
    for coluna_a, linha_a in enumerate(individuo):
        for linha_b in individuo[coluna_a + 1:]:
            delta_coluna = abs(coluna_a - individuo.index(linha_b))
            delta_linha = abs(linha_a - linha_b)
            if delta_coluna == delta_linha:
                colisões += 1
    return colisões


def calcular_media(população):
    return sum(avaliar_adaptação(individuo) for individuo in população) / len(população)


def executar_experimento(gerações, tamanho_população, taxa_mutação, elite, n):
    população = gerar_população(tamanho_população, n)
    # for geração in range(gerações):
    geração = 0
    while avaliar_adaptação(população[0]) > 0:
        if geração%1000 == 0:
            taxa_mutação += 1
            print(f'media da população na geração {geração}:  {calcular_media(população)}')
            print(f'taxa de mutação: {taxa_mutação}')
        geração += 1
        if geração%10_000 == 0:
            break
        shuffle(população)

        nova_população = []

        while len(população) > 0:
            mutação = randint(1, 100) <= taxa_mutação
            individuo_a = população.pop()
            individuo_b = população.pop()
            nova_população.append(individuo_a)
            nova_população.append(individuo_b)
            nova_população += cruzar(individuo_a, individuo_b, randint(2, len(individuo_a)-2), mutação)

        população = sorted(nova_população, key=avaliar_adaptação)[:elite]

    média = calcular_media(população)
    melhor_adaptado = população[0]
    return média, melhor_adaptado


########################################################################################################################


EXPERIMENTOS = [
    [5, 20, 10],
    [10, 40, 20],
    [15, 60, 30],
    [20, 80, 40],
    [25, 100, 50],
]
TAXA_MUTAÇÃO = 3  # %

for gerações, tamanho_população, elite in EXPERIMENTOS:
    resultados_experimento = executar_experimento(gerações, tamanho_população, TAXA_MUTAÇÃO, elite, 8)

    # print(f'gerações: {gerações}')
    print(f'tamanho da população: {tamanho_população}')
    print(f'taxa de mutação: {TAXA_MUTAÇÃO}')
    print(f'média da população: {resultados_experimento[0]}')
    print(f'fenótipo do individuo mais adaptado: {resultados_experimento[1]}')
    print(f'colisões: {avaliar_adaptação(resultados_experimento[1])}')
    print('-------------------------------------------------------------')
