import tkinter as tk
from tkinter import messagebox
import os

# Створення лог-файлу для запису ходів
log_file = "chess_log.txt"
if os.path.exists(log_file):
    os.remove(log_file)

def log_move(move):
    with open(log_file, "a") as file:
        file.write(move + "\n")

# Базовий клас для шахової фігури
class ChessPiece:
    def __init__(self, color):
        self.color = color

    def valid_moves(self, x, y, board):
        pass

class King(ChessPiece):
    def valid_moves(self, x, y, board):
        moves = [(x+dx, y+dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0]
        return [(nx, ny) for nx, ny in moves if 0 <= nx < 8 and 0 <= ny < 8]

class Queen(ChessPiece):
    def valid_moves(self, x, y, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    moves.append((nx, ny))
                    if board[nx][ny]:
                        break
                else:
                    break
        return moves

class Rook(ChessPiece):
    def valid_moves(self, x, y, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    moves.append((nx, ny))
                    if board[nx][ny]:
                        break
                else:
                    break
        return moves

class Bishop(ChessPiece):
    def valid_moves(self, x, y, board):
        moves = []
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    moves.append((nx, ny))
                    if board[nx][ny]:
                        break
                else:
                    break
        return moves

class Knight(ChessPiece):
    def valid_moves(self, x, y, board):
        moves = [(x+dx, y+dy) for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]]
        return [(nx, ny) for nx, ny in moves if 0 <= nx < 8 and 0 <= ny < 8]

class Pawn(ChessPiece):
    def valid_moves(self, x, y, board):
        moves = []
        direction = 1 if self.color == 'white' else -1
        if 0 <= x + direction < 8 and not board[x + direction][y]:
            moves.append((x + direction, y))
        if 0 <= x + direction < 8 and y - 1 >= 0 and board[x + direction][y - 1] and board[x + direction][y - 1].color != self.color:
            moves.append((x + direction, y - 1))
        if 0 <= x + direction < 8 and y + 1 < 8 and board[x + direction][y + 1] and board[x + direction][y + 1].color != self.color:
            moves.append((x + direction, y + 1))
        return moves

# Основний клас гри
class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Шахи на tkinter")
        self.board = [[None] * 8 for _ in range(8)]
        self.turn = "white"
        self.selected_piece = None
        self.selected_pos = None
        self.create_board()
        self.populate_board()

    def create_board(self):
        self.buttons = [[None] * 8 for _ in range(8)]
        for x in range(8):
            for y in range(8):
                color = 'white' if (x + y) % 2 == 0 else 'grey'
                btn = tk.Button(self.root, width=6, height=3, bg=color, command=lambda x=x, y=y: self.on_click(x, y))
                btn.grid(row=x, column=y)
                self.buttons[x][y] = btn

    def populate_board(self):
        for i in range(8):
            self.board[1][i] = Pawn("white")
            self.board[6][i] = Pawn("black")
        placements = [(Rook, 0), (Knight, 1), (Bishop, 2), (Queen, 3), (King, 4), (Bishop, 5), (Knight, 6), (Rook, 7)]
        for piece, i in placements:
            self.board[0][i] = piece("white")
            self.board[7][i] = piece("black")
        self.update_board()

    def update_board(self):
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                text = ""
                if piece:
                    text = f"{piece.__class__.__name__[0]}({piece.color[0]})"
                self.buttons[x][y]["text"] = text

    def on_click(self, x, y):
        if self.selected_piece:
            self.move_piece(x, y)
        else:
            piece = self.board[x][y]
            if piece and piece.color == self.turn:
                self.selected_piece = piece
                self.selected_pos = (x, y)
            else:
                messagebox.showerror("Помилка", "Виберіть коректну фігуру")
        self.update_board()

    def move_piece(self, x, y):
        px, py = self.selected_pos
        if (x, y) in self.selected_piece.valid_moves(px, py, self.board):
            log_move(f"{self.selected_piece.__class__.__name__} from ({px}, {py}) to ({x}, {y})")
            self.board[x][y] = self.selected_piece
            self.board[px][py] = None
            self.turn = "black" if self.turn == "white" else "white"
        else:
            messagebox.showerror("Помилка", "Некоректний хід")
        self.selected_piece = None
        self.selected_pos = None

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()
