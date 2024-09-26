import random
import tkinter as tk
from tkinter import messagebox

# تعريف البطاقات والطرنيب
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']  # أنواع البطاقات
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # ترتيب البطاقات

# دالة لإنشاء مجموعة الورق
def create_deck():
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    return deck

# دالة لتوزيع الورق على اللاعبين
def deal_cards(deck):
    random.shuffle(deck)
    player1 = deck[:13]
    player2 = deck[13:26]
    player3 = deck[26:39]
    player4 = deck[39:]
    return player1, player2, player3, player4

# دالة لتحديد الطرنيب
def choose_tarneeb():
    return random.choice(suits)

# دالة لتحديد قوة البطاقة (للمقارنة بين البطاقات)
def card_value(card, tarneeb_suit):
    rank_order = ranks.index(card[0])
    if card[1] == tarneeb_suit:
        return rank_order + len(ranks)  # تعطي الطرنيب قيمة أعلى
    return rank_order

# دالة لتحديد الفائز بالجولة
def round_winner(cards_played, tarneeb_suit, lead_suit):
    winning_card = cards_played[0]
    for card in cards_played:
        if card[1] == winning_card[1]:  # نفس النوع
            if card_value(card, tarneeb_suit) > card_value(winning_card, tarneeb_suit):
                winning_card = card
        elif card[1] == tarneeb_suit:  # الطرنيب يتفوق
            winning_card = card
    return cards_played.index(winning_card)  # إرجاع الفائز (رقم اللاعب)

# واجهة الرسوميات
class TarneebGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("لعبة طرنيب")
        self.geometry("600x400")
        self.deck = create_deck()
        self.players = deal_cards(self.deck)
        self.tarneeb_suit = choose_tarneeb()
        self.scores = [0, 0]
        self.current_round = []
        self.lead_suit = None
        self.current_player = 0
        self.initialize_ui()

    def initialize_ui(self):
        self.info_label = tk.Label(self, text=f"الطرنيب هو: {self.tarneeb_suit}", font=("Arial", 16))
        self.info_label.pack(pady=10)

        self.cards_frame = tk.Frame(self)
        self.cards_frame.pack(pady=10)

        self.update_player_cards()

    def update_player_cards(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        player_cards = self.players[self.current_player]
        for card in player_cards:
            btn = tk.Button(self.cards_frame, text=f"{card[0]} of {card[1]}", command=lambda c=card: self.play_card(c))
            btn.pack(side="left", padx=5)

    def play_card(self, card):
        self.current_round.append(card)
        self.players[self.current_player].remove(card)

        if len(self.current_round) == 1:
            self.lead_suit = card[1]

        if len(self.current_round) == 4:
            self.end_round()
        else:
            self.current_player = (self.current_player + 1) % 4
            self.update_player_cards()

    def end_round(self):
        winner = round_winner(self.current_round, self.tarneeb_suit, self.lead_suit)
        self.current_player = (self.current_player + winner) % 4

        if self.current_player % 2 == 0:  # فريق 1 و 3
            self.scores[0] += 1
        else:  # فريق 2 و 4
            self.scores[1] += 1

        self.current_round = []
        self.lead_suit = None

        messagebox.showinfo("نتيجة الجولة", f"الفائز بالجولة: اللاعب {self.current_player + 1}\n"
                                             f"النقاط: فريق 1 و 3: {self.scores[0]} | فريق 2 و 4: {self.scores[1]}")

        self.update_player_cards()

# تشغيل اللعبة
if __name__ == "__main__":
    game = TarneebGame()
    game.mainloop()