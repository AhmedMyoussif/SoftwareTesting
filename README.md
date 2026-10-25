# Tickets Lab 02 - Test Design Solution

Black-box test suite for a small cinema ticket system. The tests are written
against the published contract (L1-L4), **not** against the implementation, and
use five test-design techniques.

## Project layout

```
lab02/
├── pyproject.toml              # pytest config (testpaths=tests, pythonpath=src)
├── requirements-dev.txt        # pytest>=7.0
├── src/tickets/
│   ├── pricing.py              # ticket_price(age, student, weekday)
│   └── booking.py              # TicketBooking state machine
└── tests/
    ├── test_1_partitions.py
    ├── test_2_boundaries.py
    ├── test_3_decision_table.py
    ├── test_4_state.py
    └── test_5_error_guessing.py
```

## Contract under test

- **L1** - `age` must be an integer from 0 through 120, otherwise `ValueError`.
- **L2** - children (0-12) pay 500; adults (13-64) pay 1000, or 800 with a
  student card; seniors (65-120) pay 600.
- **L3** - on a weekday an adult student pays 700 instead of 800. The weekday
  flag changes no other price.
- **L4** - a booking starts `RESERVED`.
  - `pay()`: `RESERVED -> PAID`, charges the price once.
  - `cancel()`: `RESERVED -> CANCELLED` with no refund; `PAID -> CANCELLED`
    with one refund.
  - Any other `pay()`/`cancel()` raises `RuntimeError` and moves no money.

## Test design by technique

### 1. Equivalence partitioning (`test_1_partitions.py`)

Coverage items P1-P9: invalid age below/above range, child, adult,
adult student, senior, plus the three valid booking transitions (`pay` from
`RESERVED`, `cancel` from `RESERVED`, `cancel` from `PAID`). One representative
value per partition.

### 2. Boundary value analysis (`test_2_boundaries.py`)

Coverage items B1-B10: `-1`, `0`, `12`, `13`, `64`, `65`, `120`, `121`, the
student adult at age 13, and the child price on a weekday. These target the
partition edges where the implementation is most likely to be wrong.

### 3. Decision table (`test_3_decision_table.py`)

Coverage items D1-D8 combine the three conditions - age class
(child/adult/senior), student card, weekday - and assert the price for each
feasible rule, including that weekday only affects adult students.

### 4. State transition testing (`test_4_state.py`)

Coverage items S1-S7: initial state, `RESERVED -> PAID`,
`RESERVED -> CANCELLED`, `PAID -> CANCELLED`, and the invalid transitions
`PAID -> pay`, `CANCELLED -> pay`, `CANCELLED -> cancel`. Invalid transitions
must raise `RuntimeError` without charging or refunding.

### 5. Error guessing (`test_5_error_guessing.py`)

Coverage items E1-E7: non-integer ages (float, string, `None`), weekday not
changing non-adult-student prices, paying a cancelled booking, cancelling a
paid booking twice, and paying twice. These probe likely off-by-one and
missing-guard defects.

## Results

```
python3 -m pytest -q
43 tests: 36 passed, 7 failed
```

The 7 failures are expected: the tests encode the contract, and the
implementation violates it. They map to three bugs:

| Bug | Location | Contract | Failing tests |
| --- | --- | --- | --- |
| Age 12 treated as an adult (`age < 12` instead of `age <= 12`) | `src/tickets/pricing.py:15` | L2 | `test_age_boundaries[12-500]`, `test_weekday_does_not_change_child_price` |
| Cancelling a `CANCELLED` booking refunds again instead of raising | `src/tickets/booking.py:25` | L4 | `test_cancel_cancelled_raises_and_moves_no_money`, `test_cancel_paid_booking_twice_refunds_once` |
| Non-integer ages not rejected with `ValueError` (`12.5` accepted; `"30"`/`None` raise `TypeError`) | `src/tickets/pricing.py:13` | L1 | `test_non_integer_age_rejected[12.5]`, `[30]`, `[None]` |

No source files were modified: the exercise is to expose the defects through
tests, so the suite should fail until the implementation is fixed.

## How to run

```bash
python3 -m pip install --user -r requirements-dev.txt
python3 -m pytest -v
```

Run a single technique:

```bash
python3 -m pytest tests/test_2_boundaries.py -v
```
