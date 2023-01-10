import random
import sqlite3
import string
from fpdf import FPDF


class User:
    """Represents a user that can buy a cinema seat"""
    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        """Buy the ticket if the seat is not occupied and the card is valid"""
        if seat.is_free():
            if card.validate(price=seat.get_price()):
                seat.occupy()
                ticket = Ticket(user=self, price=seat.get_price(), seat_nr=seat.seat_id)
                ticket.to_pdf()
                return "Purchase successful!"
            else:
                return "There was a problem with your card."
        else:
            return "Seat is taken!"

class Seat:
    """Represents a cinema seat that the user can choose"""
    database = "cinema.db"

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def get_price(self):
        """Get the price of the seat"""
        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute("""
        SELECT price FROM seat WHERE seat_id=?
        """, [self.seat_id])
        result = cursor.fetchall()[0][0]  # [0][0] so it returns the pure value form the tuple from the list
        return result

    def is_free(self):
        """Check the database if it's taken or not"""
        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute("""
        SELECT taken FROM seat WHERE seat_id = ?
        """, [self.seat_id])
        result = cursor.fetchall()[0][0]

        if result == 0:
            return True
        else:
            return False

    def occupy(self):
        """Change the value of taken in database to 1 if seat is free"""
        connection = sqlite3.connect("cinema.db")
        connection.execute("""
        UPDATE Seat SET taken=? WHERE seat_id=?
        """, [1, self.seat_id])
        connection.commit()
        connection.close()


class Card:
    """Represents a bank card needed for the purchase"""
    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.type = type
        self.number = number
        self.cvc = cvc
        self.holder = holder

    def validate(self, price):
        """Check if the card is valid
        Subtract amount from balance"""
        connection = sqlite3.connect("banking.db")
        cursor = connection.cursor()
        cursor.execute("""
        SELECT balance FROM card WHERE type=? and number=? and cvc=? and holder=?
        """, [self.type, self.number, self.cvc, self.holder])
        result = cursor.fetchall()[0][0]

        if result:
            balance = result  # or here [0][0] same thing
            if balance >= price:
                connection.execute("""
                UPDATE Card SET balance = ? WHERE type=? and number=? and cvc=? and holder=?
                """, [balance-price, self.type, self.number, self.cvc, self.holder])
                connection.commit()
                connection.close()
                return True

class Ticket:
    """Represents the digital ticket"""
    def __init__(self, user, price, seat_nr):  # generate a random id using random import
        self.id = "".join([random.choice(string.ascii_letters) for i in range(8)])
        self.user = user
        self.price = price
        self.seat_nr = seat_nr

    def to_pdf(self):
        """Generate the PDF"""
        pdf = FPDF(orientation="P", unit="pt", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", style="B", size=24)
        pdf.cell(w=0, h=80, txt="Your Digital Ticket", border=1, ln=1, align="C")

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Name: ", border=1)
        pdf.set_font(family="Times", style="B", size=12)
        pdf.cell(w=0, h=25, txt=self.user.name, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Ticket ID: ", border=1)
        pdf.set_font(family="Times", style="B", size=12)
        pdf.cell(w=0, h=25, txt=self.id, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Price: ", border=1)
        pdf.set_font(family="Times", style="B", size=12)
        pdf.cell(w=0, h=25, txt=str(self.price), border=1, ln=1)  # str!!!
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Seat: ", border=1)
        pdf.set_font(family="Times", style="B", size=12)
        pdf.cell(w=0, h=25, txt=self.seat_nr, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.output("Ticket.pdf", "F")


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

    print(user.buy(seat=seat, card=card))
