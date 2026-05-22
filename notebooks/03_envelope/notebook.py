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
    # 03 - Shape a Note With an Envelope

    Goal: show why audio is not just pitch. The same frequency can sound
    different when the attack and decay change.
    """)
    return


@app.cell
def controls():
    attack = mo.ui.slider(0.001, 0.25, step=0.005, value=0.02, label="attack sec")
    decay = mo.ui.slider(0.05, 1.5, step=0.05, value=0.45, label="decay sec")
    harmonic = mo.ui.slider(0.0, 0.8, step=0.05, value=0.3, label="octave harmonic")
    mo.vstack([attack, decay, harmonic])
    return attack, decay, harmonic


@app.cell
def synth(attack, decay, harmonic):
    sample_rate = 22050
    frequency = 440.0
    duration = 1.4
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave_data = np.sin(2 * np.pi * frequency * t)
    wave_data += harmonic.value * np.sin(2 * np.pi * 2 * frequency * t)
    envelope = np.exp(-t / decay.value)
    attack_n = max(1, int(attack.value * sample_rate))
    envelope[:attack_n] *= np.linspace(0, 1, attack_n)
    audio = 0.45 * wave_data * envelope
    return audio, sample_rate


@app.cell
def write(audio, sample_rate):
    audio_path = os.path.join(tempfile.gettempdir(), "marimo_03_envelope.wav")
    pcm = np.int16(np.clip(audio, -1, 1) * 32767)
    with wave.open(audio_path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(pcm.tobytes())
    return (audio_path,)


@app.cell
def output(attack, audio_path, decay, harmonic):
    mo.vstack(
        [
            mo.md(
                f"Attack **{attack.value:.3f}s**, decay **{decay.value:.2f}s**, "
                f"octave harmonic **{harmonic.value:.2f}**."
            ),
            mo.audio(audio_path),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
