import random
suits = ("Diamonds", "Hearts", "Spades", "Clubs")
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', "Jack", "Queen", "King", "Ace")
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, "Jack": 11, "Queen": 12, "King": 13, "Ace": 14}

valid_suits = ("diamonds", "hearts", "spades", "clubs")
valid_ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', "jack", "queen", "king", "ace")

class Card():  
    def __init__(self, rank, suit):  
        while suit.lower() not in valid_suits:
            suit = input("Enter a valid suit: ") 
        self.suit = (suit.lower()).capitalize()

        while str(rank).lower() not in valid_ranks: 
            rank = input("Enter a valid rank: ")
        self.rank = ((str(rank)).lower()).capitalize() # number 
        
        self.value = values[self.rank] 

    def __str__(self):
        return f"{self.rank} of {self.suit}"
        
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
        self.stack1 = []
        self.stack2 = [] 

    def display(self, ds = None):
        if ds is None:
            ds = self.fullDeck
        for i in ds:
            print(i)
    
    def shuffle(self): 
        random.shuffle(self.fullDeck)  
        # self.dealCards()

    # def dealOneCard(self):
    #     return self.fullDeck.pop()
    
    def dealCards(self, num = 26):
        s1 = []
        s2 = []
        
        siz1 = num 
        siz2 = num
        
        while (siz2 > 0):
            item = self.fullDeck.pop()
            s2.append(item) 
            siz2 -= 1
        while (siz1 > 0):
            item = self.fullDeck.pop()
            s1.append(item) 
            siz1 -= 1 
        self.stack1 = s1 
        self.stack2 = s2   

class Player():
    def __init__(self, num, name, cardDeck):
        self.num = num
        self.name = name
        self.cardDeck = cardDeck

    def __str__(self):
        return (f"Player {self.num}: {self.name} has {len(self.cardDeck)} cards")

    def display(self, ds = None):
        if ds is None:
            ds = self.cardDeck
        for i in ds:
            print(i)

    def addCard(self, cardsToAdd):  
        if type(cardsToAdd) == list:
            self.cardDeck.extend(cardsToAdd) 
        elif (type(cardsToAdd) == type(Card('4', 'Diamonds'))):
            self.cardDeck.append(cardsToAdd) 
        return
        # return self.display(self.cardDeck)

    def removeCard(self, num = 1):
        removedCards = []
        while (num > 0 and len(self.cardDeck) > 0):
            removedCards.append(self.cardDeck.pop(0))
            num -= 1 
        if len(removedCards) == 1:
            return removedCards[0]
        else: 
            return removedCards
        # return self.display(removedCards)

def game_of_war():
    d = Deck()
    d.shuffle()
    d.dealCards()
    
    # name = input("Enter player 1's name: ")
    player1 = Player(1, "ABC", d.stack1) 
    
    # name = input("Enter player 2's name: ")
    player2 = Player(2, "PQR", d.stack2)
    
    print(player1)
    print(player2) 

    roundNum = 0

    while (len(player1.cardDeck) > 0 and len(player2.cardDeck) > 0): 
        roundNum += 1 
        if roundNum > 9999:  
            print(f"Too many rounds :(")   
            break 

        c1 = player1.removeCard() 
        c2 = player2.removeCard()  

        if c1 == [] or c2 == []:
            break

        print(f"Round {roundNum}: {player1.name} plays {c1}, {player2.name} plays {c2}")
            
        if c1.value > c2.value: 
            player1.addCard(c1)
            player1.addCard(c2) 
        elif c1.value < c2.value: 
            player2.addCard(c1)
            player2.addCard(c2)  
        else:
            p1rem = [c1]
            p2rem = [c2]
            sum1 = c1.value;
            sum2 = c2.value;

            rounds = 0 
            howManyNeeded = 3
            
            while (sum1 == sum2) and (len(player1.cardDeck) >= howManyNeeded and len(player2.cardDeck) >= howManyNeeded):
                rounds += 1
                if rounds > 9999:
                    print(f"Too many wars :( \nPlayer 1 has {len(player1.cardDeck)} cards \nPlayer 2 has {len(player2.cardDeck)} cards \n")
                    return "Player {} has won!".format(2 if len(player2.cardDeck) > len(player1.cardDeck) else 1) 

                if rounds == 1:
                    numWar = 3
                else: 
                    numWar = 1
                    howManyNeeded = 1

                while (numWar > 0 and len(player1.cardDeck) >= numWar):
                    p1rem.append(player1.removeCard())
                    sum1 += p1rem[len(p1rem) - 1].value
                    numWar -= 1
                print(sum1) 
                
                if rounds == 1:
                    numWar = 3
                else: 
                    numWar = 1
                    howManyNeeded = 1

                while (numWar > 0 and len(player2.cardDeck) >= numWar):
                    p2rem.append(player2.removeCard())
                    sum2 += p2rem[len(p2rem) - 1].value
                    numWar -= 1
                print(sum2)
            print("~~~")

            if sum1 > sum2:
                print(f"{player1.name} wins the war and takes {len(p1rem)+len(p2rem)} cards")
                player1.addCard(p1rem)
                player1.addCard(p2rem)
            elif sum1 < sum2:
                print(f"{player2.name} wins the war and takes {len(p1rem)+len(p2rem)} cards")
                player2.addCard(p1rem)
                player2.addCard(p2rem) 
            elif (sum1 == sum2): 
                player1.addCard(p1rem)
                player2.addCard(p2rem)  
                break 

    print(f"\nPlayer 1 has {len(player1.cardDeck)} cards \nPlayer 2 has {len(player2.cardDeck)} cards \n") 
    print( "Player {} has won!".format(2 if len(player2.cardDeck) > len(player1.cardDeck) else 1) )
    return len(player2.cardDeck) + len(player1.cardDeck) 

if __name__ == "__main__": 
    res = game_of_war()
    print(res)