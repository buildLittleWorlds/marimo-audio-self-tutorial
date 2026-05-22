#!/usr/bin/env python3
"""Generate Quarto chapter pages from the tutorial metadata."""

from __future__ import annotations

from pathlib import Path


REPO = "https://github.com/buildLittleWorlds/marimo-audio-self-tutorial"
SITE = "https://buildlittleworlds.github.io/marimo-audio-self-tutorial"
WASM = {
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
}


LESSONS = [
    ("01_sine_wave", "Make One Sound", "Generate a sine wave, write it as audio, and display it in Marimo.", "A notebook can be a small reproducible instrument: code creates an artifact and the browser immediately makes it inspectable.", "Look for whether students can point to the exact variables that define the sound: sample rate, frequency, duration, and amplitude."),
    ("02_wave_controls", "Add Controls", "Use sliders to change frequency, duration, and volume.", "Controls belong in one cell, and their `.value` is read later. This is the basic Marimo reactive pattern.", "Check whether the student understands why changing a slider re-runs downstream cells without manually re-running the notebook."),
    ("03_envelope", "Shape a Note With an Envelope", "Add attack, decay, and an octave harmonic.", "This is the first step from pure math sound toward musical sound. Timbre and articulation matter.", "Ask whether the student can explain why the same pitch can sound more or less note-like."),
    ("04_note_names", "Note Names to Frequencies", "Translate musician note names into frequencies.", "The notebook connects music vocabulary to signal vocabulary.", "Look for clear explanation of semitone spacing and why A4 is used as an anchor."),
    ("05_melody_synth", "Synthesize a Melody", "Represent melodies as lists of note-duration pairs.", "A melody becomes data. That data structure is later reused for ground truth.", "Assess whether the student can modify the list intentionally rather than treating it as magic."),
    ("06_visualize_waveform", "Visualize a Waveform", "Plot amplitude over time.", "Students should learn to pair listening with visual inspection.", "Ask what the plot makes visible that listening alone does not."),
    ("07_spectrum_fft", "See Frequencies With an FFT", "Inspect a signal in the frequency domain.", "This introduces the idea that pitch detection often starts by asking where energy is concentrated.", "Check whether the student can identify fundamental and harmonic peaks."),
    ("08_detect_pitch_fft", "Toy Pitch Detection", "Estimate pitch from the strongest FFT peak.", "The method is intentionally fragile, which makes it useful for teaching model limitations.", "A strong response names when this method works and when it fails."),
    ("09_upload_audio", "Upload Audio", "Read user-provided audio and preview it.", "This is where a notebook starts behaving like an app and must handle missing or surprising inputs.", "Look for thoughtful handling of file format, stereo-to-mono conversion, and no-file states."),
    ("10_onset_energy", "Find Likely Note Starts", "Use frame energy to estimate note onsets.", "Transcription is not only pitch; it is also segmentation over time.", "Ask whether the student can explain threshold choice and false positives."),
    ("11_note_event_table", "Note Events as a Table", "Represent transcription output as an inspectable table.", "Tables are the debugging bridge between raw audio and notation.", "Look for whether the student can read a note-event table before jumping to sheet music."),
    ("12_simple_transcriber", "A Tiny Toy Transcriber", "Split clean synthetic audio into fixed segments and detect pitches.", "This is a complete miniature transcription pipeline with intentionally unrealistic assumptions.", "A good student explanation separates the toy assumptions from real-world AMT challenges."),
    ("13_music21_score", "Build a music21 Score", "Turn note events into notation objects.", "This introduces the notation layer without yet worrying about browser rendering.", "Ask whether the student can map event fields to score structure."),
    ("14_verovio_svg", "Render Notation With Verovio", "Export MusicXML and render SVG notation.", "This is the publication layer: code output becomes something a musician can inspect.", "Check whether the student uses `mo.Html` for SVG rather than printing markup as text."),
    ("15_compare_ground_truth", "Compare Ground Truth and Transcription", "Put known-correct notes beside detected notes.", "Evaluation starts by separating truth from pipeline output.", "Look for precise language about matches, missing notes, and extra notes."),
    ("16_report_card", "Build an AMT Report Card", "Turn comparison into dimension scores.", "The report card makes a fuzzy transcription problem discussable.", "A strong critique says what each metric captures and what it misses."),
    ("17_overtone_filter", "Filter Octave Overtones", "Remove phantom notes caused by octave harmonics.", "This is a concrete architectural fix for a concrete failure mode.", "Ask whether the student can describe the wall, the move, the cost, and the next test."),
    ("18_tempo_quantization", "Tempo and Quantization", "Snap raw note timing to a musical grid.", "Quantization is a design tradeoff, not just a cleanup step.", "Look for recognition that coarse grids lose detail and fine grids preserve noise."),
    ("19_basic_pitch_bridge", "Bridge to Basic Pitch", "Show where a real AMT model fits into the pipeline.", "This notebook marks the transition from toy methods to real model integration.", "Assess whether the student can explain dependency, runtime, and deployment costs."),
    ("20_hf_space_app", "A Hugging Face Space-Shaped Notebook", "Assemble controls, pipeline output, report, and tables into an app pattern.", "This is the capstone architecture: source, transformation, evaluation, and public interface.", "Look for whether the student can explain how to turn an experiment into a usable demo."),
]


def chapter_text(slug: str, title: str, summary: str, notice: str, feedback: str) -> str:
    source_url = f"{REPO}/blob/main/notebooks/{slug}/notebook.py"
    wasm_line = (
        f"- [Run the browser notebook]({SITE}/notebooks/{slug}/)"
        if slug in WASM
        else "- Browser notebook: local-first for this lesson because it uses upload, notation, audio, or model dependencies that are not reliable in WASM."
    )
    return f"""# {title}

## Lesson Goal

{summary}

## What to Notice

{notice}

## Work With the Notebook

- [Open the notebook source]({source_url})
{wasm_line}

Run locally:

```bash
uv run marimo edit notebooks/{slug}/notebook.py
```

## Feedback Lens

{feedback}

## Instructor Notes

Use this lesson as a small checkpoint. Before asking students to add features,
ask them to name the input, the transformation, the output, and the current
limitation. That habit will matter more in later transcription notebooks than
any one line of code.
"""


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    chapters = root / "chapters"
    chapters.mkdir(exist_ok=True)
    for slug, title, summary, notice, feedback in LESSONS:
        (chapters / f"{slug}.qmd").write_text(
            chapter_text(slug, title, summary, notice, feedback),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

