"""Tests for core.py math primitives."""

import math

import pytest

from core import loc_weighted_mean, mean, p90, sigmoid


class TestSigmoid:
    def test_midpoint_returns_half(self):
        assert sigmoid(0.5, midpoint=0.5, steepness=8.0) == pytest.approx(0.5)

    def test_high_x_approaches_one(self):
        result = sigmoid(10.0, midpoint=0.5, steepness=8.0)
        assert result > 0.99

    def test_low_x_approaches_zero(self):
        result = sigmoid(-10.0, midpoint=0.5, steepness=8.0)
        assert result < 0.01

    def test_overflow_guard_large_positive_exponent(self):
        result = sigmoid(-1000.0, midpoint=0.0, steepness=1.0)
        assert result == 0.0

    def test_overflow_guard_large_negative_exponent(self):
        result = sigmoid(1000.0, midpoint=0.0, steepness=1.0)
        assert result == 1.0

    def test_steepness_affects_curve(self):
        gentle = sigmoid(0.6, midpoint=0.5, steepness=2.0)
        steep = sigmoid(0.6, midpoint=0.5, steepness=20.0)
        # Both above 0.5 since x > midpoint, but steep is closer to 1.0
        assert gentle > 0.5
        assert steep > gentle

    def test_zero_steepness_returns_half(self):
        assert sigmoid(100.0, midpoint=0.0, steepness=0.0) == pytest.approx(0.5)


class TestP90:
    def test_empty_returns_zero(self):
        assert p90([]) == 0.0

    def test_single_value(self):
        assert p90([7.5]) == 7.5

    def test_two_values(self):
        result = p90([2.0, 8.0])
        # idx = 0.9 * 1 = 0.9, lo=0, hi=1, frac=0.9
        # 2.0 + 0.9 * (8.0 - 2.0) = 2.0 + 5.4 = 7.4
        assert result == pytest.approx(7.4)

    def test_ten_values(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        result = p90(values)
        # idx = 0.9 * 9 = 8.1, lo=8, hi=9, frac=0.1
        # 9.0 + 0.1 * (10.0 - 9.0) = 9.1
        assert result == pytest.approx(9.1)

    def test_unsorted_input(self):
        result = p90([10.0, 1.0, 5.0, 3.0, 8.0])
        sorted_result = p90([1.0, 3.0, 5.0, 8.0, 10.0])
        assert result == pytest.approx(sorted_result)

    def test_all_same_values(self):
        assert p90([5.0, 5.0, 5.0, 5.0]) == pytest.approx(5.0)


class TestMean:
    def test_empty_returns_zero(self):
        assert mean([]) == 0.0

    def test_single_value(self):
        assert mean([4.0]) == 4.0

    def test_multiple_values(self):
        assert mean([2.0, 4.0, 6.0]) == pytest.approx(4.0)

    def test_negative_values(self):
        assert mean([-3.0, 3.0]) == pytest.approx(0.0)


class TestLocWeightedMean:
    def test_equal_weights(self):
        result = loc_weighted_mean([8.0, 6.0], [100, 100])
        assert result == pytest.approx(7.0)

    def test_unequal_weights(self):
        # 8.0 * 300 + 6.0 * 100 = 2400 + 600 = 3000 / 400 = 7.5
        result = loc_weighted_mean([8.0, 6.0], [300, 100])
        assert result == pytest.approx(7.5)

    def test_single_file(self):
        result = loc_weighted_mean([9.0], [500])
        assert result == pytest.approx(9.0)

    def test_empty_returns_zero(self):
        assert loc_weighted_mean([], []) == 0.0

    def test_zero_locs_returns_zero(self):
        assert loc_weighted_mean([5.0, 7.0], [0, 0]) == 0.0
