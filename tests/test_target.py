"""Unit tests for target.py ensuring 100% line and branch coverage.

Covers all 16 functions:
- 11 data-type functions
- 5 mathematical functions
Testing valid inputs, boundary values, invalid values, and wrong types.
"""

import pytest
import target


# ============================================================================
# 1. is_adult(age)
# ============================================================================
@pytest.mark.parametrize(
    "age,expected",
    [
        (18, True),       # Exact boundary: adult
        (19, True),       # Boundary + 1
        (100, True),      # Normal adult
        (17, False),      # Boundary - 1
        (0, False),       # Lower valid boundary
        (18.0, True),     # Float boundary
        (17.99, False),   # Float just under boundary
        (18.01, True),    # Float just above boundary
        (True, False),    # Boolean edge case (True == 1 < 18 -> False)
    ],
)
def test_is_adult_valid(age, expected):
    result = target.is_adult(age)
    assert isinstance(result, bool)
    assert result is expected


@pytest.mark.parametrize("invalid_age", [-1, -0.1, -100])
def test_is_adult_negative_raises_value_error(invalid_age):
    with pytest.raises(ValueError, match="^age cannot be negative$"):
        target.is_adult(invalid_age)


@pytest.mark.parametrize("wrong_type", ["18", None, [18], {"age": 18}])
def test_is_adult_wrong_type_raises_type_error(wrong_type):
    with pytest.raises(TypeError):
        target.is_adult(wrong_type)


# ============================================================================
# 2. celsius_to_fahrenheit(celsius)
# ============================================================================
@pytest.mark.parametrize(
    "celsius,expected",
    [
        (0, 32.0),
        (100, 212.0),
        (-40, -40.0),            # Point of equivalence
        (-273.15, -459.67),      # Absolute zero
        (37, 98.6),              # Human body temperature
        (21.555, 70.8),          # Rounding verification
        (-17.7777, 0.0),         # Rounding near zero
    ],
)
def test_celsius_to_fahrenheit_valid(celsius, expected):
    result = target.celsius_to_fahrenheit(celsius)
    assert isinstance(result, float)
    assert result == expected


@pytest.mark.parametrize("wrong_type", ["0", None, [100]])
def test_celsius_to_fahrenheit_wrong_type(wrong_type):
    with pytest.raises(TypeError):
        target.celsius_to_fahrenheit(wrong_type)


# ============================================================================
# 3. count_vowels(text)
# ============================================================================
@pytest.mark.parametrize(
    "text,expected",
    [
        ("", 0),                          # Empty string boundary
        ("aeiou", 5),                     # All lowercase vowels
        ("AEIOU", 5),                     # All uppercase vowels
        ("aEiOu", 5),                     # Mixed case vowels
        ("rhythm", 0),                    # No vowels
        ("bcdfg 123 !@#", 0),             # Consonants, digits, symbols
        ("Hello, World!", 3),             # Mixed sentence: e, o, o
        ("The Quick Brown Fox Jumps", 6),  # Multi-word sentence: e, u, i, o, o, u
        ("   a   ", 1),                   # Whitespace padded
    ],
)
def test_count_vowels_valid(text, expected):
    result = target.count_vowels(text)
    assert isinstance(result, int)
    assert result == expected


@pytest.mark.parametrize("wrong_type", [123, 3.14, None, True, False, ["a", "e"], {"a": 1}])
def test_count_vowels_non_string_raises_type_error(wrong_type):
    with pytest.raises(TypeError, match="^text must be a string$"):
        target.count_vowels(wrong_type)


# ============================================================================
# 4. invert(flag)
# ============================================================================
@pytest.mark.parametrize(
    "flag,expected",
    [
        (True, False),
        (False, True),
    ],
)
def test_invert_valid(flag, expected):
    result = target.invert(flag)
    assert isinstance(result, bool)
    assert result is expected


@pytest.mark.parametrize(
    "wrong_type",
    [
        0, 1, -1, 3.14, "True", "False", "", None, [], [True], {}, {"flag": True}
    ],
)
def test_invert_non_bool_raises_type_error(wrong_type):
    with pytest.raises(TypeError, match="^flag must be True or False$"):
        target.invert(wrong_type)


# ============================================================================
# 5. greet(name)
# ============================================================================
@pytest.mark.parametrize(
    "name,expected",
    [
        (None, "Hello, Guest!"),
        ("", "Hello, Guest!"),
        (" ", "Hello, Guest!"),
        ("   ", "Hello, Guest!"),
        ("\t\n\r ", "Hello, Guest!"),
        ("Alice", "Hello, Alice!"),
        ("  Bob  ", "Hello, Bob!"),
        ("John Doe", "Hello, John Doe!"),
        (" Dr. Smith ", "Hello, Dr. Smith!"),
    ],
)
def test_greet_valid(name, expected):
    if name is None:
        # Also test default argument calling greet()
        assert target.greet() == "Hello, Guest!"
    result = target.greet(name)
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize("non_string", [123, False, ["Alice"]])
def test_greet_non_string_behavior(non_string):
    # Documents suspected bug where non-string raises AttributeError due to .strip()
    with pytest.raises(AttributeError):
        target.greet(non_string)


# ============================================================================
# 6. find_max(numbers)
# ============================================================================
@pytest.mark.parametrize(
    "numbers,expected",
    [
        ([1, 2, 3, 4, 5], 5),
        ([10, -2, 33, 4], 33),
        ([-10, -50, -3, -20], -3),
        ([42], 42),                   # Single element boundary
        ([7, 7, 7], 7),               # Identical elements
        ([1.5, 9.9, 4.2], 9.9),       # Floats
        ([-1.5, -0.5, -3.0], -0.5),   # Negative floats
        ((1, 10, 5), 10),             # Sequence/tuple input
    ],
)
def test_find_max_valid(numbers, expected):
    result = target.find_max(numbers)
    assert result == expected


@pytest.mark.parametrize("empty_seq", [[], (), ""])
def test_find_max_empty_raises_value_error(empty_seq):
    with pytest.raises(ValueError, match="^list is empty$"):
        target.find_max(empty_seq)


# ============================================================================
# 7. get_price(prices, item)
# ============================================================================
@pytest.mark.parametrize(
    "prices,item,expected",
    [
        ({"apple": 1.5, "banana": 0.75}, "apple", 1.5),
        ({"apple": 1.5, "banana": 0.75}, "banana", 0.75),
        ({"free_item": 0}, "free_item", 0),
        ({"item": -5.0}, "item", -5.0),
        ({1: "one", 2: "two"}, 1, "one"),
    ],
)
def test_get_price_valid(prices, item, expected):
    result = target.get_price(prices, item)
    assert result == expected


@pytest.mark.parametrize(
    "prices,missing_item",
    [
        ({"apple": 1.5}, "orange"),
        ({}, "anything"),
    ],
)
def test_get_price_missing_raises_key_error(prices, missing_item):
    with pytest.raises(KeyError, match=f"'{missing_item} not found'"):
        target.get_price(prices, missing_item)


# ============================================================================
# 8. swap(pair)
# ============================================================================
@pytest.mark.parametrize(
    "pair,expected",
    [
        ((1, 2), (2, 1)),
        (("a", "b"), ("b", "a")),
        ((None, 42), (42, None)),
        ([10, 20], (20, 10)),
        ((True, False), (False, True)),
    ],
)
def test_swap_valid(pair, expected):
    result = target.swap(pair)
    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.parametrize(
    "invalid_pair",
    [
        (),
        (1,),
        (1, 2, 3),
        [],
        [1],
        [1, 2, 3, 4],
    ],
)
def test_swap_invalid_len_raises_value_error(invalid_pair):
    with pytest.raises(ValueError, match="^pair must have exactly 2 values$"):
        target.swap(invalid_pair)


# ============================================================================
# 9. common_items(set_a, set_b)
# ============================================================================
@pytest.mark.parametrize(
    "set_a,set_b,expected",
    [
        ({1, 2, 3}, {2, 3, 4}, {2, 3}),
        ({1, 2}, {3, 4}, set()),
        ({1, 2, 3}, {1, 2, 3}, {1, 2, 3}),
        (set(), {1, 2}, set()),
        ({1, 2}, set(), set()),
        (set(), set(), set()),
        ({"apple", "banana"}, {"banana", "cherry"}, {"banana"}),
    ],
)
def test_common_items_valid(set_a, set_b, expected):
    result = target.common_items(set_a, set_b)
    assert isinstance(result, set)
    assert result == expected


# ============================================================================
# 10. is_leap_year(year)
# ============================================================================
@pytest.mark.parametrize(
    "year,expected",
    [
        (2024, True),    # Divisible by 4, not 100
        (2020, True),
        (2000, True),    # Divisible by 400 (century leap year)
        (1600, True),    # Divisible by 400
        (2400, True),    # Divisible by 400
        (1900, False),   # Divisible by 100, not 400 (century non-leap)
        (2100, False),   # Divisible by 100, not 400
        (1800, False),   # Divisible by 100, not 400
        (2023, False),   # Not divisible by 4
        (2019, False),   # Not divisible by 4
        (1, False),      # Lower valid boundary
        (4, True),       # First leap year
    ],
)
def test_is_leap_year_valid(year, expected):
    result = target.is_leap_year(year)
    assert isinstance(result, bool)
    assert result is expected


@pytest.mark.parametrize("invalid_year", [0, -1, -400])
def test_is_leap_year_invalid_raises_value_error(invalid_year):
    with pytest.raises(ValueError, match="^year must be 1 or more$"):
        target.is_leap_year(invalid_year)


# ============================================================================
# 11. to_int(value)
# ============================================================================
@pytest.mark.parametrize(
    "value,expected",
    [
        ("42", 42),
        ("-100", -100),
        ("0", 0),
        (123, 123),
        (-45, -45),
        (3.14, 3),
        (-3.99, -3),
    ],
)
def test_to_int_valid(value, expected):
    result = target.to_int(value)
    assert isinstance(result, int)
    assert result == expected


@pytest.mark.parametrize("bool_val", [True, False])
def test_to_int_bool_raises_type_error(bool_val):
    with pytest.raises(TypeError, match="^bool is not allowed$"):
        target.to_int(bool_val)


@pytest.mark.parametrize("invalid_str", ["abc", "12.34", ""])
def test_to_int_invalid_str_raises_value_error(invalid_str):
    with pytest.raises(ValueError):
        target.to_int(invalid_str)


# ============================================================================
# 12. divide(a, b)
# ============================================================================
@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 2, 5.0),
        (9, 3, 3.0),
        (-10, 2, -5.0),
        (10, -2, -5.0),
        (-10, -2, 5.0),
        (0, 5, 0.0),
        (7.5, 2.5, 3.0),
    ],
)
def test_divide_valid(a, b, expected):
    result = target.divide(a, b)
    assert isinstance(result, float)
    assert result == expected


def test_divide_periodic_approx():
    result = target.divide(1, 3)
    assert isinstance(result, float)
    assert result == pytest.approx(0.3333333333333333)


@pytest.mark.parametrize("zero_b", [0, 0.0])
def test_divide_zero_raises_zero_division_error(zero_b):
    with pytest.raises(ZeroDivisionError, match="^cannot divide by zero$"):
        target.divide(10, zero_b)


# ============================================================================
# 13. power(base, exponent)
# ============================================================================
@pytest.mark.parametrize(
    "base,exponent,expected",
    [
        (2, 3, 8),
        (5, 0, 1),
        (0, 5, 0),
        (0, 0, 1),           # Standard Python 0**0 == 1
        (-2, 3, -8),
        (-2, 4, 16),
        (2, -1, 0.5),
        (4, -2, 0.0625),
        (9, 0.5, 3.0),
    ],
)
def test_power_valid(base, exponent, expected):
    result = target.power(base, exponent)
    assert result == expected


def test_power_fractional_approx():
    result = target.power(2, 0.5)
    assert result == pytest.approx(1.4142135623730951)


# ============================================================================
# 14. square_root(x)
# ============================================================================
@pytest.mark.parametrize(
    "x,expected",
    [
        (0, 0.0),
        (4, 2.0),
        (9, 3.0),
        (100, 10.0),
        (0.25, 0.5),
    ],
)
def test_square_root_valid(x, expected):
    result = target.square_root(x)
    assert isinstance(result, float)
    assert result == expected


def test_square_root_non_perfect_approx():
    result = target.square_root(2)
    assert isinstance(result, float)
    assert result == pytest.approx(1.4142135623730951)


@pytest.mark.parametrize("negative_x", [-1, -0.001, -100])
def test_square_root_negative_raises_value_error(negative_x):
    with pytest.raises(ValueError, match="^cannot take the square root of a negative number$"):
        target.square_root(negative_x)


# ============================================================================
# 15. factorial(n)
# ============================================================================
@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 1),          # Boundary: 0! == 1
        (1, 1),          # Boundary: 1! == 1
        (2, 2),
        (3, 6),
        (5, 120),
        (7, 5040),
        (10, 3628800),
    ],
)
def test_factorial_valid(n, expected):
    result = target.factorial(n)
    assert isinstance(result, int)
    assert result == expected


@pytest.mark.parametrize("negative_n", [-1, -5, -100])
def test_factorial_negative_raises_value_error(negative_n):
    with pytest.raises(ValueError, match="^factorial is not defined for negative numbers$"):
        target.factorial(negative_n)


# ============================================================================
# 16. average(numbers)
# ============================================================================
@pytest.mark.parametrize(
    "numbers,expected",
    [
        ([1, 2, 3], 2.0),
        ([10, 20], 15.0),
        ([42], 42.0),                     # Single element
        ([1.5, 2.5, 3.5], 2.5),           # Floats
        ([-5, 5], 0.0),                   # Zero result
        ([-10, -20, -30], -20.0),         # All negative
        ((2, 4, 6), 4.0),                 # Tuple input
    ],
)
def test_average_valid(numbers, expected):
    result = target.average(numbers)
    assert isinstance(result, float)
    assert result == expected


def test_average_periodic_approx():
    result = target.average([1, 2])
    assert result == 1.5
    result_periodic = target.average([1, 2, 4])
    assert result_periodic == pytest.approx(2.3333333333333335)


@pytest.mark.parametrize("empty_numbers", [[], (), ""])
def test_average_empty_raises_value_error(empty_numbers):
    with pytest.raises(ValueError, match="^list is empty$"):
        target.average(empty_numbers)


# ============================================================================
# Intentional Failure for Assignment Requirement: "Include one red run from a failing test, then a green fix."
# ============================================================================
def test_intentional_failure_for_red_ci_demonstration():
    """Temporary failing test to trigger a verified Red CI workflow run."""
    assert False, "Intentional failure for CI red-run requirement"
