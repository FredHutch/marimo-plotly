import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pandas as pd
    import plotly.express as px
    return pd, px


@app.cell
def _(mo):
    # Let the user upload a table
    table = mo.ui.file(
        label="Data Table",
        kind="area",
        multiple=False
    )
    table
    return (table,)


@app.cell
def _(mo, pd, table):
    mo.stop(len(table.value) == 0)
    if table.value[0].name.endswith(".xlsx"):
        df = pd.read_excel(table.value[0].contents)
    elif table.value[0].name.endswith((".csv", ".csv.gz")):
        df = pd.read_csv(table.value[0], compression="gzip" if table.value[0].name.endswith(".gz") else None)
    elif table.value[0].name.endswith((".tsv", ".tsv.gz")):
        df = pd.read_csv(table.value[0], compression="gzip" if table.value[0].name.endswith(".gz") else None, sep="\t")
    else:
        raise ValueError(f"Unexpected file extension: {table.value[0].name}")

    df
    return (df,)


@app.cell
def _(df, mo):
    kws = ['x', 'y', 'z', 'color']
    args = mo.md("\n".join(["- {" + kw + "}" for kw in kws])).batch(
        **{
            kw: mo.ui.dropdown(
                label=kw,
                options=df.columns.values
            )
            for kw in kws
        }
    )
    args
    return (args,)


@app.cell
def _(args, df, px):
    fig = px.scatter_3d(
        data_frame=df,
        **args.value
    )
    fig
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
