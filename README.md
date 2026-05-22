# Marimo Audio Self-Tutorial

This repository contains a 20-notebook learning path for building Marimo
notebooks about audio analysis, toy transcription, musical notation, and
Hugging Face Space-style apps.

It has two student-facing layers:

- `notebooks/` contains runnable Marimo `notebook.py` lessons.
- the GitHub Pages site is a Quarto textbook with more explanation, teaching
  notes, and links to notebook source and browser-runnable exports where those
  are feasible.

## Run a Notebook Locally

Install [uv](https://docs.astral.sh/uv/) and run:

```bash
uv sync
uv run marimo edit notebooks/01_sine_wave/notebook.py
```

If you prefer pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
marimo edit notebooks/01_sine_wave/notebook.py
```

## Build the Textbook Locally

Install [Quarto](https://quarto.org/), then run:

```bash
quarto render
```

To export the lightweight notebooks to browser-runnable Marimo WASM pages after
rendering the book:

```bash
uv run python scripts/export_wasm.py --output _site/notebooks
```

## Teaching Structure

The book moves gradually from simple signals to transcription pipelines:

1. synthetic audio and controls
2. waveform and frequency analysis
3. onset detection and toy transcription
4. notation, report cards, and deployment patterns

