"""Lab 2, technique 2: boundaries. Name each test after its coverage item."""
import pytest

from tickets.booking import TicketBooking
from tickets.pricing import ticket_price

# Coverage items (boundary values)
# B1: age -1 (just below the valid range) -> ValueError
# B2: age 0 (lower valid boundary) -> child price 500
# B3: age 12 (upper child boundary) -> child price 500
# B4: age 13 (lower adult boundary) -> adult price 1000
# B5: age 64 (upper adult boundary) -> adult price 1000
# B6: age 65 (lower senior boundary) -> senior price 600
# B7: age 120 (upper valid boundary) -> senior price 600
# B8: age 121 (just above the valid range) -> ValueError
# B9: student adult at the child/adult boundary: 13 -> 800
# B10: weekday flag at the child boundary: 12 with student/weekday -> 500


@pytest.mark.parametrize(
    "age,expected",
    [
        (0, 500),    # B2
        (12, 500),   # B3
        (13, 1000),  # B4
        (64, 1000),  # B5
        (65, 600),   # B6
        (120, 600),  # B7
    ],
)
def test_age_boundaries(age, expected):
    assert ticket_price(age, False) == expected


@pytest.mark.parametrize("age", [-1, 121])
def test_invalid_age_boundaries(age):
    with pytest.raises(ValueError):
        ticket_price(age, False)


def test_student_adult_lower_boundary():
    assert ticket_price(13, True) == 800  # B9


def test_weekday_does_not_change_child_price():
    assert ticket_price(12, True, weekday=True) == 500  # B10
