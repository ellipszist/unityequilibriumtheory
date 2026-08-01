# Thermal Source and Observable-Mapping Specification

## Purpose

This packet separates the standard thermal measurement from the unresolved UET
calibration. The graphite sources are used to lock the observable definition and
provenance requirements only. No source data are fitted or used to tune UET
parameters in this wave.

## Standard observable

Transient thermal grating (TTG) measurements probe the response between the
grating peak and valley. In the graphite source lane the relevant physical
quantity is a quasi-temperature difference, representing collective phonon
energy. Define

\[
\Delta T_q(t;\Lambda)=T_q^{\mathrm{peak}}(t;\Lambda)-T_q^{\mathrm{valley}}(t;\Lambda),
\qquad
y_{\mathrm{TTG}}(t;\Lambda)=\frac{\Delta T_q(t;\Lambda)}{\Delta T_q(0;\Lambda)}.
\]

The normalized signal is dimensionless. A calibrated raw response may be
reported in kelvin. A TTG signal does not directly measure heat flux or entropy
production.

The standard arrival-speed diagnostic is

\[
v_{\mathrm{TTG}}=\frac{\Lambda}{2t_d},
\]

with \(\Lambda\) in metres and \(t_d\) in seconds.

## UET lane

Only the following normalized measurement operator is currently defined:

\[
y_{\mathrm{TTG}}^{\mathrm{UET}}(t;\Lambda)
=
\frac{\Delta\Phi(t;\Lambda)}{\Delta\Phi(0;\Lambda)}.
\]

The dimensional bridge would require an independently justified coefficient:

\[
\Delta T_q(t;\Lambda)=\alpha_{\Phi,K}\Delta\Phi(t;\Lambda),
\qquad [\alpha_{\Phi,K}] = \mathrm{K}\;\text{per normalized }\Phi.
\]

`alpha_Phi_K` is not derived, fitted, or assigned a default in this packet.
Therefore the normalized operator is a definition for a future comparison, not
evidence that `Phi` is temperature.

## Downstream maps

The following maps remain blocked until the temperature scale and local numeric
source are closed:

- heat flux: \(q=-k\nabla T_q\), requiring \(k\), spatial units, and a calibrated \(T_q\);
- entropy production: \(\sigma=q^2/(kT_q^2)\), requiring dimensional \(q\) and \(T_q\);
- derived trace \(R\): not a directly measured TTG observable.

## Source and claim boundary

- Ding et al. (2022) is an external source candidate whose data are available
  from the corresponding author on reasonable request.
- Xie et al. (2026) declares source data provided with the study, but remains a
  locked holdout and is not locally archived or consumed here.
- The repository has source identities and measurement-operator metadata, not a
  source-normalized numeric comparison.
- Current status: `PASS_WITH_BLOCKED_DIMENSIONAL_AND_DATA_LANES` and
  `DEFINITION_ONLY / SIMULATION_ONLY`.

See [matter_space_thermal_source_review.json](./Data/03_Research/matter_space_thermal_source_review.json),
[matter_space_thermal_observable_map_readiness.json](./Result/artifacts/matter_space_thermal_observable_map_readiness.json),
and [audit_thermal_source_observable_mapping.py](../../scripts/audit/audit_thermal_source_observable_mapping.py).

## Additional source-backed diagnostics

Once a source provides a grating period and a resolved TTG dip, the standard
comparison can report diagnostics that do not require a `Phi` calibration:

\[
q_{\mathrm{TTG}}=\frac{2\pi}{\Lambda},
\qquad
v_{\mathrm{TTG}}=\frac{\Lambda}{2t_d},
\qquad
\ell_p=\frac{\Lambda}{-2\ln(-\Delta T_d)}.
\]

Here `q_TTG` is the spatial wavevector magnitude in `m^-1`, `v_TTG` is in
`m/s`, `Lambda` and `ell_p` are in metres, and `Delta T_d` is the negative,
dimensionless normalized dip used by the source convention. These are
source-backed diagnostic definitions for a future comparison. They do not
identify `Phi` with temperature, do not derive `alpha_Phi_K`, and do not close
heat-flux or entropy-production mappings.