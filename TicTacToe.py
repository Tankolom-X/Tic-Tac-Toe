import tkinter as tk
import sqlite3
from tkinter import messagebox


class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title('Tic Tac Toe')
        self.current_player = 'X'
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = []
        self.db_conn = sqlite3.connect(':memory:')
        self.create_table()
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(self.master, text='', font=('Arial', 30), width=3, height=1,
                                   command=lambda row=row, col=col: self.on_button_click(row, col))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)
        self.current_player_label = tk.Label(self.master, text='Current player: X', font=('Arial', 15))
        self.current_player_label.grid(row=4, column=0, columnspan=3)
        self.create_score_button()

    def create_table(self):
        self.db_conn.execute('''CREATE TABLE IF NOT EXISTS players (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                wins INTEGER)''')

    def create_score_button(self):
        score_button = tk.Button(self.master, text='Score', font=('Arial', 20),
                                 command=self.show_score)
        score_button.grid(row=3, column=0, columnspan=3, pady=10)

    def show_score(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''SELECT * FROM players ORDER BY wins DESC''')
        scores = cursor.fetchall()
        score_message = 'Score:\n'
        for score in scores:
            score_message += f'{score[1]}: {score[2]}\n'
        tk.messagebox.showinfo('Score', score_message)

    def on_button_click(self, row, col):
        if self.board[row][col]:
            return
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player)
        if self.check_winner():
            self.update_wins()
            self.show_winner()
        elif self.check_tie():
            self.show_tie()
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'

        self.current_player_label.config(text=f'Current player: {self.current_player}')

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
            return True
        return False

    def check_tie(self):
        for row in self.board:
            for col in row:
                if col is None:
                    return False
        return True

    def show_winner(self):
        tk.messagebox.showinfo('Game Over', f'{self.current_player} wins!')
        self.game_over()

    def show_tie(self):
        tk.messagebox.showinfo('Game Over', 'Tie!')
        self.game_over()

    def game_over(self):
        answer = tk.messagebox.askyesno('Game Over', 'Do you want to play again?')
        if answer:
            self.reset_game()
        else:
            self.master.destroy()

    def reset_game(self):
        if not self.current_player:
            self.current_player = 'X'
        self.board = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text='')

    def update_wins(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''SELECT * FROM players WHERE name=?''', (self.current_player,))
        player = cursor.fetchone()
        if player:
            cursor.execute('''UPDATE players SET wins = wins + 1 WHERE id=?''', (player[0],))
            self.db_conn.commit()
        else:
            cursor.execute('''INSERT INTO players (name, wins) VALUES (?, 1)''', (self.current_player,))
            self.db_conn.commit()


root = tk.Tk()
app = TicTacToe(root)
root.mainloop()