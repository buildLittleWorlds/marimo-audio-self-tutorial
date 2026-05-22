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
    # 10 - Find Likely Note Starts

    Goal: use frame energy to guess where notes begin. This is the seed of
    onset detection.
    """)
    return


@app.cell
def synth():
    sample_rate = 22050
    parts = []
    for freq in [261.63, 329.63, 392.0, 523.25]:
        t = np.linspace(0, 0.45, int(sample_rate * 0.45), endpoint=False)
        parts.append(0.45 * np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.25))
        parts.append(np.zeros(int(sample_rate * 0.08)))
    audio = np.concatenate(parts)
    return audio, sample_rate


@app.cell
def frame_energy(audio, sample_rate):
    frame = int(0.03 * sample_rate)
    hop = int(0.01 * sample_rate)
    energies = []
    times = []
    for start in range(0, len(audio) - frame, hop):
        chunk = audio[start : start + frame]
        energies.append(float(np.sqrt(np.mean(chunk ** 2))))
        times.append(start / sample_rate)
    energies = np.array(energies)
    times = np.array(times)
    threshold = energies.mean() + energies.std()
    onset_times = times[(energies[1:] > threshold) & (energies[:-1] <= threshold)]
    return energies, onset_times, threshold, times


@app.cell
def plot(energies, onset_times, threshold, times):
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(times, energies, label="frame energy")
    ax.axhline(threshold, color="red", linestyle="--", label="threshold")
    for x in onset_times:
        ax.axvline(x, color="green", alpha=0.5)
    ax.set_xlabel("time (sec)")
    ax.legend()
    fig
    return


@app.cell
def output(onset_times):
    mo.md(f"Estimated onset times: `{[round(float(x), 2) for x in onset_times]}`")
    return


if __name__ == "__main__":
    app.run()
