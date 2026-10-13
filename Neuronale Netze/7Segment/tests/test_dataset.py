import numpy as np
import pytest

from seven_segment.dataset import load_inputs, load_targets, segments_for_digit


def test_inputs_have_one_row_per_digit_and_seven_segments():
    inputs = load_inputs()

    assert inputs.shape == (10, 7)


def test_all_segment_patterns_are_unique():
    patterns = {tuple(row) for row in load_inputs()}

    assert len(patterns) == 10


def test_eight_lights_all_segments():
    assert segments_for_digit(8) == [1, 1, 1, 1, 1, 1, 1]


def test_one_lights_only_b_and_c():
    assert segments_for_digit(1) == [0, 1, 1, 0, 0, 0, 0]


def test_targets_are_one_hot():
    targets = load_targets()

    assert np.array_equal(targets.sum(axis=1), np.ones(10))
    assert np.array_equal(np.argmax(targets, axis=1), np.arange(10))


@pytest.mark.parametrize("digit", [-1, 10])
def test_invalid_digit_raises(digit):
    with pytest.raises(ValueError):
        segments_for_digit(digit)
