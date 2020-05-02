import random
import time

from enum import Enum
from functools import total_ordering


class Suit(Enum):
    SPADES = 4
    HEARTS = 3
    DIAMONDS = 2
    CLUBS = 1


@total_ordering
class PlayingCard:
    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit

    def get_rank(self):
        return self._rank

    def get_suit(self):
        return self._suit

    def __eq__(self, p):
        return (
            self._rank == p._rank and
            self._suit == p._suit
        )

    def __gt__(self, p):
        if self._rank > p._rank:
            return True

        if self._rank == p._rank:
            return self._suit.value > p._suit.value

        return False

    def __str__(self):
        return f'({self.get_rank()}, {self.get_suit().name})'


class Player:
    def __init__(self, name):
        self._name = name
        self._hand = []

    def get_name(self):
        return self._name

    def get_hand(self):
        return self._hand

    def set_hand(self, hand):
        self._hand = hand

    def strongest_card(self):
        if self._hand:
            return max(self._hand)


class Cheater(Player):
    def strongest_card(self):
        # return ace of spades with 20% chance
        if random.randint(1, 10) <= 2:
            return PlayingCard(14, Suit.SPADES)
        else:
            return super().strongest_card()


class Deck:
    def __init__(self):
        self._cards = []
        for i in range(13):
            self._cards.append(PlayingCard(i+2, Suit.SPADES))
            self._cards.append(PlayingCard(i+2, Suit.DIAMONDS))
            self._cards.append(PlayingCard(i+2, Suit.HEARTS))
            self._cards.append(PlayingCard(i+2, Suit.CLUBS))

    def get_cards(self):
        return self._cards

    def shuffle(self):
        for _ in range(200):
            i, j = random.randint(0, 51), random.randint(0, 51)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]

    def draw(self, n):
        if n > len(self._cards):
            return None

        drawn = []
        for _ in range(n):
            c = self._cards.pop()
            drawn.append(c)
        return drawn


class Game:
    def __init__(self, players, deck):
        self._players = players
        self._deck = deck
        self._score = {}
        # initialize the scores to zeros.
        for p in players:
            self._score[p.get_name()] = 0

    def _show_score(self):
        print("Score:")
        print("-----")
        for k, v in self._score.items():
            print(f'{k}: {v}')
        print('\n')

    def _is_more_rounds(self):
        return len(self._deck.get_cards()) >= 2 * len(self._players)

    def _play_round(self):
        winning_card = None
        winning_player = None
        for p in self._players:
            hand = self._deck.draw(2)
            p.set_hand(hand)
            print(f'player {p.get_name()} is dealt: [{hand[0]}, {hand[1]}]')
            if winning_card is None or p.strongest_card() > winning_card:
                winning_card = p.strongest_card()
                winning_player = p

        print(f'PLAYER {winning_player.get_name()} WINS THIS ROUND\n')
        self._score[winning_player.get_name()] += 1
        self._show_score()
        time.sleep(6)

    def play(self):
        while self._is_more_rounds():
            self._play_round()
        winner = max(self._score, key=self._score.get)
        print(f'\n\nPlayer {winner} won the game')


if __name__ == '__main__':
    p1 = Player('Alice')
    p2 = Player('Bob')
    p3 = Player('Karim')

    d = Deck()
    d.shuffle()
    g = Game([p1, p2, p3], d)
    g.play()
