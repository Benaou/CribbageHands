import itertools

def flush(hand):
    points=1
    for i in range(3):
        if hand[i]//13 == hand[i+1]//13:
            points += 1
    if points == 4:
        return 5 if hand[3]//13==hand[4]//13 else 4
    return 0

def knobs(hand):
    for i in range(4):
        if hand[i]%13 == 10 and hand[i]//13 == hand[4]//13:
            return 1
    return 0

def pairs(hand):
    points = 0
    for pairs in itertools.combinations(hand, 2):
        if pairs[0]%13 == pairs[1]%13:
            points += 2
    return points

def fifteen(hand):
    points = 0
    point_value = (1,2,3,4,5,6,7,8,9,10,10,10,10)
    for size in range(2,6): #check combinations of 2 through 5
        for cards in itertools.combinations(hand, size):
            if sum(map(lambda card: point_value[card%13], cards))==15:
                points += 2
    return points

def run(hand):
    cards = lambda h: map(lambda card: card%13, h)
    consecutive = lambda cards: all([cards[i+1]-cards[i]==1 for i in range(len(cards)-1)])
    if consecutive(sorted(cards(hand))):
        return len(hand)
    points=0
    for size in (4,3):
        for c in itertools.combinations(hand, size):
            if consecutive(sorted(cards(c))):
                points += len(c)
        if points:
            return points
    return 0

def number_to_abbreviation(card):
    suit = "SHCD"[card//13]
    face = "A234567890JQK"[card%13]
    return face+suit
    
if __name__ == '__main__':
    with open('cribbage_results.csv', 'a') as f:
        f.write(','.join(['card1','card2','card3','card4','flip','points','fifteens','pairs','runs','flushes','knobs']))
        f.write('\n')
        for hand in itertools.combinations(range(52), 4):
            for flip in set(range(52)).difference(set(hand)):
                h = hand+(flip,)
                f.write(','.join(map(number_to_abbreviation, h)))
                f.write(',')
                points = (fifteen(h), pairs(h), run(h), flush(h), knobs(h))
                f.write(str(sum(points)))
                f.write(',')
                f.write(','.join(map(str, points)))
                f.write('\n')
                
