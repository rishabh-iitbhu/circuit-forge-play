# MOSFET Design Heuristics

This folder contains the current MOSFET selection heuristics used by the recommendation engine.

## Selection Logic Covered

The recommendation logic now evaluates MOSFETs using the following criteria:

1. **VDS survivability**
   - Compute the peak bus voltage as $V_{in,peak} = V_{in,max} \times 1.25$.
   - Derive the required VDS rating with a conservative factor: 0.6 for silicon MOSFETs and 0.7 for SiC parts (unless a different published guideline is available).
   - Reject candidates whose VDS rating is lower than the required value.

2. **Drain-current filtering**
   - Require the device current rating to exceed the application requirement by a 20% margin: $I_D \ge 1.2 \times I_{out,max}$.
   - This prevents undersized parts from being considered.

3. **SOA and avalanche documentation**
   - Prefer parts with documented DC SOA and pulsed SOA curves.
   - Give additional credit when avalanche energy information is available.
   - Also consider whether repetitive avalanche capability is documented.

4. **RDS(on) and temperature behavior**
   - Prefer lower RDS(on), especially when a 100-125°C value is available.
   - Compare parts using elevated-temperature data rather than room-temperature values alone.
   - Apply a small penalty for high-frequency switching losses when the part is used at high frequency.

5. **VGS protection and gate-drive compatibility**
   - Check that documented VGS limits support common gate-drive voltages.
   - Prefer MOSFETs that are compatible with practical drive rails such as 10-12 V or 12-20 V.

6. **dv/dt immunity and gate-charge balance**
   - Review Qgd/Qgs ratio as a proxy for switching robustness.
   - Lower ratios are preferred because they indicate better immunity to Miller-induced turn-on and gate-loop ringing.
   - Use Qgd data to explain gate-drive energy and switching-loss trade-offs.

7. **Package inductance**
   - Prefer lower package inductance because it reduces switching-node ringing and dv/dt susceptibility.
   - This is especially important for fast switching and compact layouts.

8. **Gate-drive sensitivity and transconductance**
   - Lower Qgd reduces gate-drive energy but can increase dv/dt and EMI risk.
   - Higher gm/transconductance can make the device more sensitive to gate-voltage ringing and VGS overshoot/undershoot.
   - The recommendation text should explain these trade-offs when the data is available.

9. **Reverse-recovery behavior**
   - Use Qrr when available as the primary indicator of body-diode recovery stress.
   - If Qrr is not present, use Irr and trr information.
   - Lower recovery charge/current/time is preferred because it reduces ringing, loss, and EMI.
   - Higher temperature and higher commutation current typically increase recovery stress.
   - Slowing the rise of the opposite gate-drive pulse can help reduce reverse-recovery current.

## Notes for Documentation Authors

- If a value is missing from the component database, the reasoning should say so explicitly rather than silently omitting the check.
- The selection engine should explain both the pass/fail filter steps and the comparative trade-offs that affected the final ranking.
- These heuristics are intended to support practical design decisions, not replace a full datasheet review.