import random
import sqlite3
import string


class User:
    """Represents a user that can buy a cinema seat"""
    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        """Buy the ticket if the seat is not occupied and the card is valid"""
        pass


class Seat:
    """Represents a cinema seat that the user can choose"""
    database = "cinema.db"

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def price(self):
        """Get the price of the seat"""
        pass

    def is_free(self):
        """Check the database if it's taken or not"""
        pass

    def occupy(self):
        """Change the value of taken in database to 1 if seat is free"""
        pass


class Card:
    """Represents a bank card needed for the purchase"""
    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.type = type
        self.number = number
        self.cvc = cvc
        self.holder = holder

    def validate(self):
        """Check if the card is valid
        Subtract amount from balance"""
        pass


class Ticket:
    """Represents the digital ticket"""
    def __init__(self, user, price, seat):  # generate a random id using random import
        self.id = "".join([random.choice(string.ascii_letters) for i in range(8)])
        self.user = user
        self.price = price
        self.seat = seat

    def to_pdf(self):
        """Generate the PDF"""
        pass


# The command prompt
if __name__ == "__main__":

    name = input("Enter your full name: ")
    seat_id = input("Enter the seat ID (A1, A2, A3, B1, B2, B3, C1, C2, C3): ")
    card_type = input("Enter card type (Visa or Mastercard): ")
    card_number = input("Enter card number (8 digits): ")
    card_cvc = input("Enter card CVC (3 digits): ")
    card_holder = input("Enter the name written on the card: ")

    user = User(name=name)
    seat = Seat(seat_id=seat_id)
    card = Card(type=card_type, number=card_number, cvc=card_cvc, holder=card_holder)
