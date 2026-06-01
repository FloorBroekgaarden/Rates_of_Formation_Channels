#!/usr/bin/env python3
"""Generate interactive HTML table combining formation channel rates with simulation specs."""
import csv, os, re, html as htmllib

BASE    = '/Users/floorbroekgaarden/Projects/GitHub/Rates_of_Formation_Channels/plottingCode/All_Figures/Data_formation_channels_intrinsic/'
BPS_HTML = '/Users/floorbroekgaarden/Projects/GitHub/Rates_of_Formation_Channels/interactive_figures_and_tables/BPS_model_assumptions-9.html'
OUT_DIR = '/Users/floorbroekgaarden/Projects/GitHub/Rates_of_Formation_Channels/interactive_figures_and_tables/'
os.makedirs(OUT_DIR, exist_ok=True)

# ── helpers ───────────────────────────────────────────────────────────────────

def read_csv(path, header_row=0):
    with open(path) as f:
        rows = list(csv.reader(f))
    header = [c.strip() for c in rows[header_row]]
    data = []
    for row in rows[header_row + 1:]:
        if not row or row[0].strip() == 'model':
            continue
        d = {header[i]: row[i].strip() if i < len(row) else '' for i in range(len(header))}
        data.append(d)
    return data

def fmt_frac(v):
    try:
        f = float(v)
        return '—' if f == 0.0 else f'{f*100:.1f}%'
    except (ValueError, TypeError):
        return v if v else '—'

def fmt_rate(v):
    try:
        return f'{float(v):.2f}'
    except (ValueError, TypeError):
        return v if v else '—'

def fmt_val(v, maxlen=35):
    if not v or v == '—':
        return '—'
    v = str(v)
    if len(v) > maxlen:
        return f'<span class="truncated" title="{escape(v)}">{escape(v[:maxlen])}…</span>'
    return escape(v)

def fmt_num(v, decimals=2):
    try:
        return f'{float(v):.{decimals}f}'
    except (ValueError, TypeError):
        return v if v else '—'

def escape(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def frac_val(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return None

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lighten(h, t=0.35):
    r, g, b = hex_to_rgb(h)
    return f'#{int(r*t+255*(1-t)):02x}{int(g*t+255*(1-t)):02x}{int(b*t+255*(1-t)):02x}'

def text_on(h):
    r, g, b = hex_to_rgb(h)
    return '#1a1a2e' if (0.299*r + 0.587*g + 0.114*b)/255 > 0.55 else '#ffffff'

# ── parse BPS HTML ────────────────────────────────────────────────────────────
# Column indices (0-based) for the "val" cells in each grow row.
# Layout: 0=model, 1=paper link, 2=year, 3=code, 4=code_abbr,
# then groups of 3 (val/desc/evidence) starting at index 5.
BPS_COL_IDX = {
    'paper_link':        1,
    'year':              2,
    'code':              3,
    'code_abbr':         4,
    'stellar_tracks':    5,
    'label_1':           8,
    'label_2':          11,
    'label_3':          14,
    'label_4':          17,
    'label_author':     20,
    'sigma':            23,
    'sigma_strippedSN': 26,
    'kick_notes':       29,
    'alpha':            32,
    'alpha_notes':      35,
    'beta':             38,
    'gamma':            41,
    'CE_optimism':      44,
    'CE_prescription':  47,
    'lambda':           50,
    'RMP':              53,
    'RMP_details':      56,
    'PISN':             59,
    'MT_stability':     62,
    'AM_loss':          65,
    'Eddington':        68,
    'f_WR':             71,
    'binding_energy':   74,
    'IMF':              77,
    'period_dist':      80,
    'mass_ratio':       83,
    'f_bin':            86,
    'metallicity':      89,
    'SFR':              92,
    'max_NS_mass':      95,
    'sigma_ECSN':       98,
    'HG_donor':        101,
    'MT_stability_det':104,
    'NS_remnant':      107,
    'wind':            110,
    'tidal':           113,
}

def parse_bps_html(path):
    """Return dict: model_name -> {param_key: value_str}."""
    with open(path, encoding='utf-8') as f:
        raw = f.read()

    def clean(s):
        s = re.sub(r'<span[^>]*class="empty"[^>]*>.*?</span>', '—', s, flags=re.DOTALL)
        s = re.sub(r'<[^>]+>', ' ', s)
        s = htmllib.unescape(s)
        s = ' '.join(s.split())
        return s.strip()

    # Positions of grow rows and group headers — used as end-of-row sentinels
    row_starts   = [m.start() for m in re.finditer(r'<div class="grow"(?!\s+group)', raw)]
    group_starts = [m.start() for m in re.finditer(r'<div class="group-hdr"', raw)]
    boundaries   = sorted(row_starts + group_starts + [len(raw)])

    cell_re = re.compile(
        r'<div class="cell[^"]*"[^>]*>(.*?)(?=<div class="cell|<div class="grow|<div class="group|$)',
        re.DOTALL
    )

    models = {}
    for start in row_starts:
        end   = next((b for b in boundaries if b > start), len(raw))
        chunk = raw[start:end]
        cells = [clean(m) for m in cell_re.findall(chunk)]
        if not cells:
            continue
        model_name = cells[0]
        if not model_name or model_name == '—':
            continue
        data = {}
        for key, idx in BPS_COL_IDX.items():
            v = cells[idx] if idx < len(cells) else ''
            data[key] = '' if v == '—' else v
        models[model_name] = data
    return models

# ── paper citation mapping (read from paper appendix / figure legends) ────────
# Two-author papers: Dorozsmai & Toonen (2022), Shao & Li (2021)
PAPER_CITATIONS = {
    'BA21':   'Bavera et al. (2021)',
    'BO24':   'Boesky et al. (2024)',
    'BRI22':  'Briel et al. (2022)',
    'BRO22':  'Broekgaarden et al. (2022)',
    'DT22':   'Dorozsmai & Toonen (2022)',
    'Hen23':  'Hendriks et al. (2023)',
    'Li25':   'Li et al. (2025)',
    'OL21':   'Olejak et al. (2021)',
    'PE25':   'Pellouin et al. (2025)',
    'RG21':   'Román-Garza et al. (2022)',
    'RO23':   'Romagnolo et al. (2023)',
    'RO25':   'Romagnolo et al. (2025)',
    'SL21':   'Shao & Li (2021)',
    'Sg25':   'Sgalletta et al. (2025)',
    'Xing24': 'Xing et al. (2024)',
    'vSon22': 'van Son et al. (2022)',
    'vSon23': 'van Son et al. (2023)',
}

# ── load data ─────────────────────────────────────────────────────────────────
specs = read_csv(BASE + 'simulation_specs_detailed.csv', header_row=1)
bhbh  = read_csv(BASE + 'BH-BH_rates_review.csv',  header_row=0)
bhns  = read_csv(BASE + 'BH-NS_rates_review.csv',  header_row=0)
nsns  = read_csv(BASE + 'NS-NS_rates_review.csv',  header_row=0)
bps   = parse_bps_html(BPS_HTML)

specs_by = {r['model']: r for r in specs}
bhbh_by  = {r['model']: r for r in bhbh}
bhns_by  = {r['model']: r for r in bhns}
nsns_by  = {r['model']: r for r in nsns}

all_models = sorted(specs_by.keys())

# ── column definitions ────────────────────────────────────────────────────────

# (bps_key, display_name, format_fn, tooltip)
BPS_PHYSICS_COLS = [
    ('gamma',           'γ<br>(AM loss)',       lambda v: fmt_val(v,20), 'Angular momentum loss parameter γ'),
    ('AM_loss',         'AM loss<br>mechanism', lambda v: fmt_val(v,30), 'Physical mechanism of angular momentum loss during non-conservative MT'),
    ('Eddington',       'Edd.<br>limited',      lambda v: fmt_val(v,10), 'Whether accretion onto compact object is Eddington-limited'),
    ('f_WR',            'f_WR',                 lambda v: fmt_val(v,15), 'Multiplicative scaling factor on Wolf-Rayet wind mass-loss rates'),
    ('alpha_notes',     'α CE notes',           lambda v: fmt_val(v,30), 'Additional notes on CE efficiency parameter'),
    ('HG_donor',        'HG donor<br>CE surv.', lambda v: fmt_val(v,20), 'Whether Hertzsprung-gap donors survive common-envelope (optimistic/pessimistic)'),
    ('wind',            'wind<br>prescription', lambda v: fmt_val(v,30), 'Stellar wind mass-loss prescription'),
    ('tidal',           'tidal<br>prescription',lambda v: fmt_val(v,25), 'Tidal evolution prescription'),
    ('NS_remnant',      'NS remnant<br>mass',   lambda v: fmt_val(v,25), 'Neutron star remnant mass prescription'),
]

BPS_IC_COLS = [
    ('IMF',          'IMF',                  lambda v: fmt_val(v,30), 'Initial mass function for primary star'),
    ('period_dist',  'period<br>dist.',      lambda v: fmt_val(v,30), 'Initial orbital period/separation distribution'),
    ('mass_ratio',   'mass ratio<br>dist.',  lambda v: fmt_val(v,30), 'Initial mass ratio distribution'),
    ('f_bin',        'f_bin',                lambda v: fmt_val(v,20), 'Binary fraction'),
    ('metallicity',  'metallicity<br>range', lambda v: fmt_val(v,30), 'Range and sampling of stellar birth metallicities'),
    ('SFR',          'SFR / SFRD<br>model',  lambda v: fmt_val(v,30), 'Star formation rate density model used for cosmic merger rate'),
    ('max_NS_mass',  'max NS<br>mass [M☉]',  lambda v: fmt_val(v,20), 'Maximum gravitational NS mass before collapse to BH'),
    ('sigma_ECSN',   'σ ECSN<br>[km/s]',     lambda v: fmt_val(v,15), 'Natal kick dispersion for electron-capture supernovae'),
]

# (source_key, display_name, format_fn, fc_color, tooltip)
RATE_COLS = [
    ('All intrinsic (z=0) [Gpc^-3 yr^-1]', 'Total Rate<br>[Gpc⁻³yr⁻¹]', fmt_rate, '#444444',
     'Total intrinsic merger rate at z=0 in Gpc⁻³ yr⁻¹'),
    ('CHE', 'CHE<br>(no MT)', fmt_frac, '#b8a0ff',
     'Chemically homogeneous evolution (no mass transfer) channel fraction'),
    ('SMT before and after channel', 'classic SMT<br>(SMT+SMT)', fmt_frac, '#FFA630',
     'Classic stable mass transfer channel (SMT before and after)'),
    ('channel V intrinsic (z=0) other without CE', 'other<br>without CE', fmt_frac, '#ffb5a7',
     'Other non-CE channels'),
    ('channel I intrinsic (z=0) classic CE (SMT+CE)', 'classic CE<br>(SMT+CE)', fmt_frac, '#00A7E1',
     'Classic CE channel: stable mass transfer then common-envelope'),
    ('channel III intrinsic (z=0) SCCE', 'single-core CE<br>(SCCE)', fmt_frac, '#0474BA',
     'Single common-envelope (SCCE) channel fraction'),
    ('channel IV intrinsic (z=0) DCCE', 'double-core CE<br>(DCCE)', fmt_frac, '#20b2aa',
     'Double common-envelope (DCCE) channel fraction'),
    ('channel V intrinsic (z=0) other with CE', 'other<br>with CE', fmt_frac, '#8dd3c7',
     'Other CE channels fraction'),
    ('fraction without common envelope', 'without<br>common envelope', fmt_frac, '#FFA630',
     'Total fraction of systems formed without common envelope'),
    ('fraction with common envelope', 'with<br>common envelope', fmt_frac, '#00A7E1',
     'Total fraction of systems formed with common envelope'),
]

SPEC_PARAM_COLS = [
    ('sigma',                    'σ<br>[km/s]',   lambda v: fmt_num(v,0), 'Natal kick dispersion σ for standard SN [km/s]'),
    ('sigma_strippedSN',         'σ stripped',    lambda v: fmt_num(v,0), 'Natal kick dispersion for stripped-star SN [km/s]'),
    ('alpha',                    'α CE',          lambda v: fmt_num(v,2), 'Common-envelope efficiency parameter α'),
    ('beta',                     'β',             lambda v: fmt_num(v,2), 'Mass-transfer efficiency parameter β'),
    ('CE optimistic/pessimistic','CE opt/pess',   None,                   'Optimistic or pessimistic CE survival assumption'),
    ('CE prescription',          'CE prescrip.',  lambda v: fmt_val(v,25),'CE energy prescription'),
    ('lambda',                   'λ',             lambda v: fmt_val(v,25),'Binding-energy lambda prescription'),
    ('PISN prescription',        'PISN',          lambda v: fmt_val(v,25),'Pair-instability supernova prescription'),
    ('stability',                'MT stability',  lambda v: fmt_val(v,25),'Mass-transfer stability criterion'),
    ('RMP',                      'RMP',           lambda v: fmt_val(v,30),'Remnant-mass prescription'),
]

# ── max rates for heat-map scaling ────────────────────────────────────────────
def max_rate(dataset):
    vals = [frac_val(r.get('All intrinsic (z=0) [Gpc^-3 yr^-1]','')) for r in dataset]
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else 1.0

max_bhbh = max_rate(bhbh)
max_bhns = max_rate(bhns)
max_nsns = max_rate(nsns)

n_param  = len(SPEC_PARAM_COLS)
n_rate   = len(RATE_COLS)
n_phys   = len(BPS_PHYSICS_COLS)
n_ic     = len(BPS_IC_COLS)

# ── row rendering ─────────────────────────────────────────────────────────────
def render_rows():
    out = []
    for m in all_models:
        spec  = specs_by.get(m, {})
        bh    = bhbh_by.get(m)
        bn    = bhns_by.get(m)
        nn    = nsns_by.get(m)
        bps_d = bps.get(m, {})

        # --- paper citation column (sticky, leftmost) ---
        label_auth = spec.get('label_author', bps_d.get('label_author', ''))
        citation   = PAPER_CITATIONS.get(label_auth, label_auth)
        paper_link = spec.get('link to paper', bps_d.get('paper_link', '')).strip()
        if paper_link:
            paper_cell = (f'<td class="paper-col">'
                          f'<a href="{escape(paper_link)}" target="_blank">{escape(citation)}</a>'
                          f'</td>')
        else:
            paper_cell = f'<td class="paper-col">{escape(citation)}</td>'

        # --- model ID column (sticky, second) ---
        model_text = escape(m)
        if paper_link:
            model_cell = f'<td class="model-col"><a href="{escape(paper_link)}" target="_blank">{model_text}</a></td>'
        else:
            model_cell = f'<td class="model-col">{model_text}</td>'

        # --- simulation parameter columns ---
        par = []
        for key, _, fmt_fn, _ in SPEC_PARAM_COLS:
            v   = spec.get(key, '')
            txt = fmt_fn(v) if fmt_fn else fmt_val(v, 30)
            par.append(f'<td class="col-param param-cell">{txt}</td>')

        # --- additional physics columns (from BPS) ---
        phys = []
        for bkey, _, fmt_fn, _ in BPS_PHYSICS_COLS:
            v   = bps_d.get(bkey, '')
            txt = fmt_fn(v) if fmt_fn else fmt_val(v, 30)
            phys.append(f'<td class="col-phys phys-cell">{txt}</td>')

        # --- initial conditions columns (from BPS) ---
        ics = []
        for bkey, _, fmt_fn, _ in BPS_IC_COLS:
            v   = bps_d.get(bkey, '')
            txt = fmt_fn(v) if fmt_fn else fmt_val(v, 30)
            ics.append(f'<td class="col-ic ic-cell">{txt}</td>')

        # --- rate columns per system type ---
        def rate_section(dataset_row, cls, max_val, rate_color):
            if dataset_row is None:
                return [f'<td class="col-{cls} no-data">—</td>'] * n_rate
            cells = []
            for col_key, _, fmt_fn, ch_color, _ in RATE_COLS:
                val = dataset_row.get(col_key, '')
                if col_key == 'All intrinsic (z=0) [Gpc^-3 yr^-1]':
                    fv = frac_val(val)
                    a  = (0.1 + min(fv/max_val, 1.0)*0.5) if fv else 0
                    style = f' style="background:rgba({rate_color},{a:.3f})"' if fv else ''
                    cells.append(f'<td class="col-{cls}"{style}>{fmt_fn(val)}</td>')
                else:
                    fv = frac_val(val)
                    if fv and fv > 0:
                        r, g, b = hex_to_rgb(ch_color)
                        a = 0.15 + min(fv, 1.0)*0.6
                        cells.append(f'<td class="col-{cls}" style="background:rgba({r},{g},{b},{a:.3f})">{fmt_fn(val)}</td>')
                    else:
                        cells.append(f'<td class="col-{cls}">{fmt_fn(val)}</td>')
            return cells

        bh_cells = rate_section(bh, 'bhbh', max_bhbh, '220,100,50')
        bn_cells = rate_section(bn, 'bhns', max_bhns, '130,80,190')
        nn_cells = rate_section(nn, 'nsns', max_nsns, '50,160,80')

        out.append(
            '<tr>'
            + paper_cell
            + model_cell
            + ''.join(par)
            + ''.join(phys)
            + ''.join(ics)
            + ''.join(bh_cells)
            + ''.join(bn_cells)
            + ''.join(nn_cells)
            + '</tr>'
        )
    return '\n'.join(out)

# ── header helpers ────────────────────────────────────────────────────────────
def th2(label, cls='', tooltip='', rowspan=1, colspan=1, sort=False, style=''):
    rs = f' rowspan="{rowspan}"' if rowspan > 1 else ''
    cs = f' colspan="{colspan}"' if colspan > 1 else ''
    tt = f' title="{escape(tooltip)}"' if tooltip else ''
    c  = f' class="{cls}"' if cls else ''
    ds = ' data-sort="true"' if sort else ''
    st = f' style="{style}"' if style else ''
    return f'<th{c}{rs}{cs}{tt}{ds}{st}>{label}</th>'

def th_rate_col(label, fc_color, grp_cls, tooltip=''):
    bg  = lighten(fc_color, t=0.40)
    txt = text_on(bg)
    tt  = f' title="{escape(tooltip)}"' if tooltip else ''
    return (f'<th class="{grp_cls}" '
            f'style="background:{bg};color:{txt};font-size:11px;line-height:1.3;font-weight:600;" '
            f'data-sort="true"{tt}>{label}</th>')

def th_bps_col(label, grp_cls, bg_color, tooltip=''):
    txt = text_on(bg_color)
    tt  = f' title="{escape(tooltip)}"' if tooltip else ''
    return (f'<th class="{grp_cls}" '
            f'style="background:{bg_color};color:{txt};font-size:11px;line-height:1.3;font-weight:600;" '
            f'data-sort="true"{tt}>{label}</th>')

# ── build header rows ─────────────────────────────────────────────────────────
PHYS_BG  = '#8a6a30'   # amber/brown group header
PHYS_SUB = '#d4a853'   # sub-header tint
IC_BG    = '#5a3a7a'   # deep purple group header
IC_SUB   = '#9070c0'   # sub-header tint

grp1 = (
    th2('Paper', 'hdr-paper', 'Source paper', rowspan=2)
    + th2('Model', 'hdr-model', 'Population-synthesis model identifier', rowspan=2)
    + th2('Simulation Parameters', 'hdr-param', colspan=n_param)
    + th2('Additional Physics', 'hdr-phys', colspan=n_phys)
    + th2('Initial Conditions', 'hdr-ic', colspan=n_ic)
    + th2('BH–BH Formation Channels', 'hdr-bhbh', colspan=n_rate)
    + th2('BH–NS Formation Channels', 'hdr-bhns', colspan=n_rate)
    + th2('NS–NS Formation Channels', 'hdr-nsns', colspan=n_rate)
)

grp2 = (
    ''.join(th2(dn, 'hdr-param-col', tt, sort=True) for _, dn, _, tt in SPEC_PARAM_COLS)
    + ''.join(th_bps_col(dn, 'hdr-phys-col', lighten(PHYS_BG, 0.5), tt)
              for _, dn, _, tt in BPS_PHYSICS_COLS)
    + ''.join(th_bps_col(dn, 'hdr-ic-col', lighten(IC_BG, 0.5), tt)
              for _, dn, _, tt in BPS_IC_COLS)
    + ''.join(th_rate_col(dn, col, 'hdr-bhbh-col', tt) for _, dn, _, col, tt in RATE_COLS)
    + ''.join(th_rate_col(dn, col, 'hdr-bhns-col', tt) for _, dn, _, col, tt in RATE_COLS)
    + ''.join(th_rate_col(dn, col, 'hdr-nsns-col', tt) for _, dn, _, col, tt in RATE_COLS)
)

rows_final = render_rows()

# ── HTML ──────────────────────────────────────────────────────────────────────
html_final = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Compact Binary Formation Channel Rates — Simulation Survey</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:13px;background:#f4f6f9;color:#1a1a2e;padding:24px 20px}}
.page-header{{max-width:1500px;margin:0 auto 18px}}
.page-header h1{{font-size:1.55rem;font-weight:700;color:#1a1a2e;margin-bottom:8px;letter-spacing:-.3px}}
.page-header p{{color:#555;line-height:1.6;max-width:900px;font-size:0.875rem}}
.controls{{max-width:1500px;margin:0 auto 14px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}}
#search{{padding:7px 13px;border:1.5px solid #ccd;border-radius:20px;font-size:13px;width:240px;outline:none;transition:border-color .2s,box-shadow .2s}}
#search:focus{{border-color:#3a6ea5;box-shadow:0 0 0 3px rgba(58,110,165,.15)}}
.toggle-group{{display:flex;gap:6px;flex-wrap:wrap;align-items:center}}
.toggle-label{{font-size:12px;color:#555;font-weight:600}}
.toggle-btn{{padding:5px 13px;border-radius:20px;border:2px solid;cursor:pointer;font-size:12px;font-weight:600;transition:all .15s;user-select:none;background:transparent}}
.toggle-btn.param {{border-color:#00796b;color:#00796b}}
.toggle-btn.phys  {{border-color:#8a6a30;color:#8a6a30}}
.toggle-btn.ic    {{border-color:#5a3a7a;color:#5a3a7a}}
.toggle-btn.bhbh  {{border-color:#bf360c;color:#bf360c}}
.toggle-btn.bhns  {{border-color:#6a1b9a;color:#6a1b9a}}
.toggle-btn.nsns  {{border-color:#1b5e20;color:#1b5e20}}
.toggle-btn.active{{color:#fff!important}}
.toggle-btn.param.active {{background:#00796b}}
.toggle-btn.phys.active  {{background:#8a6a30}}
.toggle-btn.ic.active    {{background:#5a3a7a}}
.toggle-btn.bhbh.active  {{background:#bf360c}}
.toggle-btn.bhns.active  {{background:#6a1b9a}}
.toggle-btn.nsns.active  {{background:#1b5e20}}
.row-count{{margin-left:auto;font-size:12px;color:#777;white-space:nowrap}}
.table-wrap{{max-width:100%;overflow-x:auto;border-radius:10px;box-shadow:0 3px 16px rgba(0,0,0,.13)}}
table{{border-collapse:collapse;white-space:nowrap;background:#fff;min-width:100%}}
thead{{position:sticky;top:0;z-index:10}}
th,td{{padding:5px 10px;border:1px solid #e0e4ef;text-align:center;vertical-align:middle}}
/* ── group header row ── */
.hdr-paper {{background:#1a3a4a;color:#ecf0f1;font-weight:700;position:sticky;left:0;z-index:25;min-width:160px;letter-spacing:.1px}}
.hdr-model {{background:#2c3e50;color:#ecf0f1;font-weight:700;position:sticky;left:160px;z-index:25;min-width:175px;letter-spacing:.2px}}
.hdr-param {{background:#00796b;color:#fff;font-weight:700;font-size:12px}}
.hdr-phys  {{background:#8a6a30;color:#fff;font-weight:700;font-size:12px}}
.hdr-ic    {{background:#5a3a7a;color:#fff;font-weight:700;font-size:12px}}
.hdr-bhbh  {{background:#bf360c;color:#fff;font-weight:700;font-size:12px}}
.hdr-bhns  {{background:#6a1b9a;color:#fff;font-weight:700;font-size:12px}}
.hdr-nsns  {{background:#1b5e20;color:#fff;font-weight:700;font-size:12px}}
/* ── sub-header row ── */
.hdr-param-col {{background:#b2dfdb;color:#004d40;font-size:11px;line-height:1.3;font-weight:600}}
.hdr-phys-col  {{font-size:11px;line-height:1.3;font-weight:600}}
.hdr-ic-col    {{font-size:11px;line-height:1.3;font-weight:600}}
.hdr-bhbh-col  {{background:#ffccbc;color:#7f2a00;font-size:11px;line-height:1.3;font-weight:600}}
.hdr-bhns-col  {{background:#e1bee7;color:#4a0072;font-size:11px;line-height:1.3;font-weight:600}}
.hdr-nsns-col  {{background:#c8e6c9;color:#1b5e20;font-size:11px;line-height:1.3;font-weight:600}}
/* sort indicators */
th[data-sort]{{cursor:pointer}}
th[data-sort]:hover{{filter:brightness(1.1)}}
th[data-sort]::after{{content:' ↕';font-size:9px;opacity:.45}}
th[data-sort].asc::after {{content:' ▲';opacity:1}}
th[data-sort].desc::after{{content:' ▼';opacity:1}}
/* ── data cells ── */
td{{font-size:12px;color:#2a2a3e}}
.paper-col{{
  font-size:11px;font-weight:600;
  position:sticky;left:0;background:#e8f0f8;z-index:5;
  border-right:1px solid #aab;text-align:left;
  min-width:160px;padding-left:10px;
}}
.paper-col a{{color:#1a3a5a;text-decoration:none;border-bottom:1px dashed #5a8ab0}}
.paper-col a:hover{{color:#3a6ea5}}
.model-col{{
  font-family:'SF Mono','Fira Mono','Consolas',monospace;
  font-size:11px;font-weight:600;
  position:sticky;left:160px;background:#fff;z-index:5;
  border-right:2.5px solid #aab;text-align:left;
  min-width:175px;padding-left:10px;
}}
.model-col a{{color:#1a1a2e;text-decoration:none;border-bottom:1px dashed #90a}}
.model-col a:hover{{color:#3a6ea5;border-bottom-color:#3a6ea5}}
/* zebra + hover */
tbody tr:nth-child(even) td{{background-color:#f8f9ff}}
tbody tr:nth-child(even) .paper-col{{background-color:#dce8f4}}
tbody tr:nth-child(even) .model-col{{background-color:#eff1fa}}
tbody tr:hover td{{background-color:#fffde0!important}}
tbody tr:hover .paper-col{{background-color:#fffde0!important}}
tbody tr:hover .model-col{{background-color:#fffde0!important}}
/* column group tints */
.param-cell{{background:rgba(0,121,107,0.05)}}
.phys-cell {{background:rgba(138,106,48,0.06)}}
.ic-cell   {{background:rgba(90,58,122,0.05)}}
tbody tr:nth-child(even) .param-cell{{background:rgba(0,121,107,0.09)}}
tbody tr:nth-child(even) .phys-cell {{background:rgba(138,106,48,0.10)}}
tbody tr:nth-child(even) .ic-cell   {{background:rgba(90,58,122,0.08)}}
td.no-data{{color:#ccc}}
.truncated{{cursor:help;border-bottom:1px dotted #999}}
.col-hidden{{display:none!important}}
.footer{{max-width:1500px;margin:16px auto 0;font-size:11.5px;color:#888;line-height:1.55}}
.legend{{display:flex;gap:14px;flex-wrap:wrap;padding:10px 14px;background:#fff;border-radius:8px;border:1px solid #e0e4ef;max-width:1500px;margin:0 auto 14px}}
.legend-item{{font-size:11.5px;color:#555;display:flex;align-items:center;gap:5px}}
.legend-item b{{color:#333}}
.swatch{{display:inline-block;width:12px;height:12px;border-radius:3px;flex-shrink:0;border:1px solid rgba(0,0,0,.15)}}
/* ── interactive figures section ── */
.figs-section{{max-width:1500px;margin:40px auto 0}}
.figs-section h2{{font-size:1.25rem;font-weight:700;color:#1a1a2e;padding-bottom:10px;border-bottom:2px solid #e0e4ef;margin-bottom:6px}}
.figs-section .sec-intro{{font-size:0.875rem;color:#555;line-height:1.6;margin-bottom:24px;max-width:860px}}
.fig-block{{margin-bottom:40px}}
.fig-block h3{{font-size:1rem;font-weight:700;color:#2c3e50;margin-bottom:4px}}
.fig-block .fig-caption{{font-size:0.82rem;color:#666;line-height:1.55;margin-bottom:10px;max-width:860px}}
.fig-block iframe{{width:100%;border:1px solid #e0e4ef;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,.09);display:block}}
</style>
</head>
<body>

<div class="page-header">
  <h1>Compact Binary Merger Rates and Formation Channels — Simulation Survey</h1>
  <p>
    Combined table of simulated intrinsic merger rates, formation channel fractions, and model assumptions for
    <strong>BH–BH</strong>, <strong>BH–NS</strong>, and <strong>NS–NS</strong> binaries
    from <strong>{len(all_models)} population-synthesis models</strong> across {len(PAPER_CITATIONS)} studies.
    Channel fractions are evaluated at redshift <em>z</em>&nbsp;=&nbsp;0.
    Cell shading for each channel uses its own color and scales with the fraction value.
    Click any column header to sort. Use the toggles to hide/show column groups.
    Paper column and model names link to the source paper.
  </p>
</div>

<div class="controls">
  <input type="text" id="search" placeholder="🔍  Filter by model, study, or parameter…" oninput="filterTable()">
  <div class="toggle-group">
    <span class="toggle-label">Show/hide:</span>
    <button class="toggle-btn param active" onclick="toggleGroup('param')">Sim. Parameters</button>
    <button class="toggle-btn phys active"  onclick="toggleGroup('phys')">Additional Physics</button>
    <button class="toggle-btn ic active"    onclick="toggleGroup('ic')">Initial Conditions</button>
    <button class="toggle-btn bhbh active"  onclick="toggleGroup('bhbh')">BH–BH Channels</button>
    <button class="toggle-btn bhns active"  onclick="toggleGroup('bhns')">BH–NS Channels</button>
    <button class="toggle-btn nsns active"  onclick="toggleGroup('nsns')">NS–NS Channels</button>
  </div>
  <span class="row-count" id="row-count">Showing {len(all_models)} of {len(all_models)} models</span>
</div>

<div class="legend">
  <div class="legend-item"><span class="swatch" style="background:#b8a0ff"></span><b>CHE (no MT):</b> chemically homogeneous evolution</div>
  <div class="legend-item"><span class="swatch" style="background:#FFA630"></span><b>classic SMT (SMT+SMT):</b> stable mass transfer, no CE</div>
  <div class="legend-item"><span class="swatch" style="background:#ffb5a7"></span><b>other without CE:</b> other non-CE channels</div>
  <div class="legend-item"><span class="swatch" style="background:#00A7E1"></span><b>classic CE (SMT+CE):</b> stable MT then common-envelope</div>
  <div class="legend-item"><span class="swatch" style="background:#0474BA"></span><b>single-core CE (SCCE):</b> one evolved star in CE</div>
  <div class="legend-item"><span class="swatch" style="background:#20b2aa"></span><b>double-core CE (DCCE):</b> both cores in CE simultaneously</div>
  <div class="legend-item"><span class="swatch" style="background:#8dd3c7"></span><b>other with CE:</b> other CE channels</div>
  <div class="legend-item"><b>—:</b> not reported / zero</div>
</div>

<div class="table-wrap">
<table id="main-table">
<thead>
<tr>{grp1}</tr>
<tr>{grp2}</tr>
</thead>
<tbody>
{rows_final}
</tbody>
</table>
</div>

<section class="figs-section">
  <h2>Interactive Figures</h2>
  <p class="sec-intro">
    Interactive versions of Figures 9–13 from Broekgaarden et al. (2026).
    Each figure is fully interactive: hover over points for details, click legend entries to
    toggle studies, and zoom or pan with the Plotly toolbar.
  </p>

  <div class="fig-block">
    <h3>Figure 9 — BBH: intrinsic merger rate vs. formation-channel fraction, by study</h3>
    <p class="fig-caption">
      Fraction of BBH mergers forming without a CE phase as a function of the total local intrinsic
      BBH merger rate <em>R</em><sub>m</sub> for all compiled population-synthesis simulations.
      Each point represents one model; colors distinguish studies. Lines connect models within the
      same study that vary a single parameter, illustrating the parameter sensitivity within each framework.
    </p>
    <iframe src="Fig9_BH-BH_by_study_interactive.html" height="850" loading="lazy"></iframe>
  </div>

  <div class="fig-block">
    <h3>Figure 10 — BHNS: intrinsic merger rate vs. formation-channel fraction, by study</h3>
    <p class="fig-caption">
      Same as Figure 9 for BH–NS mergers.
    </p>
    <iframe src="Fig10_BH-NS_by_study_interactive.html" height="850" loading="lazy"></iframe>
  </div>

  <div class="fig-block">
    <h3>Figure 11 — BNS: intrinsic merger rate vs. formation-channel fraction, by study</h3>
    <p class="fig-caption">
      Same as Figure 9 for NS–NS (BNS) mergers.
    </p>
    <iframe src="Fig11_NS-NS_by_study_interactive.html" height="850" loading="lazy"></iframe>
  </div>

  <div class="fig-block">
    <h3>Figure 12 — BBH: without-CE fraction as a function of model parameters</h3>
    <p class="fig-caption">
      Dependence of the fraction of BBH mergers forming without a CE phase on commonly varied
      binary-evolution parameters (mass-transfer stability criterion <em>q</em><sub>c</sub>,
      CE efficiency α<sub>CE</sub>, mass-transfer efficiency β, natal kick dispersion σ,
      and remnant-mass prescription). Each panel shows controlled single-parameter variations
      within a given study. Points are individual models; horizontal lines span the range of
      variation within each parameter family.
    </p>
    <iframe src="Fig12_BH-BH_withoutCE_fraction_vs_parameters_interactive.html" height="1100" loading="lazy"></iframe>
  </div>

  <div class="fig-block">
    <h3>Figure 13 — BHNS: without-CE fraction as a function of model parameters</h3>
    <p class="fig-caption">
      Same as Figure 12 for BH–NS mergers.
    </p>
    <iframe src="Fig13_BH-NS_withoutCE_fraction_vs_parameters_interactive.html" height="1100" loading="lazy"></iframe>
  </div>
</section>

<div class="footer">
  Table generated from population-synthesis review data (Broekgaarden et al. 2026).
  For questions or corrections, contact <a href="https://floorbroekgaarden.github.io/" target="_blank" style="color:#3a6ea5;">Floor Broekgaarden</a>.
</div>

<script>
const groupCols = {{
  param: () => document.querySelectorAll('.hdr-param,.hdr-param-col,.col-param'),
  phys:  () => document.querySelectorAll('.hdr-phys,.hdr-phys-col,.col-phys'),
  ic:    () => document.querySelectorAll('.hdr-ic,.hdr-ic-col,.col-ic'),
  bhbh:  () => document.querySelectorAll('.hdr-bhbh,.hdr-bhbh-col,.col-bhbh'),
  bhns:  () => document.querySelectorAll('.hdr-bhns,.hdr-bhns-col,.col-bhns'),
  nsns:  () => document.querySelectorAll('.hdr-nsns,.hdr-nsns-col,.col-nsns'),
}};
const groupState = {{param:true,phys:true,ic:true,bhbh:true,bhns:true,nsns:true}};

function toggleGroup(g) {{
  groupState[g] = !groupState[g];
  document.querySelector(`.toggle-btn.${{g}}`).classList.toggle('active', groupState[g]);
  groupCols[g]().forEach(el => el.classList.toggle('col-hidden', !groupState[g]));
}}

function filterTable() {{
  const q = document.getElementById('search').value.toLowerCase();
  let vis = 0;
  document.querySelectorAll('#main-table tbody tr').forEach(row => {{
    const show = row.textContent.toLowerCase().includes(q);
    row.style.display = show ? '' : 'none';
    if (show) vis++;
  }});
  const tot = document.querySelectorAll('#main-table tbody tr').length;
  document.getElementById('row-count').textContent = `Showing ${{vis}} of ${{tot}} models`;
}}

let sortCol = -1, sortDir = 1;
document.querySelectorAll('th[data-sort]').forEach((th, i) => {{
  th.addEventListener('click', () => {{
    sortDir = (sortCol === i) ? -sortDir : 1;
    sortCol = i;
    document.querySelectorAll('th[data-sort]').forEach(t => t.classList.remove('asc','desc'));
    th.classList.add(sortDir === 1 ? 'asc' : 'desc');
    const tbody = document.querySelector('#main-table tbody');
    Array.from(tbody.querySelectorAll('tr'))
      .sort((a, b) => {{
        // +2 offset: paper col (0) + model col (1) have no data-sort, data cols start at td[2]
        const idx = i + 2;
        const ca = a.querySelectorAll('td')[idx]?.textContent.trim() ?? '';
        const cb = b.querySelectorAll('td')[idx]?.textContent.trim() ?? '';
        const na = parseFloat(ca.replace('%',''));
        const nb = parseFloat(cb.replace('%',''));
        if (!isNaN(na) && !isNaN(nb)) return sortDir * (na - nb);
        if (ca === '—' && cb !== '—') return sortDir;
        if (ca !== '—' && cb === '—') return -sortDir;
        return sortDir * ca.localeCompare(cb);
      }})
      .forEach(r => tbody.appendChild(r));
  }});
}});
</script>
</body>
</html>
"""

out_path = OUT_DIR + 'formation_channel_rates_table.html'
with open(out_path, 'w') as f:
    f.write(html_final)

print(f'Written: {out_path}')
print(f'Models: {len(all_models)}')
print(f'BPS data loaded for {len(bps)} models')
print(f'BH-BH: {sum(1 for m in all_models if m in bhbh_by)}  '
      f'BH-NS: {sum(1 for m in all_models if m in bhns_by)}  '
      f'NS-NS: {sum(1 for m in all_models if m in nsns_by)}')
# Spot-check a few BPS values
sample = next(iter(bps))
print(f'Sample BPS model: {sample}')
print(f'  IMF: {bps[sample].get("IMF","?")}')
print(f'  SFR: {bps[sample].get("SFR","?")}')
print(f'  gamma: {bps[sample].get("gamma","?")}')
