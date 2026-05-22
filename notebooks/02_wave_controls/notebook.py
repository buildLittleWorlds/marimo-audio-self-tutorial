import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import os
    import tempfile
    import wave

    import marimo as mo
    import numpy as np


@app.cell
def intro():
    mo.md("""
    # 02 - Add Controls

    Goal: use UI controls to change frequency, duration, and volume.

    Marimo rule to notice: create controls in one cell, read `.value` in a
    later cell. That keeps reactivity predictable.
    """)
    return


@app.cell
def controls():
    frequency = mo.ui.slider(110, 880, step=10, value=440, label="frequency Hz")
    duration = mo.ui.slider(0.2, 3.0, step=0.1, value=1.0, label="duration sec")
    volume = mo.ui.slider(0.0, 0.9, step=0.05, value=0.35, label="volume")
    mo.vstack([frequency, duration, volume])
    return duration, frequency, volume


@app.cell
def synth(duration, frequency, volume):
    sample_rate = 22050
    t = np.linspace(0, duration.value, int(sample_rate * duration.value), endpoint=False)
    audio = volume.value * np.sin(2 * np.pi * frequency.value * t)
    return audio, sample_rate


@app.cell
def write(audio, sample_rate):
    audio_path = os.path.join(tempfile.gettempdir(), "marimo_02_controls.wav")
    pcm = np.int16(np.clip(audio, -1, 1) * 32767)
    with wave.open(audio_path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(pcm.tobytes())
    return (audio_path,)


@app.cell
def output(audio_path, duration, frequency, volume):
    mo.vstack(
        [
            mo.md(
                f"Current sound: **{frequency.value} Hz**, "
                f"**{duration.value:.1f} sec**, volume **{volume.value:.2f}**."
            ),
            mo.audio(audio_path),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
