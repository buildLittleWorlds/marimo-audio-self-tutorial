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
    # 07 - See Frequencies With an FFT

    Goal: move from time-domain thinking to frequency-domain thinking.
    The spectrum should peak near the frequency you generated.
    """)
    return


@app.cell
def controls():
    fundamental = mo.ui.slider(110, 660, step=10, value=220, label="fundamental Hz")
    harmonic = mo.ui.slider(0.0, 0.8, step=0.05, value=0.4, label="octave harmonic")
    mo.vstack([fundamental, harmonic])
    return fundamental, harmonic


@app.cell
def synth(fundamental, harmonic):
    sample_rate = 22050
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.35 * np.sin(2 * np.pi * fundamental.value * t)
    audio += 0.35 * harmonic.value * np.sin(2 * np.pi * 2 * fundamental.value * t)
    return audio, sample_rate


@app.cell
def spectrum(audio, sample_rate):
    windowed = audio * np.hanning(len(audio))
    magnitudes = np.abs(np.fft.rfft(windowed))
    frequencies = np.fft.rfftfreq(len(windowed), d=1 / sample_rate)
    return frequencies, magnitudes


@app.cell
def plot(frequencies, magnitudes):
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(frequencies, magnitudes)
    ax.set_xlim(0, 1600)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("energy")
    ax.set_title("FFT magnitude spectrum")
    ax.grid(True, alpha=0.25)
    fig
    return


if __name__ == "__main__":
    app.run()
