import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import os
    import tempfile

    import marimo as mo
    import verovio
    from music21 import clef, instrument, key, meter, note, stream, tempo


@app.cell
def intro():
    mo.md("""
    # 14 - Render Notation With Verovio

    Goal: export MusicXML from music21, load it with Verovio, and display
    SVG with `mo.Html`.
    """)
    return


@app.cell
def make_score():
    score = stream.Score()
    part = stream.Part()
    part.append(instrument.Piano())
    part.append(clef.TrebleClef())
    part.append(key.KeySignature(0))
    part.append(meter.TimeSignature("4/4"))
    part.append(tempo.MetronomeMark(number=100))
    for pitch_name, beats in [("C4", 1), ("E4", 1), ("G4", 1), ("C5", 2)]:
        part.append(note.Note(pitch_name, quarterLength=beats))
    score.append(part)
    return (score,)


@app.cell
def render(score):
    xml_path = os.path.join(tempfile.gettempdir(), "marimo_14_score.musicxml")
    score.write("musicxml", fp=xml_path)
    toolkit = verovio.toolkit()
    toolkit.setOptions({"scale": 50, "pageWidth": 1400, "pageHeight": 500, "footer": "none", "header": "none"})
    toolkit.loadFile(xml_path)
    svg = toolkit.renderToSVG(1)
    return (svg,)


@app.cell
def output(svg):
    mo.vstack(
        [
            mo.md("The SVG is raw browser markup, so use `mo.Html`, not `mo.md`."),
            mo.Html(f'<div style="overflow-x:auto;border:1px solid #ddd;padding:12px;background:white;">{svg}</div>'),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
