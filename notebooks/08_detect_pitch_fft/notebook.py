import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import numpy as np


@app.cell
def intro():
    mo.md("""
    # 08 - Toy Pitch Detection

    Goal: estimate pitch by finding the strongest FFT bin. This is not a
    robust music transcription method, but it explains the first idea.
    """)
    return


@app.cell
def controls():
    true_freq = mo.ui.slider(180, 700, step=5, value=330, label="hidden test frequency")
    noise = mo.ui.slider(0.0, 0.25, step=0.01, value=0.02, label="noise")
    mo.vstack([true_freq, noise])
    return noise, true_freq


@app.cell
def synth(noise, true_freq):
    sample_rate = 22050
    duration = 1.0
    rng = np.random.default_rng(7)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.4 * np.sin(2 * np.pi * true_freq.value * t)
    audio += noise.value * rng.normal(size=len(audio))
    return audio, sample_rate


@app.cell
def detect(audio, sample_rate):
    windowed = audio * np.hanning(len(audio))
    magnitudes = np.abs(np.fft.rfft(windowed))
    frequencies = np.fft.rfftfreq(len(windowed), d=1 / sample_rate)
    magnitudes[frequencies < 80] = 0
    detected_freq = frequencies[int(np.argmax(magnitudes))]
    return (detected_freq,)


@app.cell
def output(detected_freq, true_freq):
    error = abs(detected_freq - true_freq.value)
    mo.md(
        f"""
        True frequency: **{true_freq.value:.1f} Hz**

        Detected frequency: **{detected_freq:.1f} Hz**

        Error: **{error:.1f} Hz**
        """
    )
    return


if __name__ == "__main__":
    app.run()
