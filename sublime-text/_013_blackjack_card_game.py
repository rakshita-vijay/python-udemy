##### import random
import sys

suits = ("Diamonds", "Hearts", "Spades", "Clubs")
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', "Jack", "Queen", "King", "Ace")
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
# valid_suits = ("diamonds", "hearts", "spades", "clubs")
# valid_ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', "jack", "queen", "king", "ace")

class Card():  
    def __init__(self, rank, suit):    
        self.suit = (suit.lower()).capitalize() 
        self.rank = ((str(rank)).lower()).capitalize() # number 
        
        self.value = values[self.rank] 

    def __str__(self):
        return f"{self.rank} of {self.suit} with value: {self.value}"
        
    def tipe(self):
        l = []
        l.append(self.rank)
        l.append(self.suit) 
        l.append(self.value) 
        return tuple(l) 

class Deck():
    def __init__(self): 
        self.fullDeck = []
        for rank in ranks:
            for suit in suits: 
                self.fullDeck.append(Card(rank, suit)) 
        self.shuffle()

        self.dealtCards = [] 

    def display(self, ds = None):
        if ds is None:
            ds = self.fullDeck
        for i in ds:
            print(i)
    
    def shuffle(self): 
        random.shuffle(self.fullDeck) 

    def dealOneCard(self):
        if len(self.fullDeck) == 0:
            print("Deck exhausted. Reshuffling.") 
            # self.__init__()  # Resets and fills the deck again 
            for rank in ranks:
                for suit in suits: 
                    self.fullDeck.append(Card(rank, suit)) 
            self.shuffle()

        item = self.fullDeck.pop()
        self.dealtCards.append(item)
        return self.dealtCards[-1] 
    
    # def dealCards(self, num = 1):
    #     if len(self.fullDeck) < num:
    #         print("Deck exhausted. Reshuffling.") 
    #         self.__init__()  # Resets and fills the deck again 

    #     s1 = []  
    #     siz1 = num 

    #     while (siz1 > 0):
    #         item = self.fullDeck.pop()
    #         s1.append(item) 
    #         siz1 -= 1 

    #     self.dealtCards = s1
    #     return self.dealtCards

class Dealer():
    def __init__(self, name): 
        self.name = name 
        self.dealersDeck = Deck() 
        self.dealersDealtCards = []

    def __str__(self):
        return (f"Table's dealer: {self.name}")

    def dealOneUpOneDown(self): 
        if len(self.dealersDeck.fullDeck) < 2:
            print("Deck exhausted. Reshuffling.") 
            self.dealersDeck = Deck()  # Resets and fills the deck again 

        lst = [] # [<up>, <down>]
        totVal = 0

        if len(self.dealersDeck.fullDeck) >= 2: 
            for _ in range(2):
                lst.append(self.dealersDeck.dealOneCard())
                totVal += lst[-1].value 
        print(f"Up card: {str(lst[0])}") 
        # print(f"Down card: {str(lst[1])}") 
        print(f"Total value: {totVal}") 

        self.dealersDealtCards.append(lst)
        return lst, totVal

class BankRoll():
    def __init__(self, balance): 
        self.balance = balance 
    def deposit(self, amount):
        self.balance += amount
        return f"${amount} deposited into account. Balance: ${self.balance}"

    def withdraw(self, amount):
        if self.balance < amount:
            return f"Too less funds to withdraw - balance: ${self.balance}"
        else:
            self.balance -= amount
            return f"${amount} withdrawn from account. Balance: ${self.balance}"
            
    def canWithdraw(self, amount):
        if self.balance < amount:
            print(f"Insufficient balance: ${self.balance}")
            return False
        else: 
            return True

class Player(BankRoll):
    def __init__(self, name, balance): 
        BankRoll.__init__(self, balance)
        self.name = name 
        self.bets = []
        self.hand = []

    def __str__(self):
        return (f"Player {self.name} has {self.balance} in his account")

    def display(self, ds = None):
        if ds is None:
            ds = self.hand
        for i in ds:
            print(i)

    def addCard(self, cardsToAdd):  
        if type(cardsToAdd) == list:
            self.hand.extend(cardsToAdd) 
        elif (type(cardsToAdd) == type(Card('4', 'Diamonds'))):
            self.hand.append(cardsToAdd) 
        return
        # return self.display(self.hand)

    def removeCard(self, num = 1):
        removedCards = []
        while (num > 0 and len(self.hand) > 0):
            removedCards.append(self.hand.pop(0))
            num -= 1 
        if len(removedCards) == 1:
            return removedCards[0]
        else: 
            return removedCards

    def dealTwoUp(self, deeler): 
        if len(deeler.dealersDeck.fullDeck) < 2:
            print("Deck exhausted. Reshuffling.") 
            deeler.dealersDeck = Deck()  # Resets and fills the deck again 

        lst = [] # [<up>, <up>]
        totVal = 0
        if len(deeler.dealersDeck.fullDeck) >= 2: 
            for _ in range(2):
                lst.append(deeler.dealersDeck.dealOneCard())
                totVal += lst[-1].value 
                
        print(f"1st card: {str(lst[0])}") 
        print(f"2nd card: {str(lst[1])}")
        print(f"Total value: {totVal}")
        
        if totVal >= 21: 
            self.hand.extend(lst) 
            return lst, totVal

        listFromHitOrStay, valFromHitOrStay = self.hitOrStay(deeler, totVal)
        lst.extend(listFromHitOrStay)
        totVal += valFromHitOrStay

        self.hand.extend(lst) 
        return lst, totVal

    def placeBet(self, amt):
        if self.canWithdraw(amt) == True:
            self.withdraw(amt)
            self.bets.append(amt)
            print(f"You have bet ${amt}. Balance: {self.balance}")
            return True
        else: 
            print(f"You cannot bet ${amt}") 
            return False

    def hitOrStay(self, deeler, currTotal):
        cs = []
        valFromHOrS = 0
 
        while True:
            if currTotal + valFromHOrS >= 21: 
                break
            print()
            hOrS = input("Do you want to hit (receive another card) or stay (stop receiving cards)? Enter h or s: ") 

            if hOrS.lower() == "h":
                car = deeler.dealersDeck.dealOneCard()
                cs.append(car)
                valFromHOrS += car.value 
                
                print(f"Hit card: {str(car)}") 
                print(f"Value after hit card: {currTotal + valFromHOrS}") 
            elif hOrS.lower() == "s":
                print()
                print(f"Dealer {deeler.name}'s chance now:")
                break
            else:
                print("Invalid input.") 

        return cs, valFromHOrS 

def game_of_blackjack():
    name = input("Enter dealer's name: ")
    deeler = Dealer(name) 
    # deeler.dealersDeck.shuffle() 

    print() 
    minBet = 0 
    while True:
        try:
            minBet = int(input("Enter minimum bet at the table: "))
            if minBet < 500 or minBet > sys.maxsize:
                print(f"Please enter a number between 500 and {sys.maxsize}")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number:")
            
    print()
    name = input("Enter player's name: ")
    
    print()
    amt = minBet - 1
    while True:
        try:
            amt = int(input("Enter amount to deposit: "))
            if amt < minBet or amt > sys.maxsize:
                print(f"Please enter a number between {minBet} and {sys.maxsize}")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number:")

    print()
    player = Player(name, amt) 
    
    print(player)
    print(deeler)
    print()

    while player.balance > 0: 
        betToPlace = 0
        check = True
        while check:
            try:
                betToPlace = int(input("Enter bet to place: "))
                if betToPlace < minBet or betToPlace > sys.maxsize:
                    print(f"Please enter a number between {minBet} and {sys.maxsize}")
                else:
                    check = False
                    break
            except ValueError:
                print("Invalid input. Please enter a valid number:")
                
        print()
        whoWon = 'n'
        if player.placeBet(betToPlace) == True:
            cardsPlayerDealt, valOfPlayerDealtCards = player.dealTwoUp(deeler)  
            if valOfPlayerDealtCards == 21: 
                print(f"Player {player.name} won!") 
                player.balance += player.bets[-1]
                whoWon = 'p'
            elif valOfPlayerDealtCards > 21: 
                print(f"Player {player.name} busts!")
                whoWon = 'n' 
            else:
                cardsDealerDealt, valOfDealerDealtCards = deeler.dealOneUpOneDown()
                if valOfDealerDealtCards > valOfPlayerDealtCards:
                    print(f"Dealer {deeler.name} won!")
                    whoWon = 'p'
                else: 
                    while valOfDealerDealtCards <= valOfPlayerDealtCards or valOfDealerDealtCards < 17:
                        cardsDealerDealt.append(deeler.dealersDeck.dealOneCard())
                        valOfDealerDealtCards += cardsDealerDealt[-1].value
                        
                        print(f"Dealer {deeler.name} has dealt (for themself): {cardsDealerDealt[-1]}")
                        print(f"Total Value: {valOfDealerDealtCards}")
                        
                        if valOfDealerDealtCards > 21:
                            print(f"Dealer {deeler.name} busts!")
                            player.balance += player.bets[-1]
                            whoWon = 'p'
                    if valOfDealerDealtCards <= 21 and valOfDealerDealtCards > valOfPlayerDealtCards:
                        print(f"Dealer {deeler.name} won!") 
                        whoWon = 'p'
                        
            print()
            print(player)
            choiceToContinue = input("Do you want to continue playing? Enter yes (y) or no (n): ")
            while choiceToContinue.lower() != 'y' and choiceToContinue.lower() != 'n':
                choiceToContinue = input("Invalid choice. Do you want to continue playing? Enter yes (y) or no (n): ")
            
            print()
            if choiceToContinue.lower() == 'y': 
                # print(player)
                if player.balance == 0 or player.balance < minBet:
                    choiceToDeposit = input(f"Your current balance is {player.balance}. You have to deposit amount to continue playing. Do you want to? Enter yes (y) or no (n): ")
                    while choiceToDeposit.lower() != 'y' and choiceToDeposit.lower() != 'n':
                        choiceToDeposit = input("Invalid choice. Do you want to deposit amount to continue playing? Enter yes (y) or no (n): ")
                   
                    if choiceToDeposit == 'n':
                        print(player)
                        break
                    else:
                        amt = minBet - 1
                        while True:
                            try:
                                amt = int(input("Enter amount to deposit: "))
                                if amt < minBet or amt > sys.maxsize:
                                    print(f"Please enter a number between {minBet} and {sys.maxsize}")
                                else:
                                    break
                            except ValueError:
                                print("Invalid input. Please enter a valid number:")
                        player.deposit(amt)
            else:
                print(player)
                break 

if __name__ == "__main__":
    try:
        game_of_blackjack() 
    except Exception as e:
        print("Unexpected error: ", e) 