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
    # 04 - Note Names to Frequencies

    Goal: connect musician language to signal language. A4 is 440 Hz, and
    each semitone multiplies frequency by the twelfth root of 2.
    """)
    return


@app.cell
def helpers():
    NOTE_INDEX = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4,
                  "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}

    def note_to_freq(name):
        pitch = name[:-1]
        octave = int(name[-1])
        semitones_from_a4 = NOTE_INDEX[pitch] + 12 * (octave - 4)
        return 440.0 * (2 ** (semitones_from_a4 / 12))

    note_names = [f"{p}{o}" for o in range(3, 6) for p in NOTE_INDEX]
    return note_names, note_to_freq


@app.cell
def controls(note_names):
    note_choice = mo.ui.dropdown(note_names, value="A4", label="note")
    duration = mo.ui.slider(0.2, 2.0, step=0.1, value=1.0, label="duration")
    mo.vstack([note_choice, duration])
    return duration, note_choice


@app.cell
def synth(duration, note_choice, note_to_freq):
    sample_rate = 22050
    freq = note_to_freq(note_choice.value)
    t = np.linspace(0, duration.value, int(sample_rate * duration.value), endpoint=False)
    audio = 0.35 * np.sin(2 * np.pi * freq * t)
    return audio, freq, sample_rate


@app.cell
def write(audio, sample_rate):
    audio_path = os.path.join(tempfile.gettempdir(), "marimo_04_note.wav")
    pcm = np.int16(np.clip(audio, -1, 1) * 32767)
    with wave.open(audio_path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(pcm.tobytes())
    return (audio_path,)


@app.cell
def output(audio_path, freq, note_choice):
    mo.vstack([mo.md(f"{note_choice.value} = **{freq:.2f} Hz**"), mo.audio(audio_path)])
    return


if __name__ == "__main__":
    app.run()
