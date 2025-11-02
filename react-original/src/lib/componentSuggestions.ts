import { mosfetLibrary, capacitorLibrary, inductorLibrary, MOSFET, Capacitor, Inductor } from "./componentData";

export interface ComponentSuggestion<T> {
  component: T;
  reason: string;
  score: number;
}

export function suggestMOSFETs(
  maxVoltage: number,
  maxCurrent: number,
  preferLowRdson: boolean = true
): ComponentSuggestion<MOSFET>[] {
  const voltageMargin = 1.5; // 50% margin for safety
  const currentMargin = 1.3; // 30% margin for safety

  const suitable = mosfetLibrary
    .filter((m) => m.vds >= maxVoltage * voltageMargin && m.id >= maxCurrent * currentMargin)
    .map((mosfet) => {
      let score = 100;
      let reasons: string[] = [];

      // Voltage headroom scoring
      const voltageHeadroom = (mosfet.vds / maxVoltage - voltageMargin) * 10;
      score += Math.min(voltageHeadroom, 20);

      // Current headroom scoring
      const currentHeadroom = (mosfet.id / maxCurrent - currentMargin) * 5;
      score += Math.min(currentHeadroom, 15);

      // RDS(on) scoring - lower is better
      const avgRdson = mosfetLibrary.reduce((sum, m) => sum + m.rdson, 0) / mosfetLibrary.length;
      if (mosfet.rdson < avgRdson * 0.5) {
        score += 30;
        reasons.push("Excellent low RDS(on) for minimal conduction losses");
      } else if (mosfet.rdson < avgRdson) {
        score += 15;
        reasons.push("Good RDS(on) for efficient operation");
      }

      // Qg scoring - lower is better for high frequency
      const qgNum = typeof mosfet.qg === 'number' ? mosfet.qg : 0;
      if (qgNum > 0 && qgNum < 30) {
        score += 20;
        reasons.push("Low gate charge for fast switching and reduced gate drive losses");
      } else if (qgNum > 0 && qgNum < 50) {
        score += 10;
        reasons.push("Moderate gate charge suitable for the application");
      }

      // Efficiency bonus
      const efficiency = parseFloat(mosfet.efficiencyRange.split('–')[0]);
      if (efficiency >= 96) {
        score += 25;
        reasons.push(`High efficiency range (${mosfet.efficiencyRange})`);
      } else if (efficiency >= 94) {
        score += 15;
        reasons.push(`Good efficiency range (${mosfet.efficiencyRange})`);
      }

      // Package consideration
      if (mosfet.package.includes("SuperSO8") || mosfet.package.includes("SO-8")) {
        reasons.push("Compact SMD package for easy PCB integration");
      } else if (mosfet.package.includes("TO-220")) {
        reasons.push("Standard TO-220 package with good thermal performance");
      }

      // Add voltage and current margins
      reasons.unshift(
        `${Math.round((mosfet.vds / maxVoltage - 1) * 100)}% voltage margin, ${Math.round((mosfet.id / maxCurrent - 1) * 100)}% current margin`
      );

      return {
        component: mosfet,
        reason: reasons.join("; "),
        score,
      };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  return suitable;
}

export function suggestCapacitors(
  requiredCapacitance: number,
  maxVoltage: number,
  preferLowESR: boolean = true
): ComponentSuggestion<Capacitor>[] {
  const voltageMargin = 1.5; // 50% margin
  const capacitanceRange = 0.7; // Accept 70% to 150% of required value

  const suitable = capacitorLibrary
    .filter(
      (c) =>
        c.voltage >= maxVoltage * voltageMargin &&
        c.capacitance >= requiredCapacitance * capacitanceRange
    )
    .map((cap) => {
      let score = 100;
      let reasons: string[] = [];

      // Voltage headroom
      const voltageHeadroom = (cap.voltage / maxVoltage - voltageMargin) * 10;
      score += Math.min(voltageHeadroom, 20);

      // Capacitance matching - closer to required is better
      const capRatio = cap.capacitance / requiredCapacitance;
      if (capRatio >= 0.9 && capRatio <= 1.2) {
        score += 30;
        reasons.push("Excellent capacitance match for required value");
      } else if (capRatio >= 0.7 && capRatio <= 1.5) {
        score += 15;
        reasons.push("Good capacitance value for the application");
      }

      // ESR consideration
      const esrValue = cap.esr.toLowerCase();
      if (esrValue.includes("low") || parseFloat(esrValue) < 10) {
        score += 25;
        reasons.push("Low ESR for excellent ripple current handling");
      } else if (parseFloat(esrValue) < 50) {
        score += 15;
        reasons.push("Moderate ESR suitable for the application");
      }

      // Type consideration
      if (cap.type.includes("Polymer")) {
        score += 20;
        reasons.push("Polymer type for superior ripple performance and long life");
      } else if (cap.type.includes("MLCC")) {
        score += 15;
        reasons.push("MLCC type for compact size and high-frequency performance");
      } else if (cap.type.includes("Electrolytic")) {
        reasons.push("Electrolytic type for high capacitance in bulk applications");
      }

      // Add specific use case
      reasons.push(`Ideal for: ${cap.primaryUse}`);

      // Voltage margin
      reasons.unshift(
        `${Math.round((cap.voltage / maxVoltage - 1) * 100)}% voltage margin, ${cap.capacitance}µF capacitance`
      );

      return {
        component: cap,
        reason: reasons.join("; "),
        score,
      };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  return suitable;
}

export function suggestInductors(
  requiredInductance: number,
  maxCurrent: number
): ComponentSuggestion<Inductor>[] {
  const currentMargin = 1.3; // 30% margin
  const inductanceRange = 0.8; // Accept 80% to 120% of required value

  const suitable = inductorLibrary
    .filter(
      (l) =>
        l.current >= maxCurrent * currentMargin &&
        l.satCurrent >= maxCurrent * 1.2 &&
        l.inductance >= requiredInductance * inductanceRange &&
        l.inductance <= requiredInductance * 1.2
    )
    .map((ind) => {
      let score = 100;
      let reasons: string[] = [];

      // Current headroom
      const currentHeadroom = (ind.current / maxCurrent - currentMargin) * 10;
      score += Math.min(currentHeadroom, 20);

      // Saturation current headroom
      const satHeadroom = (ind.satCurrent / maxCurrent - 1.2) * 10;
      score += Math.min(satHeadroom, 20);

      // Inductance matching
      const indRatio = ind.inductance / requiredInductance;
      if (indRatio >= 0.95 && indRatio <= 1.05) {
        score += 30;
        reasons.push("Excellent inductance match for required value");
      } else if (indRatio >= 0.8 && indRatio <= 1.2) {
        score += 15;
        reasons.push("Good inductance value for the application");
      }

      // DCR consideration - lower is better
      const avgDcr = inductorLibrary.reduce((sum, l) => sum + l.dcr, 0) / inductorLibrary.length;
      if (ind.dcr < avgDcr * 0.5) {
        score += 25;
        reasons.push("Very low DCR for minimal copper losses");
      } else if (ind.dcr < avgDcr) {
        score += 15;
        reasons.push("Low DCR for good efficiency");
      }

      // Package consideration
      if (ind.package.includes("SMD") || ind.package.includes("SER")) {
        reasons.push("Compact SMD package for easy assembly");
      } else {
        reasons.push(`${ind.package} package for robust mounting`);
      }

      // Current margins
      reasons.unshift(
        `${ind.inductance}µH inductance, ${Math.round((ind.satCurrent / maxCurrent - 1) * 100)}% saturation current margin`
      );

      return {
        component: ind,
        reason: reasons.join("; "),
        score,
      };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  return suitable;
}
