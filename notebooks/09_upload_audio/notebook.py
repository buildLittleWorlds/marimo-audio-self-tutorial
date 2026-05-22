import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import io
    import os
    import tempfile

    import marimo as mo
    import soundfile as sf


@app.cell
def intro():
    mo.md("""
    # 09 - Upload Audio

    Goal: add the user-upload path. This is the first place where a
    notebook starts to behave like an app.
    """)
    return


@app.cell
def uploader():
    audio_file = mo.ui.file(filetypes=[".wav", ".flac", ".ogg", ".mp3"], multiple=False)
    audio_file
    return (audio_file,)


@app.cell
def read_upload(audio_file):
    if audio_file.value:
        uploaded = audio_file.value[0]
        audio, sample_rate = sf.read(io.BytesIO(uploaded.contents))
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        audio_path = os.path.join(tempfile.gettempdir(), "marimo_09_upload.wav")
        sf.write(audio_path, audio, sample_rate)
        message = f"Read {len(audio)} samples at {sample_rate} Hz."
    else:
        audio = None
        sample_rate = None
        audio_path = None
        message = "Upload a short audio file to inspect it."
    return audio_path, message


@app.cell
def output(audio_path, message):
    if audio_path is None:
        out = mo.md(message)
    else:
        out = mo.vstack([mo.md(message), mo.audio(audio_path)])
    out
    return


if __name__ == "__main__":
    app.run()
