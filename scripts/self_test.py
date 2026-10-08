#!/usr/bin/env python3
"""Exercise arithmetic and actual TeX failure modes in an isolated directory."""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from geometry import Grid, figure_fit
from build import diagnostics


def arithmetic_tests():
    checks = 0
    for n, spans in [(4, [3, 1]), (6, [4, 2]), (6, [3, 3]), (6, [2, 2, 2]), (8, [5, 3])]:
        g = Grid(columns=n)
        assert abs(g.row(spans)['total_mm'] - 146) < 1e-10
        checks += 1
    assert abs(Grid().span(3) - 70) < 1e-10
    assert not figure_fit(44.667, 35, 100, 60, 10, 8)['readable']
    assert figure_fit(146, 50, 100, 60, 10, 8)['readable']
    for kwargs in [dict(columns=0), dict(columns=1.5), dict(gutter=-1), dict(gutter=40), dict(left=-1)]:
        try:
            Grid(**kwargs)
        except ValueError:
            checks += 1
        else:
            raise AssertionError(kwargs)
    return checks + 3


def document(body, config=''):
    return r'''\documentclass[10pt,aspectratio=169]{beamer}
\usepackage{theme/academic-beamer}
\title[Test]{Layout test}\author[Test]{Test}\date[T]{T}
''' + config + '\n' + r'''\begin{document}
\begin{frame}{Layout test}
''' + body + '\n' + r'''\end{frame}
\end{document}
'''


def scaffold_tests(output):
    script = Path(__file__).resolve().with_name('scaffold.py')
    listed = subprocess.run([sys.executable, str(script), '--list-presets'], capture_output=True, text=True)
    assert listed.returncode == 0 and {'classic', 'neutral'} <= set(listed.stdout.splitlines())
    default = output / 'default deck'
    neutral = output / 'neutral deck'
    for destination, extra, expected in [(default, [], 'classic'), (neutral, ['--preset', 'neutral'], 'neutral')]:
        result = subprocess.run([sys.executable, str(script), str(destination), *extra], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert r'\AcademicPreset{' + expected + '}' in (destination / 'config.tex').read_text()
        assert (destination / 'theme/parts/layout.tex').is_file()
    before = (default / 'config.tex').read_bytes()
    existing = subprocess.run([sys.executable, str(script), str(default)], capture_output=True, text=True)
    assert existing.returncode != 0 and (default / 'config.tex').read_bytes() == before
    unknown = output / 'unknown deck'
    rejected = subprocess.run([sys.executable, str(script), str(unknown), '--preset', 'missing'], capture_output=True, text=True)
    assert rejected.returncode != 0 and not unknown.exists()
    # Independent package fixture: adding files alone must make a preset usable.
    fixture = output / 'fixture skill'
    (fixture / 'scripts').mkdir(parents=True)
    shutil.copyfile(script, fixture / 'scripts/scaffold.py')
    shutil.copytree(script.parents[1] / 'assets/starter', fixture / 'assets/starter')
    (fixture / 'assets/starter/theme/presets/custom-test.tex').write_text(r'\AcademicPreset{classic}\LayoutSetup{columns=4}')
    (fixture / 'assets/starter/assets').mkdir(exist_ok=True)
    shutil.copyfile(output / 'figure.pdf', fixture / 'assets/starter/assets/vector-figure.pdf')
    custom_script = fixture / 'scripts/scaffold.py'
    listed = subprocess.run([sys.executable, str(custom_script), '--list-presets'], capture_output=True, text=True)
    assert listed.returncode == 0 and 'custom-test' in listed.stdout.splitlines()
    custom = output / 'custom deck'
    result = subprocess.run([sys.executable, str(custom_script), str(custom), '--preset', 'custom-test'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert r'\AcademicPreset{custom-test}' in (custom / 'config.tex').read_text()
    assert (custom / 'assets/vector-figure.pdf').read_bytes() == (output / 'figure.pdf').read_bytes()
    return 7


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    output = a.output.expanduser().absolute()
    if output.exists():
        p.error('test output must be a fresh directory')
    compiler = shutil.which('pdflatex')
    if not compiler:
        p.error('pdflatex not found; no dependencies installed')
    output.mkdir(parents=True)
    theme = Path(__file__).resolve().parents[1] / 'assets/starter/theme'
    cases = []
    arithmetic = arithmetic_tests()
    # Native test figure: 100x60mm with known 10pt text, used only in this sandbox.
    figure_source = output / 'figure.tex'
    figure_source.write_text(r'''\documentclass[10pt]{article}
\usepackage[paperwidth=100mm,paperheight=60mm,margin=5mm]{geometry}
\pagestyle{empty}\begin{document}Known 10pt figure label.\end{document}
''')
    fig_result = subprocess.run([compiler, '-interaction=batchmode', '-halt-on-error',
        '-no-shell-escape', f'-output-directory={output}', str(figure_source)], capture_output=True)
    assert fig_result.returncode == 0
    scaffold_checks = scaffold_tests(output)
    valid_rows = {'four': (4, [3, 1]), 'six': (6, [4, 2]), 'six_equal': (6, [2, 2, 2]), 'eight': (8, [5, 3])}
    tests = []
    for name, (n, spans) in valid_rows.items():
        body = '\\begin{GridRow}[columns=' + str(n) + ']\n'
        body += '\n'.join('\\begin{GridCell}{' + str(k) + '}Cell\\end{GridCell}' for k in spans)
        tests.append((name, document(body + '\n\\end{GridRow}'), None))
    tests += [
      ('blank', document(r'\begin{GridRow}\GridBlank{1}\begin{GridCell}{4}Question\end{GridCell}\GridBlank{1}\end{GridRow}'), None),
      ('figure_ok', document(r'\AcademicFigure[height=50mm,native-width=100mm,native-height=60mm,native-font=10,min-font=8]{figure.pdf}'), None),
      ('figure_panel', document(r'\begin{AcademicFigurePanel}{Figure title}{Local figure note.}\AcademicFigure[height=30mm]{figure.pdf}\end{AcademicFigurePanel}\AcademicNote{Bottom note.}'), None),
      ('cell_bottom_note', document(r'\begin{GridRow}\begin{GridCell}{6}Main text\AcademicNote{First note.}\end{GridCell}\end{GridRow}\AcademicNote{Second note.}'), None),
      ('negative_title_top', document('Text', r'\LayoutSetup{title-top=-1mm}'), 'spacing must be nonnegative'),
      ('negative_body_scale', document('Text', r'\LayoutSetup{korean-body-scale=0}'), 'korean-body-scale must be positive'),
      ('negative_block_scale', document('Text', r'\LayoutSetup{korean-block-scale=0}'), 'korean-block-scale must be positive'),
      ('negative_block_math_gap', document('Text', r'\LayoutSetup{block-equation-gap=-1mm}'), 'spacing must be nonnegative'),
      ('zero_equation_size', document('Text', r'\LayoutSetup{equation-size=0pt}'), 'equation-size must be positive'),
      ('short_equation_leading', document('Text', r'\LayoutSetup{equation-size=12pt,equation-leading=10pt}'), 'equation-leading must not be smaller'),
      ('block_equation', document(r'\begin{block}{Equation}\AcademicEquation{Y=\alpha+\beta X}\end{block}'), None),
      ('stat_table', document(r'\begin{GridRow}\begin{GridCell}{4}\begin{AcademicStatTable}{Xrr}\textbf{Term}&\textbf{(1)}&\textbf{(2)}\\\midrule Estimate&0.12&0.08\\&(0.09)&(0.11)\\\end{AcademicStatTable}\end{GridCell}\begin{GridCell}{2}Interpretation\end{GridCell}\end{GridRow}'), None),
      ('relation_table', document(r'\begin{AcademicRelationTable}{XX}\AcademicTableHeading{Concept}&\AcademicTableHeading{Meaning}\\[1mm]\AcademicTableLabel{Income}&Resource\\[2mm]\AcademicTableLabel{Sales}&Local spending\\\end{AcademicRelationTable}'), None),
      ('preset_classic', document(r'\begin{GridRow}\begin{GridCell}{6}Classic\end{GridCell}\end{GridRow}', r'\AcademicPreset{classic}\convertcolorspec{named}{ABAccent}{RGB}{\ABTestColor}\typeout{ABPALETTE=\ABTestColor}'), None),
      ('preset_neutral', document(r'\begin{GridRow}\begin{GridCell}{6}Neutral\end{GridCell}\end{GridRow}', r'\AcademicPreset{neutral}\convertcolorspec{named}{ABAccent}{RGB}{\ABTestColor}\typeout{ABPALETTE=\ABTestColor}'), None),
      ('custom_preset', document(r'\begin{GridRow}\begin{GridCell}{2}Left\end{GridCell}\begin{GridCell}{2}Right\end{GridCell}\end{GridRow}', r'\AcademicPreset{custom-test}\convertcolorspec{named}{ABAccent}{RGB}{\ABTestColor}\typeout{ABPALETTE=\ABTestColor}'), None),
      ('unknown_preset', document('Text', r'\AcademicPreset{missing}'), 'Unknown presets missing'),
      ('invalid_preset', document('Text', r'\AcademicPreset{../classic}'), 'Invalid design identifier'),
      ('short_row', document(r'\begin{GridRow}\begin{GridCell}{5}Cell\end{GridCell}\end{GridRow}'), 'row spans must sum'),
      ('long_row', document(r'\begin{GridRow}\begin{GridCell}{7}Cell\end{GridCell}\end{GridRow}'), 'row spans exceed'),
      ('zero_span', document(r'\begin{GridRow}\begin{GridCell}{0}Cell\end{GridCell}\end{GridRow}'), 'span must be a positive'),
      ('zero_columns', document('Text', r'\LayoutSetup{columns=0}'), 'columns must be positive'),
      ('negative_margin', document('Text', r'\LayoutSetup{margin-left=-1mm}'), 'spacing must be nonnegative'),
      ('negative_track', document('Text', r'\LayoutSetup{gutter=40mm}'), 'track width must be positive'),
      ('tall_row', document(r'\begin{GridRow}\begin{GridCell}{6}\rule{1mm}{20mm}\end{GridCell}\end{GridRow}', r'\LayoutSetup{max-row-height=5mm}'), 'row height exceeds'),
      ('wide_equation', document(r'\AcademicEquation{\rule{200mm}{1pt}}'), 'equation exceeds local width'),
      ('unreadable_figure', document(r'\AcademicFigure[height=30mm,native-width=100mm,native-height=60mm,native-font=10,min-font=8]{figure.pdf}'), 'figure labels would be unreadable'),
      ('partial_metadata', document(r'\AcademicFigure[native-width=100mm]{figure.pdf}'), 'metadata must be complete'),
      ('negative_metadata', document(r'\AcademicFigure[native-width=-100mm,native-height=100mm]{figure.pdf}'), 'metadata must be complete'),
      ('negative_minfont', document(r'\AcademicFigure[min-font=-1]{figure.pdf}'), 'minimum figure font must be positive'),
      ('nested_rows', document(r'\begin{GridRow}\begin{GridCell}{6}\begin{GridRow}\begin{GridCell}{6}Text\end{GridCell}\end{GridRow}\end{GridCell}\end{GridRow}'), 'nested GridRows'),
    ]
    outline_counts = {}
    if shutil.which('kpsewhich') and subprocess.run(['kpsewhich', 'kotex.sty'], capture_output=True).returncode == 0:
        korean = document(r'''\newlength{\ABOutside}\newlength{\ABInside}
\settowidth{\ABOutside}{한글본문}\typeout{ABKWIDTH-OUT=\the\ABOutside}
\begin{block}{Block}
\begin{itemize}\item \settowidth{\ABInside}{한글본문}\typeout{ABKWIDTH-IN=\the\ABInside}한글본문\end{itemize}
\AcademicEquation{Y=\alpha+\beta X}
\end{block}
''').replace(r'\usepackage{theme/academic-beamer}', r'\usepackage{kotex}\usepackage{theme/academic-beamer}')
        tests.append(('korean_block_size', korean, None))
    for mode, expected in [('none', 0), ('start', 1), ('sections', 1), ('both', 2)]:
        name = 'outline_' + mode
        source = document('Main text', r'\AcademicOutlineSetup{mode=' + mode + '}')
        source = source.replace(r'\begin{frame}{Layout test}',
            r'\AcademicOutline\section{First}\begin{frame}{Layout test}')
        tests.append((name, source, None))
        outline_counts[name] = expected
    for name, source, failure in tests:
        folder = output / name
        folder.mkdir()
        shutil.copytree(theme, folder / 'theme')
        if name == 'custom_preset':
            (folder / 'theme/presets/custom-test.tex').write_text(r'\AcademicPreset{classic}\AcademicPalette{custom-test}\LayoutSetup{columns=4}')
            (folder / 'theme/palettes/custom-test.tex').write_text(r'\AcademicColors{94,114,168}{24,55,78}')
        shutil.copyfile(output / 'figure.pdf', folder / 'figure.pdf')
        (folder / 'main.tex').write_text(source)
        result = subprocess.run([compiler, '-interaction=nonstopmode', '-halt-on-error',
            '-no-shell-escape', 'main.tex'], cwd=folder, capture_output=True, text=True)
        log = (folder / 'main.log').read_text(errors='replace')
        normalized = re.sub(r'\s+', ' ', re.sub(r'\(academic-beamer\)\s*', ' ', log))
        if failure:
            assert result.returncode != 0 and failure in normalized, (name, result.stdout[-1800:])
        else:
            fatal, _ = diagnostics(log)
            assert result.returncode == 0 and not fatal, (name, result.stdout[-1800:], fatal)
            if name in ('preset_classic', 'preset_neutral', 'custom_preset'):
                expected_rgb = {'preset_classic': '141,198,63', 'preset_neutral': '125,170,204', 'custom_preset': '94,114,168'}[name]
                assert 'ABPALETTE=' + expected_rgb in normalized, normalized[-1800:]
                expected_n = 4 if name == 'custom_preset' else 6
                assert 'ABGRID: n=' + str(expected_n) + ';' in normalized
            if name == 'korean_block_size':
                outside = float(re.search(r'ABKWIDTH-OUT=([0-9.]+)pt', log).group(1))
                inside = float(re.search(r'ABKWIDTH-IN=([0-9.]+)pt', log).group(1))
                assert abs(inside / outside - 0.87 / 0.90) < 0.002, (inside, outside)
            if name in ('block_equation', 'korean_block_size'):
                assert 'ABMATH: size=12.0pt;' in normalized
                gap = float(re.search(r'ABMATH: size=12.0pt; gap=([0-9.]+)pt', normalized).group(1))
                assert abs(gap - 4.5 * 72.27 / 25.4) < 0.01
            for usable, actual in re.findall(r'usable=([0-9.]+)pt;.*?actual=([0-9.]+)pt', normalized):
                assert abs(float(usable) - float(actual)) <= 0.01
            if name in outline_counts:
                assert normalized.count('ABOUTLINE: frame emitted') == outline_counts[name]
                pages = re.search(r'Output written on main.pdf \((\d+) page', normalized)
                assert pages and int(pages.group(1)) == 1 + outline_counts[name]
        cases.append({'case': name, 'expected': 'reject' if failure else 'accept', 'pass': True})
    assert diagnostics('Overfull \\vbox (10pt too high)')[0]
    assert diagnostics('LaTeX Warning: There were undefined references.')[0]
    report = {'arithmetic_checks': arithmetic, 'scaffold_checks': scaffold_checks, 'compiler_cases': cases,
              'status': 'pass', 'visual_review': 'not performed by this test'}
    (output / 'test-results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
