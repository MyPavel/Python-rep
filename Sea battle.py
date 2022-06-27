# Исключения
class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Error! Out of the range"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Error! Already shot here"


class BoardWrongShipException(BoardException):
    pass


# Создание точки
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Dot: {self.x}, {self.y}"


# Создание корабля
class Ship:
    def __init__(self, head, l, o):
        self.head = head
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.head.x
            cur_y = self.head.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def hit(self, shot):
        return shot in self.dots


# Создание доски
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 0 | 1 | 2 | 3 | 4 | 5 |"
        for i, row in enumerate(self.field):
            res += f"\n{i} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # Добавление корабля
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    # Границы корабля
    def contour(self, ship, verb=False):
        border = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in border:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    # Выстрелы
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Ship destroyed!")
                    return False
                else:
                    print("Ship hit!")
                    return True

        self.field[d.x][d.y] = "."
        print("Miss!")
        return False

    def begin(self):
        self.busy = []


# Описание игрока

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Computer turn: {d.x + 1} {d.y + 1}")
        return d


# Тип игрока
class User(Player):
    def ask(self):
        while True:
            cords = input("Enter coordinates to shoot: ").split()

            if len(cords) != 2:
                print(" Enter two coordinates! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Enter numbers! ")
                continue

            x, y = int(x), int(y)

            return Dot(x, y)


# Алгоритм игры
from random import randint


class Game:
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    # Приветствие
    def greet(self):
        print("Welcome to Sea Battle game \n"
              "For shooting, please enter coordinates \n"
              "X-axis enter X \n"
              "Y-axis enter Y")

    # Основной цикл игры
    def loop(self):
        num = 0
        while True:
            print("///////////////////////////")
            print("Your Board:")
            print(self.us.board)
            print("///////////////////////////")
            print("AI Board:")
            print(self.ai.board)
            print("///////////////////////////")
            if num % 2 == 0:
                print("Your move!")
                repeat = self.us.move()
            else:
                print("AI move!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("Game over! \nCongratulation! You are win")
                print(self.ai.board)
                break

            if self.us.board.count == 7:
                print("Game over! \nAI win!")
                print(self.us.board)
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()