import random
import copy


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True
        drop_counter = 0
        for row in state:
            for col in row:
                if col != ' ':
                    drop_counter += 1
        if drop_counter >= 8:
            drop_phase = False

        value_state = self.max_value(state, 3, drop_phase) # this returns list with state at [1]
        new_state = value_state[1]

        def find_moves(state, new_state, drop_phase):
            if drop_phase:
                for row_number in range(len(state)):
                    for col_number in range(len(state[row_number])):
                        if state[row_number][col_number] == ' ' and new_state[row_number][col_number] == self.my_piece: # if valid and correct piece
                            return [(row_number, col_number)]
            else:
                for row_number in range(len(state)):
                    for col_number in range(len(state[row_number])):
                        if state[row_number][col_number] == ' ' and new_state[row_number][col_number] == self.my_piece: # if valid and correct piece - row_number and col_number denote NEW placement
                            # check ORIGINAL placement has piece and NEW placement has ' '
                            # move up row - 1
                            if row_number != 0 and state[row_number - 1][col_number] == self.my_piece and new_state[row_number - 1][col_number] == ' ':
                                return [(row_number, col_number),(row_number - 1, col_number)]
                            # move down row + 1
                            elif row_number != 4 and state[row_number + 1][col_number] == self.my_piece and new_state[row_number + 1][col_number] == ' ':
                                return [(row_number, col_number),(row_number + 1, col_number)]
                            # move left col - 1
                            elif col_number != 0 and state[row_number][col_number - 1] == self.my_piece and new_state[row_number][col_number - 1] == ' ':
                                return [(row_number, col_number),(row_number, col_number - 1)]
                            # move right col + 1
                            elif col_number != 4 and state[row_number][col_number + 1] == self.my_piece and new_state[row_number][col_number + 1] == ' ':
                                return [(row_number, col_number),(row_number, col_number + 1)]
                            # move up left row - 1, col - 1
                            elif row_number != 0 and col_number != 0 and state[row_number - 1][col_number - 1] == self.my_piece and new_state[row_number - 1][col_number - 1] == ' ':
                                return [(row_number, col_number),(row_number - 1, col_number - 1)]
                            # move up right row - 1, col + 1
                            elif row_number != 0 and col_number != 4 and state[row_number - 1][col_number + 1] == self.my_piece and new_state[row_number - 1][col_number + 1] == ' ':
                                return [(row_number, col_number),(row_number - 1, col_number + 1)]
                            # move down left row + 1, col - 1
                            elif row_number != 4 and col_number != 0 and state[row_number + 1][col_number - 1] == self.my_piece and new_state[row_number + 1][col_number - 1] == ' ':
                                return [(row_number, col_number),(row_number + 1, col_number - 1)]
                            # move down right row + 1, col + 1
                            elif row_number != 4 and col_number != 4 and state[row_number + 1][col_number + 1] == self.my_piece and new_state[row_number + 1][col_number + 1] == ' ':
                                return [(row_number, col_number),(row_number + 1, col_number + 1)]

        move = find_moves(state, new_state, drop_phase)
        if move is None:
            successor = self.succ(state, drop_phase, False)[0]
            move = find_moves(state, successor, drop_phase)
        # TESTING
        # print(self.my_piece)
        # print(state)
        # print(new_state)
        # print(move)
        return move


    def succ(self, state, drop_phase, opponent):
        current_piece = self.opp if opponent else self.my_piece
        legal_successors = []
        if drop_phase:
            for row_num in range(len(state)):
                for col_num in range(len(state[row_num])):
                    if state[row_num][col_num] == ' ':
                        state_copy = copy.deepcopy(state)
                        state_copy[row_num][col_num] = current_piece
                        legal_successors.append(state_copy)
        else:
            for row_num in range(len(state)):
                for col_num in range(len(state[row_num])):
                    if state[row_num][col_num] == current_piece:
                        # move up, row-1
                        if row_num != 0 and state[row_num - 1][col_num] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row_num][col_num] = ' '
                            state_copy[row_num - 1][col_num] = current_piece
                            legal_successors.append(state_copy)
                        # move down, row+1
                        if row_num != 4 and state[row_num + 1][col_num] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row_num][col_num] = ' '
                            state_copy[row_num + 1][col_num] = current_piece
                            legal_successors.append(state_copy)
                        # move left, col-1
                        if col_num != 0 and state[row_num][col_num - 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row_num][col_num] = ' '
                            state_copy[row_num][col_num - 1] = current_piece
                            legal_successors.append(state_copy)
                        # move right, col+1
                        if col_num != 4 and state[row_num][col_num + 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row_num][col_num] = ' '
                            state_copy[row_num][col_num + 1] = current_piece
                            legal_successors.append(state_copy)
                        # move up left, (row-1,col-1)
                        if row_num != 0 and col_num != 0 and state[row_num - 1][col_num - 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row_num][col_num] = ' '
                            state_copy[row_num - 1][col_num - 1] = current_piece
                            legal_successors.append(state_copy)
                        # move up right, (row-1,col+1)
                        if row_num != 0 and col_num != 4 and state[row_num - 1][col_num + 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row_num][col_num] = ' '
                            state_copy[row_num - 1][col_num + 1] = current_piece
                            legal_successors.append(state_copy)
                        # move down left, (row+1,col-1)
                        if row_num != 4 and col_num != 0 and state[row_num + 1][col_num - 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row_num][col_num] = ' '
                            state_copy[row_num + 1][col_num - 1] = current_piece
                            legal_successors.append(state_copy)
                        # move down right, (row+1,col+1)
                        if row_num != 4 and col_num != 4 and state[row_num + 1][col_num + 1] == ' ':
                            state_copy = copy.deepcopy(state)
                            state_copy[row_num][col_num] = ' '
                            state_copy[row_num + 1][col_num + 1] = current_piece
                            legal_successors.append(state_copy)
        return legal_successors


    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)


    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece


    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")


    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == state[i + 3][j + 3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # check / diagonal wins
        for i in range(3,5):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i - 1][j + 1] == state[i - 2][j + 2] == state[i - 3][j + 3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j] == state[i][j + 1] == state[i + 1][j + 1]:
                    return 1 if state[i][j] == self.my_piece else -1

        return 0  # no winner yet


    def heuristic_game_value(self, state):  # if blank +3, if filled +5, if line not possible +0
        terminated = self.game_value(state)
        if terminated != 0:
            return terminated
        
        my_total = 0
        opp_total = 0

        for row in state:
            for i in range(2):
                my_potential = 0
                opp_potential = 0
                my_temp = 0
                opp_temp = 0
                if row[i] == self.my_piece:
                    if row[i + 1] == row[i]:
                        my_potential += 1
                        my_temp += 5
                    elif row[i + 1] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if row[i + 2] == row[i]:
                        my_potential += 1
                        my_temp += 5
                    elif row[i + 2] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if row[i + 3] == row[i]:
                        my_potential += 1
                        my_temp += 5
                    elif row[i + 3] == ' ':
                        my_potential += 1
                        my_temp += 3
                elif row[i] == self.opp:
                    if row[i + 1] == row[i]:
                        opp_potential += 1
                        opp_temp += 5
                    elif row[i + 1] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if row[i + 2] == row[i]:
                        opp_potential += 1
                        opp_temp += 5
                    elif row[i + 2] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if row[i + 3] == row[i]:
                        opp_potential += 1
                        opp_temp += 5
                    elif row[i + 3] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                if my_potential == 3:
                    my_total += my_temp
                if opp_potential == 3:
                    opp_total += opp_temp

        for col in range(5):
            for i in range(2):
                my_potential = 0
                opp_potential = 0
                my_temp = 0
                opp_temp = 0
                if state[i][col] == self.my_piece:
                    if state[i + 1][col] == state[i][col]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i + 1][col] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if state[i + 2][col] == state[i][col]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i + 2][col] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if state[i + 3][col] == state[i][col]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i + 3][col] == ' ':
                        my_potential += 1
                        my_temp += 3
                elif state[i][col] == self.opp:
                    if state[i + 1][col] == state[i][col]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i + 1][col] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if state[i + 2][col] == state[i][col]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i + 2][col] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if state[i + 3][col] == state[i][col]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i + 3][col] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                if my_potential == 3:
                    my_total += my_temp
                if opp_potential == 3:
                    opp_total += opp_temp

        for i in range(2):
            for j in range(2):
                my_potential = 0
                opp_potential = 0
                my_temp = 0
                opp_temp = 0
                if state[i][j] == self.my_piece:
                    if state[i + 1][j + 1] == state[i][j]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i + 1][j + 1] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if state[i + 2][j + 2] == state[i][j]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i + 2][j + 2] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if state[i + 3][j + 3] == state[i][j]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i + 3][j + 3] == ' ':
                        my_potential += 1
                        my_temp += 3
                elif state[i][j] == self.opp:
                    if state[i + 1][j + 1] == state[i][j]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i + 1][j + 1] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if state[i + 2][j + 2] == state[i][j]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i + 2][j + 2] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if state[i + 3][j + 3] == state[i][j]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i + 3][j + 3] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                if my_potential == 3:
                    my_total += my_temp
                if opp_potential == 3:
                    opp_total += opp_temp

        for i in range(3,5):
            for j in range(2):
                my_potential = 0
                opp_potential = 0
                my_temp = 0
                opp_temp = 0
                if state[i][j] == self.my_piece:
                    if state[i - 1][j + 1] == state[i][j]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i - 1][j + 1] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if state[i - 2][j + 2] == state[i][j]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i - 2][j + 2] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if state[i - 3][j + 3] == state[i][j]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i - 3][j + 3] == ' ':
                        my_potential += 1
                        my_temp += 3
                elif state[i][j] == self.opp:
                    if state[i - 1][j + 1] == state[i][j]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i - 1][j + 1] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if state[i - 2][j + 2] == state[i][j]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i - 2][j + 2] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if state[i - 3][j + 3] == state[i][j]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i - 3][j + 3] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                if my_potential == 3:
                    my_total += my_temp
                if opp_potential == 3:
                    opp_total += opp_temp

        for i in range(4):
            for j in range(4):
                my_potential = 0
                opp_potential = 0
                my_temp = 0
                opp_temp = 0
                if state[i][j] == self.my_piece:
                    if state[i + 1][j] == state[i][j]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i + 1][j] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if state[i][j + 1] == state[i][j]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i][j + 1] == ' ':
                        my_potential += 1
                        my_temp += 3
                    if state[i + 1][j + 1] == state[i][j]:
                        my_potential += 1
                        my_temp += 5
                    elif state[i + 1][j + 1] == ' ':
                        my_potential += 1
                        my_temp += 3
                elif state[i][j] == self.opp:
                    if state[i + 1][j] == state[i][j]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i + 1][j] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if state[i][j + 1] == state[i][j]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i][j + 1] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                    if state[i + 1][j + 1] == state[i][j]:
                        opp_potential += 1
                        opp_temp += 5
                    elif state[i + 1][j + 1] == ' ':
                        opp_potential += 1
                        opp_temp += 3
                if my_potential == 3:
                    my_total += my_temp
                if opp_potential == 3:
                    opp_total += opp_temp
        
        difference = my_total - opp_total
        if difference > 0:
            return my_total/(my_total + opp_total)
        elif difference < 0:
            return -opp_total/(my_total + opp_total)
        else:
            return 0


    def max_value(self, state, depth, drop_phase, minimax = True):
        terminated = self.game_value(state)
        if terminated != 0:
            return [terminated, state]
        elif depth == 0:
            return [self.heuristic_game_value(state), state]
        elif minimax is True:
            my_count = 0
            opp_count = 0
            for row in state:
                my_count += row.count(self.my_piece)
                opp_count += row.count(self.opp)
            opponent = False
            if my_count > opp_count:
                opponent = True
            successors = self.succ(state, drop_phase, opponent)
            recursive_values = []
            for successor in successors:
                recursive_values.append(self.max_value(successor, depth - 1, drop_phase, False))
            max_value = -2
            rec_value = None
            for recursive_value in recursive_values:
                value = recursive_value[0]
                if value > max_value:
                    max_value = value
                    rec_value = recursive_value
            index_rec = recursive_values.index(rec_value)
            return [recursive_values[index_rec][0], recursive_values[index_rec][1]] # recursive values = [value,state]
        else:
            successors = self.succ(state, drop_phase, True)
            recursive_values = []
            for successor in successors:
                recursive_values.append(self.max_value(successor, depth - 1, drop_phase, True))
            min_value = 2
            rec_value = None
            for recursive_value in recursive_values:
                value = recursive_value[0]
                if value < min_value:
                    min_value = value
                    rec_value = recursive_value
            index_rec = recursive_values.index(rec_value)
            return [recursive_values[index_rec][0], recursive_values[index_rec][1]] # recursive values = [value,state]


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
    # ai = TeekoPlayer()
    # print(ai.my_piece)
    # print("Test Initialize Game") # 3.239
    # ai.board = [[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "]]
    # ai.make_move(ai.board)
    # print("Test Drop Phase") # 1.631
    # ai.board = [[" ", "r", "b", " ", " "], [" ", " ", " ", "r", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", "b"]]
    # ai.make_move(ai.board)
    # print("Test After Drop Phase") # 1.177
    # ai.board = [[" ", "r", "b", " ", "b"], ["b", " ", " ", " ", " "], ["r", " ", " ", " ", "r"], [" ", " ", "b", " ", " "], ["r", " ", " ", " ", " "]]
    # ai.make_move(ai.board)