#!/usr/bin/env python3
"""Build/check a multi-file Beamer deck and optionally render review PNGs."""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def diagnostics(log):
    fatal = []
    warnings = []
    for line in log.splitlines():
        if re.search(r'Overfull|Missing character:|Undefined control sequence|Academic Beamer:|Package academic-beamer Error|^! |LaTeX Error:', line):
            fatal.append(line.strip())
        elif 'Warning:' in line or 'Underfull' in line:
            warnings.append(line.strip())
    if re.search(r'(?:Citation|Reference).*undefined|There were undefined', log):
        fatal.append('Undefined reference or citation')
    return fatal, warnings


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--render', action='store_true')
    a = p.parse_args()
    source = a.source.expanduser().resolve(strict=True)
    if source.suffix != '.tex':
        p.error('source must be a .tex file')
    output = a.output.expanduser().absolute()
    latexmk = shutil.which('latexmk')
    renderer = shutil.which('pdftoppm')
    if not latexmk:
        p.error('latexmk is unavailable; use an existing TeX installation')
    if a.render and not renderer:
        p.error('pdftoppm is unavailable; no dependencies installed')
    output.mkdir(parents=True, exist_ok=True)
    build_dir = output / '.build'
    build_dir.mkdir(exist_ok=True)
    result = subprocess.run([latexmk, '-pdf', '-silent', '-interaction=nonstopmode',
        '-halt-on-error', '-no-shell-escape', f'-outdir={build_dir}', source.name],
        cwd=source.parent, capture_output=True, text=True)
    (build_dir / 'build-console.txt').write_text(result.stdout + result.stderr)
    log_path = build_dir / f'{source.stem}.log'
    fatal, warnings = diagnostics(log_path.read_text(errors='replace') if log_path.exists() else '')
    pdf = build_dir / f'{source.stem}.pdf'
    if result.returncode or fatal or not pdf.exists():
        print(json.dumps({'status': 'failed', 'errors': fatal, 'log': str(log_path)}, indent=2))
        raise SystemExit(1)
    rendered = []
    if a.render:
        renders = output / 'renders'
        renders.mkdir(exist_ok=True)
        prefix = renders / source.stem
        # Clear only this deck's previous numbered preview files, never a directory tree.
        pattern = re.compile(re.escape(source.stem) + r'-\d+\.png\Z')
        for file in renders.iterdir():
            if file.is_file() and pattern.fullmatch(file.name):
                file.unlink()
        proc = subprocess.run([renderer, '-scale-to', '1600', '-png', str(pdf), str(prefix)],
            capture_output=True, text=True)
        (build_dir / 'render-console.txt').write_text(proc.stdout + proc.stderr)
        if proc.returncode:
            raise SystemExit('PNG rendering failed; see render-console.txt')
        rendered = sorted(str(x) for x in renders.iterdir() if pattern.fullmatch(x.name))
        if not rendered:
            raise SystemExit('No rendered PNGs found')
    final = output / pdf.name
    with tempfile.NamedTemporaryFile(dir=output, suffix='.pdf', delete=False) as staging:
        stage_path = Path(staging.name)
    try:
        shutil.copyfile(pdf, stage_path)
        os.replace(stage_path, final)
    finally:
        stage_path.unlink(missing_ok=True)
    report = {'status': 'automatic_checks_passed', 'pdf': str(final),
        'pdf_sha256': hashlib.sha256(final.read_bytes()).hexdigest(),
        'warnings': warnings, 'rendered_pages': len(rendered), 'visual_review': 'pending',
        'readability_metadata_unverified': 'readability unverified' in log_path.read_text(errors='replace')}
    (output / f'{source.stem}-checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
