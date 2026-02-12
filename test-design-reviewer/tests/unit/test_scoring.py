"""Tests for scoring.py domain logic."""

import pytest

from scoring import (
    PROPERTY_CODES,
    aggregate_file,
    aggregate_suite,
    blend_scores,
    compute_farley_index,
    full_pipeline,
    get_rating,
    normalize_property,
)


class TestNormalizeProperty:
    def test_base_score_with_no_signals(self):
        """Zero signals should yield conservative base score of 5.0."""
        score = normalize_property("U", neg_count=0, pos_count=0, total_methods=20)
        assert score == pytest.approx(5.0)

    def test_base_score_with_zero_methods(self):
        """Zero total methods should yield 5.0."""
        score = normalize_property("U", neg_count=0, pos_count=0, total_methods=0)
        assert score == pytest.approx(5.0)

    def test_high_negatives_low_score(self):
        """Many negative signals should produce a low score."""
        score = normalize_property("U", neg_count=18, pos_count=0, total_methods=20)
        assert score < 3.0

    def test_high_positives_high_score(self):
        """Many positive signals should produce a high score."""
        score = normalize_property("U", neg_count=0, pos_count=18, total_methods=20)
        assert score > 7.0

    def test_both_signals_moderate(self):
        """Mixed signals should produce a moderate score."""
        score = normalize_property("U", neg_count=5, pos_count=5, total_methods=20)
        assert 3.0 < score < 7.0

    def test_custom_params_override(self):
        """Custom params should override defaults."""
        custom = {
            "neg_midpoint": 0.5, "neg_steepness": 1.0,
            "pos_midpoint": 0.5, "pos_steepness": 1.0,
            "neg_weight": 0.5, "pos_weight": 0.5,
        }
        score = normalize_property("U", neg_count=0, pos_count=0, total_methods=20, params=custom)
        assert score == pytest.approx(5.0)

    def test_all_properties_return_base_with_no_signals(self):
        """Every property should return 5.0 with no signals."""
        for prop in PROPERTY_CODES:
            score = normalize_property(prop, neg_count=0, pos_count=0, total_methods=10)
            assert score == pytest.approx(5.0), f"Property {prop} should return 5.0"


class TestBlendScores:
    def test_default_sixty_forty(self):
        # 0.6 * 8.0 + 0.4 * 6.0 = 4.8 + 2.4 = 7.2
        assert blend_scores(8.0, 6.0) == pytest.approx(7.2)

    def test_custom_weights(self):
        # 0.5 * 8.0 + 0.5 * 6.0 = 7.0
        assert blend_scores(8.0, 6.0, static_weight=0.5) == pytest.approx(7.0)

    def test_edge_zero(self):
        assert blend_scores(0.0, 0.0) == pytest.approx(0.0)

    def test_edge_ten(self):
        assert blend_scores(10.0, 10.0) == pytest.approx(10.0)

    def test_static_only(self):
        assert blend_scores(8.0, 6.0, static_weight=1.0) == pytest.approx(8.0)

    def test_llm_only(self):
        assert blend_scores(8.0, 6.0, static_weight=0.0) == pytest.approx(6.0)


class TestComputeFarleyIndex:
    def test_all_nines_exemplary(self):
        scores = {p: 9.0 for p in PROPERTY_CODES}
        index = compute_farley_index(scores)
        assert index == pytest.approx(9.0)

    def test_all_twos_critical(self):
        scores = {p: 2.0 for p in PROPERTY_CODES}
        index = compute_farley_index(scores)
        assert index == pytest.approx(2.0)

    def test_all_fives(self):
        scores = {p: 5.0 for p in PROPERTY_CODES}
        index = compute_farley_index(scores)
        assert index == pytest.approx(5.0)

    def test_mixed_scores_weighted(self):
        """Verify that higher-weighted properties have more influence."""
        # U and M have 1.5x weight, F has 0.75x
        base = {p: 5.0 for p in PROPERTY_CODES}

        # Boost U by 2 points
        boosted_u = dict(base)
        boosted_u["U"] = 7.0
        delta_u = compute_farley_index(boosted_u) - compute_farley_index(base)

        # Boost F by 2 points
        boosted_f = dict(base)
        boosted_f["F"] = 7.0
        delta_f = compute_farley_index(boosted_f) - compute_farley_index(base)

        # U (weight 1.5) should have more influence than F (weight 0.75)
        assert delta_u > delta_f

    def test_formula_manual_calculation(self):
        """Verify against hand-calculated result."""
        scores = {"U": 8.0, "M": 7.0, "R": 9.0, "A": 6.0, "N": 5.0, "G": 7.0, "F": 8.0, "T": 6.0}
        # (8*1.5 + 7*1.5 + 9*1.25 + 6*1.0 + 5*1.0 + 7*1.0 + 8*0.75 + 6*1.0) / 9.0
        # = (12 + 10.5 + 11.25 + 6 + 5 + 7 + 6 + 6) / 9.0
        # = 63.75 / 9.0 = 7.083...
        expected = 63.75 / 9.0
        assert compute_farley_index(scores) == pytest.approx(expected)


class TestGetRating:
    def test_exemplary_at_nine(self):
        assert get_rating(9.0) == "Exemplary"

    def test_exemplary_at_ten(self):
        assert get_rating(10.0) == "Exemplary"

    def test_excellent(self):
        assert get_rating(7.5) == "Excellent"
        assert get_rating(8.9) == "Excellent"

    def test_good(self):
        assert get_rating(6.0) == "Good"
        assert get_rating(7.4) == "Good"

    def test_fair(self):
        assert get_rating(4.5) == "Fair"
        assert get_rating(5.9) == "Fair"

    def test_poor(self):
        assert get_rating(3.0) == "Poor"
        assert get_rating(4.4) == "Poor"

    def test_critical(self):
        assert get_rating(0.0) == "Critical"
        assert get_rating(2.9) == "Critical"


class TestAggregateFile:
    def test_empty_methods_returns_base(self):
        result = aggregate_file([])
        for prop in PROPERTY_CODES:
            assert result[prop] == pytest.approx(5.0)

    def test_single_method(self):
        method = {p: 8.0 for p in PROPERTY_CODES}
        result = aggregate_file([method])
        for prop in PROPERTY_CODES:
            assert result[prop] == pytest.approx(8.0)

    def test_mean_aggregation(self):
        m1 = {p: 6.0 for p in PROPERTY_CODES}
        m2 = {p: 8.0 for p in PROPERTY_CODES}
        result = aggregate_file([m1, m2])
        for prop in PROPERTY_CODES:
            assert result[prop] == pytest.approx(7.0)

    def test_missing_property_defaults_to_base(self):
        m1 = {"U": 8.0}  # Only U present
        result = aggregate_file([m1])
        assert result["U"] == pytest.approx(8.0)
        assert result["M"] == pytest.approx(5.0)


class TestAggregateSuite:
    def test_equal_locs(self):
        f1 = {p: 8.0 for p in PROPERTY_CODES}
        f2 = {p: 6.0 for p in PROPERTY_CODES}
        result = aggregate_suite([f1, f2], [100, 100])
        for prop in PROPERTY_CODES:
            assert result[prop] == pytest.approx(7.0)

    def test_loc_weighted_favors_larger_files(self):
        f1 = {p: 9.0 for p in PROPERTY_CODES}  # large file
        f2 = {p: 3.0 for p in PROPERTY_CODES}  # small file
        result = aggregate_suite([f1, f2], [900, 100])
        for prop in PROPERTY_CODES:
            # 9.0*900 + 3.0*100 = 8100+300 = 8400/1000 = 8.4
            assert result[prop] == pytest.approx(8.4)

    def test_single_file(self):
        f1 = {p: 7.5 for p in PROPERTY_CODES}
        result = aggregate_suite([f1], [200])
        for prop in PROPERTY_CODES:
            assert result[prop] == pytest.approx(7.5)


class TestFullPipeline:
    def test_no_signals_returns_base_scores(self):
        data = {
            "properties": {
                p: {"neg_count": 0, "pos_count": 0, "total_methods": 10}
                for p in PROPERTY_CODES
            }
        }
        result = full_pipeline(data)
        assert result["farley_index"] == pytest.approx(5.0)
        assert result["rating"] == "Fair"
        for prop in PROPERTY_CODES:
            assert result["static_scores"][prop] == pytest.approx(5.0)
        assert "blended_scores" not in result

    def test_with_llm_scores(self):
        data = {
            "properties": {
                p: {"neg_count": 0, "pos_count": 0, "total_methods": 10}
                for p in PROPERTY_CODES
            },
            "llm_scores": {p: 8.0 for p in PROPERTY_CODES},
        }
        result = full_pipeline(data)
        assert "blended_scores" in result
        # static=5.0, llm=8.0, blend = 0.6*5.0 + 0.4*8.0 = 3.0+3.2 = 6.2
        for prop in PROPERTY_CODES:
            assert result["blended_scores"][prop] == pytest.approx(6.2)
        assert result["farley_index"] == pytest.approx(6.2)
        assert result["rating"] == "Good"

    def test_high_positives_high_index(self):
        data = {
            "properties": {
                p: {"neg_count": 0, "pos_count": 19, "total_methods": 20}
                for p in PROPERTY_CODES
            }
        }
        result = full_pipeline(data)
        assert result["farley_index"] > 7.0

    def test_high_negatives_low_index(self):
        data = {
            "properties": {
                p: {"neg_count": 19, "pos_count": 0, "total_methods": 20}
                for p in PROPERTY_CODES
            }
        }
        result = full_pipeline(data)
        assert result["farley_index"] < 3.0

    def test_custom_static_weight(self):
        data = {
            "properties": {
                p: {"neg_count": 0, "pos_count": 0, "total_methods": 10}
                for p in PROPERTY_CODES
            },
            "llm_scores": {p: 10.0 for p in PROPERTY_CODES},
            "static_weight": 0.0,  # LLM only
        }
        result = full_pipeline(data)
        assert result["farley_index"] == pytest.approx(10.0)

    def test_missing_properties_default_to_base(self):
        """Properties not in input should default to base 5.0."""
        data = {
            "properties": {
                "U": {"neg_count": 0, "pos_count": 18, "total_methods": 20},
            }
        }
        result = full_pipeline(data)
        # U should be high, all others 5.0
        assert result["static_scores"]["U"] > 7.0
        assert result["static_scores"]["M"] == pytest.approx(5.0)
