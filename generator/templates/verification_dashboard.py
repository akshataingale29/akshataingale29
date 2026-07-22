"""Template for the Verification Dashboard SVG."""

def render(projects: list, theme: dict) -> str:
    """Render the Verification Dashboard SVG.
    
    Only projects that have a 'verification' block will be rendered.
    """
    
    # Filter projects that have verification blocks
    verif_projects = [p for p in projects if "verification" in p]
    
    # SVG base header
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="850" height="300" viewBox="0 0 850 300">',
        '  <defs>',
        '    <style>',
        f'      .bg {{ fill: {theme.get("void", "#050510")}; rx: 8; stroke: {theme.get("star_dust", "#1e293b")}; stroke-width: 2; }}',
        f'      .header-bg {{ fill: {theme.get("star_dust", "#1e293b")}; rx: 8; }}',
        f'      .text-head {{ fill: {theme.get("text_bright", "#f1f5f9")}; font-family: monospace; font-size: 14px; font-weight: bold; }}',
        f'      .text-row {{ fill: {theme.get("text_dim", "#94a3b8")}; font-family: monospace; font-size: 13px; }}',
        f'      .text-pass {{ fill: {theme.get("synapse_cyan", "#64FFDA")}; font-family: monospace; font-size: 13px; font-weight: bold; }}',
        f'      .text-warn {{ fill: {theme.get("axon_amber", "#ff9900")}; font-family: monospace; font-size: 13px; font-weight: bold; }}',
        '      ',
        '      .cov-bg { fill: #1c1c38; rx: 3; }',
        '      .cov-bar { fill: #00d4ff; rx: 3; stroke-dasharray: 120; stroke-dashoffset: 120; }',
        '      ',
        f'      .divider {{ stroke: {theme.get("star_dust", "#1e293b")}; stroke-width: 1; }}',
        '',
        '      /* Animations */',
        '      .row { opacity: 0; animation: fade-in 0.5s forwards; }',
    ]

    # Generate animation delays dynamically based on the number of projects
    for i in range(len(verif_projects)):
        svg.append(f'      .r{i+1} {{ animation-delay: {0.3 + (i * 0.3):.1f}s; }}')
        svg.append(f'      .fill{i+1} {{ animation: fill-bar-{i+1} 1s forwards ease-out {0.5 + (i * 0.3):.1f}s; }}')

    svg.append('')
    svg.append('      @keyframes fade-in { to { opacity: 1; } }')
    
    # Generate keyframes for coverage bars
    for i, p in enumerate(verif_projects):
        cov = p["verification"].get("coverage", 0)
        # stroke-dashoffset for 120 width: 120 - (120 * cov / 100)
        offset = int(120 - (120 * cov / 100))
        svg.append(f'      @keyframes fill-bar-{i+1} {{ to {{ stroke-dashoffset: {offset}; }} }}')

    svg.extend([
        '    </style>',
        '  </defs>',
        '',
        '  <rect width="850" height="300" class="bg" />',
        '  ',
        '  <!-- Header Bar -->',
        '  <rect x="0" y="0" width="850" height="40" class="header-bg" />',
        '  <circle cx="20" cy="20" r="5" fill="#ef4444" />',
        '  <circle cx="40" cy="20" r="5" fill="#eab308" />',
        '  <circle cx="60" cy="20" r="5" fill="#22c55e" />',
        '  <text x="80" y="25" class="text-head">xrun -f run.f -cov -assert | Verification Dashboard</text>',
        '  ',
        '  <!-- Table Headers -->',
        '  <text x="30" y="70" class="text-head">IP / SUBSYSTEM</text>',
        '  <text x="280" y="70" class="text-head">METHODOLOGY</text>',
        '  <text x="450" y="70" class="text-head">FUNC. COVERAGE</text>',
        '  <text x="650" y="70" class="text-head">ASSERTIONS</text>',
        '  <text x="760" y="70" class="text-head">STATUS</text>',
        '  ',
        '  <path class="divider" d="M 0 85 L 850 85" />',
    ])

    # Generate rows
    y_base = 115
    for i, p in enumerate(verif_projects):
        v = p["verification"]
        name = v.get("name", p["repo"].split("/")[-1])
        methodology = v.get("methodology", "N/A")
        coverage = v.get("coverage", 0)
        assertions_pass = v.get("assertions_pass", 0)
        assertions_total = v.get("assertions_total", 0)
        status = v.get("status", "N/A")
        
        status_class = "text-pass" if status == "PASS" else "text-warn"
        y = y_base + (i * 30)
        
        svg.extend([
            f'  <!-- Row {i+1} -->',
            f'  <g class="row r{i+1}">',
            f'    <text x="30" y="{y}" class="text-row">{name}</text>',
            f'    <text x="280" y="{y}" class="text-row">{methodology}</text>',
            f'    <rect x="450" y="{y-10}" width="120" height="10" class="cov-bg" />',
            f'    <path class="cov-bar fill{i+1}" d="M 450 {y-5} L 570 {y-5}" stroke-width="10" />',
            f'    <text x="580" y="{y}" class="text-row">{coverage}%</text>',
            f'    <text x="650" y="{y}" class="text-row">{assertions_pass}/{assertions_total}</text>',
            f'    <text x="760" y="{y}" class="{status_class}">{status}</text>',
            f'  </g>',
        ])

    svg.append('</svg>')
    
    return "\n".join(svg)
