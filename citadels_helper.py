from dataclasses import dataclass, field
import random
import typing

characters_name = [
    (1, 'Asasin'),
    (2, 'Thief'),
    (3, 'Magician'),
    (4, 'King'),
    (5, 'Bishop'),
    (6, 'Merchant'),
    (7, 'Architect'),
    (8, 'Warlord')
]

persons_state = {}


@dataclass
class Character:
    name: str
    player_name: str = field(default='')
    status: int = field(default=-1)

    class CharacterStatus:
        FACEDOWN = -2
        SETUP = -1
        IN_GAME = 0
        DEAD = 1
        ROBBED = 2

    def define_player(self, player_name: str) -> None:
        """Define a player for the character for this round"""
        self.player_name = player_name
        self.status = self.CharacterStatus.IN_GAME

    def to_kill(self) -> None:
        """Set player to dead state"""
        self.status = self.CharacterStatus.DEAD

    def is_killed(self) -> bool:
        """Check the player's dead"""
        if self.status == self.CharacterStatus.DEAD:
            return True
        return False

    def to_rob(self) -> None:
        """Set player to robbed state"""
        self.status = self.CharacterStatus.DEAD

    def is_robbed(self) -> bool:
        """Check the player's robbed"""
        if self.status == self.CharacterStatus.ROBBED:
            return True
        return False


class CharacterAsasin(Character):
    def make_action(self, character) -> None:
        character.to_kill()


class CharacterThief(Character):
    def make_action(self, character) -> None:
        character.to_rob()


class PersonFactory:
    def __init__(self):
        self._types = {}

    def register_type(self, name: str, character: typing.Type[Character]):
        self._types[name] = character

    def get_character(self, name):
        character = self._types.get(name)
        if not character:
            raise ValueError(name)
        return character(name=name)


factory = PersonFactory()
factory.register_type("Asasin", CharacterAsasin)
factory.register_type("Thief", CharacterThief)


def rotate(l, n):
    return l[n:] + l[:n]


class Citadels:

    def __init__(self):
        self.players = []
        self.character_deck = []
        self.out_game_faceup = []
        self.out_game_facedown = None

    def add_player(self, name: str):
        """Add player's name to list of players"""
        self.players += name

    def setup_character_deck(self):
        """Setup the Character Deck with empty addition parameters"""
        for order_num, name in characters_name:
            self.character_deck = Character(name=name)

    def remove_characters(self) -> None:
        """Remove some cards from the Character Deck according to number of players"""
        self.remove_facedown()
        number_of_players = len(self.players)
        if number_of_players == 4:
            for _ in range(2):
                self.remove_faceup()
        elif number_of_players == 5:
            self.remove_faceup()

    def remove_facedown(self) -> None:
        """Draw one random card from the Character Deck and set it facedown"""
        index = random.randrange(len(self.character_deck))
        self.out_game_facedown = self.character_deck[index]
        self.character_deck[index].status = Character.CharacterStatus.FACEDOWN

    def remove_faceup(self) -> None:
        """Draw one random card from the Character Deck and set it faceup"""
        index = random.randrange(len(self.character_deck))
        self.out_game_faceup += self.character_deck.pop(index)

    def change_the_king(self, name: str) -> None:
        """Rotate the list of players to replace the king player to the top"""
        self.players = rotate(self.players, self.players.index(name))

    @staticmethod
    def need_to_choose_character_for_action(person: dict) -> bool:
        if person[0] in [1, 2]:
            return True
        return False
