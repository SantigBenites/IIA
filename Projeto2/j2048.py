from jogos import *

from aux_classes import *
from players import *
from func_timeout import func_timeout, FunctionTimedOut
from timeit import default_timer as timer

class Jogo2048_29(Game):

    # positions -> {(1,2), (3,4)}
    def __init__(self, positions):
        
        table =  [[Quadradinho((y, x), 0) for x in range(4)] for y in range(4)]

        for t in positions: table[t[0]][t[1]] = Quadradinho((t[0], t[1]), 2)

        self.initial = Estado2048_29(table, 'defensor', 0)

    def actions(self, state):
        """ Retorna as possiveis acoes a tomar por um atacante ou defensor da seguinte forma:
            Atacantes: "cima", "baixo", "direita" e "esquerda", desde que válidas;
            Defensores: uma string "id_linha, id_coluna" correspondente às coordenadas de cada célula vazia."""
        
        s = state.copy()
        movimentos = ["cima", "baixo", "esquerda", "direita"]
        r = []

        if s.played == 'defensor':
            r = [s.dir_action(mov) for mov in movimentos if s.dir_action(mov) != '']
        else:
            r = s.defense_action()

        return r        

    
    def result(self, state, move):

        if state.played == 'defensor':
            return state.dir_result(move)
        else:
            return state.defense_result(move)
    
    def utility(self, state, player):
        return state.score

    def terminal_test(self, state):
        return not bool(self.actions(state))

    def display(self, state):
        print("Estado atual da board:")
        state.display()
        print("Score atual -> " + str(state.score))
        print("Proximo jogador -> ", end="")
        print("Atacante") if state.played == 'defensor' else print("Defensor")
        print("\n")

    def to_move(self, state):
        r = ""
        if state.played == 'defensor': 
            r = "atacante"
        else: 
            r = "defensor"
        return r


def jogar_sem_timeout(game, jogador1, jogador2, verbose = True):
        """ Copia direta da funcao presente em jogos.py, no caso retorna o score final do jogo. """
        estado = game.initial
        if verbose :
            game.display(estado)

        fim = False
        jogadores = (jogador1,jogador2)
        ind_proximo = 0
    
        while not fim :
            jogada = jogadores[ind_proximo](game,estado)
            estado = game.result(estado,jogada)
            if verbose :
                game.display(estado)
            fim = game.terminal_test(estado)
            ind_proximo = 1 - ind_proximo
               
        utilidade = game.utility(estado, game.to_move(game.initial))
    
        return utilidade

def jogar_com_timeout(game, jogador1, jogador2, verbose = True):
        """ Copia direta da funcao presente em jogos.py, no caso retorna o score final do jogo. """
        estado = game.initial
        if verbose :
            game.display(estado)

        
        fim = False
        timedout = False
        jogadores = (jogador1,jogador2)
        ind_proximo = 0
        nsecs = 1.5

        start = timer()
        while ((not timedout) and (not fim)):
            #start = timer()
            try:
                jogada = func_timeout(nsecs, jogadores[ind_proximo], (game, estado))
                estado = game.result(estado, jogada)
                fim = game.terminal_test(estado)
                if verbose :
                    game.display(estado)

            except FunctionTimedOut:
                print("O player " + game.to_move(estado) + " demorou muito tempo a decidir.")
                timedout = True

            ind_proximo = 1 - ind_proximo
            #end = timer()
            #print("ElapsedTime " + str(end - start))
               
        utilidade = game.utility(estado, game.to_move(game.initial))
        end = timer()
        print("ElapsedTime " + str(end - start))
    
        return utilidade