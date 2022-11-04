from jogos import *
from aux_classes import *

# ----------------- Players -------------------------

def jogador_atack(game, state) :
    return alphabeta_cutoff_search_new(state, game, 3, eval_fn=eval_Not_Random_Monte_Carlo)

def jogador_defend(game, state):
    return alphabeta_cutoff_search_new(state, game, 3, eval_fn=eval_combination_defend)

def jogador_hipolito(game, state):
    return alphabeta_cutoff_search_new(state, game, 3, eval_fn=eval_hipolito)

def gerador(eval):
    def jogador(game, state):
        return alphabeta_cutoff_search_new(state, game, 3, eval_fn=eval)
    return jogador

def gerador_eval_combination(weights):
    def eval_combination_atack(state, player) :
        return eval_AllTypesOfSnakes(state,player) * weights[0] + eval_zeros_count(state,player) * weights[1] + -eval_smooth(state,player) * weights[2] + -eval_Monotonicity(state,player) * weights[3]
    return eval_combination_atack

def jogador_obsessive_attack(jogo,estado):
    movimentos = ["cima", "esquerda", "direita", "baixo"]
    for mov in movimentos:
        if estado.dir_action(mov) != "" :
            return mov

def jogador_obsessive_defense(game, state):
    #assume que existem acoes disponiveis
    acoes_disp = game.actions(state) # lista do estilo ["l,c", "l,c"]

    #distancia = sqrt((0 - l)^2 + (0 - c)^2), ou, de forma proporcional (0 - l)^2 + (0 - c)^2 -> que vamos minimizar
    acao_escolhida = acoes_disp[0]
    c_dist = dist((0,0), (int(acao_escolhida[0]), int(acao_escolhida[2])))
    for acao in acoes_disp:
        if dist((0,0), (int(acao[0]), int(acao[2]))) < c_dist:
            c_dist = dist((0,0), (int(acao[0]), int(acao[2])))
            acao_escolhida = acao

    return acao_escolhida



# ----------------- Players -------------------------

# ----------------- Funções Players -------------------------

def eval_combination_atack(state,player):
    return eval_Not_Random_Monte_Carlo(state,player)
    #if maxValueInMatrix(state) < 1024:
    #    return eval_AllTypesOfSnakes(state,player) + (eval_zeros_count(state,player) ** 2) + (eval_smooth(state,player)*0.89) - (eval_king_loneliness(state, player) * 0.85) + (eval_NoBigValInMiddle(state,player) * 5) + (monotonicityCrime(state,player)*0.65)
    #else:
    #    return eval_Not_Random_Monte_Carlo(state,player)

def eval_combination_atack_MonteCarlo(state,player) :
    return eval_AllTypesOfSnakes(state,player) + (eval_zeros_count(state,player) ** 2) + (eval_smooth(state,player)*0.89) + (monotonicityCrime(state,player)*0.65)
    #return eval_AllTypesOfSnakes(state,player) + (eval_zeros_count(state,player) ** 2) + (eval_smooth(state,player)*0.89) - (eval_king_loneliness(state, player) * 0.85) + (eval_NoBigValInMiddle(state,player) * 5) + (monotonicityCrime(state,player)*0.65)

def eval_combination_atack_SquaredOccupied(state,player) :
    return eval_AllTypesOfSnakes(state,player) + (eval_zeros_count(state,player) ** 2)

def eval_combination_atack_StackOverFlow(state,player) :
    return eval_Monotonicity(state,player) + eval_smooth(state,player) + eval_n_possible_moves(state,player)
        
def eval_combination_defend(state,player) :
    return eval_otilopih(state,player) * 0.8 - eval_AllTypesOfSnakes(state,player) + eval_king_loneliness(state, player) * 0.05 - eval_smooth(state, player) * 0.05 - eval_Monotonicity(state, player) * 0.1 - (eval_NoBigValInMiddle(state,player) * 5)


def eval_SpeedHeuristic(state, player):

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


    





def eval_AllTypesOfSnakes(state, player):
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

def eval_BigValues_Edges(state, player):
    valMap = [(0,0), (0,3), (3,0), (3,3)]
    maxVal = maxValueInMatrix(state)

    for x in valMap:
        if maxVal == state.board[x[0]][x[1]]:
            return maxVal
    
    return 0

def eval_NoBigValInMiddle(state, player):
    valMap = [[0,0,0,0], [0,-4,-4,0], [0,-4,-4,0], [0,0,0,0]]
    tempResult = [[ a*(b.val) for a,b in zip(valMap[i],state.board[i]) ] for i in range(3)]

    return sum(sum(tempResult,[]))


def eval_zeros_count(state,jogador):
    """ Retorna o numero de espacos ocupados por tiles iguais a 0. """
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
    """ Retorna o numero de espacos vazios a volta do tile com maior valor. """
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

def eval_Monotonicity(state, player):
    """ Retorna a monotonicidade da board. """
    sum = 0
    for x in range(4):
        boolIsInOrder = True
        for y in range(4):
            if(y >= 1):
                boolIsInOrder = state.board[x][y-1].val < state.board[x][y].val and boolIsInOrder
        if boolIsInOrder == True:
            sum += 1

    for y in range(4):
        boolIsInOrder = True
        for x in range(4):
            if(x >= 1):
                boolIsInOrder = state.board[x-1][y].val < state.board[x][y].val and boolIsInOrder
        if boolIsInOrder == True:
            sum += 1

    for x in range(4):
        boolIsInOrder = True
        for y in range(4):
            if(y >= 1):
                boolIsInOrder = state.board[x][y-1].val < state.board[x-4][y].val and boolIsInOrder
        if boolIsInOrder == True:
            sum += 1

    for y in range(4):
        boolIsInOrder = True
        for x in range(4):
            if(x >= 1):
                boolIsInOrder = state.board[x-1][y].val < state.board[x-4][y-4].val and boolIsInOrder
        if boolIsInOrder == True:
            sum += 1

    return sum

def eval_hipolito(state, player):
    """ Retorna o score de uma dado estado"""
    return state.score if player == "atacante" else -state.score

def eval_Monte_Carlo(state,player):
    possibleMoves = ["cima", "baixo", "esquerda", "direita"]

    validFirstMoves = []
    validFirstMoves = [state.dir_action(mov) for mov in possibleMoves if state.dir_action(mov) != '']

    moveSimulationTotalScores = [0] * len(validFirstMoves)
    
    for move in validFirstMoves :
        simulationScore = 0
        for i in range(2) :
            simulation = state.copy()
            simulation.dir_result(move)
            depth = 0
            possibleMovesActions = [simulation.dir_action(mov) for mov in possibleMoves if simulation.dir_action(mov) != '']
            possibleMovesDefense = simulation.defense_action()
            while (not(simulation.gameOver(simulation)) and (depth < 2) and (len(possibleMovesActions)-1) > 0 and (len(possibleMovesDefense)-1)) > 0 :

                simulation = simulation.dir_result(possibleMovesActions[random.randint(0,len(possibleMovesActions)-1)])
                simulation.display()
                simulation = simulation.defense_result(possibleMovesDefense[random.randint(0,len(possibleMovesDefense)-1)])
                depth = depth + 1
                
                possibleMovesActions = [simulation.dir_action(mov) for mov in possibleMoves if simulation.dir_action(mov) != '']
                possibleMovesDefense = simulation.defense_action()
                simulationScore += state.score
            
        moveSimulationTotalScores[validFirstMoves.index(move)] = simulationScore

    
    if len(moveSimulationTotalScores) == 0:
        return 0
    else:
        return max(moveSimulationTotalScores) if player == "atacante" else -max(moveSimulationTotalScores)


def eval_Not_Random_Monte_Carlo(state,player):

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
        

# ----------------- /Funções Players -------------------------



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

def dist(p1, p2):
    """ Retorna distancia ao quadrado entre 2 pontos. 
        Assume p1 e p2 tuplos com x e y"""
    return ((p1[0] - p2[0]) * (p1[0] - p2[0])) + ((p1[1] - p2[1]) * (p1[1] - p2[1]))

# crime

def fitness(state,player):
        snakeVal = eval_AllTypesOfSnakes(state,player)

        m = maxValueInMatrix(state)
        return snakeVal - pow((state.board[3][0].val != m)*abs(state.board[3][0].val - m), 2)

def monotonicityCrime(state,player):
        """Monotonicity heuristic tries to ensure that the values of the tiles are all either increasing or decreasing along both the left/right and up/down directions"""
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