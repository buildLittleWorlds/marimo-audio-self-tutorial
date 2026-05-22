import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd


@app.cell
def intro():
    mo.md("""
    # 15 - Compare Ground Truth and Transcription

    Goal: separate the known correct melody from the pipeline output.
    That makes debugging easier and makes student claims more precise.
    """)
    return


@app.cell
def data():
    truth = pd.DataFrame({"slot": [1, 2, 3, 4], "truth": ["C4", "E4", "G4", "C5"]})
    detected = pd.DataFrame({"slot": [1, 2, 3, 4, 5], "detected": ["C4", "E4", "G4", "G5", "C5"]})
    comparison = truth.merge(detected, on="slot", how="outer")
    comparison["match"] = comparison["truth"] == comparison["detected"]
    return comparison, detected, truth


@app.cell
def output(comparison, detected, truth):
    mo.vstack(
        [
            mo.md("Ground truth:"),
            mo.ui.table(truth),
            mo.md("Pipeline output:"),
            mo.ui.table(detected),
            mo.md("Slot-by-slot comparison:"),
            mo.ui.table(comparison),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
