---
title: "R01 Crypto Physics Model"
summary: "Active-fluid interpretation and falsifiable implications for crypto order-book mechanics."
tags: [parallax, crypto, microstructure, physics-model]
related: ["docs/research/R01-crypto/MICROSTRUCTURE.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md"]
created_on: 2026-07-31
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
---

# Physics model of market microstructure

## Working intuition

Treat the limit order book as an active, adaptive fluid system. Aggressive buying and selling
produce flow; resting liquidity resists or absorbs it; price moves when local capacity is exhausted.
Unlike an ordinary fluid, the channel reacts to the flow: traders add, cancel, move, and hide
liquidity as market conditions change.

The mapping is:

- aggressive market buys and sells → flow;
- signed order-flow imbalance → pressure differential;
- resting depth → resistance or absorption capacity;
- limit-order additions → new material entering the channel;
- cancellations → walls disappearing;
- liquidity refill → compressibility or replenishment;
- autocorrelated recent flow → momentum or memory;
- price movement → displacement of the boundary after local capacity is exhausted.

A visible sell wall does not push price downward. It absorbs upward flow only while it remains
posted. Effective resistance must therefore account for both visible depth and its probability of
surviving until challenged:

```text
effective resistance
    ≈ visible depth × P(order survives until challenged)
      + expected liquidity refill
```

## Initial dynamics

The first approximation is:

```text
expected price velocity
    ≈ (net aggressive flow + directional book change)
      / effective surviving liquidity
```

Book depth evolves as a coupled state rather than a fixed boundary:

```text
d(depth)/dt
    = additions - cancellations - executions + repricing
```

The model should keep executions and cancellations separate. A wall consumed by aggressive flow
and a wall withdrawn by its maker may produce the same visible depth change but imply different
continuation and refill behavior.

## Identification

Before any of this can be estimated it has to be identifiable. In `velocity = pressure /
resistance`, multiplying both quantities by any constant leaves every prediction unchanged, so
only the ratio is pinned down and the two "forces" are a reparameterisation rather than a
measurement. Resting depth is directly observable, so **resistance carries the scale and pressure
is estimated relative to it**. Fix this convention before fitting; afterwards it is undetectable.

Dimensional coherence is the constraint the analogy earns for free, and it should be enforced:
pressure in quote notional per second, resistance in quote notional, velocity in log return per
second. Anything proposed as a contributor to pressure must be expressible in flow units. A daily
macro state is not, so its route into the model must be a stated mapping with a sign prior, not a
free function fitted after the fact.

## Testing the equation before estimating the states

The exponents of the governing equation can be measured on their own:

```text
directional mid response  ~  k * |net flow| ** delta  *  resting depth ** -gamma
```

`delta = 1` is the naive ratio form and Kyle (1985). `delta ≈ 0.5` is the empirical square-root
law, which the locally linear order book model derives from a hydrodynamic treatment of *latent*
liquidity rather than visible depth. The literature's prior is that the naive form is rejected in
this specific direction. Run `parallax book impact`; see `MICROSTRUCTURE.md`.

## The analogy's standing

The mappings above are definitions, not laws. Nothing in them can be violated, there is no
conservation and no invariant, so their internal coherence is not evidence about markets. The
analogy may generate features and functional forms. It may never justify a result. Only the
out-of-sample comparison below does that.

## Falsifiable claim

A model of pressure, resistance, persistence, and refill predicts future mid-price displacement
better than standard order-flow imbalance alone, out of sample, at horizons long enough to trade
after measured costs.

The baseline is standard order-flow and queue imbalance. The physics model has value only if its
additional state variables improve forecast error, calibration, or economically meaningful
conditional returns beyond that baseline. The analogy itself is not an edge.

## Expected output

Because traders observe and react to the same state, this is not a deterministic conservation-law
system. The model should estimate distributions rather than exact trajectories, including:

- expected mid-price displacement over each forecast horizon;
- probability of upward or downward boundary movement;
- probability that a visible liquidity void refills before price reaches it;
- probability that a challenged wall persists, is consumed, or is cancelled;
- uncertainty and regime sensitivity for every estimate.

Failure to beat the baseline after costs rejects the hypothesis in its current form.
