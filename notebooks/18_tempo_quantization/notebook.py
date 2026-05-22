import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd


@app.cell
def intro():
    mo.md("""
    # 18 - Tempo and Quantization

    Goal: show how raw seconds become musical beats. Quantization is a
    design choice: too coarse loses detail, too fine keeps noise.
    """)
    return


@app.cell
def controls():
    bpm = mo.ui.slider(60, 160, step=5, value=100, label="tempo BPM")
    grid = mo.ui.dropdown(["4", "8", "16", "32"], value="16", label="subdivision")
    mo.vstack([bpm, grid])
    return bpm, grid


@app.cell
def raw_events():
    events = [
        {"start": 0.03, "end": 0.47, "pitch": "C4"},
        {"start": 0.51, "end": 0.96, "pitch": "E4"},
        {"start": 1.02, "end": 1.46, "pitch": "G4"},
        {"start": 1.53, "end": 2.21, "pitch": "C5"},
    ]
    return


@app.cell
def quantize(bpm, grid, raw_events):
    sec_per_beat = 60 / bpm.value
    sec_per_grid = sec_per_beat * (4 / int(grid.value))
    quantized = []
    for event in raw_events:
        start_q = round(event["start"] / sec_per_grid) * sec_per_grid
        duration_q = max(sec_per_grid, round((event["end"] - event["start"]) / sec_per_grid) * sec_per_grid)
        quantized.append({"start": round(start_q, 3), "duration": round(duration_q, 3), "pitch": event["pitch"]})
    return quantized, sec_per_grid


@app.cell
def output(quantized, raw_events, sec_per_grid):
    mo.vstack(
        [
            mo.md(f"Grid size: **{sec_per_grid:.3f} sec**"),
            mo.md("Raw events:"),
            mo.ui.table(pd.DataFrame(raw_events)),
            mo.md("Quantized events:"),
            mo.ui.table(pd.DataFrame(quantized)),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
