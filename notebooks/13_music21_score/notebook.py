import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    from music21 import clef, instrument, key, meter, note, stream, tempo


@app.cell
def intro():
    mo.md("""
    # 13 - Build a music21 Score

    Goal: convert note events into a real notation object. This notebook
    does not render yet; it teaches the data structure.
    """)
    return


@app.cell
def event_data():
    events = [("C4", 1), ("E4", 1), ("G4", 1), ("C5", 2)]
    return (events,)


@app.cell
def make_score(events):
    score = stream.Score()
    part = stream.Part()
    part.append(instrument.Piano())
    part.append(clef.TrebleClef())
    part.append(key.KeySignature(0))
    part.append(meter.TimeSignature("4/4"))
    part.append(tempo.MetronomeMark(number=100))
    for pitch_name, beats in events:
        part.append(note.Note(pitch_name, quarterLength=beats))
    score.append(part)
    summary = score.show("text")
    return


@app.cell
def output(events):
    mo.md(
        f"""
        Built a `music21.stream.Score` from this event list:

        `{events}`

        Next step: render the score as SVG.
        """
    )
    return


if __name__ == "__main__":
    app.run()
