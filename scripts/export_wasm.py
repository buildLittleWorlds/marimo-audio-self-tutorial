#!/usr/bin/env python3
"""Export lightweight Marimo notebooks as browser-runnable WASM pages."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


WASM_NOTEBOOKS = [
    "01_sine_wave",
    "02_wave_controls",
    "03_envelope",
    "04_note_names",
    "05_melody_synth",
    "06_visualize_waveform",
    "07_spectrum_fft",
    "08_detect_pitch_fft",
    "10_onset_energy",
    "11_note_event_table",
    "12_simple_transcriber",
]


def export_notebook(repo_root: Path, output_root: Path, slug: str) -> None:
    source = repo_root / "notebooks" / slug / "notebook.py"
    destination = output_root / slug
    destination.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "marimo",
        "export",
        "html-wasm",
        str(source),
        "-o",
        str(destination),
        "--mode",
        "run",
        "--show-code",
        "--force",
    ]
    print(f"Exporting {slug} -> {destination}")
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="_site/notebooks",
        help="Directory where exported WASM notebook folders should be written.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    output_root = (repo_root / args.output).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    for slug in WASM_NOTEBOOKS:
        export_notebook(repo_root, output_root, slug)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

