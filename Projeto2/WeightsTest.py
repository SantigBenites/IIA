from j2048 import *
from timeit import default_timer as timer
from random import randint, randrange

c_score = 0
c_weights = [random.randint(0,3),random.randint(0,3), random.randint(0,3), random.randint(0,3)] #comecar com valores sensiveis, hahahahha, são 4 da manhã metende os valores sensiveis no c* 
best_score = 0
changed_var = randint(0, 3)
change_inc = 0.05 # incrementos muito pequenos vao dar problema, mas muito grandes a mesma coisa...
change_dir = randrange(-1, 2, 2)
changed_last_val = c_weights[changed_var]
a = {(random.randint(0,3),random.randint(0,3)),(random.randint(0,3),random.randint(0,3))}
while len(a) != 2:
    a = {(random.randint(0,3),random.randint(0,3)),(random.randint(0,3),random.randint(0,3))}
game = Jogo2048_29(a)

for x in range(100000):

    if c_score > best_score:
        # se o score aumentou então continua a mudar a varivel na mesma direcao
        best_score = c_score
        changed_last_val = c_weights[changed_var]
        c_weights[changed_var] = c_weights[changed_var] + (change_inc * change_dir)
    else:
        #escolhe uma nova e tenta novamente (tambem reverte o falhanço anterior)
        c_weights[changed_var] = changed_last_val # reverter o falhanço

        changed_var = randint(0, 3) # encontrar nova variavel e nova dir
        change_dir = randrange(-1, 2, 2)

        changed_last_val = c_weights[changed_var] # future proofing

        c_weights[changed_var] = c_weights[changed_var] + (change_inc * change_dir) 

    funcao_avaliacao = gerador_eval_combination(c_weights)
    jog_gerado = gerador(funcao_avaliacao)

    resultados = [jogar_sem_timeout(game, jog_gerado, random_player, verbose=False) for y in range(5)]
    avrg = sum(resultados, 0)/5

    c_score = avrg

    f = open("resultados.txt", "a")
    f.write("Weights: " + str(c_weights) + " Score: " + str(avrg) + "\n")
    f.close()
    print("Teminou execução: " + str(x))