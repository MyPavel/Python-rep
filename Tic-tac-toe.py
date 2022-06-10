# Создание поля
def game_field(a):
    print('  0 1 2')
    for i in range(len(field)):
        print(str(i), *field[i])

# Ввод данных игроков
def player_input(a):
    while True:
        place = input('Enter two coordinates:').split()
        if len(place) != 2:
            print('Error! Enter two numbers')
            continue
        if not (place[0].isdigit() and place[1].isdigit()):
            print('Error! Enter only numbers')
            continue
        x, y = map(int, place)
        if not ((0 <= x < 3) and (0 <= y < 3)):
            print('Error! Enter number below 2')
            continue
        elif a[x][y] != '_':
            print('Error! The field is already filled')
        break
    return x, y

# Проверка условий победы
def win(a, player):
    def win_rate(a1, a2, a3, player):
        if a1 == player and a2 == player and a3 == player:
            return True
    if win_rate(a[0][0], a[0][1], a[0][2], player) or win_rate(a[0][1], a[1][1], a[2][1], player) or \
                win_rate(a[0][2], a[1][2], a[2][2], player) or win_rate(a[1][0], a[1][1], a[1][2], player) or \
                win_rate(a[2][0], a[2][1], a[2][2], player) or win_rate(a[0][0], a[1][0], a[2][0], player) or \
                win_rate(a[0][0], a[1][1], a[2][2], player) or win_rate(a[2][0], a[1][1], a[0][2], player):
            return True
    return False

# Ход игры
field = [['_'] * 3 for _ in range(3)]
count = 0
while True:
    if count == 9:
        print('Draw')
        break
    elif count % 2 == 0:
        player = 'x'
    else:
        player = 'o'
    game_field(field)
    x, y = player_input(field)
    field[x][y] = player
    if win(field, player):
        print('Player:', player, 'wins!')
        break
    count += 1