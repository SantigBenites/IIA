class Quadradinho:

    def __init__(self, pos, value):
        self.pos = pos
        self.val = value
        self.has_merged = False

    def copy(self):
        """ Cria uma copia do objeto e retorna-a. """
        return Quadradinho( tuple([self.pos[0], self.pos[1]]) , self.val)

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

def maxValueInMatrix(state):
    valMatrix = [[tile.val for tile in lista] for lista in state.board]
    maxVal = max(sum(valMatrix,[]))
    return maxVal