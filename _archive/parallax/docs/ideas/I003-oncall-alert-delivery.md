---
title: "I003 On-Call Alert Delivery for Self-Hosted Monitoring"
summary: "A wearable for on-call alerting is the wrong product; the real and freshly-vacated gap is push delivery for self-hosted alerting after Grafana OnCall's March 2026 archival."
tags: [parallax, idea, oncall, alerting, wearable, grafana, revenue-experiment]
related: ["docs/ideas/README.md", "docs/ideas/I002-crew-tier-routing-audit.md"]
created_on: 2026-08-04
updated_on: 2026-08-04
status: draft
idea_id: I003
---

# I003: on-call alert delivery for self-hosted monitoring

## The original idea

A dedicated wearable watch for on-call engineers: vibrates on alert, displays service health metrics
like a wrist-sized Grafana. The premise is that people miss pages overnight.

## The premise is right; the form factor is wrong

The pain is real and well-documented — missed overnight pages are why PagerDuty has a business. But
three things argue against building hardware.

**Everything the device does already runs on hardware people own.** Vibration on alert, a metric
readout, an acknowledge button — all of it is a watch *app*, on a watch the target user already
wears. The differentiating value is entirely software; the hardware contributes cost, certification,
firmware, supply chain, returns, and a support burden, and contributes nothing that Apple and
Samsung have not already commoditised.

**A wrist is the wrong actuator for the hard case.** The unsolved part of "can't wake up" is not
notification routing — iOS Critical Alerts and Android DND-bypass channels already punch through
silent modes. It is that **wrist vibration is a weak waking stimulus for a deep sleeper.** The
market that had to solve exactly this problem — deaf and hard-of-hearing alarm clocks — converged
on **bed shakers**, not wrist devices, decades ago. If the requirement is "reliably wake a sleeping
adult by vibration," the answer is a transducer under the mattress driven by a webhook, which is a
weekend project with a smart plug, not a hardware company.

**It is the wrong product to start with a two-week interview horizon and a $272/month burn.**

## The real gap, and it opened four months ago

**Grafana OnCall OSS entered maintenance mode on 2025-03-11 and was archived on 2026-03-24.** The
Cloud Connection that relayed SMS, phone, and push notifications was deprecated the same day.
Every self-hosted Grafana OnCall user lost mobile push in March 2026. Grafana's official migration
path is Grafana Cloud IRM — **cloud-only, with no self-hosted option**, which is precisely the thing
this cohort chose to avoid.

Separately, **PagerDuty's Apple Watch app is effectively abandoned**: it shows the on-call schedule
and little else. Community requests to acknowledge, snooze, resolve, or view incident detail on the
wrist date to 2019–2021 and remain unimplemented.

So there are two adjacent gaps, both software:

1. **Push delivery for self-hosted alerting** — the stranded Grafana OnCall cohort needs a relay
   they can run themselves, or a thin hosted relay that speaks to a self-hosted Alertmanager.
2. **Wrist-side interaction quality** — acknowledge and resolve from the watch, which the incumbent
   does not do well.

## The one genuinely novel feature

**Sleep-stage-aware escalation.** The watch already estimates sleep stage. Escalate modality and
intensity as a function of it — gentle haptic in light sleep, full alarm plus bed-shaker relay in
deep sleep — and stop escalating once motion indicates the user is awake. Nobody does this. It is
defensible, it is software on existing hardware, and it connects directly to the R03 wearables
work. It is a feature, not a company, but it is the thing that would make a demo memorable.

## The honest objection

**The segment with the pain is the segment least willing to pay.** People self-host alerting
specifically to avoid PagerDuty's per-seat pricing. The enterprises that pay $21+/user/month are
already served and will not switch to an indie tool for compliance reasons. So the addressable
revenue may be close to zero even if the product is good and the need is real.

That objection is strong enough that it should be tested *before* any building.

## As a preregistered revenue experiment

Per the constellation self-sufficiency doctrine, this is a demand hypothesis, not a build decision.

- **Hypothesis:** the stranded Grafana OnCall OSS cohort will pay for self-hostable push delivery.
- **Cheapest evidence:** the migration cohort is searching *right now* — comparison and
  "alternatives" articles cluster around the March 2026 archival. Measure search interest for
  Grafana OnCall alternatives, count GitHub issues and forum threads about lost push, and check
  whether existing free alternatives (GoAlert, OneUptime) already absorbed them.
- **Metric:** ten unsolicited expressions of willingness to pay, from a landing page and posts in
  the relevant communities, before any code.
- **Budget:** one weekend and no hardware spend.
- **Kill date:** two weeks from start. If the free alternatives already cover it, kill it —
  competing with free, self-hostable, and adequate is not a business.

## Revision 2026-08-04: the reframe, and it is a better idea

Daniel: *"I would never buy a fitness watch, but I'd consider a customizable watch I can connect to
WiFi and make API requests to display whatever I want — checking my Linux box, or my agents. I
don't like to keep my Linux box on because I am not tracking what's going on."*

That last sentence is the actual product. The job is not **alerting** — it is **ambient awareness of
an unattended machine**, and the outcome it buys is being *willing to leave the box running*. That
is a different and better-specified need than "wake me for a page," and it is one Daniel has
himself.

### The hardware already exists — twice — so do not build it

**Pebble is back and fully open source.** Eric Migicovsky's Core Devices reacquired the trademark
and open-sourced the entire stack: watch OS, iOS and Android companion apps, developer tools, and
the app-store backend, plus published electrical and mechanical design files. Pebble Time 2 began
shipping January 2026; Pebble 2 Duo claims up to 30 days of battery. This is, almost exactly, the
described product.

**Watchy (SQFMI)** is the hacker version: ESP32-S3, e-ink, WiFi and BLE, MIT-licensed,
OSHWA-certified, programmable in Arduino, MicroPython, or ESP-IDF, reprogrammable over WiFi, and
explicitly built for pulling internet APIs. LILYGO's T-Watch S3 and T-Wrist are adjacent options.

So the build collapses to firmware plus a data plane, which is the interesting part anyway.

### The harder question: is a watch the right surface?

For desk-adjacent ambient awareness a **small always-on display is strictly better** — larger,
permanently in view, no wrist real estate, no battery anxiety, no arm-raise. The watch wins only
when away from the desk, and when away, a phone push is usually adequate. The watch's genuine
advantage is narrow: a passive glance without unlocking anything.

Worth deciding honestly whether the anxiety is *while at the desk* or *while away*, because the
answer picks the form factor and they are not the same product.

### The actual hard part is the signal, not the display

"I am not tracking what's going on" is a **monitoring** problem. The missing piece is an aggregated
health signal — one value, or one colour, meaning fine / degraded / needs you — derived from run
state, worker liveness, disk, and queue depth. Building a watch first means building a renderer for
a signal that does not exist yet.

That signal is cheap to prototype and the data sources already exist in the bridge (`agent_run_list`,
`workflow_run_status`, run records). A single HTTP endpoint returning one status value, or a Cowork
artifact that polls it, is a same-day build.

### Sequencing, and the cheap falsification

1. Define the aggregate health signal and expose it at one endpoint.
2. Render it somewhere zero-cost — a browser tab, a Cowork artifact, a terminal strip.
3. **Test the actual hypothesis:** does ambient visibility change willingness to leave the box
   running? Run it for a week and observe whether the box stays up.
4. Only if step 3 succeeds does the display surface matter — and then buy a Pebble or a Watchy
   rather than building hardware.

If a browser tab showing one status colour does not resolve the anxiety, a watch will not either.
That is the whole experiment, and it costs a day.

## Related but separate: the bed shaker

Worth noting as a private tool regardless of the product question. An Alertmanager webhook driving
a smart plug and a vibration transducer solves Daniel's own on-call wake-up problem for well under
$50, needs no company, and would generate the operational experience that any version of this
product would need anyway.
