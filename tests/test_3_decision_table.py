"""Lab 2, technique 3: decision_table. Name each test after its coverage item."""
import pytest

from tickets.booking import TicketBooking
from tickets.pricing import ticket_price

# Decision table for L2-L3.
# Conditions: age class (child/adult/senior), student card, weekday.
# D1: child, no student card, not weekday          -> 500
# D2: child, student card, weekday                 -> 500
# D3: adult, no student card, not weekday          -> 1000
# D4: adult, no student card, weekday              -> 1000
# D5: adult, student card, not weekday             -> 800
# D6: adult, student card, weekday                 -> 700
# D7: senior, no student card, not weekday         -> 600
# D8: senior, student card, weekday                -> 600


@pytest.mark.parametrize(
    "age,student,weekday,expected",
    [
        (8, False, False, 500),   # D1
        (8, True, True, 500),     # D2
        (30, False, False, 1000),  # D3
        (30, False, True, 1000),  # D4
        (30, True, False, 800),   # D5
        (30, True, True, 700),    # D6
        (70, False, False, 600),  # D7
        (70, True, True, 600),    # D8
    ],
)
def test_pricing_decision_table(age, student, weekday, expected):
    assert ticket_price(age, student, weekday) == expected
