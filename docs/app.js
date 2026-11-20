import { profiles } from './profiles.js';
import { calculate, rpmLimit } from './model.js';

const form = document.querySelector('#calculator');
const selector = document.querySelector('#profile');
const mode = document.querySelector('#mode');
const format = (digits = 0) => new Intl.NumberFormat('et-EE', {
  minimumFractionDigits: digits, maximumFractionDigits: digits,
});
const integer = format();
const decimal = format(2);
const fuelFormat = format(1);
const start = Math.PI * .75;
const sweep = Math.PI * 1.5;
const centerX = 100;
const centerY = 82;
const radius = 70;
const gauges = [
  ['volume', 'L', decimal],
  ['rpm', 'p/min', integer],
  ['temperature', '°C', integer],
].map(([id, unit, numberFormat]) => {
  const input = document.querySelector('#' + id);
  const canvas = input.parentElement.querySelector('canvas');
  return { input, canvas, unit, numberFormat };
});

profiles.forEach((profile, index) => selector.add(new Option(profile.name, index)));
selector.value = String(profiles.findIndex(profile => profile.name === '2.0L R6 Bensiin'));
document.querySelector('#profile-count').textContent = profiles.length + ' profiili';

function drawGauge({ canvas, input, unit, numberFormat }) {
  const ratio = window.devicePixelRatio || 1;
  const width = Math.ceil(200 * ratio);
  const height = Math.ceil(165 * ratio);
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
  const context = canvas.getContext('2d');
  context.setTransform(width / 200, 0, 0, height / 165, 0, 0);
  context.clearRect(0, 0, 200, 165);

  function arc(r, from, to, color, lineWidth) {
    context.beginPath();
    context.arc(centerX, centerY, r, from, to);
    context.strokeStyle = color;
    context.lineWidth = lineWidth;
    context.stroke();
  }

  const value = input.valueAsNumber;
  const fraction = (value - Number(input.min)) / (Number(input.max) - Number(input.min));
  const angle = start + sweep * fraction;
  context.beginPath();
  context.arc(centerX, centerY, radius + 8, 0, Math.PI * 2);
  context.fillStyle = '#101823';
  context.fill();
  arc(radius, start, start + sweep, '#344459', 5);
  if (fraction > 0) arc(radius, start, angle, '#5fe0b6', 5);

  for (let index = 0; index <= 40; index++) {
    const tick = start + sweep * index / 40;
    const major = index % 5 === 0;
    context.beginPath();
    context.moveTo(centerX + Math.cos(tick) * 62, centerY + Math.sin(tick) * 62);
    context.lineTo(centerX + Math.cos(tick) * (major ? 54 : 58),
                   centerY + Math.sin(tick) * (major ? 54 : 58));
    context.strokeStyle = major ? '#c4d0df' : '#52677f';
    context.lineWidth = 1;
    context.stroke();
  }

  context.beginPath();
  context.moveTo(centerX, centerY);
  context.lineTo(centerX + Math.cos(angle) * 50, centerY + Math.sin(angle) * 50);
  context.strokeStyle = '#edf3fa';
  context.lineWidth = 3;
  context.stroke();
  context.beginPath();
  context.arc(centerX, centerY, 5, 0, Math.PI * 2);
  context.fillStyle = '#5fe0b6';
  context.fill();

  const valueText = numberFormat.format(value);
  context.textAlign = 'center';
  context.fillStyle = '#edf3fa';
  context.font = 'bold 23px system-ui';
  context.fillText(valueText, centerX, 121);
  context.fillStyle = '#a8b7c9';
  context.font = '13px system-ui';
  context.fillText(unit, centerX, 142);
  context.fillText(input.min, 34, 154);
  context.fillText(input.max, 166, 154);
  input.setAttribute('aria-valuetext', valueText + ' ' + unit);
}

function selectedProfile() {
  return profiles[Number(selector.value)];
}

function render() {
  const profile = selectedProfile();
  const values = Object.fromEntries(gauges.map(({ input }) => [input.id, input.valueAsNumber]));
  const results = calculate(profile, values);
  const formats = { fuel: fuelFormat, air: decimal, airNeeded: decimal, power: integer, torque: integer };
  for (const [id, value] of Object.entries(results)) {
    document.getElementById(id).textContent = (id === 'power' || id === 'torque' ? '≈ ' : '') +
      formats[id].format(value);
  }
  const custom = Object.keys(values).some(key => values[key] !== profile[key]);
  mode.toggleAttribute('data-custom', custom);
  mode.textContent = custom ? 'Kohandatud töörežiim' : 'Profiili algväärtused';
  gauges.forEach(drawGauge);
}

function reset() {
  const profile = selectedProfile();
  document.querySelector('#rpm').max = rpmLimit(profile);
  for (const { input } of gauges) input.value = profile[input.id];
  render();
}

for (const { canvas, input } of gauges) {
  let lastProgress = null;
  function moveNeedle(event) {
    const box = canvas.getBoundingClientRect();
    const x = (event.clientX - box.left) * 200 / box.width - centerX;
    const y = (event.clientY - box.top) * 165 / box.height - centerY;
    if (Math.hypot(x, y) < radius * .2) return;

    const turn = Math.PI * 2;
    let progress = (Math.atan2(y, x) - start + turn) % turn;
    if (progress > sweep) {
      const useMinimum = lastProgress === null ? progress > (turn + sweep) / 2 : lastProgress < sweep / 2;
      progress = useMinimum ? 0 : sweep;
    }
    lastProgress = progress;
    const min = Number(input.min);
    const step = Number(input.step);
    const offset = progress / sweep * (Number(input.max) - min);
    input.valueAsNumber = Number((min + Math.round(offset / step) * step).toFixed(2));
    render();
  }
  canvas.addEventListener('pointerdown', event => {
    if (!event.isPrimary || event.button !== 0) return;
    lastProgress = null;
    canvas.setPointerCapture(event.pointerId);
    moveNeedle(event);
  });
  canvas.addEventListener('pointermove', event => {
    if (canvas.hasPointerCapture(event.pointerId)) moveNeedle(event);
  });
  input.addEventListener('input', render);
}

selector.addEventListener('change', reset);
form.addEventListener('reset', event => {
  event.preventDefault();
  reset();
});
form.addEventListener('submit', event => event.preventDefault());
reset();
