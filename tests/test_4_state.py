"""Lab 2, technique 4: state. Name each test after its coverage item."""
import pytest

from tickets.booking import TicketBooking

# State transitions for L4.
# S1: new booking is RESERVED, nothing charged or refunded
# S2: RESERVED --pay--> PAID, charged once
# S3: RESERVED --cancel--> CANCELLED, no refund
# S4: PAID --cancel--> CANCELLED, refunded once
# S5: PAID --pay--> RuntimeError, no extra charge
# S6: CANCELLED --pay--> RuntimeError, no charge
# S7: CANCELLED --cancel--> RuntimeError, no extra refund


def test_new_booking_starts_reserved():
    booking = TicketBooking(1000)  # S1
    assert booking.state == "RESERVED"
    assert booking.charged == 0
    assert booking.refunded == 0


def test_reserved_to_paid_charges_once():
    booking = TicketBooking(1000)  # S2
    booking.pay()
    assert booking.state == "PAID"
    assert booking.charged == 1000
    assert booking.refunded == 0


def test_reserved_to_cancelled_has_no_refund():
    booking = TicketBooking(1000)  # S3
    booking.cancel()
    assert booking.state == "CANCELLED"
    assert booking.charged == 0
    assert booking.refunded == 0


def test_paid_to_cancelled_refunds_once():
    booking = TicketBooking(1000)  # S4
    booking.pay()
    booking.cancel()
    assert booking.state == "CANCELLED"
    assert booking.charged == 1000
    assert booking.refunded == 1000


def test_pay_paid_raises_and_moves_no_money():
    booking = TicketBooking(1000)  # S5
    booking.pay()
    with pytest.raises(RuntimeError):
        booking.pay()
    assert booking.charged == 1000
    assert booking.refunded == 0


def test_pay_cancelled_raises_and_moves_no_money():
    booking = TicketBooking(1000)  # S6
    booking.cancel()
    with pytest.raises(RuntimeError):
        booking.pay()
    assert booking.charged == 0
    assert booking.refunded == 0


def test_cancel_cancelled_raises_and_moves_no_money():
    booking = TicketBooking(1000)  # S7
    booking.cancel()
    with pytest.raises(RuntimeError):
        booking.cancel()
    assert booking.charged == 0
    assert booking.refunded == 0
