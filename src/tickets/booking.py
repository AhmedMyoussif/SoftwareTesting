"""Lab 2 booking life cycle. Test it against contract L4, not against this code."""


class TicketBooking:
    """L4: a booking starts RESERVED.

    pay():    RESERVED -> PAID and charges the price once.
    cancel(): RESERVED -> CANCELLED with no refund;
              PAID -> CANCELLED and refunds the price once.
    Any other pay() or cancel() raises RuntimeError and moves no money.
    """

    def __init__(self, price):
        self.price = price
        self.state = "RESERVED"
        self.charged = 0
        self.refunded = 0

    def pay(self):
        if self.state != "RESERVED":
            raise RuntimeError(f"cannot pay a {self.state} booking")
        self.charged += self.price
        self.state = "PAID"

    def cancel(self):
        if self.state == "RESERVED":
            self.state = "CANCELLED"
            return
        self.refunded += self.price
        self.state = "CANCELLED"
