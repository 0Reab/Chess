import random
from datetime import datetime, timedelta
from game import Game


def get_code(array, code):
    for code_obj in array:
        if code_obj.code == code:
            return code_obj
    return None


def start_game():
    return Game()


class Code:
    def __init__(self, owner):
        self.generation_time = datetime.now()
        self.expiry_time = self.set_expiry(minutes=5000)
        self.code = self.generate_code()
        self.owner = owner

    def generate_code(self) -> int:
        return random.randint(10000,99999)

    def set_expiry(self, minutes=5) -> datetime:
        return self.generation_time + timedelta(minutes=minutes)

    def is_expired(self) -> bool:
        return datetime.now() > self.expiry_time
