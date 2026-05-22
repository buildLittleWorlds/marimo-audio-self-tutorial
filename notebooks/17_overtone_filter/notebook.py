import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd


@app.cell
def intro():
    mo.md("""
    # 17 - Filter Octave Overtones

    Goal: demonstrate one specific music transcription failure. A note can
    create a strong octave harmonic, and a pitch detector may treat it as a
    separate note.
    """)
    return


@app.cell
def controls():
    window = mo.ui.slider(0.01, 0.20, step=0.01, value=0.05, label="same-onset window sec")
    mo.vstack([window])
    return (window,)


@app.cell
def data():
    # tuples are start, end, midi pitch, label
    events = [
        (0.00, 0.50, 60, "C4"),
        (0.01, 0.45, 72, "C5 phantom"),
        (0.55, 1.00, 64, "E4"),
        (1.10, 1.60, 67, "G4"),
        (1.11, 1.50, 79, "G5 phantom"),
    ]
    return (events,)


@app.cell
def filter_events(events, window):
    keep = [True] * len(events)
    for i, (s_i, _, p_i, _) in enumerate(events):
        for j, (s_j, _, p_j, _) in enumerate(events):
            if i != j and abs(s_i - s_j) <= window.value and p_i == p_j + 12:
                keep[i] = False
    filtered = [event for event, should_keep in zip(events, keep) if should_keep]
    return (filtered,)


@app.cell
def output(events, filtered, window):
    before = pd.DataFrame(events, columns=["start", "end", "midi", "label"])
    after = pd.DataFrame(filtered, columns=["start", "end", "midi", "label"])
    mo.vstack(
        [
            mo.md(f"Window: **{window.value:.2f} sec**"),
            mo.md("Before filtering:"),
            mo.ui.table(before),
            mo.md("After filtering:"),
            mo.ui.table(after),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
