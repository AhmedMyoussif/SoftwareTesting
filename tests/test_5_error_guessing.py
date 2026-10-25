"""Lab 2, technique 5: error_guessing. Name each test after its coverage item."""
import pytest

from tickets.booking import TicketBooking
from tickets.pricing import ticket_price

# Error-guessing probes.
# E1: non-integer ages (float, string, None) are rejected with ValueError
# E2: weekday does not change an adult non-student price
# E3: weekday does not change a senior student price
# E4: child with a student card on a weekday still pays 500
# E5: paying a cancelled booking raises and does not charge
# E6: cancelling a paid booking twice refunds only once
# E7: paying twice charges only once


@pytest.mark.parametrize("age", [12.5, "30", None])
def test_non_integer_age_rejected(age):
    with pytest.raises(ValueError):
        ticket_price(age, False)  # E1


def test_weekday_does_not_change_adult_non_student_price():
    assert ticket_price(30, False, weekday=True) == 1000  # E2


def test_weekday_does_not_change_senior_student_price():
    assert ticket_price(70, True, weekday=True) == 600  # E3


def test_child_student_weekday_price():
    assert ticket_price(8, True, weekday=True) == 500  # E4


def test_pay_cancelled_booking_raises():
    booking = TicketBooking(1000)  # E5
    booking.cancel()
    with pytest.raises(RuntimeError):
        booking.pay()
    assert booking.charged == 0


def test_cancel_paid_booking_twice_refunds_once():
    booking = TicketBooking(1000)  # E6
    booking.pay()
    booking.cancel()
    with pytest.raises(RuntimeError):
        booking.cancel()
    assert booking.refunded == 1000


def test_pay_twice_charges_once():
    booking = TicketBooking(1000)  # E7
    booking.pay()
    with pytest.raises(RuntimeError):
        booking.pay()
    assert booking.charged == 1000
