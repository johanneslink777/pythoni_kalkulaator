const ambientPressure = 1.01325;
const dieselCurve = [
  [600, .62, 0], [1000, .72, .12], [1800, .86, .8], [2500, .9, 1],
  [3500, .86, 1], [4500, .7, .8], [5000, .55, .6],
];
const petrolCurve = [
  [600, .55, 0], [1000, .65, .05], [2000, .78, .4], [3000, .85, .85],
  [4500, .92, 1], [6000, .85, .95], [7500, .65, .75],
];

export function rpmLimit(profile) {
  return (profile.diesel ? dieselCurve : petrolCurve).at(-1)[0];
}

export function calculate(profile, { volume, rpm, temperature }) {
  const curve = profile.diesel ? dieselCurve : petrolCurve;
  const index = curve.findIndex(([pointRpm], i) => i > 0 && rpm <= pointRpm);
  if (index < 1 || rpm < curve[0][0]) throw new RangeError('Pöörded on väljaspool mudeli vahemikku.');

  const [leftRpm, leftFill, leftBoost] = curve[index - 1];
  const [rightRpm, rightFill, rightBoost] = curve[index];
  const fraction = (rpm - leftRpm) / (rightRpm - leftRpm);
  const fill = leftFill + fraction * (rightFill - leftFill);
  const boost = leftBoost + fraction * (rightBoost - leftBoost);
  const pressure = ambientPressure + (profile.pressure - ambientPressure) * boost;
  const density = pressure * 100000 / (287.05 * (temperature + 273.15));
  const air = volume * rpm / 2 * fill * density / 1000;
  const fuel = air * 1000 / profile.ratio;
  const [energy, efficiency] = profile.diesel ? [42.6, .32] : [43.5, .24];
  const power = fuel * energy / 60 * efficiency;
  const torque = power * 60000 / (2 * Math.PI * rpm);
  return { air, airNeeded: air, fuel, power, torque };
}
