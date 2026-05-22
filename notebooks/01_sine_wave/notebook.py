import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import math
    import os
    import tempfile
    import wave

    import marimo as mo
    import numpy as np


@app.cell
def intro():
    mo.md("""
    # 01 - Make One Sound

    Goal: understand that a Marimo notebook can generate an audio file and
    immediately show it in the browser.

    Teaching point: Marimo notebooks are ordinary Python files with reactive
    cells. The last expression in a cell is what the learner sees.
    """)
    return


@app.cell
def make_wave():
    sample_rate = 22050
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.35 * np.sin(2 * np.pi * frequency * t)
    return audio, frequency, sample_rate


@app.cell
def write_wave(audio, sample_rate):
    audio_path = os.path.join(tempfile.gettempdir(), "marimo_01_sine.wav")
    pcm = np.int16(np.clip(audio, -1, 1) * 32767)
    with wave.open(audio_path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(pcm.tobytes())
    return (audio_path,)


@app.cell
def show_audio(audio_path, frequency):
    mo.vstack(
        [
            mo.md(f"Generated a **{frequency:.0f} Hz** sine wave."),
            mo.audio(audio_path),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
