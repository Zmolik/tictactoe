from random import choice


class TicTacToe:

    def __init__(self):
        self.game = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        """
        0 1 2       (1, 3)(2, 3)(3, 3)
        3 4 5       (1, 2)(2, 2)(3, 2)
        6 7 8       (1, 1)(2, 1)(3, 1)
        """

    def has_player_won(self, player):
        if self.game[0] == player and self.game[1] == player and self.game[2] == player:
            return True
        if self.game[3] == player and self.game[4] == player and self.game[5] == player:
            return True
        if self.game[6] == player and self.game[7] == player and self.game[8] == player:
            return True
        if self.game[0] == player and self.game[3] == player and self.game[6] == player:
            return True
        if self.game[1] == player and self.game[4] == player and self.game[7] == player:
            return True
        if self.game[2] == player and self.game[5] == player and self.game[8] == player:
            return True
        if self.game[0] == player and self.game[4] == player and self.game[8] == player:
            return True
        if self.game[2] == player and self.game[4] == player and self.game[6] == player:
            return True

    def game_status(self):
        if self.has_player_won('X'):
            return 'X wins'
        if self.has_player_won('O'):
            return 'O wins'
        if ' ' not in self.game:
            return 'Draw'
        return False

    def print_game(self):
        print('---------')
        print(f'| {self.game[0]} {self.game[1]} {self.game[2]} |')
        print(f'| {self.game[3]} {self.game[4]} {self.game[5]} |')
        print(f'| {self.game[6]} {self.game[7]} {self.game[8]} |')
        print('---------')

    @staticmethod
    def convert_coordinates(coor):
        if coor[0] == '1' and coor[1] == '3':
            return 0
        if coor[0] == '2' and coor[1] == '3':
            return 1
        if coor[0] == '3' and coor[1] == '3':
            return 2
        if coor[0] == '1' and coor[1] == '2':
            return 3
        if coor[0] == '2' and coor[1] == '2':
            return 4
        if coor[0] == '3' and coor[1] == '2':
            return 5
        if coor[0] == '1' and coor[1] == '1':
            return 6
        if coor[0] == '2' and coor[1] == '1':
            return 7
        if coor[0] == '3' and coor[1] == '1':
            return 8

    def make_move(self, index, sign):
        if self.game[index] == 'X' or self.game[index] == 'O':
            print('This cell is occupied! Choose another one!')
            self.user_move(sign)
        else:
            self.game[index] = sign
            self.print_game()

    def user_move(self, sign):
        while True:
            coor = input('Enter the coordinates: > ').split()
            if len(coor) != 2:
                print('You should enter numbers!')
            elif not coor[0].isnumeric() or not coor[1].isnumeric():
                print('You should enter numbers!')
            elif not (1 <= int(coor[0]) <= 3) or not (1 <= int(coor[1]) <= 3):
                print('Coordinates should be from 1 to 3!')
            else:
                break
        self.make_move(self.convert_coordinates(coor), sign)

    def new_game(self):
        self.game = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.print_game()

    def ai_move_easy(self, sign):
        print('Making move level "easy"')
        empty_fields = self.find_empty_fields()
        self.make_move(choice(empty_fields), sign)

    def ai_move(self, difficulty, ai, human):
        if difficulty == 'easy':
            self.ai_move_easy(ai)
        elif difficulty == 'medium':
            self.ai_move_medium(ai)
        elif difficulty == 'hard':
            self.ai_move_hard(human, ai)

    def find_empty_fields(self):
        empty_fields = []
        for i, field in enumerate(self.game):
            if field == ' ':
                empty_fields.append(i)
        return empty_fields

    def ai_move_medium(self, sign):
        print('Making move level "medium"')
        empty_fields = self.find_empty_fields()
        for index in empty_fields:
            self.game[index] = sign
            if self.has_player_won(sign):
                self.print_game()
                return True
            else:
                self.game[index] = ' '
        signs = {'O', 'X'}
        signs.remove(sign)
        opponent_sign = signs.pop()
        for index in empty_fields:
            self.game[index] = opponent_sign
            if self.has_player_won(opponent_sign):
                self.game[index] = sign
                self.print_game()
                return True
            else:
                self.game[index] = ' '
        self.make_move(choice(empty_fields), sign)

    def minimax(self, player, human, ai):
        empty_fields = self.find_empty_fields()

        if self.has_player_won(human):
            return {'index': None, 'score': -10}
        elif self.has_player_won(ai):
            return {'index': None, 'score': 10}
        elif len(empty_fields) == 0:
            return {'index': None, 'score': 0}

        # an array to collect all the objects
        moves = []
        # loop through available spots
        for i in range(len(empty_fields)):
            # create an object for each and store the index of that spot
            move = dict()
            move['index'] = empty_fields[i]
            # set the empty spot to the current player
            self.game[empty_fields[i]] = player

            # collect the score resulted from calling minimax on the opponent of the current player
            if player == ai:
                result = self.minimax(human, human, ai)
                move['score'] = result['score']
            else:
                result = self.minimax(ai, human, ai)
                move['score'] = result['score']

            # reset the spot to empty
            self.game[empty_fields[i]] = ' '
            # push the object to the array
            moves.append(move)

        # if it is the computer's turn loop over the moves and choose the move with the highest score
        if player == ai:
            best_score = -10000
            for i in range(len(moves)):
                if moves[i]['score'] > best_score:
                    best_score = moves[i]['score']
                    best_move = i
        else:
            # else loop over the moves and choose the move with the lowest score
            best_score = 10000
            for i in range(len(moves)):
                if moves[i]['score'] < best_score:
                    best_score = moves[i]['score']
                    best_move = i
        # return the chosen move (object) from the moves array
        return moves[best_move]

    def ai_move_hard(self, human, ai):
        print('Making move level "hard"')
        empty_fields = self.find_empty_fields()
        if len(empty_fields) == 9:
            self.make_move(choice(empty_fields), ai)
        else:
            move = self.minimax(ai, human, ai)
            print(move)
            self.game[move['index']] = ai
            self.print_game()

    def main(self):
        user_input = input('Input command: > ').split()
        while user_input[0] != 'exit':
            if user_input[0] != 'start':
                print('Bad parameters!')
                user_input = input('Input command: > ').split()
                continue
            if user_input[1] == 'user' and user_input[2] in ('easy', 'medium', 'hard'):  # X = user, p O = AI
                self.new_game()
                while not self.game_status():
                    self.user_move('X')
                    if self.game_status():
                        break
                    self.ai_move(user_input[2], 'O', 'X')
                print(self.game_status(), '\n')
            elif user_input[2] == 'user' and user_input[1] in ('easy', 'medium', 'hard'):  # X = AI, O = user
                self.new_game()
                while not self.game_status():
                    self.ai_move(user_input[1], 'X', 'O')
                    if self.game_status():
                        break
                    self.user_move('O')
                print(self.game_status(), '\n')
            elif user_input[1] == 'user' and user_input[2] == 'user':  # X = user, O = user
                self.new_game()
                while not self.game_status():
                    self.user_move('X')
                    if self.game_status():
                        break
                    self.user_move('O')
                print(self.game_status(), '\n')
            else:
                print('Bad parameters!')
            user_input = input('Input command: > ').split()
        print('Bye!')


tictactoe = TicTacToe()
tictactoe.main()