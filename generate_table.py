#!/usr/bin/env python3
"""Generate interactive HTML table combining formation channel rates with simulation specs."""
import csv
import os
import math

BASE = '/Users/floorbroekgaarden/Projects/GitHub/Rates_of_Formation_Channels/plottingCode/All_Figures/Data_formation_channels_intrinsic/'
OUT_DIR = '/Users/floorbroekgaarden/Projects/GitHub/Rates_of_Formation_Channels/interactive_figures_and_tables/'

os.makedirs(OUT_DIR, exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────

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
    """Format fraction as percentage with 1 decimal."""
    try:
        f = float(v)
        if f == 0.0:
            return '—'
        return f'{f * 100:.1f}%'
    except (ValueError, TypeError):
        return v if v else '—'

def fmt_rate(v):
    """Format rate to 2 decimal places."""
    try:
        f = float(v)
        return f'{f:.2f}'
    except (ValueError, TypeError):
        return v if v else '—'

def fmt_val(v, maxlen=40):
    """Format a generic string value, truncate if too long."""
    if not v:
        return '—'
    if len(v) > maxlen:
        return f'<span class="truncated" title="{escape(v)}">{escape(v[:maxlen])}…</span>'
    return escape(v)

def fmt_num(v, decimals=2):
    """Format a numeric string."""
    try:
        f = float(v)
        return f'{f:.{decimals}f}'
    except (ValueError, TypeError):
        return v if v else '—'

def escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def frac_val(v):
    """Return float fraction or None."""
    try:
        return float(v)
    except (ValueError, TypeError):
        return None

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lighten(h, t=0.35):
    """Blend hex color with white at fraction t (0=white, 1=original)."""
    r, g, b = hex_to_rgb(h)
    return f'#{int(r*t+255*(1-t)):02x}{int(g*t+255*(1-t)):02x}{int(b*t+255*(1-t)):02x}'

def text_on(h):
    """Return dark or light text color for readability on background h."""
    r, g, b = hex_to_rgb(h)
    return '#1a1a2e' if (0.299*r + 0.587*g + 0.114*b) / 255 > 0.55 else '#ffffff'

# ── load data ─────────────────────────────────────────────────────────────────

specs = read_csv(BASE + 'simulation_specs_detailed.csv', header_row=1)
bhbh  = read_csv(BASE + 'BH-BH_rates_review.csv',  header_row=0)
bhns  = read_csv(BASE + 'BH-NS_rates_review.csv',  header_row=0)
nsns  = read_csv(BASE + 'NS-NS_rates_review.csv',  header_row=0)

specs_by = {r['model']: r for r in specs}
bhbh_by  = {r['model']: r for r in bhbh}
bhns_by  = {r['model']: r for r in bhns}
nsns_by  = {r['model']: r for r in nsns}

all_models = sorted(specs_by.keys())

# ── column definitions ────────────────────────────────────────────────────────

# (source_key, display_name, format_fn, fc_color, tooltip)
# Colors match obtain_fc_dict() palette in the plotting code
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

SPEC_PUB_COLS = [
    # (spec_key, display_name, format_fn, tooltip)
    ('label_author', 'Study', None, 'Short author–year label for this study'),
    ('year',         'Year',  None, 'Publication year'),
    ('code',         'Code',  None, 'Population-synthesis code name'),
    ('stellar_tracks','Tracks',None,'Stellar evolution tracks used'),
]

SPEC_PARAM_COLS = [
    ('sigma',                   'σ<br>[km/s]',    lambda v: fmt_num(v,0), 'Natal kick dispersion σ for standard SN [km/s]'),
    ('sigma_strippedSN',        'σ stripped',     lambda v: fmt_num(v,0), 'Natal kick dispersion for stripped-star SN [km/s]'),
    ('alpha',                   'α CE',           lambda v: fmt_num(v,2), 'Common-envelope efficiency parameter α'),
    ('beta',                    'β',              lambda v: fmt_num(v,2), 'Mass-transfer efficiency parameter β'),
    ('CE optimistic/pessimistic','CE opt/pess',   None,                   'Optimistic or pessimistic CE survival assumption'),
    ('CE prescription',         'CE prescrip.',   lambda v: fmt_val(v,25),'CE energy prescription'),
    ('lambda',                  'λ',              lambda v: fmt_val(v,25),'Binding-energy lambda prescription'),
    ('PISN prescription',       'PISN',           lambda v: fmt_val(v,25),'Pair-instability supernova prescription'),
    ('stability',               'MT stability',   lambda v: fmt_val(v,25),'Mass-transfer stability criterion'),
    ('RMP',                     'RMP',            lambda v: fmt_val(v,30),'Remnant-mass prescription'),
]

# ── collect max rate per system type for heat-map scaling ─────────────────────

def max_rate(dataset):
    vals = []
    for r in dataset:
        v = frac_val(r.get('All intrinsic (z=0) [Gpc^-3 yr^-1]', ''))
        if v is not None:
            vals.append(v)
    return max(vals) if vals else 1.0

max_bhbh = max_rate(bhbh)
max_bhns = max_rate(bhns)
max_nsns = max_rate(nsns)

# ── HTML generation ───────────────────────────────────────────────────────────

def heatmap_style(frac, alpha_max=0.55):
    """Return inline style string for a fraction heat-map cell."""
    if frac is None or frac == 0.0:
        return ''
    intensity = min(frac, 1.0)
    a = intensity * alpha_max
    return f' style="background:rgba(255,140,0,{a:.3f})"'

def rate_heatmap_style(rate_val, max_val, color='200,100,50'):
    if rate_val is None or rate_val == 0.0:
        return ''
    intensity = min(rate_val / max_val, 1.0)
    a = 0.1 + intensity * 0.5
    return f' style="background:rgba({color},{a:.3f})"'

def render_rate_cell(row, col_key, fmt, max_val, color):
    val = row.get(col_key, '') if row else ''
    if col_key == 'All intrinsic (z=0) [Gpc^-3 yr^-1]':
        fv = frac_val(val)
        style = rate_heatmap_style(fv, max_val, color)
        return f'<td{style}>{fmt(val)}</td>'
    else:
        fv = frac_val(val)
        style = heatmap_style(fv)
        return f'<td{style}>{fmt(val)}</td>'

# Count columns for span calculations
n_pub   = len(SPEC_PUB_COLS)
n_param = len(SPEC_PARAM_COLS)
n_rate  = len(RATE_COLS)

rows_html = []
for m in all_models:
    spec = specs_by.get(m, {})
    bh   = bhbh_by.get(m)
    bn   = bhns_by.get(m)
    nn   = nsns_by.get(m)

    # model ID cell (sticky)
    paper_link = spec.get('link to paper', '').strip()
    model_text = escape(m)
    if paper_link:
        model_cell = f'<td class="model-col"><a href="{escape(paper_link)}" target="_blank" title="Open paper for {model_text}">{model_text}</a></td>'
    else:
        model_cell = f'<td class="model-col">{model_text}</td>'

    # publication cols
    pub_cells = []
    for key, _, fmt_fn, _ in SPEC_PUB_COLS:
        v = spec.get(key, '')
        if fmt_fn:
            pub_cells.append(f'<td>{fmt_fn(v)}</td>')
        else:
            pub_cells.append(f'<td>{fmt_val(v, 30)}</td>')

    # parameter cols
    param_cells = []
    for key, _, fmt_fn, _ in SPEC_PARAM_COLS:
        v = spec.get(key, '')
        if fmt_fn:
            param_cells.append(f'<td>{fmt_fn(v)}</td>')
        else:
            param_cells.append(f'<td>{fmt_val(v, 30)}</td>')

    # rate cols for each system type
    def rate_cells(dataset_row, max_val, color):
        if dataset_row is None:
            return ''.join(['<td class="no-data">—</td>'] * n_rate)
        cells = []
        for col_key, _, fmt_fn, _, _ in RATE_COLS:
            cells.append(render_rate_cell(dataset_row, col_key, fmt_fn, max_val, color))
        return ''.join(cells)

    row_html = (
        '<tr>'
        + model_cell
        + ''.join(pub_cells)
        + ''.join(param_cells)
        + rate_cells(bh, max_bhbh, '220,100,50')
        + rate_cells(bn, max_bhns, '130,80,190')
        + rate_cells(nn, max_nsns, '50,160,80')
        + '</tr>'
    )
    rows_html.append(row_html)

rows_str = '\n'.join(rows_html)

# Build header rows
def th(label, cls='', tooltip='', rowspan=1, colspan=1):
    rs = f' rowspan="{rowspan}"' if rowspan > 1 else ''
    cs = f' colspan="{colspan}"' if colspan > 1 else ''
    tt = f' title="{escape(tooltip)}"' if tooltip else ''
    c  = f' class="{cls}"' if cls else ''
    return f'<th{c}{rs}{cs}{tt}>{label}</th>'

# Row 1: group headers
grp_row1 = (
    th('Model ID', 'hdr-model', rowspan=2)
    + th('Publication Info', 'hdr-pub', colspan=n_pub)
    + th('Simulation Parameters', 'hdr-param', colspan=n_param)
    + th('BH–BH Formation Channels', 'hdr-bhbh', colspan=n_rate)
    + th('BH–NS Formation Channels', 'hdr-bhns', colspan=n_rate)
    + th('NS–NS Formation Channels', 'hdr-nsns', colspan=n_rate)
)

# Row 2: individual column headers
def col_headers(cols_list, cls):
    return ''.join(th(dn, cls, tt) for _, dn, _, tt in cols_list)

def rate_col_headers(cls):
    return ''.join(th(dn, cls, tt) for _, dn, _, _, tt in RATE_COLS)

grp_row2 = (
    ''.join(th(dn, 'hdr-pub-col', tt) for _, dn, _, tt in SPEC_PUB_COLS)
    + ''.join(th(dn, 'hdr-param-col', tt) for _, dn, _, tt in SPEC_PARAM_COLS)
    + rate_col_headers('hdr-bhbh-col')
    + rate_col_headers('hdr-bhns-col')
    + rate_col_headers('hdr-nsns-col')
)

# ── final HTML ────────────────────────────────────────────────────────────────

n_total_cols = 1 + n_pub + n_param + n_rate * 3

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Compact Binary Formation Channel Rates — Simulation Survey</title>
<style>
  /* ── reset & base ── */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 13px;
    background: #f4f6f9;
    color: #1a1a2e;
    padding: 20px;
  }}

  /* ── page header ── */
  .page-header {{
    max-width: 1600px;
    margin: 0 auto 18px;
  }}
  .page-header h1 {{
    font-size: 1.6rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 6px;
  }}
  .page-header p {{
    color: #555;
    line-height: 1.55;
    max-width: 860px;
    font-size: 0.9rem;
  }}
  .page-header a {{ color: #3a6ea5; }}

  /* ── controls bar ── */
  .controls {{
    max-width: 1600px;
    margin: 0 auto 14px;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
  }}
  #search {{
    padding: 7px 12px;
    border: 1px solid #ccd;
    border-radius: 6px;
    font-size: 13px;
    width: 260px;
    outline: none;
    transition: border-color .2s;
  }}
  #search:focus {{ border-color: #3a6ea5; }}
  .toggle-group {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }}
  .toggle-btn {{
    padding: 5px 12px;
    border-radius: 20px;
    border: 2px solid;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
    transition: all .15s;
    user-select: none;
  }}
  .toggle-btn.pub    {{ border-color:#3f51b5; color:#3f51b5; background:#f0f1fb; }}
  .toggle-btn.param  {{ border-color:#00796b; color:#00796b; background:#e0f2f1; }}
  .toggle-btn.bhbh   {{ border-color:#bf360c; color:#bf360c; background:#fbe9e7; }}
  .toggle-btn.bhns   {{ border-color:#6a1b9a; color:#6a1b9a; background:#f3e5f5; }}
  .toggle-btn.nsns   {{ border-color:#1b5e20; color:#1b5e20; background:#e8f5e9; }}
  .toggle-btn.active {{ color:#fff !important; }}
  .toggle-btn.pub.active   {{ background:#3f51b5; }}
  .toggle-btn.param.active {{ background:#00796b; }}
  .toggle-btn.bhbh.active  {{ background:#bf360c; }}
  .toggle-btn.bhns.active  {{ background:#6a1b9a; }}
  .toggle-btn.nsns.active  {{ background:#1b5e20; }}
  .row-count {{
    margin-left: auto;
    font-size: 12px;
    color: #666;
    padding: 5px 0;
  }}

  /* ── table wrapper ── */
  .table-wrap {{
    max-width: 100%;
    overflow-x: auto;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,.12);
  }}

  /* ── table ── */
  table {{
    border-collapse: collapse;
    white-space: nowrap;
    background: #fff;
    min-width: 100%;
  }}
  thead {{ position: sticky; top: 0; z-index: 10; }}
  th, td {{
    padding: 5px 9px;
    border: 1px solid #dde;
    text-align: center;
    vertical-align: middle;
  }}

  /* ── group header row ── */
  .hdr-model  {{ background:#2c3e50; color:#fff; font-size:12px; position:sticky; left:0; z-index:20; min-width:160px; }}
  .hdr-pub    {{ background:#3f51b5; color:#fff; font-size:12px; }}
  .hdr-param  {{ background:#00796b; color:#fff; font-size:12px; }}
  .hdr-bhbh   {{ background:#bf360c; color:#fff; font-size:12px; }}
  .hdr-bhns   {{ background:#6a1b9a; color:#fff; font-size:12px; }}
  .hdr-nsns   {{ background:#1b5e20; color:#fff; font-size:12px; }}

  /* ── column sub-header row ── */
  .hdr-pub-col   {{ background:#c5cae9; color:#1a237e; font-size:11px; line-height:1.2; }}
  .hdr-param-col {{ background:#b2dfdb; color:#004d40; font-size:11px; line-height:1.2; }}
  .hdr-bhbh-col  {{ background:#ffccbc; color:#7f2a00; font-size:11px; line-height:1.2; }}
  .hdr-bhns-col  {{ background:#e1bee7; color:#4a0072; font-size:11px; line-height:1.2; }}
  .hdr-nsns-col  {{ background:#c8e6c9; color:#1b5e20; font-size:11px; line-height:1.2; }}

  /* sortable indicator */
  th[data-sort] {{ cursor:pointer; }}
  th[data-sort]:hover {{ filter: brightness(1.12); }}
  th[data-sort]::after {{ content:' ↕'; font-size:10px; opacity:.5; }}
  th[data-sort].asc::after  {{ content:' ▲'; opacity:1; }}
  th[data-sort].desc::after {{ content:' ▼'; opacity:1; }}

  /* ── data cells ── */
  td {{ font-size: 12px; color: #222; }}
  .model-col {{
    font-family: 'SF Mono', 'Fira Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    position: sticky;
    left: 0;
    background: #fff;
    z-index: 5;
    border-right: 2px solid #aab;
    text-align: left;
    min-width: 160px;
  }}
  .model-col a {{ color:#1a1a2e; text-decoration:none; border-bottom:1px dotted #888; }}
  .model-col a:hover {{ color:#3a6ea5; }}

  /* zebra striping */
  tbody tr:nth-child(even) td {{ background-color: #f9faff; }}
  tbody tr:nth-child(even) .model-col {{ background-color: #f0f2f8; }}
  tbody tr:hover td {{ background-color: #fffbe6 !important; }}
  tbody tr:hover .model-col {{ background-color: #fffbe6 !important; }}

  td.no-data {{ color: #bbb; }}

  /* pub / param cell coloring */
  td.pub-cell   {{ background: #f0f1fb; }}
  td.param-cell {{ background: #f0faf9; }}

  /* truncated text */
  .truncated {{ cursor: help; border-bottom: 1px dotted #999; }}

  /* ── hidden columns ── */
  .col-pub   {{ }}
  .col-param {{ }}
  .col-bhbh  {{ }}
  .col-bhns  {{ }}
  .col-nsns  {{ }}
  .col-hidden {{ display: none !important; }}

  /* ── footer ── */
  .footer {{
    max-width: 1600px;
    margin: 16px auto 0;
    font-size: 11px;
    color: #888;
  }}
</style>
</head>
<body>

<div class="page-header">
  <h1>Compact Binary Formation Channel Rates — Simulation Survey</h1>
  <p>
    Combined table of simulated merger rates and formation channel fractions for
    BH–BH, BH–NS, and NS–NS binaries from {len(all_models)} population-synthesis models.
    Channel fractions are intrinsic rates at <em>z</em> = 0 normalised to the total rate per model.
    Hover over truncated cells (…) to read the full text.
    Click column headers to sort. Use the toggles to show/hide column groups.
    Model names link to the corresponding paper.
  </p>
</div>

<div class="controls">
  <input type="text" id="search" placeholder="🔍  Filter models…" oninput="filterTable()">
  <div class="toggle-group">
    <span style="font-size:12px;color:#555;font-weight:600;">Toggle columns:</span>
    <button class="toggle-btn pub active"   onclick="toggleGroup('pub')">Publication Info</button>
    <button class="toggle-btn param active" onclick="toggleGroup('param')">Sim. Parameters</button>
    <button class="toggle-btn bhbh active"  onclick="toggleGroup('bhbh')">BH–BH</button>
    <button class="toggle-btn bhns active"  onclick="toggleGroup('bhns')">BH–NS</button>
    <button class="toggle-btn nsns active"  onclick="toggleGroup('nsns')">NS–NS</button>
  </div>
  <span class="row-count" id="row-count">Showing {len(all_models)} of {len(all_models)} models</span>
</div>

<div class="table-wrap">
<table id="main-table">
<thead>
<tr>
{grp_row1}
</tr>
<tr>
{grp_row2}
</tr>
</thead>
<tbody>
{rows_str}
</tbody>
</table>
</div>

<div class="footer">
  <p>
    Channel definitions — Ch. I: stable mass transfer followed by common-envelope (SMT+CE);
    Ch. III: single CE (SCCE); Ch. IV: double CE (DCCE); SMT: stable mass transfer only (no CE);
    CHE: chemically homogeneous evolution. Rates in Gpc⁻³ yr⁻¹ (intrinsic, <em>z</em> = 0).
    Fractions are shown as percentages; orange shading scales with fraction value.
    &mdash; Table generated from review data by Floor Broekgaarden.
  </p>
</div>

<script>
// ── column group toggle ────────────────────────────────────────────────────
const groupCols = {{
  pub:   document.querySelectorAll('.hdr-pub, .hdr-pub-col, .col-pub'),
  param: document.querySelectorAll('.hdr-param, .hdr-param-col, .col-param'),
  bhbh:  document.querySelectorAll('.hdr-bhbh, .hdr-bhbh-col, .col-bhbh'),
  bhns:  document.querySelectorAll('.hdr-bhns, .hdr-bhns-col, .col-bhns'),
  nsns:  document.querySelectorAll('.hdr-nsns, .hdr-nsns-col, .col-nsns'),
}};
const groupState = {{ pub: true, param: true, bhbh: true, bhns: true, nsns: true }};

function toggleGroup(g) {{
  groupState[g] = !groupState[g];
  const btn = document.querySelector(`.toggle-btn.${{g}}`);
  btn.classList.toggle('active', groupState[g]);
  groupCols[g].forEach(el => el.classList.toggle('col-hidden', !groupState[g]));
}}

// ── search / filter ────────────────────────────────────────────────────────
function filterTable() {{
  const q = document.getElementById('search').value.toLowerCase();
  const rows = document.querySelectorAll('#main-table tbody tr');
  let visible = 0;
  rows.forEach(row => {{
    const text = row.textContent.toLowerCase();
    const show = text.includes(q);
    row.style.display = show ? '' : 'none';
    if (show) visible++;
  }});
  document.getElementById('row-count').textContent =
    `Showing ${{visible}} of ${{rows.length}} models`;
}}

// ── sort ───────────────────────────────────────────────────────────────────
let sortCol = -1, sortDir = 1;

document.querySelectorAll('th[data-sort]').forEach((th, idx) => {{
  th.addEventListener('click', () => {{
    if (sortCol === idx) {{ sortDir *= -1; }}
    else {{ sortCol = idx; sortDir = 1; }}
    document.querySelectorAll('th[data-sort]').forEach(t =>
      t.classList.remove('asc', 'desc'));
    th.classList.add(sortDir === 1 ? 'asc' : 'desc');
    sortTable(idx, sortDir);
  }});
}});

function sortTable(colIdx, dir) {{
  const tbody = document.querySelector('#main-table tbody');
  const rows  = Array.from(tbody.querySelectorAll('tr'));
  rows.sort((a, b) => {{
    const cellA = a.querySelectorAll('td')[colIdx]?.textContent.trim() || '';
    const cellB = b.querySelectorAll('td')[colIdx]?.textContent.trim() || '';
    const na = parseFloat(cellA.replace('%',''));
    const nb = parseFloat(cellB.replace('%',''));
    if (!isNaN(na) && !isNaN(nb)) return dir * (na - nb);
    return dir * cellA.localeCompare(cellB);
  }});
  rows.forEach(r => tbody.appendChild(r));
}}
</script>
</body>
</html>
"""

# ── add class tags to data cells and header cells ─────────────────────────────
# We need to re-generate with proper class attributes on data cells.
# Instead, let's regenerate rows with class annotations.

def render_rows():
    out = []
    for m in all_models:
        spec = specs_by.get(m, {})
        bh   = bhbh_by.get(m)
        bn   = bhns_by.get(m)
        nn   = nsns_by.get(m)

        # model cell
        paper_link = spec.get('link to paper', '').strip()
        model_text = escape(m)
        if paper_link:
            mc = f'<td class="model-col"><a href="{escape(paper_link)}" target="_blank">{model_text}</a></td>'
        else:
            mc = f'<td class="model-col">{model_text}</td>'

        # pub cells
        pub = []
        for key, _, fmt_fn, _ in SPEC_PUB_COLS:
            v = spec.get(key, '')
            txt = fmt_fn(v) if fmt_fn else fmt_val(v, 30)
            pub.append(f'<td class="col-pub pub-cell">{txt}</td>')

        # param cells
        par = []
        for key, _, fmt_fn, _ in SPEC_PARAM_COLS:
            v = spec.get(key, '')
            txt = fmt_fn(v) if fmt_fn else fmt_val(v, 30)
            par.append(f'<td class="col-param param-cell">{txt}</td>')

        # rate section
        def rate_section(dataset_row, cls, max_val, rate_color):
            if dataset_row is None:
                return [f'<td class="col-{cls} no-data">—</td>'] * n_rate
            cells = []
            for col_key, _, fmt_fn, ch_color, _ in RATE_COLS:
                val = dataset_row.get(col_key, '')
                if col_key == 'All intrinsic (z=0) [Gpc^-3 yr^-1]':
                    fv = frac_val(val)
                    a = (0.1 + min(fv / max_val, 1.0) * 0.5) if fv else 0
                    style = f' style="background:rgba({rate_color},{a:.3f})"' if fv else ''
                    cells.append(f'<td class="col-{cls}"{style}>{fmt_fn(val)}</td>')
                else:
                    fv = frac_val(val)
                    if fv and fv > 0:
                        r, g, b = hex_to_rgb(ch_color)
                        a = 0.15 + min(fv, 1.0) * 0.6
                        cells.append(f'<td class="col-{cls}" style="background:rgba({r},{g},{b},{a:.3f})">{fmt_fn(val)}</td>')
                    else:
                        cells.append(f'<td class="col-{cls}">{fmt_fn(val)}</td>')
            return cells

        bh_cells = rate_section(bh, 'bhbh', max_bhbh, '220,100,50')
        bn_cells = rate_section(bn, 'bhns', max_bhns, '130,80,190')
        nn_cells = rate_section(nn, 'nsns', max_nsns, '50,160,80')

        out.append(
            '<tr>'
            + mc
            + ''.join(pub)
            + ''.join(par)
            + ''.join(bh_cells)
            + ''.join(bn_cells)
            + ''.join(nn_cells)
            + '</tr>'
        )
    return '\n'.join(out)

# rebuild group header row 1 with colspan on group headers
n_pub_   = len(SPEC_PUB_COLS)
n_param_ = len(SPEC_PARAM_COLS)
n_rate_  = len(RATE_COLS)

def th2(label, cls='', tooltip='', rowspan=1, colspan=1, sort=False):
    rs = f' rowspan="{rowspan}"' if rowspan > 1 else ''
    cs = f' colspan="{colspan}"' if colspan > 1 else ''
    tt = f' title="{escape(tooltip)}"' if tooltip else ''
    c  = f' class="{cls}"' if cls else ''
    ds = ' data-sort="true"' if sort else ''
    return f'<th{c}{rs}{cs}{tt}{ds}>{label}</th>'

grp1 = (
    th2('Model', 'hdr-model', 'Population-synthesis model identifier', rowspan=2)
    + th2('Publication Info', 'hdr-pub', colspan=n_pub_)
    + th2('Simulation Parameters', 'hdr-param', colspan=n_param_)
    + th2('BH–BH Formation Channels', 'hdr-bhbh', colspan=n_rate_)
    + th2('BH–NS Formation Channels', 'hdr-bhns', colspan=n_rate_)
    + th2('NS–NS Formation Channels', 'hdr-nsns', colspan=n_rate_)
)

def th_rate_col(label, fc_color, grp_cls, tooltip=''):
    """Sub-header cell with inline background color from fc_dict palette."""
    bg = lighten(fc_color, t=0.40)
    txt = text_on(bg)
    tt = f' title="{escape(tooltip)}"' if tooltip else ''
    return (f'<th class="{grp_cls}" style="background:{bg};color:{txt};'
            f'font-size:11px;line-height:1.3;font-weight:600;" data-sort="true"{tt}>{label}</th>')

grp2 = (
    ''.join(th2(dn, 'hdr-pub-col',   tt, sort=True) for _, dn, _, tt in SPEC_PUB_COLS)
    + ''.join(th2(dn, 'hdr-param-col', tt, sort=True) for _, dn, _, tt in SPEC_PARAM_COLS)
    + ''.join(th_rate_col(dn, col, 'hdr-bhbh-col', tt) for _, dn, _, col, tt in RATE_COLS)
    + ''.join(th_rate_col(dn, col, 'hdr-bhns-col', tt) for _, dn, _, col, tt in RATE_COLS)
    + ''.join(th_rate_col(dn, col, 'hdr-nsns-col', tt) for _, dn, _, col, tt in RATE_COLS)
)

rows_final = render_rows()

html_final = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Compact Binary Formation Channel Rates — Simulation Survey</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 13px;
  background: #f4f6f9;
  color: #1a1a2e;
  padding: 24px 20px;
}}
.page-header {{
  max-width: 1500px;
  margin: 0 auto 18px;
}}
.page-header h1 {{
  font-size: 1.55rem;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 8px;
  letter-spacing: -.3px;
}}
.page-header p {{
  color: #555;
  line-height: 1.6;
  max-width: 860px;
  font-size: 0.875rem;
}}
.page-header a {{ color: #3a6ea5; }}
.controls {{
  max-width: 1500px;
  margin: 0 auto 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}}
#search {{
  padding: 7px 13px;
  border: 1.5px solid #ccd;
  border-radius: 20px;
  font-size: 13px;
  width: 240px;
  outline: none;
  transition: border-color .2s, box-shadow .2s;
}}
#search:focus {{ border-color: #3a6ea5; box-shadow: 0 0 0 3px rgba(58,110,165,.15); }}
.toggle-group {{
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  align-items: center;
}}
.toggle-label {{ font-size: 12px; color: #555; font-weight: 600; }}
.toggle-btn {{
  padding: 5px 13px;
  border-radius: 20px;
  border: 2px solid;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all .15s;
  user-select: none;
  background: transparent;
}}
.toggle-btn.pub   {{ border-color:#3f51b5; color:#3f51b5; }}
.toggle-btn.param {{ border-color:#00796b; color:#00796b; }}
.toggle-btn.bhbh  {{ border-color:#bf360c; color:#bf360c; }}
.toggle-btn.bhns  {{ border-color:#6a1b9a; color:#6a1b9a; }}
.toggle-btn.nsns  {{ border-color:#1b5e20; color:#1b5e20; }}
.toggle-btn.active {{ color:#fff !important; }}
.toggle-btn.pub.active   {{ background:#3f51b5; }}
.toggle-btn.param.active {{ background:#00796b; }}
.toggle-btn.bhbh.active  {{ background:#bf360c; }}
.toggle-btn.bhns.active  {{ background:#6a1b9a; }}
.toggle-btn.nsns.active  {{ background:#1b5e20; }}
.row-count {{
  margin-left: auto;
  font-size: 12px;
  color: #777;
  white-space: nowrap;
}}
.table-wrap {{
  max-width: 100%;
  overflow-x: auto;
  border-radius: 10px;
  box-shadow: 0 3px 16px rgba(0,0,0,.13);
}}
table {{
  border-collapse: collapse;
  white-space: nowrap;
  background: #fff;
  min-width: 100%;
}}
thead {{ position: sticky; top: 0; z-index: 10; }}
th, td {{
  padding: 5px 10px;
  border: 1px solid #e0e4ef;
  text-align: center;
  vertical-align: middle;
}}
/* Group header row */
.hdr-model  {{ background:#2c3e50; color:#ecf0f1; font-weight:700; position:sticky; left:0; z-index:25; min-width:175px; letter-spacing:.2px; }}
.hdr-pub    {{ background:#3f51b5; color:#fff; font-weight:700; font-size:12px; }}
.hdr-param  {{ background:#00796b; color:#fff; font-weight:700; font-size:12px; }}
.hdr-bhbh   {{ background:#bf360c; color:#fff; font-weight:700; font-size:12px; }}
.hdr-bhns   {{ background:#6a1b9a; color:#fff; font-weight:700; font-size:12px; }}
.hdr-nsns   {{ background:#1b5e20; color:#fff; font-weight:700; font-size:12px; }}
/* Sub-header row */
.hdr-pub-col   {{ background:#c5cae9; color:#1a237e; font-size:11px; line-height:1.3; font-weight:600; }}
.hdr-param-col {{ background:#b2dfdb; color:#004d40; font-size:11px; line-height:1.3; font-weight:600; }}
.hdr-bhbh-col  {{ background:#ffccbc; color:#7f2a00; font-size:11px; line-height:1.3; font-weight:600; }}
.hdr-bhns-col  {{ background:#e1bee7; color:#4a0072; font-size:11px; line-height:1.3; font-weight:600; }}
.hdr-nsns-col  {{ background:#c8e6c9; color:#1b5e20; font-size:11px; line-height:1.3; font-weight:600; }}
/* Sort indicator */
th[data-sort] {{ cursor:pointer; }}
th[data-sort]:hover {{ filter: brightness(1.1); }}
th[data-sort]::after {{ content:' ↕'; font-size:9px; opacity:.45; }}
th[data-sort].asc::after  {{ content:' ▲'; opacity:1; }}
th[data-sort].desc::after {{ content:' ▼'; opacity:1; }}
/* Data cells */
td {{ font-size: 12px; color: #2a2a3e; }}
.model-col {{
  font-family: 'SF Mono', 'Fira Mono', 'Consolas', monospace;
  font-size: 11px;
  font-weight: 600;
  position: sticky;
  left: 0;
  background: #fff;
  z-index: 5;
  border-right: 2.5px solid #aab;
  text-align: left;
  min-width: 175px;
  padding-left: 10px;
}}
.model-col a {{
  color: #1a1a2e;
  text-decoration: none;
  border-bottom: 1px dashed #90a;
}}
.model-col a:hover {{ color: #3a6ea5; border-bottom-color: #3a6ea5; }}
/* Zebra + hover */
tbody tr:nth-child(even) td {{ background-color: #f8f9ff; }}
tbody tr:nth-child(even) .model-col {{ background-color: #eff1fa; }}
tbody tr:hover td {{ background-color: #fffde0 !important; }}
tbody tr:hover .model-col {{ background-color: #fffde0 !important; }}
/* Pub/param tint */
.pub-cell   {{ background: rgba(63,81,181,0.05); }}
.param-cell {{ background: rgba(0,121,107,0.05); }}
tbody tr:nth-child(even) .pub-cell   {{ background: rgba(63,81,181,0.09); }}
tbody tr:nth-child(even) .param-cell {{ background: rgba(0,121,107,0.09); }}
td.no-data {{ color: #ccc; }}
.truncated {{ cursor: help; border-bottom: 1px dotted #999; }}
.col-hidden {{ display: none !important; }}
.footer {{
  max-width: 1500px;
  margin: 16px auto 0;
  font-size: 11.5px;
  color: #888;
  line-height: 1.55;
}}
.legend {{
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
  margin-top: 8px;
  padding: 10px 14px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e0e4ef;
  max-width: 1500px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 12px;
}}
.legend-item {{ font-size: 11.5px; color: #555; display:flex; align-items:center; gap:5px; }}
.legend-item b {{ color: #333; }}
.swatch {{ display:inline-block; width:12px; height:12px; border-radius:3px; flex-shrink:0; border:1px solid rgba(0,0,0,.15); }}
</style>
</head>
<body>

<div class="page-header">
  <h1>Compact Binary Merger Rates and Formation Channels — Simulation Survey</h1>
  <p>
    This table combines simulated intrinsic merger rates and formation channel fractions for
    <strong>BH–BH</strong>, <strong>BH–NS</strong>, and <strong>NS–NS</strong> binaries
    from <strong>{len(all_models)} population-synthesis models</strong> across multiple studies.
    Channel fractions are evaluated at redshift <em>z</em>&nbsp;=&nbsp;0.
    Cell shading for each channel uses its own color (matching the formation-channel figures) and scales with the fraction value.
    Rate columns are shaded relative to the maximum across all models for that binary type.
    Click any column header to sort. Use the toggles to hide/show column groups.
    Model names link to the source paper.
  </p>
</div>

<div class="controls">
  <input type="text" id="search" placeholder="🔍  Filter by model name or value…" oninput="filterTable()">
  <div class="toggle-group">
    <span class="toggle-label">Show/hide:</span>
    <button class="toggle-btn pub active"   onclick="toggleGroup('pub')">Publication Info</button>
    <button class="toggle-btn param active" onclick="toggleGroup('param')">Sim. Parameters</button>
    <button class="toggle-btn bhbh active"  onclick="toggleGroup('bhbh')">BH–BH Channels</button>
    <button class="toggle-btn bhns active"  onclick="toggleGroup('bhns')">BH–NS Channels</button>
    <button class="toggle-btn nsns active"  onclick="toggleGroup('nsns')">NS–NS Channels</button>
  </div>
  <span class="row-count" id="row-count">Showing {len(all_models)} of {len(all_models)} models</span>
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

<div class="legend">
  <div class="legend-item"><span class="swatch" style="background:#b8a0ff"></span><b>CHE (no MT):</b> chemically homogeneous evolution</div>
  <div class="legend-item"><span class="swatch" style="background:#FFA630"></span><b>classic SMT (SMT+SMT):</b> stable mass transfer, no CE</div>
  <div class="legend-item"><span class="swatch" style="background:#ffb5a7"></span><b>other without CE:</b> other non-CE channels</div>
  <div class="legend-item"><span class="swatch" style="background:#00A7E1"></span><b>classic CE (SMT+CE):</b> stable MT then common-envelope</div>
  <div class="legend-item"><span class="swatch" style="background:#0474BA"></span><b>single-core CE (SCCE):</b> one evolved star in CE</div>
  <div class="legend-item"><span class="swatch" style="background:#20b2aa"></span><b>double-core CE (DCCE):</b> both cores in CE simultaneously</div>
  <div class="legend-item"><span class="swatch" style="background:#8dd3c7"></span><b>other with CE:</b> other CE channels</div>
  <div class="legend-item"><span class="swatch" style="background:#FFA630"></span><b>without common envelope:</b> total f(no CE)</div>
  <div class="legend-item"><span class="swatch" style="background:#00A7E1"></span><b>with common envelope:</b> total f(CE)</div>
  <div class="legend-item"><b>—:</b> not reported / zero</div>
</div>

<div class="footer">
  Table generated from population-synthesis review data.
  For questions or corrections, contact Floor Broekgaarden.
</div>

<script>
const groupCols = {{
  pub:   () => document.querySelectorAll('.hdr-pub, .hdr-pub-col, .col-pub'),
  param: () => document.querySelectorAll('.hdr-param, .hdr-param-col, .col-param'),
  bhbh:  () => document.querySelectorAll('.hdr-bhbh, .hdr-bhbh-col, .col-bhbh'),
  bhns:  () => document.querySelectorAll('.hdr-bhns, .hdr-bhns-col, .col-bhns'),
  nsns:  () => document.querySelectorAll('.hdr-nsns, .hdr-nsns-col, .col-nsns'),
}};
const groupState = {{ pub:true, param:true, bhbh:true, bhns:true, nsns:true }};

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
        // offset by 1 because model col has no data-sort, it occupies col 0
        const idx = i + 1;
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
print(f'BH-BH models in table: {sum(1 for m in all_models if m in bhbh_by)}')
print(f'BH-NS models in table: {sum(1 for m in all_models if m in bhns_by)}')
print(f'NS-NS models in table: {sum(1 for m in all_models if m in nsns_by)}')
