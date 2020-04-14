import pygame
import pygame.time
import sys
import random
import numpy as np
from HandEvaluator import *

NAVY_BLUE = (0, 0, 128)
DARK_GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WIDTH = 1200
HEIGHT = 600
WINDOW_SIZE = (WIDTH,HEIGHT)

BIG_CARD_SIZE = (100, 140)
SMALL_CARD_SIZE = (60, 90)

POT = 0

RANKS = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
RANKING = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
VALUE_DICT = dict(zip(RANKS, RANKING))
SUITS = ["H", "S", "C", "D"]

class Deck:
    
    def __init__(self):
        self.ftr = []
        self.deck = []
        for suit in SUITS:
            for value in RANKS:
                self.deck.append(value + suit)
    
    def draw_card(self):
        return self.deck.pop()
    
    def shuffle(self):
        random.shuffle(self.deck)
        
        
class Player:
    
    def __init__(self, cards, betsize, balance, turn, sb, name):
        self.cards = cards
        self.betsize = betsize
        self.betplaced = betsize
        self.balance = balance
        self.turn = turn
        self.sb = sb
        self.taken_turn = False
        self.name = name
        
    def place_bet(self, betsize):
        self.betsize += betsize
        
    def confirm_bet(self):
        self.balance -= (self.betsize-self.betplaced)
        self.betplaced = self.betsize

    def opp_fold(self, pot):
        self.betsize = 0
        self.betplaced = 0
        self.balance += pot
        
    def change_turn(self):
        self.turn = not self.turn
        
    def clear_bet(self):
        self.betsize = 0
        self.betplaced = 0
        self.taken_turn = False
        

class Drawer:
    
    def __init__(self, screen):
        self.screen = screen
        
    def draw_all(self, ftr, currentPlayer, oppPlayer, blank, end):
        self.draw_table()
        self.draw_ftr(ftr)
        if blank:
            self.draw_blank_game()
        elif end:
            self.draw_front_player(currentPlayer, oppPlayer)
            self.draw_back_player(oppPlayer, True)
            self.draw_end_game(currentPlayer, oppPlayer)
        else:
            self.draw_front_player(currentPlayer, oppPlayer)
            self.draw_back_player(oppPlayer, False)
        pygame.display.update()
        
    def draw_table(self):
        self.screen.fill(NAVY_BLUE)
        pygame.draw.ellipse(self.screen, DARK_GREEN, (100, 100, 1000, 400))  # (x, y, width, height)
        pygame.draw.ellipse(self.screen, BLACK, (50, 50, 1100, 500), 100)
        pygame.draw.rect(self.screen, WHITE, (335, 220, 530, 160), 5)
        
    def draw_ftr(self, cards):  # Cards that will be displayed on table (flop, turn, river)
        for index, card in enumerate(cards):   
            image = pygame.image.load(card + ".png")
            image = pygame.transform.scale(image, BIG_CARD_SIZE)
            rect = image.get_rect().move((340+105*index, 230))
            self.screen.blit(image, rect)
        # Display pot value
        textsurface = myfont.render("POT: $" + str(POT), False, WHITE)
        self.screen.blit(textsurface, (340, 200))
              
    def draw_front_player(self, Player, oppPlayer):
        for index, card in enumerate(Player.cards):  # Cards of front Player
            image = pygame.image.load(card + ".png")
            image = pygame.transform.scale(image, SMALL_CARD_SIZE)
            rect = image.get_rect().move((560+20*index, 475))
            self.screen.blit(image, rect)
        # Balance of front facing player
        myfont = pygame.font.SysFont(None, 27)
        textsurface = myfont.render("$" + str(Player.balance), False, WHITE)
        self.screen.blit(textsurface, (545-SMALL_CARD_SIZE[0], 510)) 
        textsurface = myfont.render(Player.name, False, WHITE)
        self.screen.blit(textsurface, (565, 575))
        # Evaluate hand
        _, hand, result_front = eval_hand(Player.cards+deck.ftr)
        textsurface = myfont.render(result_front + ": " + str(hand), False, WHITE)
        self.screen.blit(textsurface, (340, 400))
        
        # Display bet size of opponent
        opp_bet = myfont.render("BET SIZE: " + str(oppPlayer.betplaced), False, WHITE)
        self.screen.blit(opp_bet, (550, 150))
        
        text_bet = myfont.render("BET: $" + str(Player.betsize), False, WHITE)
        self.screen.blit(text_bet, (580+SMALL_CARD_SIZE[0]+20, 510))
        # Increase bet button
        pygame.draw.rect(self.screen, WHITE, (750, 485, 25, 25))
        pygame.draw.rect(self.screen, BLACK, (750, 485, 25, 25), 1)
        text_plus = myfont.render("+", False, BLACK)
        self.screen.blit(text_plus, (758, 486))
        
        # Decrease bet button
        pygame.draw.rect(self.screen, WHITE, (750, 510, 25, 25))
        pygame.draw.rect(self.screen, BLACK, (750, 510, 25, 25), 1)
        text_min = myfont.render("-", False, BLACK)
        self.screen.blit(text_min, (760, 511))
        
        # Place bet button
        pygame.draw.rect(self.screen, GREEN, (660, 550, 75, 25))
        pygame.draw.rect(self.screen, BLACK, (660, 550, 75, 25), 1)
        text_min = myfont.render("Enter", False, BLACK)
        self.screen.blit(text_min, (665, 555))
        
        # Fold button
        pygame.draw.rect(self.screen, RED, (750, 550, 75, 25))
        pygame.draw.rect(self.screen, BLACK, (750, 550, 75, 25), 1)
        text_min = myfont.render("Fold", False, BLACK)
        self.screen.blit(text_min, (755, 555))

        
    def draw_back_player(self, Player, show_cards):
        for index, card in enumerate(Player.cards):  # Cards of back Player
            if show_cards:  # when we have to show cards at the end
                image = pygame.image.load(card + ".png")
            else:
                image = pygame.image.load("card_back.png")
            image = pygame.transform.scale(image, SMALL_CARD_SIZE)
            rect = image.get_rect().move((560+20*index, 35))
            self.screen.blit(image, rect)
        # Balance of back facing player        
        textsurface = myfont.render("$" + str(Player.balance), False, WHITE)
        self.screen.blit(textsurface, (580+SMALL_CARD_SIZE[0]+20, 70))
        textsurface = myfont.render(Player.name, False, WHITE)
        self.screen.blit(textsurface, (565, 10)) 
        
    def draw_blank_game(self):  # Used in between turns, hide all information
        for i in range(2):
            image = pygame.image.load("card_back.png")
            image = pygame.transform.scale(image, SMALL_CARD_SIZE)
            rect = image.get_rect().move((560+20*i, 35))
            self.screen.blit(image, rect)
            rect = image.get_rect().move((560+20*i, 475))
            self.screen.blit(image, rect)
        
    def draw_end_game(self, currentPlayer, oppPlayer):
        rank_front, res_front, text_front = eval_hand(currentPlayer.cards+deck.ftr)
        rank_back, res_back, text_back = eval_hand(oppPlayer.cards+deck.ftr)
        if rank_front > rank_back:
            text = currentPlayer.name + " wins $" + str(POT) + " with: " + text_front
            winner = "current"
        elif rank_back > rank_front:
            text = oppPlayer.name + " wins $" + str(POT) + " with: " + text_back
            winner = "opp"
        else:
            value1 = np.array([VALUE_DICT[card[:-1]] for card in res_front])
            value2 = np.array([VALUE_DICT[card[:-1]] for card in res_back])
            diff = value1 - value2
            try:
                if np.nonzero(diff)[0][0] > 0:
                    text = currentPlayer.name + " wins $" + str(POT) + " with: " + text_front
                    winner = "current"
                else:
                    text = oppPlayer.name + " wins $" + str(POT) + " with: " + text_back
                    winner = "opp"
            except:
                text = "Split pot"
                winner = "split"
        textsurface = myfont.render(text, False, WHITE)
        self.screen.blit(textsurface, (450, 200)) 
        
        _ = end_game(currentPlayer, oppPlayer, winner)
        
    def draw_bet_error(self):
        textsurface = myfont.render("Bet not equal to opponents bet!", False, WHITE)
        self.screen.blit(textsurface, (540, 430))
        pygame.display.update()


    
def end_game(currentPlayer, oppPlayer, winner):
    global POT, deck
    if winner == "current":
        currentPlayer.opp_fold(POT)
    elif winner == "opp":
        oppPlayer.opp_fold(POT)
    else:
        currentPlayer.opp_fold(POT/2)
        oppPlayer.opp_fold(POT/2)
    POT = 0
    deck = Deck()
    deck.shuffle()
    if Player1.sb:
        Player1.sb = False
        Player1.turn = False
        Player1.cards = [deck.draw_card() for i in range(2)]
        
        Player2.sb = True
        Player2.turn = True
        Player2.cards = [deck.draw_card() for i in range(2)]                    
    else:
        Player1.sb = True
        Player1.turn = True 
        Player1.cards = [deck.draw_card() for i in range(2)]
        
        Player2.sb = False
        Player2.turn = False
        Player2.cards = [deck.draw_card() for i in range(2)]   
    return deck
        
        
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE) 
pygame.display.set_caption("Poker")
myfont = pygame.font.SysFont(None, 27)
clock = pygame.time.Clock()     
    
deck = Deck()
deck.shuffle()
Player1 = Player([deck.draw_card() for i in range(2)], 0, 1000, True, True, "Player 1")
Player2 = Player([deck.draw_card() for i in range(2)], 0, 1000, False, False, "Player 2")

drawer = Drawer(screen)

space_pressed = 0
blank = False
end = False

while True:   
    if Player1.turn:
        currentPlayer = Player1
        oppPlayer = Player2
    else:
        currentPlayer = Player2
        oppPlayer = Player1  
    drawer.draw_all(deck.ftr, currentPlayer, oppPlayer, blank, end)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed += 1
                blank = True
            if event.key == pygame.K_SPACE and space_pressed > 1:
                currentPlayer.taken_turn = True
                if currentPlayer.betsize == oppPlayer.betplaced and oppPlayer.taken_turn:  # We draw cards
                    currentPlayer.clear_bet()
                    oppPlayer.clear_bet()
                    if not deck.ftr:  # We need to draw the flop
                        deck.ftr += [deck.draw_card() for i in range(3)]
                    elif len(deck.ftr) <= 4:  # Draw extra card
                        deck.ftr.append(deck.draw_card())
                    else:
                        drawer.draw_all(deck.ftr, currentPlayer, oppPlayer, False, True)
                        pygame.time.wait(3000)
                                            
                    if Player1.sb:
                        currentPlayer = Player1
                        oppPlayer = Player2    
                    else:
                        currentPlayer = Player2
                        oppPlayer = Player1
                    currentPlayer.turn = True
                    oppPlayer.turn = False
                else:
                    currentPlayer.change_turn()
                    oppPlayer.change_turn()
                space_pressed = 0
                blank = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            (pos_x, pos_y) = pygame.mouse.get_pos()
            # Increase bet button is pressed
            if pos_x >= 750 and pos_x <= 775 and pos_y >= 485 and pos_y <= 510:
                currentPlayer.place_bet(10)
            # Decrease bet button is pressed
            if pos_x >= 750 and pos_x <= 775 and pos_y >= 510 and pos_y <= 535:
                currentPlayer.place_bet(-10)
            # Enter button is pressed
            if pos_x >= 660 and pos_x <= 660+75 and pos_y >= 550 and pos_y <= 550+25:
                if currentPlayer.betsize >= oppPlayer.betplaced:
                    POT += (currentPlayer.betsize-currentPlayer.betplaced)
                    currentPlayer.confirm_bet()
                else:  # incorrect bet, it should be at least equal to opponents bet
                    drawer.draw_bet_error()
                    pygame.time.wait(3000)
            # Fold button is pressed
            if pos_x >= 750 and pos_x <= 750+75 and pos_y >= 550 and pos_y <= 550+25:
                deck = end_game(currentPlayer, oppPlayer, "opp")