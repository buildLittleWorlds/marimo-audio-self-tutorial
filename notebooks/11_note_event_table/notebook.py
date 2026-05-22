import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd


@app.cell
def intro():
    mo.md("""
    # 11 - Note Events as a Table

    Goal: make the intermediate transcription visible. Before sheet music,
    use a table with start time, duration, pitch, and confidence.
    """)
    return


@app.cell
def toy_events():
    events = [
        {"start": 0.00, "duration": 0.50, "pitch": "C4", "confidence": 0.93},
        {"start": 0.52, "duration": 0.50, "pitch": "E4", "confidence": 0.90},
        {"start": 1.04, "duration": 0.50, "pitch": "G4", "confidence": 0.88},
        {"start": 1.56, "duration": 0.80, "pitch": "C5", "confidence": 0.86},
    ]
    event_table = pd.DataFrame(events)
    return (event_table,)


@app.cell
def output(event_table):
    mo.vstack(
        [
            mo.md("This table is easier to debug than finished notation."),
            mo.ui.table(event_table),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
