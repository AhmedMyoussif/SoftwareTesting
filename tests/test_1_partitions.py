"""Lab 2, technique 1: partitions. Name each test after its coverage item."""
import pytest

from tickets.booking import TicketBooking
from tickets.pricing import ticket_price

# Coverage items (equivalence partitions)
# P1: age below the valid range -> ValueError
# P2: age above the valid range -> ValueError
# P3: child age (0-12) -> 500
# P4: adult age (13-64) without a student card -> 1000
# P5: adult age (13-64) with a student card, not a weekday -> 800
# P6: senior age (65-120) -> 600
# P7: pay() from RESERVED -> PAID, charged once
# P8: cancel() from RESERVED -> CANCELLED, no refund
# P9: cancel() from PAID -> CANCELLED, refunded once


@pytest.mark.parametrize(
    "age,student,weekday,expected",
    [
        (6, False, False, 500),   # P3
        (30, False, False, 1000),  # P4
        (30, True, False, 800),    # P5
        (70, False, False, 600),   # P6
    ],
)
def test_pricing_partition(age, student, weekday, expected):
    assert ticket_price(age, student, weekday) == expected


@pytest.mark.parametrize("age", [-1, 121])
def test_invalid_age_partition(age):
    with pytest.raises(ValueError):
        ticket_price(age, False)


def test_pay_reserved_charges_once():
    booking = TicketBooking(1000)
    booking.pay()
    assert booking.state == "PAID"
    assert booking.charged == 1000
    assert booking.refunded == 0


def test_cancel_reserved_has_no_refund():
    booking = TicketBooking(1000)
    booking.cancel()
    assert booking.state == "CANCELLED"
    assert booking.charged == 0
    assert booking.refunded == 0


def test_cancel_paid_refunds_once():
    booking = TicketBooking(1000)
    booking.pay()
    booking.cancel()
    assert booking.state == "CANCELLED"
    assert booking.charged == 1000
    assert booking.refunded == 1000
