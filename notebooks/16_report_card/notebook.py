import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo


@app.cell
def intro():
    mo.md("""
    # 16 - Build an AMT Report Card

    Goal: turn comparison results into explainable dimensions: note count,
    pitch precision, pitch recall, and overall score.
    """)
    return


@app.cell
def controls():
    include_phantom = mo.ui.checkbox(value=True, label="include one phantom octave note")
    miss_note = mo.ui.checkbox(value=False, label="miss one true note")
    mo.vstack([include_phantom, miss_note])
    return include_phantom, miss_note


@app.cell
def score(include_phantom, miss_note):
    truth = {"C4", "E4", "G4", "C5"}
    detected = {"C4", "E4", "G4", "C5"}
    if include_phantom.value:
        detected.add("G5")
    if miss_note.value:
        detected.discard("E4")
    count_score = max(0, 100 - 25 * abs(len(detected) - len(truth)))
    precision = int(100 * len(detected & truth) / max(1, len(detected)))
    recall = int(100 * len(detected & truth) / len(truth))
    overall = (count_score + precision + recall) // 3
    phantom = sorted(detected - truth)
    missing = sorted(truth - detected)
    return (
        count_score,
        detected,
        missing,
        overall,
        phantom,
        precision,
        recall,
        truth,
    )


@app.cell
def output(
    count_score,
    detected,
    missing,
    overall,
    phantom,
    precision,
    recall,
    truth,
):
    mo.md(
        f"""
        Truth: `{sorted(truth)}`

        Detected: `{sorted(detected)}`

        | Dimension | Score | Detail |
        | --- | ---: | --- |
        | Note count | {count_score} | truth {len(truth)}, detected {len(detected)} |
        | Pitch precision | {precision} | phantom: {phantom or "none"} |
        | Pitch recall | {recall} | missing: {missing or "none"} |
        | Overall | **{overall}** | |
        """
    )
    return


if __name__ == "__main__":
    app.run()
