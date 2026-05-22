import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import matplotlib.pyplot as plt
    import marimo as mo
    import numpy as np


@app.cell
def intro():
    mo.md("""
    # 06 - Visualize a Waveform

    Goal: pair listening with looking. A waveform plot shows amplitude
    over time.
    """)
    return


@app.cell
def controls():
    frequency = mo.ui.slider(110, 880, step=10, value=440, label="frequency Hz")
    zoom_ms = mo.ui.slider(5, 100, step=5, value=30, label="plot window ms")
    mo.vstack([frequency, zoom_ms])
    return frequency, zoom_ms


@app.cell
def synth(frequency):
    sample_rate = 22050
    duration = 1.0
    time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.4 * np.sin(2 * np.pi * frequency.value * time)
    return audio, sample_rate, time


@app.cell
def plot(audio, sample_rate, time, zoom_ms):
    n = int(sample_rate * zoom_ms.value / 1000)
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(time[:n] * 1000, audio[:n])
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("amplitude")
    ax.set_title("First slice of the waveform")
    ax.grid(True, alpha=0.25)
    fig
    return


if __name__ == "__main__":
    app.run()
