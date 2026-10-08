#!/usr/bin/env python3
"""Copy a clean editable starter to a new directory, without overwriting."""
import argparse
import re
import shutil
from pathlib import Path


def main():
    source = Path(__file__).resolve().parents[1] / 'assets' / 'starter'
    presets = sorted(file.stem for file in (source / 'theme/presets').glob('*.tex')
                     if re.fullmatch(r'[a-z][a-z0-9-]*', file.stem))
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('destination', type=Path, nargs='?')
    p.add_argument('--preset', choices=presets, default='classic')
    p.add_argument('--list-presets', action='store_true', help='list available designs without writing files')
    a = p.parse_args()
    if a.list_presets:
        print('\n'.join(presets))
        return
    if a.destination is None:
        p.error('destination is required unless --list-presets is used')
    target = a.destination.expanduser().absolute()
    if target.exists() or target.is_symlink():
        p.error('destination already exists; no files changed')
    config = (source / 'config.tex').read_text()
    selector = r'\AcademicPreset{classic}'
    if config.count(selector) != 1:
        p.error('starter must have exactly one default preset selector; no files changed')
    config = config.replace(selector, r'\AcademicPreset{' + a.preset + '}')
    def ignore_generated(directory, names):
        ignored = set(shutil.ignore_patterns('.build', 'output', '__pycache__', '*.aux', '*.log',
            '*.nav', '*.snm', '*.toc', '*.out', '*.fls', '*.fdb_latexmk', '*.synctex.gz')(directory, names))
        if Path(directory) == source:
            ignored.add('main.pdf')
        return ignored

    # Keep legitimate vector PDF assets; exclude only builds and deck output.
    shutil.copytree(source, target, ignore=ignore_generated)
    (target / 'config.tex').write_text(config)
    print(f'Created editable starter: {target} (preset: {a.preset})')


if __name__ == '__main__':
    main()
