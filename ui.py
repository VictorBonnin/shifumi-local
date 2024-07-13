import tkinter as tk
from tkinter import simpledialog, Toplevel, Label, Button
import requests

class CustomDialog(Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")  # Définir la taille de la fenêtre
        self.resizable(False, False)
        
        label = Label(self, text=message, wraplength=350, justify="left", font=("Helvetica", 12))
        label.pack(pady=20)
        
        button = Button(self, text="OK", command=self.destroy, width=10, height=2)
        button.pack(pady=10)
        
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pierre-Feuille-Ciseaux")
        self.root.geometry("400x300")  # Définir la taille de la fenêtre

        self.player_id = simpledialog.askstring("Pseudo", "Entrez votre pseudo:")
        self.label = tk.Label(root, text=f"Joueur: {self.player_id}", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.choice_label = tk.Label(root, text="Choisissez votre option:", font=("Helvetica", 12))
        self.choice_label.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.rock_button = tk.Button(self.button_frame, text="Pierre", command=lambda: self.send_choice("rock"), width=10, height=2)
        self.rock_button.pack(side=tk.LEFT, padx=5)

        self.paper_button = tk.Button(self.button_frame, text="Feuille", command=lambda: self.send_choice("paper"), width=10, height=2)
        self.paper_button.pack(side=tk.LEFT, padx=5)

        self.scissors_button = tk.Button(self.button_frame, text="Ciseaux", command=lambda: self.send_choice("scissors"), width=10, height=2)
        self.scissors_button.pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=20)

        self.reset_button = tk.Button(root, text="Réinitialiser", command=self.reset_game, width=15, height=2)
        self.reset_button.pack(pady=10)

    def send_choice(self, choice):
        response = requests.post('http://localhost:5000/play', json={"player_id": self.player_id, "choice": choice})
        if response.status_code == 200:
            CustomDialog(self.root, "Info", response.json().get("message", ""))
        else:
            CustomDialog(self.root, "Error", response.json().get("message", ""))

        result_response = requests.get('http://localhost:5000/result')
        if result_response.status_code == 200:
            self.result_label.config(text=result_response.json().get("winner", ""))
        else:
            self.result_label.config(text="")

    def reset_game(self):
        response = requests.post('http://localhost:5000/reset')
        if response.status_code == 200:
            CustomDialog(self.root, "Info", "Le jeu a été réinitialisé.")
        else:
            CustomDialog(self.root, "Error", "Impossible de réinitialiser le jeu.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameUI(root)
    root.mainloop()