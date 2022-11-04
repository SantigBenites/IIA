from IIA2122_proj2_29 import *
from timeit import default_timer as timer



a = {(random.randint(0,3),random.randint(0,3)),(random.randint(0,3),random.randint(0,3))}
while len(a) != 2:
    a = {(random.randint(0,3),random.randint(0,3)),(random.randint(0,3),random.randint(0,3))}

game = Jogo2048_29(a)

#start = timer()
#resultados = [jogar_com_timeout(game,jogador_atack, jogador_hipolito, verbose= False) for x in range(10)]
#print(resultados)
#print("jogador_defend vs jogador_hipolito Average is ->" + str(sum(resultados, 0)/10))
#end = timer()
#print("Total ElapsedTime " + str(end - start))


start = timer()
print(jogar_com_timeout(game,gerador(func_ataque_29), gerador(eval_hipolito),1, verbose= True))
end = timer()
print("Total ElapsedTime " + str(end - start))

#defenders = [jogador_hipolito,jogador_defend,jogador_obsessive_defense,random_player]
#atackers = [jogador_hipolito,jogador_atack,jogador_obsessive_attack,random_player]
#
#tournament = []
#
#f = open("tournament.txt", "a")
#start = timer()
#
#for defense in defenders:
#    for atack in atackers:
#        resultados = [game.jogar(atack, defense) for x in range(10)]
#        resultAverage = sum(resultados, 0)/10
#        tournament.append("defender -> " + str(defense.__name__) + " atacker-> " + str(atack.__name__) + " result-> " + str(resultAverage))
#
#end = timer()
#print(tournament)
#for item in tournament:
#    f.write(item + "\n")
#f.close()
#