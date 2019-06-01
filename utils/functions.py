import copy

from move import Move


def print_board(board):
    print("Showing board:")
    for row in board:
        print(row)
    print()


def transpose(board):
    return [[x] for x in zip(*board)]


# @staticmethod
# def flip_along_x_axis(board):
#     return board[::-1]


def has_empty_spot(list):
    return [x for sub in list for x in sub if not x]


def is_horizontally_winning(board):
    for row in board:
        for i in range(len(board)):
            tmp = set([x[i] if x != " " else x for x in row])
            if len(tmp) == 1 and tmp != {" "}:
                print("weszloooo")
                return True
    return False


def is_vertically_winning(board):
    is_horizontally_winning(transpose(board))


def is_diagonally_winning(board):
    length = len(board[0])
    diagonal1 = [board[i][i] for i in range(length)]
    diagonal2 = [board[length-i-1][i] for i in [x for x in range(length)]]
    for diagonal in [diagonal1, diagonal2]:
        for i in range(len(diagonal[0])):  # it's same as length, but these two mean sth else
            tmp = set([x[i] if x != " " else x for x in diagonal])
            if len(tmp) == 1 and tmp != {" "}:
                return True
    return False


def check_if_winning(board):
    if is_vertically_winning(board) or is_horizontally_winning(board) or is_diagonally_winning(board):
        return True
    return False


def find_difference_between_boards(board_x, board_y):
    for i in range(len(board_y)):
        for j in range(len(board_x[i])):
            if board_x[i][j] != board_y[i][j]:
                return i, j, [x for x in [board_x[i][j], board_y[i][j]] if x][0]


def minmax(root, last_picked_pawn, steps=[]):
    if not has_empty_spot(root.board):
        winning = check_if_winning(root.board)
        if winning and [x[1] for x in steps][0] == last_picked_pawn:
            print("Board")
            for row in root.board:
                print(row)
            print("IS WINNING!")
            print("WINNING STEPS")
            return steps
    for move in root.moves:
        i, j, pawn = find_difference_between_boards(root.board, move.board)
        position = ''.join([str(i), str(j)])
        # that's cheating, dunno if not totaly bad approach
        # otherwise last move is always last... which is weird
        return minmax(move, last_picked_pawn, [[position, pawn]]+steps)
    # return draw move


def recursive_combinations(pos, pawns, board, root):
    # import time
    if pawns:
        combs = [[x, y] for x in pos for y in pawns]
        # print(f"{len(combs)} combinations, {len(pos)} positions, {len(pawns)} pawns")
        for comb in combs:
            board_cpy = copy.deepcopy(board)
            pos_comb, pawn_comb = comb
            i, j = [int(x) for x in pos_comb]
            board_cpy[i][j] = pawn_comb
            rest_pos = [x for x in pos if x != pos_comb]
            rest_pawns = [x for x in pawns if x != pawn_comb]
            node = Move(copy.deepcopy(board_cpy), copy.deepcopy(rest_pos), copy.deepcopy(rest_pawns), root.level+1)
            root.add_move(node)
            # print()
            # print(f"root at level {root.level} added node on level {node.level}")
            # print(f"root has {len(root.moves)} moves already")
            recursive_combinations(copy.deepcopy(rest_pos), copy.deepcopy(rest_pawns), copy.deepcopy(board_cpy), node)
    # else:
    #     print("END of branch")
        ### return root