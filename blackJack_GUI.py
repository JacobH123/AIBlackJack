from PySide6.QtWidgets import (
     QWidget, QPushButton, QTextEdit, QVBoxLayout,
    QHBoxLayout, QMessageBox, QLabel
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
from utils import resource_path
#from blackJack_AI import *
from loadModel import *
import numpy as np
import random
import os





class BlackJackGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack AI Advisor")
        self.setStyleSheet("background-color: #0d1117; color: white;")
        self.setFixedSize(600, 600)

        self.deck = []
        self.player_hand = []
        self.dealer_card = None
        self.starting_money = 10000
        self.money = self.starting_money
        self.current_bet = 0
        self.money_active = False

        self.result_image_label = QLabel(self)
        self.result_text_label = QLabel(self)
        self.welcome_label = QLabel(self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.welcome_label.setText("Welcome to AI Blackjack")
        layout.addWidget(self.welcome_label)


        self.welcome_image = QLabel(self)
        self.welcome_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap("sprites/diamonds.jpg")
        scaled_pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.welcome_image.setPixmap(scaled_pixmap)
        layout.addWidget(self.welcome_image)

        self.result_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_text_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(self.result_text_label)
        self.result_text_label.hide()

        self.result_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_image_label)
        self.result_image_label.hide()

        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Segoe UI", 15))
        self.display.setStyleSheet("""
            QTextEdit {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        layout.addWidget(self.display)
        self.display.hide()

        self.hbox = QHBoxLayout()
        self.hit_button = QPushButton("Hit")
        self.stay_button = QPushButton("Stay")

        for btn in [self.hit_button, self.stay_button]:
            btn.setStyleSheet(self.button_style())
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(40)
            self.hbox.addWidget(btn)

        self.hit_button.clicked.connect(self.player_hit)
        self.stay_button.clicked.connect(self.player_stay)

        layout.addLayout(self.hbox)

        self.start_button_box = QHBoxLayout()

        self.start_button = QPushButton("Play")
        self.start_button.setStyleSheet(self.button_style(purple=True))
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.setFixedHeight(40)
        self.start_button_box.addWidget(self.start_button)

        self.playMoneyButton = QPushButton("Play With Money")
        self.playMoneyButton.setStyleSheet(self.button_style(purple=True))
        self.playMoneyButton.setCursor(Qt.PointingHandCursor)
        self.playMoneyButton.setFixedHeight(40)
        self.start_button_box.addWidget(self.playMoneyButton)

        layout.addLayout(self.start_button_box)

        # Continue/Quit buttons for money mode
        self.continue_quit_hbox = QHBoxLayout()
        self.continue_button = QPushButton("Continue")
        self.continue_button.setStyleSheet(self.button_style(purple=True))
        self.continue_button.setCursor(Qt.PointingHandCursor)
        self.continue_button.setFixedHeight(40)
        self.continue_button.hide()
        self.continue_quit_hbox.addWidget(self.continue_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.setStyleSheet(self.button_style(purple=True))
        self.quit_button.setCursor(Qt.PointingHandCursor)
        self.quit_button.setFixedHeight(40)
        self.quit_button.setFixedWidth(270)
        self.quit_button.hide()
        self.continue_quit_hbox.addWidget(self.quit_button)
        layout.addLayout(self.continue_quit_hbox)

        # Money layout
        self.money_layout = QVBoxLayout()
        self.money_buttons_layout = QHBoxLayout()

        self.money_buttons = []
        self.bet_options = [1000, 5000, 10000]
        for amount in self.bet_options:
            btn = QPushButton(f"${amount}")
            btn.setStyleSheet(self.button_style())
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(40)
            btn.clicked.connect(lambda _, a=amount: self.select_money(a))
            self.money_buttons.append(btn)
            self.money_buttons_layout.addWidget(btn)

        self.money_label = QLabel("Select Starting Money:")
        self.money_label.setStyleSheet("font-weight: bold;")
        self.money_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.money_layout.addWidget(self.money_label)
        self.money_layout.addLayout(self.money_buttons_layout)

        self.bet_button = QPushButton("Bet and Play")
        self.bet_button.setStyleSheet(self.button_style(purple=True))
        self.bet_button.setCursor(Qt.PointingHandCursor)
        self.bet_button.setFixedHeight(40)
        self.bet_button.clicked.connect(self.start_money_game)
        self.money_layout.addWidget(self.bet_button)

        self.money_layout_widget = QWidget()
        self.money_layout_widget.setLayout(self.money_layout)
        self.money_layout_widget.hide()
        layout.addWidget(self.money_layout_widget)


        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_game)
        self.playMoneyButton.clicked.connect(self.start_game_with_money)
        self.continue_button.clicked.connect(self.continue_money_game)
        self.quit_button.clicked.connect(self.quit_money_game)

        self.set_controls(False)
        self.show_action_buttons(False)

    def set_Image(self, image_path, size=(100, 100)):
        full_path = os.path.join(os.path.dirname(__file__), image_path)
        pixmap = QPixmap(full_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(size[0], size[1], Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.result_image_label.setPixmap(pixmap)
            self.result_image_label.show()

    def set_controls(self, enabled):
        self.hit_button.setEnabled(enabled)
        self.stay_button.setEnabled(enabled)

    def show_action_buttons(self, visible: bool):
        self.hit_button.setVisible(visible)
        self.stay_button.setVisible(visible)

    def select_money(self, amount):
        self.current_bet = amount
        self.money_label.setText(f"Selected Bet: ${amount}")

    def reset_game_state(self):
        full_deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
        random.shuffle(full_deck)

        self.player_hand = [full_deck.pop(), full_deck.pop()]
        self.dealer_card = full_deck.pop()
        self.deck = full_deck.copy()

        self.result_image_label.clear()
        self.result_image_label.hide()
        self.result_text_label.clear()
        self.result_text_label.hide()

        self.set_controls(True)
        self.show_action_buttons(True)
        self.update_display()

    def start_game_with_money(self):
        self.money_active = True
        self.money = self.starting_money
        self.current_bet = 0

        self.welcome_image.hide()
        self.display.show()
        self.display.setText(f"You have ${self.money}. Choose a bet amount and click 'Bet and Play'.")

        self.money_label.setText("Select Your Bet:")
        self.set_controls(False)
        self.show_action_buttons(False)
        self.result_image_label.clear()
        self.result_text_label.clear()
        self.result_image_label.hide()
        self.result_text_label.hide()

        self.player_hand = []
        self.dealer_card = None
        self.deck = []

        self.playMoneyButton.hide()
        self.start_button.hide()
        self.money_layout_widget.show()


    def start_money_game(self):
        if self.current_bet <= 0:
            QMessageBox.warning(self, "No Bet", "Please select a bet amount first.")
            return
        if self.money < self.current_bet:
            QMessageBox.warning(self, "Insufficient Funds", "Not enough money to place the bet.")
            return
        self.money_layout_widget.hide()
        self.money -= self.current_bet
        self.start_game()

    def start_game(self):
        self.welcome_image.hide()
        self.display.show()
        self.playMoneyButton.hide()
        self.welcome_label.hide()
        self.hide_continue_quit_buttons()

        self.reset_game_state()

        if self.money_active:
            self.start_button.hide()
        else:
            #self.start_button.setText("Restart Game")
            #self.start_button.show()
            self.start_button.hide()
            self.quit_button.show()

    def update_display(self):
        best_move, evs = recommend_best_move_model(self.player_hand, self.dealer_card)

        display_text = (
            f" Your hand: {self.player_hand} (Total: {hand_value_np(self.player_hand)})\n"
            f" Dealer shows: {self.dealer_card}\n\n"
            f" AI recommends: {best_move.upper()}\n"
            f"Expected Values:\n"
            f"   • Hit   → {evs['hit']:.3f}\n"
            f"   • Stand → {evs['stand']:.3f}"
        )
        if self.money_active:
            display_text += f"\n\n💰 Money remaining: ${self.money}"
        self.display.setText(display_text)



    def player_hit(self):
        if not self.deck:
            QMessageBox.warning(self, "Deck Empty", "No more cards.")
            return

        card = self.deck.pop()
        self.player_hand.append(card)

        if hand_value_np(self.player_hand) > 21:
            self.result_text_label.setText("YOU LOSE!")
            self.result_text_label.show()
            self.set_Image("sprites/catww1.png", size=(150, 150))
            self.set_controls(False)
            self.show_action_buttons(False)
            self.display.setText(
                f"You drew a {card} and busted! 💥\n\n"
                f"Your hand: {self.player_hand} (Total: {hand_value_np(self.player_hand)})"
            )
            if self.money_active:
                self.display.append(f"\n💰 Money remaining: ${self.money}")
               # self.money -= self.current_bet   //This was causing a bug
                self.show_continue_quit_buttons()
        else:
            self.update_display()

    def player_stay(self):
        dealer_hand = [self.dealer_card]
        while hand_value_np(dealer_hand) < 17 and self.deck:
            dealer_hand.append(self.deck.pop())

        p, d = hand_value_np(self.player_hand), hand_value_np(dealer_hand)
        result = "You lost." if d <= 21 and d > p else (
            "It's a tie." if d == p else "🎉 You win!")

        if result == "You lost.":
            self.result_text_label.setText("YOU LOSE!")
            self.set_Image("sprites/catww1.png", size=(150, 150))
            #if self.money_active:
              #  self.money = self.current_bet
        elif "win" in result.lower():
            self.result_text_label.setText("YOU WIN!")
            self.set_Image("sprites/mrFresh.png", size=(150, 150))
            if self.money_active:
                self.money += self.current_bet * 2
        else:
            self.result_text_label.setText("IT'S A TIE!")
            self.money += self.current_bet 
        self.result_text_label.show()
        self.set_controls(False)
        self.show_action_buttons(False)

        self.display.setText(
            f"Your hand: {self.player_hand} (Total: {p})\n\n"
            f"Dealer's hand: {dealer_hand} (Total: {d})\n"
            f"{result}"
        )
        if self.money_active:
            self.display.append(f"\n💰 Money remaining: ${self.money}")
            self.show_continue_quit_buttons()

    def button_style(self, purple=False):
        if purple:
            return """
                QPushButton {
                    background-color: #6a36bf;
                    color: white;
                    font-weight: bold;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #8457cf;
                }
            """
        return """
            QPushButton {
                background-color: #21262d;
                color: white;
                border: 1px solid #30363d;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #30363d;
            }
        """

    def show_continue_quit_buttons(self):
        self.start_button.hide()
        self.continue_button.show()
        self.quit_button.show()


    def hide_continue_quit_buttons(self):
        self.continue_button.hide()
        self.quit_button.hide()
        self.start_button.show()

    def continue_money_game(self):
        self.hide_continue_quit_buttons()
        self.start_button.hide()
        if self.money <= 0:
            QMessageBox.information(self, "Game Over", "You are out of money!")
            self.quit_money_game()
            return
        self.current_bet = 0
        self.money_label.setText("Select Your Bet:")
        self.display.setText(f"You have ${self.money}. Choose a bet amount and click 'Bet and Play'.")

        self.money_layout_widget.show()

    def quit_money_game(self):
        self.welcome_image.show()
        self.display.hide()
        #self.resize(500, 500)
        self.money_active = False
        self.money = self.starting_money
        self.current_bet = 0
        #self.hbox.hide()#added this to hide hit/stay
        self.hit_button.hide()
        self.stay_button.hide()
        self.hide_continue_quit_buttons()
        self.result_image_label.clear()
        self.result_image_label.hide()
        self.result_text_label.clear()
        self.result_text_label.hide()
        self.display.clear()
        self.welcome_label.show()
        self.start_button.setText("Play")
        self.playMoneyButton.show()
        self.money_layout_widget.hide()
        self.start_button.show()




