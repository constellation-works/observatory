// Declarative control panel — kills the slider/button boilerplate every sim
// used to re-implement by hand.
//
//   const panel = createPanel([
//     { type: 'button', label: 'Pause', onClick: (btn) => { ... } },
//     { type: 'range',  key: 'speed', label: 'Speed', min: 1, max: 200, value: 30,
//       format: (v) => `${v} days/sec` },
//     { type: 'toggle', key: 'trails', label: 'Trails', value: true },
//     { type: 'select', key: 'view', label: 'View', options: ['inner', 'full'] },
//     { type: 'readout', key: 'energy' },
//   ], { mount: document.getElementById('controls') });
//
//   panel.values.speed          // current slider value (number)
//   panel.set('speed', 60)      // programmatic update (fires onChange)
//   panel.setReadout('energy', 'E = -1.234')
//
// Styling comes from lib/web/style.css (.orrery-controls).
//
// Accessibility, relied on by _lib/web/chapter.js: every labelled control gets a
// generated id with its <label for>, the value readout is an aria-live region
// referenced by aria-describedby, and toggles carry aria-pressed. Native range,
// select and button elements are used throughout, so Tab / arrows / Enter / Space
// work without extra key handling.
let uid = 0;
const nextId = (key) => `ctl-${key ?? 'x'}-${++uid}`;

export function createPanel(defs, { mount = document.body, className = 'orrery-controls' } = {}) {
  const el = document.createElement('div');
  el.className = className;
  const values = {};
  const controls = {}; // key -> { input?, out?, def }

  for (const def of defs) {
    switch (def.type) {
      case 'button': {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = def.label;
        if (def.title) btn.title = def.title;
        if (def.ariaLabel) btn.setAttribute('aria-label', def.ariaLabel);
        btn.addEventListener('click', () => def.onClick?.(btn));
        el.appendChild(btn);
        if (def.key) controls[def.key] = { input: btn, def };
        break;
      }
      case 'range': {
        const id = nextId(def.key);
        const outId = `${id}-out`;
        const label = document.createElement('label');
        label.textContent = def.label ?? def.key;
        label.htmlFor = id;
        const input = document.createElement('input');
        input.id = id;
        input.type = 'range';
        input.min = def.min ?? 0;
        input.max = def.max ?? 1;
        input.step = def.step ?? 'any';
        input.value = def.value ?? def.min ?? 0;
        const out = document.createElement('span');
        out.className = 'readout';
        out.id = outId;
        out.setAttribute('aria-live', 'polite');
        input.setAttribute('aria-describedby', outId);
        const fmt = def.format ?? ((v) => String(v));
        const update = () => {
          values[def.key] = Number(input.value);
          out.textContent = fmt(values[def.key]);
          input.setAttribute('aria-valuetext', out.textContent);
        };
        input.addEventListener('input', () => { update(); def.onChange?.(values[def.key]); });
        update();
        el.append(label, input, out);
        controls[def.key] = { input, out, def };
        break;
      }
      case 'toggle': {
        const btn = document.createElement('button');
        btn.type = 'button';
        values[def.key] = !!def.value;
        const paint = () => {
          btn.textContent = def.label ?? def.key;
          btn.classList.toggle('active', values[def.key]);
          btn.setAttribute('aria-pressed', String(values[def.key]));
        };
        btn.addEventListener('click', () => {
          values[def.key] = !values[def.key];
          paint();
          def.onChange?.(values[def.key]);
        });
        paint();
        el.appendChild(btn);
        controls[def.key] = { input: btn, def };
        break;
      }
      case 'select': {
        const id = nextId(def.key);
        const label = document.createElement('label');
        label.textContent = def.label ?? def.key;
        label.htmlFor = id;
        const sel = document.createElement('select');
        sel.id = id;
        for (const opt of def.options) {
          const o = document.createElement('option');
          if (typeof opt === 'object') { o.value = opt.value; o.textContent = opt.label; }
          else { o.value = opt; o.textContent = opt; }
          sel.appendChild(o);
        }
        if (def.value != null) sel.value = def.value;
        values[def.key] = sel.value;
        sel.addEventListener('change', () => {
          values[def.key] = sel.value;
          def.onChange?.(sel.value);
        });
        el.append(label, sel);
        controls[def.key] = { input: sel, def };
        break;
      }
      case 'readout': {
        const out = document.createElement('span');
        out.className = 'readout';
        out.id = nextId(def.key);
        out.setAttribute('aria-live', def.live ?? 'polite');
        out.textContent = def.value ?? '';
        el.appendChild(out);
        controls[def.key] = { out, def };
        break;
      }
      default:
        throw new Error(`panel: unknown control type '${def.type}'`);
    }
  }

  mount.appendChild(el);
  return {
    el,
    values,
    controls,
    get: (key) => values[key],
    element: (key) => controls[key]?.input,
    set(key, val) {
      const c = controls[key];
      if (!c?.input) return;
      c.input.value = val;
      c.input.dispatchEvent(new Event(c.def.type === 'select' ? 'change' : 'input'));
    },
    setLabel(key, text) {
      const c = controls[key];
      if (c?.input) c.input.textContent = text;
    },
    setReadout(key, text) {
      const c = controls[key];
      if (c?.out) c.out.textContent = text;
    },
  };
}
