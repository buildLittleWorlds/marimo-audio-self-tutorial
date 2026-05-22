import marimo

__generated_with = "0.23.8"
app = marimo.App(width="full")

with app.setup:
    import os
    import tempfile

    import marimo as mo
    import pandas as pd


@app.cell
def intro():
    mo.md("""
    # 20 - A Hugging Face Space-Shaped Notebook

    Goal: assemble the teaching pieces into an app pattern:
    controls -> audio source -> transcription events -> report -> notation.
    """)
    return


@app.cell
def controls():
    source = mo.ui.radio(["Demo melody", "Uploaded audio later"], value="Demo melody", label="audio source")
    show_truth = mo.ui.checkbox(value=True, label="show ground truth when available")
    mo.vstack([source, show_truth])
    return show_truth, source


@app.cell
def event_pipeline(source):
    if source.value == "Demo melody":
        truth = [("C4", 1), ("E4", 1), ("G4", 1), ("C5", 2)]
        detected = [("C4", 1), ("E4", 1), ("G4", 1), ("G5", 1), ("C5", 1)]
        status = "Demo pipeline: includes one octave phantom note on purpose."
    else:
        truth = None
        detected = []
        status = "Upload handling would go here; keep it in its own cell."
    return detected, status, truth


@app.cell
def report(detected, truth):
    if truth is None:
        report_md = "No ground truth is available for this audio."
    else:
        truth_pitches = {p for p, _ in truth}
        detected_pitches = {p for p, _ in detected}
        phantom = sorted(detected_pitches - truth_pitches)
        missing = sorted(truth_pitches - detected_pitches)
        precision = int(100 * len(truth_pitches & detected_pitches) / max(1, len(detected_pitches)))
        recall = int(100 * len(truth_pitches & detected_pitches) / len(truth_pitches))
        report_md = f"""
        | Dimension | Score | Detail |
        | --- | ---: | --- |
        | Pitch precision | {precision} | phantom: {phantom or "none"} |
        | Pitch recall | {recall} | missing: {missing or "none"} |
        """
    return (report_md,)


@app.cell
def tables(detected, truth):
    detected_table = pd.DataFrame(detected, columns=["pitch", "beats"])
    truth_table = pd.DataFrame(truth or [], columns=["pitch", "beats"])
    return detected_table, truth_table


@app.cell
def output(detected_table, report_md, show_truth, status, truth_table):
    pieces = [mo.md(status), mo.md("## AMT Report Card"), mo.md(report_md)]
    if show_truth.value and len(truth_table) > 0:
        pieces.extend([mo.md("## Ground Truth"), mo.ui.table(truth_table)])
    pieces.extend([mo.md("## Current Pipeline"), mo.ui.table(detected_table)])
    mo.vstack(pieces)
    return


if __name__ == "__main__":
    app.run()
