import sys
import random
import json
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit

class SnakesGame(QWidget):

    def draw_board(self, qp):
        square_size = self.width() // self.board_size

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.game_board[x][y] == 1:
                    qp.setBrush(QColor(0, 255, 0))
                elif self.game_board[x][y] == 2:
                    qp.setBrush(QColor(255, 0, 0))
                else:
                    continue

                qp.drawRoundedRect(int(x * square_size), int(y * square_size), int(square_size), int(square_size), 2, 2)



    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_board(qp)
        qp.end()

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('Snakes Game')

        self.board_size = 20
        self.game_board = [[0 for x in range(self.board_size)] for y in range(self.board_size)]
        self.snake_length = 3
        self.snake = [(self.board_size//2, self.board_size//2 + i) for i in range(self.snake_length)]
        for (x, y) in self.snake:
            self.game_board[x][y] = 1
        self.food = self.generate_food()

        self.direction = 'right'
        self.score = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.move_snake)
        self.timer.start(100)

        self.update()
        self.show()


    def keyPressEvent(self, event):

        key = event.key()

        if key == Qt.Key_Left and self.direction != 'right':
            self.direction = 'left'
        elif key == Qt.Key_Right and self.direction != 'left':
            self.direction = 'right'
        elif key == Qt.Key_Up and self.direction != 'down':
            self.direction = 'up'
        elif key == Qt.Key_Down and self.direction != 'up':
            self.direction = 'down'
        elif key == Qt.Key_R:
            self.restart_game()

    def restart_game(self):
        self.close()
        self.__init__()

    def move_snake(self):
        head = self.snake[-1]
        x, y = head

        if self.direction == 'left':
            x -= 1
            if x < 0:
                x = self.board_size - 1
        elif self.direction == 'right':
            x += 1
            if x >= self.board_size:
                x = 0
        elif self.direction == 'up':
            y -= 1
            if y < 0:
                y = self.board_size - 1
        elif self.direction == 'down':
            y += 1
            if y >= self.board_size:
                y = 0

        if self.game_board[x][y] == 1:
            self.timer.stop()
            self.game_over()

        self.snake.append((x, y))
        if (x, y) == self.food:
            self.food = self.generate_food()
            self.score += 10
        else:
            self.game_board[self.snake[0][0]][self.snake[0][1]] = 0
            self.snake.pop(0)

        self.game_board[x][y] = 1

        self.update()


    def generate_food(self):

        while True:
            x = random.randint(0, self.board_size-1)
            y = random.randint(0, self.board_size-1)
            if self.game_board[x][y] == 0:
                self.game_board[x][y] = 2
                return (x, y)

    def game_over(self):
        self.timer.stop()
        self.score_label = QLabel(self)
        self.score_label.setText('Game Over! Your score is: {}. Press R to restart.'.format(self.score))
        self.score_label.setGeometry(0, 300, 200, 20)
        self.score_label.show()

        self.name_label = QLabel("Enter your name:", self)
        self.name_label.setGeometry(210, 300, 100, 20)
        self.name_label.show()

        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(320, 300, 200, 20)
        self.name_input.show()

        self.save_button = QPushButton("Save Score", self)
        self.save_button.setGeometry(530, 300, 100, 20)
        self.save_button.clicked.connect(self.save_score_and_display_leaderboard)
        self.save_button.show()

        self.restart_button = QPushButton("Restart Game", self)
        self.restart_button.setGeometry(530, 330, 100, 20)
        self.restart_button.clicked.connect(self.restart_game)
        self.restart_button.show()


    def save_score_and_display_leaderboard(self):
        name = self.name_input.text()
        if name:
            self.save_score(name, self.score)
            self.display_leaderboard()

    def display_leaderboard(self):
        scores = self.load_scores()

        leaderboard_label = QLabel(self)
        leaderboard_label.setText("Top 5 Scores:")
        leaderboard_label.setGeometry(0, 330, 200, 20)
        leaderboard_label.show()

        for i, score in enumerate(scores, start=1):
            score_label = QLabel(self)
            score_label.setText(f"{i}. {score['name']} - {score['score']}")
            score_label.setGeometry(0, 330 + 20 * i, 200, 20)
            score_label.show()

    def save_score(self, name, score):
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []

        scores.append({"name": name, "score": score})
        scores.sort(key=lambda x: x["score"], reverse=True)
        scores = scores[:5]

        with open("scores.json", "w") as file:
            json.dump(scores, file)

    def load_scores(self):
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []

        return scores

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SnakesGame()
    sys.exit(app.exec_())
