# Protocol-v1 failed baseline

The frozen velocity-Verlet reconstruction completed, and M1, M2, C1 and C2
passed. Control C3 failed without a tolerance change: halving `delta t` while
holding physical duration fixed moved the recurrence by 0.0510563, above the
protocol limit of 0.01. M3 and M4 also missed their reference tolerances. The
matching `metrics.json` is retained here as the small, tracked summary; the
full regenerable run remains under `_outputs/` and is intentionally ignored.
