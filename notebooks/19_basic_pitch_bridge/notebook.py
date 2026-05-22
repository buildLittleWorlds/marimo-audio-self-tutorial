import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import os

    import marimo as mo
    import pandas as pd


@app.cell
def intro():
    mo.md("""
    # 19 - Bridge to Basic Pitch

    Goal: show the integration pattern for a real AMT model. This notebook
    explains where Basic Pitch fits without hiding the dependency cost.
    """)
    return


@app.cell
def controls():
    use_demo = mo.ui.checkbox(value=True, label="use demo events instead of running Basic Pitch")
    mo.vstack([use_demo])
    return (use_demo,)


@app.cell
def transcribe(use_demo):
    if use_demo.value:
        status = "Using demo events. Uncheck the box after adding an audio path."
        events = [(0.0, 0.5, 60, 0.9, None), (0.5, 1.0, 64, 0.88, None), (1.0, 1.5, 67, 0.86, None)]
    else:
        import basic_pitch
        from basic_pitch.inference import predict

        audio_path = "replace-with-a-real-audio-file.wav"
        model_path = os.path.join(os.path.dirname(basic_pitch.__file__), "saved_models", "icassp_2022", "nmp.onnx")
        _, _, events = predict(audio_path, model_or_model_path=model_path)
        status = f"Basic Pitch returned {len(events)} events."
    return events, status


@app.cell
def table(events):
    rows = [
        {"start": round(float(s), 3), "end": round(float(e), 3), "midi": int(p), "confidence": round(float(a), 3)}
        for s, e, p, a, _ in events
    ]
    event_table = pd.DataFrame(rows)
    return (event_table,)


@app.cell
def output(event_table, status):
    mo.vstack([mo.md(status), mo.ui.table(event_table)])
    return


if __name__ == "__main__":
    app.run()
