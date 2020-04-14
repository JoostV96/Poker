import copy

RANKS = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
RANKING = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
VALUE_DICT = dict(zip(RANKS, RANKING))
SUITS = ["H", "S", "C", "D"]

def one_pair(hand):
    hand = hand[:]
    for i in range(len(hand)-1):
        if hand[i][:-1] == hand[i+1][:-1]:
            pair = hand[i:i+2]
            del hand[i:i+2]
            return pair + hand[:3]       
        
def two_pair(hand):
    hand = hand[:]
    first_pair = one_pair(hand)
    if first_pair:
        first_pair = first_pair[:2]
        [hand.remove(card) for card in first_pair]
        second_pair = one_pair(hand)
        if second_pair:
            return first_pair + second_pair[:3]
    
def trips(hand):
    hand = hand[:]
    
    for i in range(len(hand)-2):
        if hand[i][:-1] == hand[i+2][:-1]:
            trips = hand[i:i+3]
            del hand[i:i+3]
            return trips + hand[:2]
        
def carre(hand):
    hand = hand[:]
    two_pairs = two_pair(hand)
    if two_pairs:
        if two_pairs[0][:-1] == two_pairs[3][:-1]:
            return two_pairs
        
def fullhouse(hand):
    hand = hand[:]
    tripple = trips(hand)
    if tripple:
        tripple = tripple[:3]
        [hand.remove(card) for card in tripple]
        pair = one_pair(hand)
        if pair:
            return tripple + pair[:2]
        
def straight(hand):
    hand = hand[:]

    for i in range(len(hand)-4):
        if VALUE_DICT[hand[i][:-1]] - VALUE_DICT[hand[i+4][:-1]] == 4:
            check_straight = hand[i:i+5]
            if all(VALUE_DICT[check_straight[i][:-1]] > VALUE_DICT[check_straight[i+1][:-1]]
                    for i in range(len(check_straight)-1)):
                return check_straight
            
    # Check straight with Ace as 1
    DICT_COPY = copy.deepcopy(VALUE_DICT)
    DICT_COPY["A"] = 1

    for i in range(len(hand)-4):
        if DICT_COPY[hand[i][:-1]] - DICT_COPY[hand[i+4][:-1]] == 4:
            check_straight = hand[i:i+5]
            if all(DICT_COPY[check_straight[i][:-1]] > DICT_COPY[check_straight[i+1][:-1]]
                    for i in range(len(check_straight)-1)):
                return check_straight 
    
def flush(hand):
    hand = hand[:]
    suits_only = [card[-1] for card in hand]
    suits_count = [suits_only.count(suit) for suit in SUITS]
    for i in range(len(suits_count)):
        if suits_count[i] >= 5:
            return [card for card in hand if SUITS[i] in card][:5]

def straight_flush(hand):
    hand = hand[:]
    straight_hand = straight(hand)
    if straight_hand:
        flush_hand = flush(straight_hand)
        if flush_hand:
            return flush_hand
        
def eval_hand(hand):
    hand = sorted(hand[:], key=lambda x:VALUE_DICT[x[:-1]], reverse=True)
    if straight_flush(hand):
        return 9, straight_flush(hand), "STRAIGHT FLUSH"
    if carre(hand):
        return 8, carre(hand), "CARRE" 
    if fullhouse(hand):
        return 7, fullhouse(hand), "FULLHOUSE"
    if flush(hand):
        return 6, flush(hand), "FLUSH"
    if straight(hand):
        return 5, straight(hand), "STRAIGHT"
    if trips(hand):
        return 4, trips(hand), "TRIPS"
    if two_pair(hand):
        return 3, two_pair(hand), "TWO PAIR"
    if one_pair(hand):
        return 2, one_pair(hand), "ONE PAIR"
    else:
        return 1, hand[:5], "HIGH CARD"