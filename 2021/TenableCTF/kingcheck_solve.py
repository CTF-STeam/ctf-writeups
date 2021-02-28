# STeam code

'''
Takes '+' and ' ' delimited data of chess matches and parses into list of seperate matches
''' 
def ParseMatches(chess_matches):
    return [c.split('+') for c in chess_matches.split(' ')]

'''
:param chess_match: A list of chess pieces and their location on the board. ie: ['w,p,a2', 'w,q,a6','w,k,c1','b,r,h1','b,k,g3']
:return: returns True or False if a King is in check
'''
def IsKingInCheck(chess_match):
    #print(chess_match)
    pieces = dict()
    wk_pos = None
    bk_pos = None
    for data in chess_match:
        color, rank, coord = data.split(',')
        #print(color, rank, coord)
        pieces[coord] = (color, rank)
        if rank == 'k':
            if color == 'w':
                wk_pos = coord
            else:
                bk_pos = coord
    #print(pieces)
    #print(to_int(wk_pos), bk_pos)
    if isInCheck('w', wk_pos, pieces):
        return True
    if isInCheck('b', bk_pos, pieces):
        return True
    return False

def enemyColor(color):
    if color == 'w':
        return 'b'
    else:
        return 'w'

def isInCheck(color, pos, pieces):
    eColor = enemyColor(color)
    cp = closest_w(pos, pieces)
    if cp is not None and cp[0] == eColor and cp[1] in ['q', 'r']:
        return True
    cp = closest_e(pos, pieces)
    if cp is not None and cp[0] == eColor and cp[1] in ['q', 'r']:
        return True
    cp = closest_n(pos, pieces)
    if cp is not None and cp[0] == eColor and cp[1] in ['q', 'r']:
        return True
    cp = closest_s(pos, pieces)
    if cp is not None and cp[0] == eColor and cp[1] in ['q', 'r']:
        return True
    cp = closest_ws(pos, pieces)
    if cp is not None and cp[0] == eColor and cp[1] in ['q', 'b']:
        return True
    cp = closest_wn(pos, pieces)
    if cp is not None and cp[0] == eColor and cp[1] in ['q', 'b']:
        return True
    cp = closest_en(pos, pieces)
    if cp is not None and cp[0] == eColor and cp[1] in ['q', 'b']:
        return True
    cp = closest_es(pos, pieces)
    if cp is not None and cp[0] == eColor and cp[1] in ['q', 'b']:
        return True
    kn_pos = get_knight_matepos(pos)
    for p in kn_pos:
        if p not in pieces:
            continue
        piece = pieces[p]
        if piece[0] == eColor and piece[1] == 'n':
            return True
    pn_pos = get_pawn_matepos(color, pos)
    for p in pn_pos:
        if p not in pieces:
            continue
        piece = pieces[p]
        if piece[0] == eColor and piece[1] == 'p':
            return True

def to_int(pos):
    return (ord(pos[0]) - ord('a'), ord(pos[1]) - ord('1'))

def to_char(pos):
    return chr(pos[0] + ord('a')) + chr(pos[1] + ord('1'))

def closest_w(pos, pieces):
    ipos = to_int(pos)
    for x in range(ipos[0] - 1, -1, -1):
        xpos = to_char((x, ipos[1]))
        if xpos in pieces:
            return pieces[xpos]
    return None

def closest_e(pos, pieces):
    ipos = to_int(pos)
    for x in range(ipos[0] + 1, 8):
        xpos = to_char((x, ipos[1]))
        if xpos in pieces:
            return pieces[xpos]
    return None

def closest_n(pos, pieces):
    ipos = to_int(pos)
    for y in range(ipos[1] - 1, -1, -1):
        ypos = to_char((ipos[0], y))
        if ypos in pieces:
            return pieces[ypos]
    return None

def closest_s(pos, pieces):
    ipos = to_int(pos)
    for y in range(ipos[1] + 1, 8):
        ypos = to_char((ipos[0], y))
        if ypos in pieces:
            return pieces[ypos]
    return None

def closest_ws(pos, pieces):
    ipos = to_int(pos)
    for i in range(1, ipos[1] + 1):
        npos = to_char((ipos[0] - i, ipos[1] - i))
        if npos in pieces:
            return pieces[npos]
    return None

def closest_wn(pos, pieces):
    ipos = to_int(pos)
    for i in range(1, 8 - ipos[1]):
        npos = to_char((ipos[0] - i, ipos[1] + i))
        if npos in pieces:
            return pieces[npos]
    return None

def closest_en(pos, pieces):
    ipos = to_int(pos)
    for i in range(1, 8 - ipos[1]):
        npos = to_char((ipos[0] + i, ipos[1] + i))
        if npos in pieces:
            return pieces[npos]
    return None

def closest_es(pos, pieces):
    ipos = to_int(pos)
    for i in range(1, ipos[1] + 1):
        npos = to_char((ipos[0] + i, ipos[1] - i))
        if npos in pieces:
            return pieces[npos]
    return None

def get_knight_matepos(pos):
    ipos = to_int(pos)
    return [to_char((ipos[0] - 2, ipos[1] - 1)), to_char((ipos[0] - 2, ipos[1] + 1)), to_char((ipos[0] + 2, ipos[1] - 1)), to_char((ipos[0] + 2, ipos[1] + 1)), to_char((ipos[0] - 1, ipos[1] - 2)), to_char((ipos[0] - 1, ipos[1] + 2)), to_char((ipos[0] + 1, ipos[1] - 2)), to_char((ipos[0] + 1, ipos[1] + 2))]

def get_pawn_matepos(color, pos):
    ipos = to_int(pos)
    if color == 'w':
        return [to_char((ipos[0] - 1, ipos[1] + 1)), to_char((ipos[0] + 1, ipos[1] + 1))]
    else:
        return [to_char((ipos[0] - 1, ipos[1] - 1)), to_char((ipos[0] + 1, ipos[1] - 1))]

# Parses chess matches from raw_input and calls "IsKingInCheck" for each match. Result is then printed
result = []
chess_matches = ParseMatches(raw_input())
#chess_matches = ParseMatches('w,p,c6+w,q,c8+w,p,g7+w,k,e5+b,b,b2+b,p,f3+b,k,f1 w,p,c4+w,r,a6+w,p,e6+w,p,h6+w,p,g7+w,k,h5+b,r,b2+b,p,f3+b,k,c2')
for chess_match in chess_matches:
    result.append(IsKingInCheck(chess_match))
    
print(result)
