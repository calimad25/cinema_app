import random
import sqlite3

class User:

    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        pass


class Seat:

    database = "cinema.db"

    def __init__(self, seat_id):
        self.seat.it = seat_id

    def price(self):
        pass

    def is_free(self):
        pass

    def occupy(self):
        pass


class Card:

    database = "banking.db"

    def __init__(self, type, number, CVC, holder):
        self.type = type
        self.number = number
        self.CVC = CVC
        self.holder = holder

    def validate(self):
        pass

class Ticket:

    def __init__(self, id, user, price, seat):  # generate a random id using random import
        self.id = id
        self.user = user
        self.price = price
        self.seat = seat

    def to_pdf(self):
        pass
