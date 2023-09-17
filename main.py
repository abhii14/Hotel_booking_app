import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """check if hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, costumer_name, hotel_object):
        self.costumer_name = costumer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thankyou for your reservation!
        Here is your booking data
        Name: {self.costumer_name}
        Hotel name : {self.hotel.name}
         """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number":self.number, "expiration":expiration,
                     "holder":holder, "cvc":cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False




print(df)
hotel_ID = input("Enter the hotel id: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    card_number = input("Enter your credit card number")
    credit_card = SecureCreditCard(number=card_number)
    card_expiry = input("Enter the card expiry date")
    card_name = input("Enter the name on card")
    card_cvc = input("Enter your card cvc")
    if credit_card.validate(expiration=card_expiry, holder=card_name, cvc=card_cvc):
        passw = input("Enter your password")
        if credit_card.authenticate(given_password=passw):
            hotel.book()
            name = input("Enter your Name: ")
            reservation_ticket = ReservationTicket(costumer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
        else:
            print("Credit card not valid")
    else:
        print("There was a problem with your payment")
else:
    print("Hotel is not free. ")