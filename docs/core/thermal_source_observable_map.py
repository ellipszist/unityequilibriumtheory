"""Declared TTG observable maps for a thermal source package.

The standard experimental quantity in a transient thermal grating (TTG) lane is
the difference in quasi-temperature between the grating peak and valley.  This
module keeps that measurement operator separate from the unresolved UET
calibration that would turn ``Phi`` into kelvin.
"""

from __future__ import annotations

from math import isfinite, log, pi


THERMAL_SOURCE_MAP_SCHEMA_VERSION = "1.0"
NORMALIZED_TTG_OBSERVABLE = "normalized_quasi_temperature_difference"


def normalized_ttg_signal(
    response_peak: float,
    response_valley: float,
    initial_response_difference: float,
) -> float:
    """Return the dimensionless TTG signal implied by a response field.

    ``response_peak`` and ``response_valley`` may be temperature-like values
    or a lane-specific normalized response such as ``Phi``.  The ratio is a
    measurement-operator definition, not evidence that the input is a
    temperature.
    """

    values = (
        response_peak,
        response_valley,
        initial_response_difference,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("TTG response values must be finite")
    if abs(float(initial_response_difference)) <= 1.0e-15:
        raise ValueError("initial TTG response difference must be nonzero")
    return (float(response_peak) - float(response_valley)) / float(
        initial_response_difference
    )


def quasi_temperature_difference_from_phi(
    phi_peak: float,
    phi_valley: float,
    temperature_scale_K: float | None,
) -> float | None:
    """Map a dimensionless ``Phi`` difference to kelvin when calibrated.

    The scale is deliberately required as an explicit input.  ``None`` means
    that the physical temperature map is not closed and no silent default is
    allowed.
    """

    if not all(isfinite(float(value)) for value in (phi_peak, phi_valley)):
        raise ValueError("Phi values must be finite")
    if temperature_scale_K is None:
        return None
    if not isfinite(float(temperature_scale_K)) or temperature_scale_K <= 0.0:
        raise ValueError("temperature_scale_K must be finite and positive")
    return float(temperature_scale_K) * (float(phi_peak) - float(phi_valley))


def ttg_wave_speed(grating_period_m: float, dip_time_s: float) -> float:
    """Return the standard TTG half-period arrival-speed estimate in m/s."""

    if not all(isfinite(float(value)) for value in (grating_period_m, dip_time_s)):
        raise ValueError("grating period and dip time must be finite")
    if grating_period_m <= 0.0 or dip_time_s <= 0.0:
        raise ValueError("grating period and dip time must be positive")
    return float(grating_period_m) / (2.0 * float(dip_time_s))


def ttg_wavevector(grating_period_m: float) -> float:
    """Return the TTG spatial wavevector magnitude in inverse metres.

    ``Lambda`` is the physical grating period. This is a source-backed
    observable definition, not a UET parameter fit.
    """

    if not isfinite(float(grating_period_m)):
        raise ValueError("grating period must be finite")
    if grating_period_m <= 0.0:
        raise ValueError("grating period must be positive")
    return 2.0 * pi / float(grating_period_m)


def ttg_propagation_length(
    grating_period_m: float,
    normalized_dip_signal: float,
) -> float:
    """Return the TTG propagation-length diagnostic in metres.

    The source convention uses a negative normalized dip ``DeltaT_d`` and
    ``l_p = Lambda / (-2 log(-DeltaT_d))``. The domain ``-1 < DeltaT_d < 0``
    is enforced so the logarithm is finite and the diagnostic remains
    physically interpretable. This relation does not calibrate ``Phi``.
    """

    values = (grating_period_m, normalized_dip_signal)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("grating period and dip signal must be finite")
    if grating_period_m <= 0.0:
        raise ValueError("grating period must be positive")
    if not -1.0 < normalized_dip_signal < 0.0:
        raise ValueError("normalized dip signal must satisfy -1 < dip < 0")
    return float(grating_period_m) / (-2.0 * log(-float(normalized_dip_signal)))


__all__ = [
    "NORMALIZED_TTG_OBSERVABLE",
    "THERMAL_SOURCE_MAP_SCHEMA_VERSION",
    "normalized_ttg_signal",
    "quasi_temperature_difference_from_phi",
    "ttg_wave_speed",
    "ttg_wavevector",
    "ttg_propagation_length",
]
