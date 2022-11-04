from jogos import *
from func_timeout import func_timeout, FunctionTimedOut

#Elementos do Grupo
#
#Nome: Santiago Benites
#
#Número: 54392
#
#Nome: João Ferreira
#
#Número: 55312
#
#Nome: Beatriz Rosa 
#
#Número: 55313

# -------------------------------------------- Classe Quadradinho --------------------------------------------

class Quadradinho:

    def __init__(self, pos, value):
        self.pos = pos
        self.val = value
        self.has_merged = False

    def copy(self):
        """ Cria uma copia do objeto e retorna-a. """
        return Quadradinho( tuple([self.pos[0], self.pos[1]]) , self.val)

# -------------------------------------------- /Classe Quadradinho --------------------------------------------

# -------------------------------------------- Classe Estado2048_29 --------------------------------------------

class Estado2048_29():

    def __init__(self, board, player, score):
        """Assume player = 'defensor' ou player = 'atacante' """
        self.board = board
        self.played = player
        self.score = score

    def get_tile(self, pos):
        return self.board[pos[0]][pos[1]]

    def copy(self):
        """ Cria uma copia do objeto e retorna-a. """
        return Estado2048_29([[t.copy() for t in self.board[y]] for y in range(4)], self.played, self.score)

    def tile_state(self, pos):
        """ Devolve: 
             -1 se a posicao for fora do board;
            0 se a posicao estiver vazia;
             1 se a posicao estiver ocupada"""
        
        r = 0
        x = pos[0]
        y = pos[1]

        if (x < 0 or y < 0 or x > 3 or y > 3):
            return -1
        
        if (self.board[x][y].val == 0):
            return 0
        
        if (not(self.board[x][y].val == 0)):
            return 1

    def gameOver(self,state):
        s = state.copy()
        movimentos = ["cima", "baixo", "esquerda", "direita"]
        r = []

        if s.played == 'defensor':
            r = [s.dir_action(mov) for mov in movimentos if s.dir_action(mov) != '']
        else:
            r = s.defense_action()

        return not bool(r)

    # ----------------- Funções Atacante -------------------------

    def ult_pos_disp(self, pos, vec):
        """ Devolve um tuplo com 2 posicoes na board, uma com a ultima tile desocupada numa direcao vec e outra com a seguinte"""
        c_pos = (pos[0], pos[1]) 
        prox = (c_pos[0] + vec[0], c_pos[1] + vec[1])

        while ((self.tile_state(prox) == 0) and (not (self.tile_state(prox) == 1))):
            c_pos = prox
            prox  = (c_pos[0] + vec[0], c_pos[1] + vec[1])

        return (c_pos, prox)

    def get_vector(self, dir):
        """ Devolve o vetor associado a uma direcao, no referencial da board,
            Assume dir = "cima", "baixo", "direita" e "esquerda" """
        return {
            'cima'    : (-1,  0),
            'baixo'   : ( 1,  0),
            'direita' : ( 0,  1),
            'esquerda': ( 0, -1),
        } [dir]

    def matrix_dir(self, vector):
        """ Cria uma matriz cujas 2 listas determinam a ordem pela qual o tabuleiro vai ser atravessado pelas funcoes actions e result. """
        r = [[x for x in range(4)] for y in range(2)]

        if (vector[0] == 1): r[0].reverse()
        if (vector[1] == 1): r[1].reverse()
    
        return r

    def dir_action(self, dir): # funcao de action direcional para atacante
        """ Retorna dir se a acao eh admissivel, senao retorna "".
            Assume dir = "cima", "baixo", "direita" e "esquerda" """
        
        v = self.get_vector(dir)
        t = self.matrix_dir(v)

        for x in t[0]:
            for y in t[1]:
                tile = self.board[x][y]
                if (not (tile.val == 0)):
                    mov = self.ult_pos_disp((x, y), v)
                    if (not (mov[0] == (x, y))):
                        return dir
                    if (self.tile_state(mov[1]) == 1):
                        nx = mov[1][0]
                        ny = mov[1][1]
                        if (tile.val == self.board[nx][ny].val):
                            return dir

        return ""

    def remove_merge_info(self):

        for lista in self.board:
            for tile in lista:
                tile.has_merged = False

    def dir_result(self, dir): # result para atacante
        
        nscore = 0

        s = self.copy()

        prevscore = s.score

        v = s.get_vector(dir)
        t = s.matrix_dir(v)

        s.remove_merge_info()

        for x in t[0]:
            for y in t[1]:

                tile = s.board[x][y]
                
                if (not (tile.val == 0)):
                    mov = s.ult_pos_disp((x, y), v)
                    prox = mov[1]

                    if ((s.tile_state(prox) == 1) and (s.board[prox[0]][prox[1]].val == tile.val) and (not s.board[prox[0]][prox[1]].has_merged)):
                        n_tile = Quadradinho(prox, tile.val * 2)
                        n_tile.has_merged = True
                        s.board[prox[0]][prox[1]] = n_tile
                        s.board[x][y] = Quadradinho((x, y) , 0)
                        nscore += n_tile.val

                    elif (s.tile_state(mov[0]) == 0):
                        nx = mov[0][0]
                        ny = mov[0][1]
                        tile.pos = (nx, ny)
                        s.board[nx][ny] = tile
                        s.board[x][y] = Quadradinho((x, y), 0)
        
        s.score = prevscore + nscore
        s.played = 'atacante'

        return s

    # ----------------- /Funções Atacante -------------------------

    # ----------------- Funções Defensor -------------------------

    def defense_action(self):
        """ Devolve uma lista de strigs do estilo "id_linha, id_coluna" 
            correspondente as coordenadas de cada celula vazia do board. """
        return [str(tile.pos[0]) + "," + str(tile.pos[1]) for tile in sum(self.board, []) if tile.val == 0]    

    def defense_result(self, position):
        """ Dada uma position "x, y" e um estado vamos colocar nessa certa posticao um 2 (position[0] == x e position[3] = y)"""
        # devemos copiar o board ou o estado?
        s = self.copy()
        pos = (int(position[0]), int(position[2]))
        s.board[pos[0]][pos[1]] = Quadradinho(pos, 2)
        s.played = 'defensor'
        return s

    # ----------------- /Funções Defensor -------------------------

    # ----------------- Funções Display -------------------------

    def board_to_string(self):
        """ Transforma uma matriz de tiles numa matrix de strings com o valor de cada tile. """
        board = self.board
        return [[str(tile.val) for tile in lista] for lista in board]

    def biggest_str(self):
        """ Devolve o tamanho da do maior numero da board. """
        int_list = [tile.val for tile in sum(self.board, [])]
        return len(str(max(int_list)))

    def display(self):
        """ Imprime no ecra uma representacao do board. """
        str_rep = self.board_to_string()
        size = self.biggest_str()


        division  = ('┣' + ('━'*(size - 1) + '━━━╋')*4)[:-1] + '┫'
        empty_row = ("┃ {} "*4) + "┃"

        middle = [] # stringbuilder-like aproach

        print(('┏' + ('━'*(size - 1) + '━━━┳')*4)[:-1] + '┓') # first line

        for x in range(4):
            #              espacos em branco se string for "0", caso contrario formata a string para ter o tamanho apropriado
            str_rep[x] = [(" " * size) if s == "0" else (" " * (size - len(s))) + s for s in str_rep[x]]

            middle.append(empty_row.format(*str_rep[x]))
            middle.append(division)

        middle.pop()
        print(*middle, sep='\n') #imprimir todas as linhas seguidas de newline

        print(('┗' + ('━'*(size - 1) + '━━━┻')*4)[:-1] + '┛') # last line

    # ----------------- /Funções Display -------------------------

    # ----------------- /Funções Auxiliares -------------------------

    


# -------------------------------------------- /Classe Estado2048_29 --------------------------------------------

# -------------------------------------------- Classe do Jogo --------------------------------------------

class Jogo2048_29(Game):

    # positions -> {(1,2), (3,4)}
    def __init__(self, positions):
        
        table =  [[Quadradinho((y, x), 0) for x in range(4)] for y in range(4)]

        for t in positions: 
            table[t[0]][t[1]] = Quadradinho((t[0], t[1]), 2)

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
        print("Atacante\n") if state.played == 'defensor' else print("Defensor\n")
        #print("\n")

    def to_move(self, state):
        r = ""
        if state.played == 'defensor': 
            r = "atacante"
        else: 
            r = "defensor"
        return r

# -------------------------------------------- /Classe do Jogo --------------------------------------------

# -------------------------------------------- Funções para executar jogos --------------------------------------------

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

def jogar_com_timeout(game, jogador1, jogador2, nsecs=1, verbose = True):
        """ Copia direta da funcao presente em jogos.py, no caso retorna o score final do jogo. """
        estado = game.initial
        if verbose :
            game.display(estado)

        
        fim = False
        timedout = False
        jogadores = (jogador1,jogador2)
        ind_proximo = 0
        
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
    
        return utilidade

# -------------------------------------------- /Funções para executar jogos --------------------------------------------

# -------------------------------------------- Funções Auxiliares --------------------------------------------

def maxValueInMatrix(state):
        """ Recebendo um objeto Estado2048_29 retorna o valor
            do maior tile no board. """
        valMatrix = [[tile.val for tile in lista] for lista in state.board]
        maxVal = max(sum(valMatrix,[]))
        return maxVal

def dist(p1, p2):
    """ Retorna distancia ao quadrado entre 2 pontos. 
        Assume p1 e p2 tuplos com x e y"""
    return ((p1[0] - p2[0]) * (p1[0] - p2[0])) + ((p1[1] - p2[1]) * (p1[1] - p2[1]))

# -------------------------------------------- /Funções Auxiliares --------------------------------------------

# ------------------------------------------------------ Jogadores ------------------------------------------------------

def jogador_hipolito_29(game, state):
    return alphabeta_cutoff_search_new(state, game, 3, eval_fn=eval_hipolito)

def gerador(eval):
    """ Recebe uma função de avaliação e retorna um jogador
        alphabeta_cutoff_search_new com profundidade 3 """
    def jogador(game, state):
        return alphabeta_cutoff_search_new(state, game, 3, eval_fn=eval)
    return jogador

def gerador_eval_combination(weights):
    """ Recebe um array que se assume ser composto por 4 números 
        e retorna uma função de avaliação aplicando esses pesos a
        4 heuristicas selecionadas. """
    def eval_combination_atack(state, player) :
        return eval_AllTypesOfSnakes(state,player) * weights[0] + eval_zeros_count(state,player) * weights[1] + -eval_smooth(state,player) * weights[2] + -eval_Monotonicity(state,player) * weights[3]
    return eval_combination_atack

# ------------------------------------------------------ /Jogadores ------------------------------------------------------

# -------------------------------------------- Funções de Avaliação --------------------------------------------

def eval_combination_atack(state,player):
    """ Combina Varias heuristicas"""
    return eval_AllTypesOfSnakes(state,player) + (eval_zeros_count(state,player) ** 2) + (eval_smooth(state,player)*0.89) - (eval_king_loneliness(state, player) * 0.85) + (eval_NoBigValInMiddle(state,player) * 5) + (eval_Monotonicity(state,player)*0.65)

def eval_hipolito(state, player):
    """ Retorna o score de uma dado estado"""
    return state.score if player == "atacante" else -state.score

def eval_n_possible_moves(state,jogador):
    """ Retorna a numero de jogadas possiveis. """
    s = state.copy()
    movimentos = ["cima", "baixo", "esquerda", "direita"]
    r = []
    r = [s.dir_action(mov) for mov in movimentos if s.dir_action(mov) != '']
    return len(r)

def eval_board_sum(state,jogador):
    """ Retorna a soma de todos os valores da board. """
    tempResult = [[ a.val for a in state.board[i] ] for i in range(3)]
    return (sum(sum(tempResult,[])))

def eval_snake(state, player):
    """ Retorna um metrica que relaciona os valores da board com a forma de uma cobrinha. """
    cobrinha = [[32768,16384,8192,4096],[256,512,1024,2048],[128,64,32,16],[1,2,4,8]]
    tempResult = [ [a*(b.val) for a,b in zip(cobrinha[i], state.board[i])] for i in range(3)]
    
    return (sum(sum(tempResult, [])))

def eval_AllTypesOfSnakes(state, player):
    """ Retorna uma metrica que correlaciona diretamente a 
        posição dos tiles de maior valor com um padrão em 
        cobra para todos os cantos. (evolução de snake)"""
        
    valueMaps = [ ([[32768,16384,8192,4096], [256,512,1024,2048], [128,64,32,16], [1,2,4,8]],(0,0)), #TopLeftSideways
                  ([[4096,8192,16384,32768], [2048,1024,512,256], [16,32,64,128], [8,4,2,1]],(3,0)), #TopRightSideways
                  ([[1,2,4,8], [128,64,32,16], [256,512,1024,2048], [32768,16384,8192,4096]],(0,3)), #BottomLeftSideways
                  ([[8,4,2,1], [16,32,64,128], [2048,1024,512,256], [4096,8192,16384,32768]],(3,3)), #BottomRightSideways
                  ([[32768,256,128,1], [16384,512,64,2], [8192,1024,32,4], [4096,2048,16,8]],(0,0)), #TopLeftVertical
                  ([[1,128,256,32768], [2,64,512,16384], [4,32,1024,8192], [8,16,2048,4096]],(3,0)), #TopRightVertical
                  ([[4096,2048,16,8], [8192,1024,32,4], [16384,512,64,2], [32768,256,128,1]],(0,3)), #BottomLeftVertical
                  ([[8,16,2048,4096], [4,32,1024,8192], [2,64,512,16384], [1,128,256,32768]],(3,3))  #BottomRightVertical
                ]

    m = maxValueInMatrix(state)
    valuesMapResults = []
    for x in valueMaps:
        tempResult = [[ a*(b.val) for a,b in zip(x[0][i],state.board[i]) ] for i in range(3)]
        valuesMapResults.append((sum(sum(tempResult,[]))) - pow((state.board[x[1][0]][x[1][1]].val != m)*abs(state.board[x[1][0]][x[1][1]].val - m), 2))
    
    return max(valuesMapResults)

def eval_zeros_count(state,jogador):
    """ Retorna o numero de tiles vazios. """
    count =0
    for x in range(4):
        for y in range(4):
            if state.board[x][y].val == 0:
                count+= 1
    return count

def eval_smooth(state, player):
    """ Retorna uma metrica diretamente proporcional a suavidade do board. """
    a = state.board
    t = [list(l) for l in zip(*a)]

    h = sum(a, [])
    v = sum(t, [])

    r = 0
    for x in range(len(h)-1):
        r += abs(h[x].val - h[x+1].val)
        r += abs(v[x].val - v[x+1].val)
    
    return r

def eval_otilopih(state, player):
    """ Retorna o simetrico do score atual. """
    return -state.score

def eval_king_loneliness(state, player):
    """ Retorna o simetrico do numero de espacos 
        vazios a volta do tile com maior valor. """
    maxVal = maxValueInMatrix(state)
    val = 0
    positions = [(0,1),(1,0),(-1,0),(0,-1)]
    for x in range(4):
        for y in range(4):
            if state.board[x][y].val == maxVal:
                for pos in positions:
                    if 0 < x + pos[0] < 3 and 0 < y + pos[1] < 3 and state.board[x + pos[0]][y + pos[1]].val == 0:
                        val = val + 1 
    return -val

def eval_BigValues_Edges(state, player):
    """ Avalia mais favoravelmente boards com 
        os maiores tiles nos cantos"""
    valMap = [(0,0), (0,3), (3,0), (3,3)]
    maxVal = maxValueInMatrix(state)

    for x in valMap:
        if maxVal == state.board[x[0]][x[1]]:
            return maxVal
    
    return 0

def eval_NoBigValInMiddle(state, player):
    """ Avalia desfavoravelmente boards com tiles grandes no meio"""
    valMap = [[0,0,0,0], [0,-4,-4,0], [0,-4,-4,0], [0,0,0,0]]
    tempResult = [[ a*(b.val) for a,b in zip(valMap[i],state.board[i]) ] for i in range(3)]

    return sum(sum(tempResult,[]))

def eval_Not_Random_Monte_Carlo(state,player):
    """ Devolve uma metrica que considera as futuras ações 
        do algoritmo e tenta maximizar o score dessa forma. """
    possibleMoves = ["cima", "baixo", "esquerda", "direita"]
    validFirstMoves = []
    validFirstMoves = [state.dir_action(mov) for mov in possibleMoves if state.dir_action(mov) != '']

    moveSimulationTotalScores = [0] * len(validFirstMoves)

    for move in validFirstMoves:
        simulationScore = 0
        if not(state.gameOver(state)):
            simulation = state.copy().dir_result(move)
            #jogada = ChoseNextMove(simulation,"atacante")
            #estado = simulation.defense_result(jogada)
            simulationScore = eval_SpeedHeuristic(simulation,"defensor")
        moveSimulationTotalScores[validFirstMoves.index(move)] = simulationScore
    if len(moveSimulationTotalScores) == 0:
        return 0
    else:
        return max(moveSimulationTotalScores) if player == "atacante" else -max(moveSimulationTotalScores)

# https://en.wikipedia.org/wiki/Occam%27s_razor
def ChoseNextMove(state,player):
    possibleMoves = state.defense_action()
    simScores = []
    for a in possibleMoves:
        simulation = state.defense_result(a)
        simScores.append(eval_hipolito(simulation,player))
    
    maxVal = min(simScores)
    return possibleMoves[simScores.index(maxVal)]

def eval_SpeedHeuristic(state, player):
    """ Combinação e optimização de todas as heuristicas uteis. """
    val = []
    maxVal = maxValueInMatrix(state)
    valueMaps = [ ([[32768,16384,8192,4096], [256,512,1024,2048], [128,64,32,16], [1,2,4,8]],(0,0)), #TopLeftSideways
                  ([[4096,8192,16384,32768], [2048,1024,512,256], [16,32,64,128], [8,4,2,1]],(3,0)), #TopRightSideways
                  ([[1,2,4,8], [128,64,32,16], [256,512,1024,2048], [32768,16384,8192,4096]],(0,3)), #BottomLeftSideways
                  ([[8,4,2,1], [16,32,64,128], [2048,1024,512,256], [4096,8192,16384,32768]],(3,3)), #BottomRightSideways
                  ([[32768,256,128,1], [16384,512,64,2], [8192,1024,32,4], [4096,2048,16,8]],(0,0)), #TopLeftVertical
                  ([[1,128,256,32768], [2,64,512,16384], [4,32,1024,8192], [8,16,2048,4096]],(3,0)), #TopRightVertical
                  ([[4096,2048,16,8], [8192,1024,32,4], [16384,512,64,2], [32768,256,128,1]],(0,3)), #BottomLeftVertical
                  ([[8,16,2048,4096], [4,32,1024,8192], [2,64,512,16384], [1,128,256,32768]],(3,3))  #BottomRightVertical
                ]

    #eval_AllTypesOfSnakes
    valuesMapResults = []

    for x in valueMaps:
        tempResult = [[ a*(b.val) for a,b in zip(x[0][i],state.board[i]) ] for i in range(4)]
        valuesMapResults.append((sum(sum(tempResult,[]))) - pow((state.board[x[1][0]][x[1][1]].val != maxVal)*abs(state.board[x[1][0]][x[1][1]].val - maxVal), 2))

    val.append(max(valuesMapResults))

    #Zeros
    zeroCount = 0
    smoothnessCount = 0
    monoCounter = 0
    #kingScore = 0
    a = state.board
    t = [list(l) for l in zip(*a)]

    h = sum(a, [])
    v = sum(t, [])

    for x in range(4):
        for y in range(4):
            smoothnessCount += abs(h[x].val - h[x+1].val)
            smoothnessCount += abs(v[x].val - v[x+1].val)

            if state.board[x][y].val == 0:
                zeroCount+= 1
            
            diffX = state.board[x][0].val - state.board[x][1].val
            for i in range(3):
                if (state.board[x][i].val - state.board[x][i+1].val) * diffX <= 0:
                        monoCounter += 1
            
            diffY = state.board[0][x].val - state.board[1][x].val
            for k in range(3):
                if (state.board[k][x].val - state.board[k + 1][x].val) * diffY <= 0:
                        monoCounter += 1
                
            #if state.board[x][y].val == maxVal:
            #    for pos in positions:
            #        if 0 < x + pos[0] < 3 and 0 < y + pos[1] < 3 and state.board[x + pos[0]][y + pos[1]].val == 0:
            #            kingScore = kingScore + 1 

    val.append(zeroCount ** 2 )
    val.append(smoothnessCount *0.89 )
    val.append(monoCounter)
    #val.append(-(kingScore * 0.85))

    return sum(val,0)

def eval_Monotonicity(state, player):
    """ Retorna uma metrica que representa a monotonicidade da board. """
    mono = 0

    row = 4
    col = 4
    for r in state.board:
        diff = r[0].val - r[1].val
        for i in range(col - 1):
            if (r[i].val - r[i + 1].val) * diff <= 0:
                mono += 1
            diff = r[i].val - r[i + 1].val

    for j in range(row):
        diff = state.board[0][j].val - state.board[1][j].val
        for k in range(col - 1):
            if (state.board[k][j].val - state.board[k + 1][j].val) * diff <= 0:
                mono += 1
            diff = state.board[k][j].val - state.board[k + 1][j].val

    return mono

# -------------------------------------------- /Funções de Avaliação --------------------------------------------

# -------------------------------------------- Funções de Avaliação para Ataque e Defesa --------------------------------------------

def func_defesa_29(state, player):
    """ Combinação de varias funções de avaliação 
    para obter a melhor defesa possivel"""
    return eval_otilopih(state, player) * 0.8 - eval_AllTypesOfSnakes(state, player) + eval_king_loneliness(state, player) * 0.05 - eval_smooth(state, player) * 0.05 - eval_Monotonicity(state, player) * 0.1 - (eval_NoBigValInMiddle(state,player) * 5)

def func_ataque_29(state, player):
    return eval_Not_Random_Monte_Carlo(state,player)

# -------------------------------------------- /Funções de Avaliação para Ataque e Defesa --------------------------------------------