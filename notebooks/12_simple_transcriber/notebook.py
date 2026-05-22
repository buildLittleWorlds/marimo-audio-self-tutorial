import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import numpy as np
    import pandas as pd


@app.cell
def intro():
    mo.md("""
    # 12 - A Tiny Toy Transcriber

    Goal: split a clean synthetic melody into fixed segments and detect the
    strongest pitch in each segment.
    """)
    return


@app.cell
def data():
    note_freqs = {"C4": 261.63, "E4": 329.63, "G4": 392.0, "C5": 523.25}
    truth = [("C4", 0.5), ("E4", 0.5), ("G4", 0.5), ("C5", 0.5)]
    return note_freqs, truth


@app.cell
def synth(note_freqs, truth):
    sample_rate = 22050
    chunks = []
    for name, _duration in truth:
        t = np.linspace(0, _duration, int(sample_rate * _duration), endpoint=False)
        chunks.append(0.4 * np.sin(2 * np.pi * note_freqs[name] * t))
    audio = np.concatenate(chunks)
    return audio, sample_rate


@app.cell
def transcribe(audio, note_freqs, sample_rate, truth):
    rows = []
    cursor = 0
    for _, _duration in truth:
        n = int(sample_rate * _duration)
        segment = audio[cursor : cursor + n]
        mags = np.abs(np.fft.rfft(segment * np.hanning(len(segment))))
        freqs = np.fft.rfftfreq(len(segment), d=1 / sample_rate)
        peak = freqs[int(np.argmax(mags))]
        detected = min(note_freqs, key=lambda name: abs(note_freqs[name] - peak))
        rows.append({"start": cursor / sample_rate, "duration": _duration, "detected": detected, "peak_hz": round(float(peak), 1)})
        cursor += n
    detected_table = pd.DataFrame(rows)
    return (detected_table,)


@app.cell
def output(detected_table):
    mo.vstack([mo.md("Fixed-window toy transcription:"), mo.ui.table(detected_table)])
    return


if __name__ == "__main__":
    app.run()
