import mpmath as mp
import numpy as np

from eml_symbolic_regression.verify import DataSplit, verify_candidate


class _StubCandidate:
    candidate_kind = "exact_eml"

    def __init__(self, *, numpy_value: complex, mpmath_value: complex | None = None, fail_mpmath: bool = False) -> None:
        self.numpy_value = complex(numpy_value)
        self.mpmath_value = complex(mpmath_value) if mpmath_value is not None else complex(numpy_value)
        self.fail_mpmath = fail_mpmath
        self.mpmath_calls = 0

    def evaluate_numpy(self, context):
        shape = np.asarray(context["x"], dtype=np.complex128).shape
        return np.full(shape, self.numpy_value, dtype=np.complex128)

    def evaluate_mpmath(self, context):
        self.mpmath_calls += 1
        if self.fail_mpmath:
            raise AssertionError("mpmath evaluation should have been skipped")
        return mp.mpc(self.mpmath_value)

    def to_sympy(self):
        raise NotImplementedError


def _split() -> DataSplit:
    return DataSplit(
        name="heldout",
        inputs={"x": np.asarray([0.0, 1.0, 2.0], dtype=np.complex128)},
        target=np.asarray([1.0, 1.0, 1.0], dtype=np.complex128),
    )


def test_verify_candidate_performs_high_precision_for_exact_match():
    candidate = _StubCandidate(numpy_value=1.0, mpmath_value=1.0)

    report = verify_candidate(candidate, [_split()], tolerance=1e-8)

    assert report.status == "recovered"
    assert report.reason == "verified"
    assert report.high_precision_status == "performed"
    assert report.high_precision_max_error == 0.0
    assert candidate.mpmath_calls > 0


def test_verify_candidate_skips_high_precision_for_decisive_numeric_failure():
    candidate = _StubCandidate(numpy_value=2.0, fail_mpmath=True)

    report = verify_candidate(candidate, [_split()], tolerance=1e-8)

    assert report.status == "failed"
    assert report.reason == "heldout_failed"
    assert report.high_precision_status == "skipped_numeric_failure"
    assert report.high_precision_max_error == 1.0
    assert candidate.mpmath_calls == 0


def test_verify_candidate_keeps_high_precision_for_near_miss_numeric_failure():
    candidate = _StubCandidate(numpy_value=1.005, mpmath_value=1.0)

    report = verify_candidate(candidate, [_split()], tolerance=1e-8)

    assert report.status == "failed"
    assert report.reason == "heldout_failed"
    assert report.high_precision_status == "performed"
    assert report.high_precision_max_error == 0.0
    assert candidate.mpmath_calls > 0
