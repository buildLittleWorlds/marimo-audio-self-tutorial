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
    # 05 - Synthesize a Melody

    Goal: represent a melody as a list of `(note, beats)` pairs, then
    generate audio from that list.
    """)
    return


@app.cell
def data():
    melodies = {
        "Ode opening": [("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1), ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1)],
        "Twinkle opening": [("C4", 1), ("C4", 1), ("G4", 1), ("G4", 1), ("A4", 1), ("A4", 1), ("G4", 2)],
        "C arpeggio": [("C4", 0.5), ("E4", 0.5), ("G4", 0.5), ("C5", 1.5)],
    }
    NOTE_FREQS = {"C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
                  "G4": 392.00, "A4": 440.00, "C5": 523.25}
    return NOTE_FREQS, melodies


@app.cell
def controls(melodies):
    melody = mo.ui.dropdown(list(melodies.keys()), value="Ode opening", label="melody")
    tempo = mo.ui.slider(60, 150, step=5, value=100, label="tempo BPM")
    mo.vstack([melody, tempo])
    return melody, tempo


@app.cell
def synth(NOTE_FREQS, melodies, melody, tempo):
    sample_rate = 22050
    chunks = []
    for name, beats in melodies[melody.value]:
        seconds = beats * 60 / tempo.value
        t = np.linspace(0, seconds, int(sample_rate * seconds), endpoint=False)
        envelope = np.exp(-t / max(0.05, seconds * 0.7))
        chunks.append(0.35 * np.sin(2 * np.pi * NOTE_FREQS[name] * t) * envelope)
    audio = np.concatenate(chunks)
    return audio, sample_rate


@app.cell
def write(audio, sample_rate):
    audio_path = os.path.join(tempfile.gettempdir(), "marimo_05_melody.wav")
    pcm = np.int16(np.clip(audio, -1, 1) * 32767)
    with wave.open(audio_path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(pcm.tobytes())
    return (audio_path,)


@app.cell
def output(audio_path, melodies, melody, tempo):
    mo.vstack(
        [
            mo.md(f"Now playing **{melody.value}** at **{tempo.value} BPM**."),
            mo.audio(audio_path),
            mo.md(f"Data representation: `{melodies[melody.value]}`"),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
