# Cobalt UI — Design System Reference

**How to use this file with your AI tool (v0, Lovable, Bolt, Cursor, Claude):**
1. Paste this ENTIRE file into your tool as context (or attach it) and say: *"Use the Cobalt UI design system in this file for all styling and components."*
2. Add the **CSS tokens** (section 1) to your global stylesheet, and merge the **Tailwind config** (section 2) into `tailwind.config.js`.
3. Load the font once in `<head>`:
   `<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">`
4. Dark mode: add `class="dark"` to `<html>` — every token flips automatically; components need no changes.
5. Copy any component from section 3 as-is. Only dependencies: React + Tailwind (+ `lucide-react` for icons).

**Rules the system enforces** (keep these in your prompts):
- Cobalt `primary` for primary actions/links. Volt green is a RARE highlight — one per view max, always dark text on it, never body text color, never borders-only meaning.
- Pill (fully rounded) buttons and chips. Cards/inputs use `rounded-lg`.
- Every interactive element shows a visible focus ring (`focus-visible` styles included).
- Meet WCAG AA: shipped pairings all pass 4.5:1 (text) / 3:1 (UI). Don't put white text on volt or light-blue.
- Respect `prefers-reduced-motion` (tokens include it).

---

## 1. Design tokens (CSS custom properties)

```css
:root {
  /* ---- Brand core (from brand guidelines) ---- */
  --cobalt-50:#E8EFFC; --cobalt-100:#D2E0FA; --cobalt-200:#A6C1F4; --cobalt-300:#79A1ED;
  --cobalt-400:#4D7FE3; --cobalt-500:#1F5FD6; --cobalt-600:#004ACB; --cobalt-700:#003DA8;
  --cobalt-800:#002F82; --cobalt-900:#00235E;
  --volt-300:#E3FF66; --volt-400:#D9FF33; --volt-500:#CEFF00; --volt-600:#A5CC00; --volt-700:#647A00;
  --navy-950:#10122E; --navy-900:#1C1F48; /* brand Dark Blue */
  --ice:#E9F1F7;                            /* brand Light Blue */
  /* ---- Neutrals (navy-tinted, extrapolated) ---- */
  --neutral-0:#FFFFFF; --neutral-50:#F6F8FB; --neutral-100:#E9EDF4; --neutral-200:#D4DAE7;
  --neutral-300:#B0B8CC; --neutral-400:#8891AB; --neutral-500:#67718F; --neutral-600:#4D5674;
  --neutral-700:#363E5C; --neutral-800:#262C4A; --neutral-900:#1C1F48; --neutral-950:#10122E;
  /* ---- Semantic status (accessible defaults, not in brand doc) ---- */
  --success-600:#0E7A43; --success-100:#DCF5E7; --success-300:#5BD598;
  --warning-600:#A16207; --warning-100:#FBF0D4; --warning-300:#F5C64C;
  --error-600:#C22C1F;  --error-100:#FBE3E0;  --error-300:#F2988E;
  --info-600:#0B62B8;   --info-100:#DEEDFB;   --info-300:#7DBCF0;

  /* ---- Semantic aliases (LIGHT) — components use ONLY these ---- */
  --bg:#FFFFFF; --bg-subtle:#F6F8FB; --bg-section:#E9F1F7; --bg-inverse:#1C1F48;
  --surface:#FFFFFF; --surface-raised:#FFFFFF; --surface-overlay:rgba(28,31,72,0.5);
  --text:#1C1F48; --text-secondary:#4D5674; --text-muted:#67718F; --text-inverse:#FFFFFF;
  --text-on-primary:#FFFFFF; --text-on-accent:#1C1F48;
  --border:#D4DAE7; --border-strong:#B0B8CC; --border-focus:#004ACB;
  --primary:#004ACB; --primary-hover:#003DA8; --primary-active:#002F82; --primary-subtle:#E8EFFC;
  --accent:#CEFF00; --accent-hover:#D9FF33; --accent-subtle:#F4FFC2;
  --success:#0E7A43; --success-bg:#DCF5E7; --warning:#A16207; --warning-bg:#FBF0D4;
  --error:#C22C1F; --error-bg:#FBE3E0; --info:#0B62B8; --info-bg:#DEEDFB;
  --ring:0 0 0 2px var(--bg), 0 0 0 4px var(--border-focus);

  /* ---- Typography ---- */
  --font-sans:'Instrument Sans','Helvetica Neue',Helvetica,Arial,sans-serif;
  --text-display:4.5rem; --lh-display:1.02; --ls-display:-0.02em;  /* 72pt H1, brand */
  --text-h1:3rem;   --lh-h1:1.08;  --ls-h1:-0.015em;               /* 48 */
  --text-h2:2.25rem;--lh-h2:1.15;  --ls-h2:-0.01em;                /* 36 */
  --text-h3:1.875rem;--lh-h3:1.2;                                  /* 30 */
  --text-h4:1.5rem; --lh-h4:1.3;                                   /* 24, extrapolated */
  --text-lg:1.125rem;--lh-lg:1.6;                                  /* 18 body, brand */
  --text-base:1rem; --lh-base:1.55;                                /* 16 UI/buttons */
  --text-sm:0.875rem;--lh-sm:1.5;  --text-xs:0.75rem; --lh-xs:1.45;
  --weight-regular:400; --weight-medium:500; --weight-semibold:600;

  /* ---- Spacing (4px base) ---- */
  --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px; --space-5:20px;
  --space-6:24px; --space-8:32px; --space-10:40px; --space-12:48px; --space-16:64px;
  --space-20:80px; --space-24:96px;

  /* ---- Radius / borders ---- */
  --radius-sm:6px; --radius-md:10px; --radius-lg:16px; --radius-xl:24px; --radius-full:9999px;
  --border-1:1px; --border-2:2px;

  /* ---- Elevation (brand dot shadow: #000 @ 18%, blur 3–10) ---- */
  --shadow-sm:0 1px 3px rgba(0,0,0,0.10);
  --shadow-md:0 2px 6px rgba(0,0,0,0.12);
  --shadow-lg:0 6px 16px rgba(16,18,46,0.14);
  --shadow-xl:0 12px 32px rgba(16,18,46,0.18);

  /* ---- Z-index ---- */
  --z-nav:100; --z-dropdown:200; --z-overlay:300; --z-modal:400; --z-popover:500; --z-toast:600;

  /* ---- Motion ---- */
  --duration-fast:150ms; --duration-base:250ms; --duration-slow:400ms;
  --ease-standard:cubic-bezier(0.2,0,0,1); --ease-enter:cubic-bezier(0,0,0.2,1);
  --ease-exit:cubic-bezier(0.4,0,1,1);
}

.dark {
  --bg:#0B0D1A; --bg-subtle:#12141F; --bg-section:#151827; --bg-inverse:#E9F1F7;
  --surface:#12141F; --surface-raised:#1A1D2B; --surface-overlay:rgba(4,5,12,0.7);
  --text:#E9F1F7; --text-secondary:#A8AFC2; --text-muted:#7E869C; --text-inverse:#1C1F48;
  --text-on-primary:#FFFFFF; --text-on-accent:#1C1F48;
  --border:#272B3D; --border-strong:#3D4258; --border-focus:#79A1ED;
  --primary:#4D7FE3; --primary-hover:#79A1ED; --primary-active:#A6C1F4; --primary-subtle:#1A2A55;
  --accent:#CEFF00; --accent-hover:#D9FF33; --accent-subtle:#3A4200;
  --success:#5BD598; --success-bg:#0B3B23; --warning:#F5C64C; --warning-bg:#3E2E06;
  --error:#F2988E; --error-bg:#4A1610; --info:#7DBCF0; --info-bg:#0A2E4E;
  --shadow-sm:0 1px 3px rgba(0,0,0,0.4); --shadow-md:0 2px 6px rgba(0,0,0,0.45);
  --shadow-lg:0 6px 16px rgba(0,0,0,0.5); --shadow-xl:0 12px 32px rgba(0,0,0,0.55);
}

html { font-family:var(--font-sans); color:var(--text); background:var(--bg); }
*:focus-visible { outline:none; box-shadow:var(--ring); border-radius:var(--radius-sm); }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration:0.01ms !important; transition-duration:0.01ms !important; }
}
```

## 2. Tailwind config

```js
// tailwind.config.js — v3. (Tailwind v4: put these in @theme instead.)
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{js,jsx,ts,tsx,html}'],
  theme: {
    extend: {
      fontFamily: { sans: ['Instrument Sans','Helvetica Neue','Arial','sans-serif'] },
      colors: {
        cobalt: {50:'#E8EFFC',100:'#D2E0FA',200:'#A6C1F4',300:'#79A1ED',400:'#4D7FE3',500:'#1F5FD6',600:'#004ACB',700:'#003DA8',800:'#002F82',900:'#00235E'},
        volt: {300:'#E3FF66',400:'#D9FF33',500:'#CEFF00',600:'#A5CC00',700:'#647A00'},
        navy: {900:'#1C1F48',950:'#10122E'},
        ice: '#E9F1F7',
        neutral: {0:'#FFFFFF',50:'#F6F8FB',100:'#E9EDF4',200:'#D4DAE7',300:'#B0B8CC',400:'#8891AB',500:'#67718F',600:'#4D5674',700:'#363E5C',800:'#262C4A',900:'#1C1F48',950:'#10122E'},
        // semantic aliases -> CSS vars, so dark mode is automatic
        bg:'var(--bg)','bg-subtle':'var(--bg-subtle)','bg-section':'var(--bg-section)',
        surface:'var(--surface)','surface-raised':'var(--surface-raised)',
        body:'var(--text)',secondary:'var(--text-secondary)',muted:'var(--text-muted)',
        line:'var(--border)','line-strong':'var(--border-strong)',
        primary:{DEFAULT:'var(--primary)',hover:'var(--primary-hover)',active:'var(--primary-active)',subtle:'var(--primary-subtle)'},
        accent:{DEFAULT:'var(--accent)',hover:'var(--accent-hover)',subtle:'var(--accent-subtle)'},
        success:{DEFAULT:'var(--success)',bg:'var(--success-bg)'},
        warning:{DEFAULT:'var(--warning)',bg:'var(--warning-bg)'},
        error:{DEFAULT:'var(--error)',bg:'var(--error-bg)'},
        info:{DEFAULT:'var(--info)',bg:'var(--info-bg)'},
      },
      fontSize: {
        display:['4.5rem',{lineHeight:'1.02',letterSpacing:'-0.02em',fontWeight:'500'}],
        h1:['3rem',{lineHeight:'1.08',letterSpacing:'-0.015em',fontWeight:'500'}],
        h2:['2.25rem',{lineHeight:'1.15',letterSpacing:'-0.01em',fontWeight:'500'}],
        h3:['1.875rem',{lineHeight:'1.2',fontWeight:'500'}],
        h4:['1.5rem',{lineHeight:'1.3',fontWeight:'500'}],
        lg:['1.125rem',{lineHeight:'1.6'}], base:['1rem',{lineHeight:'1.55'}],
        sm:['0.875rem',{lineHeight:'1.5'}], xs:['0.75rem',{lineHeight:'1.45'}],
      },
      borderRadius: { sm:'6px', md:'10px', lg:'16px', xl:'24px' },
      boxShadow: {
        sm:'var(--shadow-sm)', md:'var(--shadow-md)', lg:'var(--shadow-lg)', xl:'var(--shadow-xl)',
        ring:'0 0 0 2px var(--bg), 0 0 0 4px var(--border-focus)',
      },
      zIndex: { nav:'100', dropdown:'200', overlay:'300', modal:'400', popover:'500', toast:'600' },
      transitionTimingFunction: { standard:'cubic-bezier(0.2,0,0,1)', enter:'cubic-bezier(0,0,0.2,1)', exit:'cubic-bezier(0.4,0,1,1)' },
      transitionDuration: { fast:'150ms', base:'250ms', slow:'400ms' },
    },
  },
};
```

**Shared focus-ring class used by every component below:**
```js
const RING = 'focus-visible:outline-none focus-visible:shadow-ring';
```

---

## 3. Components (React + Tailwind)

### Button
```jsx
import { Loader2 } from 'lucide-react';
const RING = 'focus-visible:outline-none focus-visible:shadow-ring';

export function Button({ variant='primary', size='md', loading, disabled, icon:Icon, children, className='', ...props }) {
  const sizes = {
    sm:'h-9 px-4 text-sm gap-1.5',            // 36px — pair with ≥8px spacing for touch
    md:'h-11 px-5 text-base gap-2',           // 44px — default, meets touch target
    lg:'h-13 px-7 text-lg gap-2.5',
  };
  const variants = {
    primary:'bg-primary text-white hover:bg-primary-hover active:bg-primary-active',
    accent:'bg-accent text-navy-900 hover:bg-accent-hover active:bg-volt-400', // volt: max one per view
    secondary:'bg-transparent text-body border border-line-strong hover:bg-bg-subtle active:bg-primary-subtle',
    ghost:'bg-transparent text-body hover:bg-bg-subtle active:bg-primary-subtle',
    danger:'bg-error text-white hover:opacity-90 active:opacity-80',
  };
  return (
    <button
      className={`inline-flex items-center justify-center rounded-full font-medium select-none
        transition-colors duration-fast ease-standard ${RING}
        disabled:opacity-45 disabled:pointer-events-none ${sizes[size]} ${variants[variant]} ${className}`}
      disabled={disabled || loading} aria-busy={loading || undefined} {...props}>
      {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> : Icon && <Icon className="h-4 w-4" aria-hidden />}
      {children}
    </button>
  );
}
```
*Do:* one `primary` per section; `accent` (volt) at most once per view. *Don't:* put white text on volt, or use volt for destructive actions.

### IconButton
```jsx
export function IconButton({ icon:Icon, label, variant='ghost', size='md', className='', ...props }) {
  const sizes = { sm:'h-9 w-9', md:'h-11 w-11', lg:'h-12 w-12' };
  const variants = {
    ghost:'text-secondary hover:bg-bg-subtle hover:text-body',
    outline:'border border-line-strong text-secondary hover:bg-bg-subtle hover:text-body',
    primary:'bg-primary text-white hover:bg-primary-hover',
  };
  return (
    <button aria-label={label} title={label}
      className={`inline-flex items-center justify-center rounded-full transition-colors duration-fast ${RING} ${sizes[size]} ${variants[variant]} ${className}`} {...props}>
      <Icon className="h-5 w-5" aria-hidden />
    </button>
  );
}
```
*Do:* always pass `label` — it is the accessible name.

### Link
```jsx
export function TextLink({ children, className='', ...props }) {
  return <a className={`text-primary underline underline-offset-4 decoration-cobalt-200 hover:decoration-primary rounded-sm transition-colors duration-fast ${RING} ${className}`} {...props}>{children}</a>;
}
```
*Do:* keep underlines — color alone can't convey "link" (AA).

### Badge / Tag
```jsx
export function Badge({ tone='neutral', children }) {
  const tones = {
    neutral:'bg-bg-subtle text-secondary border-line',
    primary:'bg-primary-subtle text-primary border-transparent dark:text-cobalt-200',
    accent:'bg-accent text-navy-900 border-transparent',
    success:'bg-success-bg text-success border-transparent',
    warning:'bg-warning-bg text-warning border-transparent',
    error:'bg-error-bg text-error border-transparent',
    info:'bg-info-bg text-info border-transparent',
  };
  return <span className={`inline-flex items-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-medium ${tones[tone]}`}>{children}</span>;
}
```
*Do:* pair status color with a word or icon — never color alone.

### Avatar
```jsx
export function Avatar({ src, name='', size='md' }) {
  const sizes = { sm:'h-8 w-8 text-xs', md:'h-10 w-10 text-sm', lg:'h-14 w-14 text-lg' };
  const initials = name.split(' ').map(w=>w[0]).slice(0,2).join('').toUpperCase();
  return (
    <span className={`relative inline-flex shrink-0 items-center justify-center rounded-full bg-primary-subtle font-medium text-primary dark:text-cobalt-200 overflow-hidden ${sizes[size]}`}>
      {src ? <img src={src} alt={name} className="h-full w-full object-cover" /> : <span aria-hidden>{initials}</span>}
      {!src && <span className="sr-only">{name}</span>}
    </span>
  );
}
```

### Chip (selectable / dismissible)
```jsx
import { X } from 'lucide-react';
export function Chip({ selected, onSelect, onDismiss, children }) {
  return (
    <span className={`inline-flex items-center gap-1 rounded-full border text-sm font-medium transition-colors duration-fast
      ${selected ? 'border-primary bg-primary-subtle text-primary dark:text-cobalt-200' : 'border-line bg-surface text-secondary hover:border-line-strong'}`}>
      <button onClick={onSelect} aria-pressed={selected} className={`px-3 py-1.5 rounded-full ${RING}`}>{children}</button>
      {onDismiss && <button onClick={onDismiss} aria-label={`Remove ${children}`} className={`mr-1 rounded-full p-0.5 hover:bg-bg-subtle ${RING}`}><X className="h-3.5 w-3.5" aria-hidden /></button>}
    </span>
  );
}
```

### Divider
```jsx
export function Divider({ label }) {
  if (!label) return <hr className="border-line" />;
  return (
    <div role="separator" className="flex items-center gap-3 text-xs font-medium uppercase tracking-wide text-muted">
      <span className="h-px flex-1 bg-line" /><span>{label}</span><span className="h-px flex-1 bg-line" />
    </div>
  );
}
```

### Spinner
```jsx
export function Spinner({ size='md', label='Loading' }) {
  const sizes = { sm:'h-4 w-4 border-2', md:'h-6 w-6 border-2', lg:'h-9 w-9 border-[3px]' };
  return (
    <span role="status" className="inline-flex items-center gap-2 text-secondary">
      <span className={`animate-spin rounded-full border-line border-t-primary ${sizes[size]}`} aria-hidden />
      <span className="sr-only">{label}</span>
    </span>
  );
}
```

### Tooltip
```jsx
export function Tooltip({ content, children }) {
  return (
    <span className="group/tt relative inline-flex">
      {children}
      <span role="tooltip" className="pointer-events-none absolute bottom-full left-1/2 z-popover mb-2 -translate-x-1/2 whitespace-nowrap
        rounded-md bg-navy-900 px-2.5 py-1.5 text-xs text-white opacity-0 shadow-md transition-opacity duration-fast
        group-hover/tt:opacity-100 group-focus-within/tt:opacity-100 dark:bg-ice dark:text-navy-900">
        {content}
      </span>
    </span>
  );
}
```
*Don't:* hide critical info in tooltips only (not touch-accessible).

### Skeleton
```jsx
export function Skeleton({ className='h-4 w-full' }) {
  return <span aria-hidden className={`block animate-pulse rounded-md bg-neutral-100 dark:bg-navy-900 ${className}`} />;
}
```

### FormField (label + helper + error wrapper) — the validation pattern
```jsx
export function FormField({ id, label, helper, error, required, children }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-medium text-body">
        {label}{required && <span className="text-error" aria-hidden> *</span>}
      </label>
      {children({ id, 'aria-invalid': !!error || undefined,
        'aria-describedby': error ? `${id}-error` : helper ? `${id}-helper` : undefined })}
      {error
        ? <p id={`${id}-error`} role="alert" className="flex items-center gap-1 text-sm text-error">{error}</p>
        : helper && <p id={`${id}-helper`} className="text-sm text-muted">{helper}</p>}
    </div>
  );
}
// Usage: <FormField id="email" label="Email" error={err}>{p => <Input {...p} />}</FormField>
```

### Input
```jsx
export function Input({ className='', ...props }) {
  return <input className={`h-11 w-full rounded-md border border-line bg-surface px-3.5 text-base text-body placeholder:text-muted
    transition-colors duration-fast hover:border-line-strong
    focus:border-primary focus:outline-none focus:shadow-ring
    aria-[invalid=true]:border-error disabled:opacity-45 disabled:bg-bg-subtle disabled:pointer-events-none ${className}`} {...props} />;
}
```

### Textarea
```jsx
export function Textarea({ className='', rows=4, ...props }) {
  return <textarea rows={rows} className={`w-full rounded-md border border-line bg-surface px-3.5 py-2.5 text-base text-body placeholder:text-muted
    transition-colors duration-fast hover:border-line-strong focus:border-primary focus:outline-none focus:shadow-ring
    aria-[invalid=true]:border-error disabled:opacity-45 disabled:bg-bg-subtle ${className}`} {...props} />;
}
```

### Select
```jsx
import { ChevronDown } from 'lucide-react';
export function Select({ className='', children, ...props }) {
  return (
    <span className="relative block">
      <select className={`h-11 w-full appearance-none rounded-md border border-line bg-surface pl-3.5 pr-10 text-base text-body
        transition-colors duration-fast hover:border-line-strong focus:border-primary focus:outline-none focus:shadow-ring
        aria-[invalid=true]:border-error disabled:opacity-45 ${className}`} {...props}>{children}</select>
      <ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" aria-hidden />
    </span>
  );
}
```

### Checkbox
```jsx
export function Checkbox({ label, description, ...props }) {
  return (
    <label className="flex cursor-pointer items-start gap-3 has-[:disabled]:opacity-45 has-[:disabled]:cursor-not-allowed">
      <input type="checkbox" className={`mt-0.5 h-5 w-5 shrink-0 cursor-pointer appearance-none rounded-sm border border-line-strong bg-surface
        transition-colors duration-fast checked:border-primary checked:bg-primary
        checked:bg-[url('data:image/svg+xml,%3Csvg viewBox=%220 0 16 16%22 fill=%22white%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cpath d=%22M12.7 4.7a1 1 0 0 0-1.4-1.4L6.5 8.09 4.7 6.3a1 1 0 0 0-1.4 1.4l2.5 2.5a1 1 0 0 0 1.4 0l5.5-5.5z%22/%3E%3C/svg%3E')]
        bg-center bg-no-repeat ${RING}`} {...props} />
      <span><span className="text-base text-body">{label}</span>
        {description && <span className="block text-sm text-muted">{description}</span>}</span>
    </label>
  );
}
```

### Radio
```jsx
export function RadioGroup({ legend, options, value, onChange, name }) {
  return (
    <fieldset className="flex flex-col gap-2.5">
      <legend className="mb-1 text-sm font-medium text-body">{legend}</legend>
      {options.map(o => (
        <label key={o.value} className="flex cursor-pointer items-center gap-3">
          <input type="radio" name={name} value={o.value} checked={value===o.value} onChange={()=>onChange(o.value)}
            className={`h-5 w-5 cursor-pointer appearance-none rounded-full border border-line-strong bg-surface transition-all duration-fast
              checked:border-[6px] checked:border-primary ${RING}`} />
          <span className="text-base text-body">{o.label}</span>
        </label>
      ))}
    </fieldset>
  );
}
```

### Switch
```jsx
export function Switch({ checked, onChange, label }) {
  return (
    <label className="flex cursor-pointer items-center gap-3">
      <button role="switch" aria-checked={checked} onClick={()=>onChange(!checked)}
        className={`relative h-7 w-12 shrink-0 rounded-full transition-colors duration-base ease-standard ${RING}
          ${checked ? 'bg-primary' : 'bg-neutral-300 dark:bg-navy-900'}`}>
        <span className={`absolute top-1 h-5 w-5 rounded-full bg-white shadow-sm transition-all duration-base ease-standard ${checked ? 'left-6' : 'left-1'}`} />
      </button>
      <span className="text-base text-body">{label}</span>
    </label>
  );
}
```

### Slider
```jsx
export function Slider({ label, min=0, max=100, value, onChange, unit='' }) {
  const pct = ((value-min)/(max-min))*100;
  return (
    <div className="flex flex-col gap-2">
      <div className="flex justify-between text-sm"><span className="font-medium text-body">{label}</span><span className="text-muted">{value}{unit}</span></div>
      <input type="range" min={min} max={max} value={value} onChange={e=>onChange(+e.target.value)}
        aria-label={label} style={{background:`linear-gradient(to right, var(--primary) ${pct}%, var(--border) ${pct}%)`}}
        className={`h-1.5 w-full cursor-pointer appearance-none rounded-full ${RING}
          [&::-webkit-slider-thumb]:h-5 [&::-webkit-slider-thumb]:w-5 [&::-webkit-slider-thumb]:appearance-none
          [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-white [&::-webkit-slider-thumb]:shadow-md
          [&::-webkit-slider-thumb]:border [&::-webkit-slider-thumb]:border-line-strong`} />
    </div>
  );
}
```

### Navbar
```jsx
export function Navbar({ links=[], active, cta }) {
  return (
    <header className="sticky top-0 z-nav border-b border-line bg-bg/85 backdrop-blur">
      <nav aria-label="Main" className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <a href="#" className={`flex items-center gap-2 font-medium text-body rounded-sm ${RING}`}>
          <span className="h-2.5 w-2.5 rounded-full bg-accent shadow-sm" aria-hidden /> Product
        </a>
        <div className="hidden items-center gap-1 md:flex">
          {links.map(l => (
            <a key={l} href="#" aria-current={active===l ? 'page' : undefined}
              className={`rounded-full px-4 py-2 text-sm font-medium transition-colors duration-fast ${RING}
                ${active===l ? 'bg-primary-subtle text-primary dark:text-cobalt-200' : 'text-secondary hover:bg-bg-subtle hover:text-body'}`}>{l}</a>
          ))}
        </div>
        {cta}
      </nav>
    </header>
  );
}
```

### Sidebar
```jsx
export function Sidebar({ sections, active, onSelect }) {
  return (
    <nav aria-label="Sidebar" className="flex h-full w-60 flex-col gap-6 border-r border-line bg-bg-subtle p-4">
      {sections.map(s => (
        <div key={s.title}>
          <p className="px-3 pb-2 text-xs font-semibold uppercase tracking-wider text-muted">{s.title}</p>
          <ul className="flex flex-col gap-0.5">
            {s.items.map(it => (
              <li key={it.label}>
                <button onClick={()=>onSelect(it.label)} aria-current={active===it.label ? 'page' : undefined}
                  className={`flex w-full items-center gap-2.5 rounded-md px-3 py-2 text-sm font-medium transition-colors duration-fast ${RING}
                    ${active===it.label ? 'bg-primary-subtle text-primary dark:text-cobalt-200' : 'text-secondary hover:bg-neutral-100 dark:hover:bg-navy-900 hover:text-body'}`}>
                  {it.icon && <it.icon className="h-4 w-4" aria-hidden />}{it.label}
                </button>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </nav>
  );
}
```

### Tabs
```jsx
import { useState } from 'react';
export function Tabs({ tabs, defaultTab }) {
  const [active, setActive] = useState(defaultTab ?? tabs[0].label);
  return (
    <div>
      <div role="tablist" className="flex gap-1 border-b border-line">
        {tabs.map(t => (
          <button key={t.label} role="tab" aria-selected={active===t.label}
            onClick={()=>setActive(t.label)}
            className={`-mb-px rounded-t-md px-4 py-2.5 text-sm font-medium transition-colors duration-fast border-b-2 ${RING}
              ${active===t.label ? 'border-primary text-primary dark:text-cobalt-200' : 'border-transparent text-secondary hover:text-body hover:border-line-strong'}`}>
            {t.label}
          </button>
        ))}
      </div>
      <div role="tabpanel" className="pt-4">{tabs.find(t=>t.label===active)?.content}</div>
    </div>
  );
}
```

### Breadcrumbs
```jsx
import { ChevronRight } from 'lucide-react';
export function Breadcrumbs({ items }) {
  return (
    <nav aria-label="Breadcrumb">
      <ol className="flex flex-wrap items-center gap-1.5 text-sm">
        {items.map((it, i) => {
          const last = i === items.length-1;
          return (
            <li key={it.label} className="flex items-center gap-1.5">
              {last ? <span aria-current="page" className="font-medium text-body">{it.label}</span>
                : <a href={it.href} className={`text-secondary hover:text-primary rounded-sm transition-colors duration-fast ${RING}`}>{it.label}</a>}
              {!last && <ChevronRight className="h-3.5 w-3.5 text-muted" aria-hidden />}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
```

### Pagination
```jsx
import { ChevronLeft, ChevronRight } from 'lucide-react';
export function Pagination({ page, pages, onPage }) {
  const nums = Array.from({length: pages}, (_,i)=>i+1).filter(n => n===1 || n===pages || Math.abs(n-page)<=1);
  const withGaps = nums.flatMap((n,i)=> i && n - nums[i-1] > 1 ? ['…', n] : [n]);
  const btn = `inline-flex h-10 min-w-10 items-center justify-center rounded-full px-2 text-sm font-medium transition-colors duration-fast ${RING}`;
  return (
    <nav aria-label="Pagination" className="flex items-center gap-1">
      <button className={`${btn} text-secondary hover:bg-bg-subtle disabled:opacity-45`} disabled={page===1} onClick={()=>onPage(page-1)} aria-label="Previous page"><ChevronLeft className="h-4 w-4" aria-hidden /></button>
      {withGaps.map((n,i) => n==='…' ? <span key={`g${i}`} className="px-1 text-muted">…</span> :
        <button key={n} aria-current={n===page ? 'page' : undefined} onClick={()=>onPage(n)}
          className={`${btn} ${n===page ? 'bg-primary text-white' : 'text-secondary hover:bg-bg-subtle'}`}>{n}</button>)}
      <button className={`${btn} text-secondary hover:bg-bg-subtle disabled:opacity-45`} disabled={page===pages} onClick={()=>onPage(page+1)} aria-label="Next page"><ChevronRight className="h-4 w-4" aria-hidden /></button>
    </nav>
  );
}
```

### Menu / Dropdown
```jsx
import { useState, useRef, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';
export function Menu({ label, items }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  useEffect(() => {
    const close = e => { if (!ref.current?.contains(e.target)) setOpen(false); };
    const esc = e => e.key==='Escape' && setOpen(false);
    document.addEventListener('click', close); document.addEventListener('keydown', esc);
    return () => { document.removeEventListener('click', close); document.removeEventListener('keydown', esc); };
  }, []);
  return (
    <div ref={ref} className="relative inline-block">
      <button aria-haspopup="menu" aria-expanded={open} onClick={()=>setOpen(!open)}
        className={`inline-flex h-11 items-center gap-2 rounded-full border border-line-strong px-5 text-base font-medium text-body hover:bg-bg-subtle transition-colors duration-fast ${RING}`}>
        {label} <ChevronDown className={`h-4 w-4 transition-transform duration-fast ${open?'rotate-180':''}`} aria-hidden />
      </button>
      {open && (
        <div role="menu" className="absolute left-0 z-dropdown mt-2 min-w-48 rounded-lg border border-line bg-surface-raised p-1.5 shadow-lg">
          {items.map(it => it.divider ? <hr key="d" className="my-1.5 border-line" /> :
            <button key={it.label} role="menuitem" onClick={() => { it.onClick?.(); setOpen(false); }}
              className={`flex w-full items-center gap-2.5 rounded-md px-3 py-2 text-sm text-body hover:bg-bg-subtle transition-colors duration-fast ${RING}
                ${it.danger ? 'text-error' : ''}`}>
              {it.icon && <it.icon className="h-4 w-4 text-muted" aria-hidden />}{it.label}
            </button>)}
        </div>
      )}
    </div>
  );
}
```

### Modal / Dialog
```jsx
import { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
export function Modal({ open, onClose, title, children, footer }) {
  const ref = useRef(null);
  useEffect(() => {
    if (open) { ref.current?.querySelector('button, input, a')?.focus(); }
    const esc = e => e.key==='Escape' && onClose();
    document.addEventListener('keydown', esc);
    return () => document.removeEventListener('keydown', esc);
  }, [open, onClose]);
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-modal flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-[var(--surface-overlay)] backdrop-blur-sm" onClick={onClose} aria-hidden />
      <div ref={ref} role="dialog" aria-modal="true" aria-labelledby="modal-title"
        className="relative w-full max-w-md rounded-xl bg-surface-raised p-6 shadow-xl animate-[modalIn_250ms_cubic-bezier(0,0,0.2,1)]">
        <div className="flex items-start justify-between gap-4">
          <h2 id="modal-title" className="text-h4 font-medium text-body">{title}</h2>
          <button onClick={onClose} aria-label="Close dialog" className={`rounded-full p-1.5 text-muted hover:bg-bg-subtle hover:text-body ${RING}`}><X className="h-5 w-5" aria-hidden /></button>
        </div>
        <div className="pt-3 text-base text-secondary">{children}</div>
        {footer && <div className="flex justify-end gap-3 pt-6">{footer}</div>}
      </div>
    </div>
  );
}
// global.css: @keyframes modalIn { from { opacity:0; transform:translateY(8px) scale(0.98); } }
```

### Drawer
```jsx
export function Drawer({ open, onClose, title, children, side='right' }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-modal">
      <div className="absolute inset-0 bg-[var(--surface-overlay)]" onClick={onClose} aria-hidden />
      <div role="dialog" aria-modal="true" aria-label={title}
        className={`absolute top-0 h-full w-full max-w-sm bg-surface-raised shadow-xl p-6 overflow-y-auto
          ${side==='right' ? 'right-0 animate-[drawerInR_400ms_cubic-bezier(0,0,0.2,1)]' : 'left-0 animate-[drawerInL_400ms_cubic-bezier(0,0,0.2,1)]'}`}>
        <div className="flex items-center justify-between pb-4">
          <h2 className="text-h4 font-medium text-body">{title}</h2>
          <button onClick={onClose} aria-label="Close" className={`rounded-full p-1.5 text-muted hover:bg-bg-subtle ${RING}`}><X className="h-5 w-5" aria-hidden /></button>
        </div>
        {children}
      </div>
    </div>
  );
}
// global.css: @keyframes drawerInR { from { transform:translateX(100%); } } @keyframes drawerInL { from { transform:translateX(-100%); } }
```

### Toast / Snackbar
```jsx
import { CheckCircle2, AlertTriangle, XCircle, Info, X } from 'lucide-react';
const TOAST_META = {
  success:{icon:CheckCircle2, cls:'text-success'}, warning:{icon:AlertTriangle, cls:'text-warning'},
  error:{icon:XCircle, cls:'text-error'}, info:{icon:Info, cls:'text-info'},
};
export function Toast({ tone='info', title, description, onDismiss }) {
  const { icon:Icon, cls } = TOAST_META[tone];
  return (
    <div role="status" className="pointer-events-auto flex w-full max-w-sm items-start gap-3 rounded-lg border border-line bg-surface-raised p-4 shadow-lg animate-[toastIn_250ms_cubic-bezier(0,0,0.2,1)]">
      <Icon className={`h-5 w-5 shrink-0 ${cls}`} aria-hidden />
      <div className="flex-1 text-sm"><p className="font-medium text-body">{title}</p>
        {description && <p className="text-secondary">{description}</p>}</div>
      <button onClick={onDismiss} aria-label="Dismiss" className={`rounded-full p-1 text-muted hover:bg-bg-subtle ${RING}`}><X className="h-4 w-4" aria-hidden /></button>
    </div>
  );
}
// Place inside: <div className="fixed bottom-6 right-6 z-toast flex flex-col gap-3" />
// global.css: @keyframes toastIn { from { opacity:0; transform:translateY(12px); } }
```

### Alert / Banner
```jsx
export function Alert({ tone='info', title, children, onDismiss }) {
  const { icon:Icon, cls } = TOAST_META[tone];
  const bg = { success:'bg-success-bg', warning:'bg-warning-bg', error:'bg-error-bg', info:'bg-info-bg' }[tone];
  return (
    <div role={tone==='error' ? 'alert' : 'status'} className={`flex items-start gap-3 rounded-lg p-4 ${bg}`}>
      <Icon className={`h-5 w-5 shrink-0 ${cls}`} aria-hidden />
      <div className="flex-1 text-sm text-body"><p className="font-medium">{title}</p>{children && <div className="pt-0.5 text-secondary">{children}</div>}</div>
      {onDismiss && <button onClick={onDismiss} aria-label="Dismiss" className={`rounded-full p-1 text-muted hover:bg-black/5 ${RING}`}><X className="h-4 w-4" aria-hidden /></button>}
    </div>
  );
}
```

### Popover
```jsx
import { useState, useRef, useEffect } from 'react';
export function Popover({ trigger, children }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  useEffect(() => {
    const close = e => { if (!ref.current?.contains(e.target)) setOpen(false); };
    document.addEventListener('click', close);
    return () => document.removeEventListener('click', close);
  }, []);
  return (
    <span ref={ref} className="relative inline-block">
      <span onClick={()=>setOpen(!open)}>{trigger}</span>
      {open && <div role="dialog" className="absolute left-1/2 z-popover mt-2 w-64 -translate-x-1/2 rounded-lg border border-line bg-surface-raised p-4 shadow-lg text-sm text-secondary">{children}</div>}
    </span>
  );
}
```

### Progress
```jsx
export function Progress({ value, max=100, label }) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && <div className="flex justify-between text-sm"><span className="font-medium text-body">{label}</span><span className="text-muted">{Math.round(value/max*100)}%</span></div>}
      <div role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={max} aria-label={label}
        className="h-2 w-full overflow-hidden rounded-full bg-neutral-100 dark:bg-navy-900">
        <div className="h-full rounded-full bg-primary transition-all duration-slow ease-standard" style={{width:`${value/max*100}%`}} />
      </div>
    </div>
  );
}
```

### Card
```jsx
export function Card({ title, subtitle, children, footer, interactive, className='' }) {
  return (
    <div tabIndex={interactive ? 0 : undefined}
      className={`rounded-xl border border-line bg-surface p-6 shadow-sm
        ${interactive ? `cursor-pointer transition-all duration-base ease-standard hover:shadow-md hover:border-line-strong ${RING}` : ''} ${className}`}>
      {title && <h3 className="text-h4 font-medium text-body">{title}</h3>}
      {subtitle && <p className="pt-0.5 text-sm text-muted">{subtitle}</p>}
      {children && <div className={title ? 'pt-4' : ''}>{children}</div>}
      {footer && <div className="mt-5 border-t border-line pt-4">{footer}</div>}
    </div>
  );
}
```

### Table
```jsx
export function Table({ columns, rows, caption }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-line">
      <table className="w-full border-collapse text-sm">
        {caption && <caption className="sr-only">{caption}</caption>}
        <thead>
          <tr className="border-b border-line bg-bg-subtle text-left">
            {columns.map(c => <th key={c.key} scope="col" className="px-4 py-3 font-medium text-secondary">{c.label}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.map((r,i) => (
            <tr key={i} className="border-b border-line last:border-0 transition-colors duration-fast hover:bg-bg-subtle">
              {columns.map(c => <td key={c.key} className="px-4 py-3 text-body">{r[c.key]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### List
```jsx
export function List({ items }) {
  return (
    <ul className="divide-y divide-line rounded-xl border border-line bg-surface">
      {items.map(it => (
        <li key={it.title} className="flex items-center gap-4 p-4">
          {it.leading}
          <div className="min-w-0 flex-1"><p className="truncate font-medium text-body">{it.title}</p>
            {it.subtitle && <p className="truncate text-sm text-muted">{it.subtitle}</p>}</div>
          {it.trailing}
        </li>
      ))}
    </ul>
  );
}
```

### Accordion
```jsx
export function Accordion({ items }) {
  return (
    <div className="divide-y divide-line rounded-xl border border-line">
      {items.map(it => (
        <details key={it.q} className="group">
          <summary className={`flex cursor-pointer list-none items-center justify-between gap-4 p-4 font-medium text-body hover:bg-bg-subtle transition-colors duration-fast ${RING}`}>
            {it.q}
            <ChevronDown className="h-4 w-4 shrink-0 text-muted transition-transform duration-base group-open:rotate-180" aria-hidden />
          </summary>
          <div className="px-4 pb-4 text-sm text-secondary">{it.a}</div>
        </details>
      ))}
    </div>
  );
}
```

### Stat / Metric
```jsx
import { TrendingUp, TrendingDown } from 'lucide-react';
export function Stat({ label, value, delta, trend }) {
  const up = trend === 'up';
  return (
    <div className="rounded-xl border border-line bg-surface p-5 shadow-sm">
      <p className="text-sm text-muted">{label}</p>
      <p className="pt-1 text-h2 font-medium tracking-tight text-body">{value}</p>
      {delta && (
        <p className={`flex items-center gap-1 pt-1 text-sm font-medium ${up ? 'text-success' : 'text-error'}`}>
          {up ? <TrendingUp className="h-4 w-4" aria-hidden /> : <TrendingDown className="h-4 w-4" aria-hidden />}
          {delta}<span className="sr-only">{up ? 'increase' : 'decrease'}</span>
        </p>
      )}
    </div>
  );
}
```

### Container / Grid helpers
```jsx
export const Container = ({ children, className='' }) => <div className={`mx-auto w-full max-w-6xl px-6 ${className}`}>{children}</div>;
export const Stack = ({ gap='4', children, className='' }) => <div className={`flex flex-col gap-${gap} ${className}`}>{children}</div>;
export const Row = ({ gap='4', children, className='' }) => <div className={`flex flex-wrap items-center gap-${gap} ${className}`}>{children}</div>;
export const Grid = ({ cols='3', gap='6', children, className='' }) => <div className={`grid gap-${gap} md:grid-cols-${cols} ${className}`}>{children}</div>;
// Page section rhythm: py-16 (64px) between major sections, gap-6 (24px) between cards.
```

### Empty state
```jsx
export function EmptyState({ icon:Icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-line-strong bg-bg-subtle px-6 py-14 text-center">
      {Icon && <span className="mb-1 flex h-12 w-12 items-center justify-center rounded-full bg-primary-subtle"><Icon className="h-6 w-6 text-primary dark:text-cobalt-200" aria-hidden /></span>}
      <p className="text-h4 font-medium text-body">{title}</p>
      <p className="max-w-sm text-sm text-muted">{description}</p>
      {action && <div className="pt-3">{action}</div>}
    </div>
  );
}
```

---

## 4. Chart / data-viz color ramps

Use in order; don't skip. Pair every color with a label or pattern — never color alone.
```js
export const chart = {
  categorical: ['#004ACB','#79A1ED','#1C1F48','#CEFF00','#67718F','#A6C1F4'], // volt = highlight series only
  sequentialBlue: ['#E8EFFC','#A6C1F4','#4D7FE3','#004ACB','#002F82'],
  diverging: ['#C22C1F','#F2988E','#E9EDF4','#79A1ED','#004ACB'],
  grid:'var(--border)', axisText:'var(--text-muted)',
};
```

## 5. Icon guidance
- Use **lucide-react**, `strokeWidth={2}`, sizes 16/20/24 px only.
- Icon color follows text color of its context (`currentColor`); decorative icons get `aria-hidden`.
- Icon-only buttons need `aria-label`. Never use volt green as icon color on white.

## 6. Voice & tone for UI copy
Sentence case everywhere (buttons, titles, labels). Verbs first on buttons ("Create project", not "Project creation"). Short, factual, no exclamation marks.
