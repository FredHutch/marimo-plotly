import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    # If the script is running in WASM (instead of local development mode), load micropip
    import sys
    if "pyodide" in sys.modules:
        import micropip
        running_in_wasm = True
    else:
        micropip = None
        running_in_wasm = False
    return micropip, running_in_wasm


@app.cell
async def _(micropip, mo, running_in_wasm):
    with mo.status.spinner("Loading dependencies"):
        # If we are running in WASM, some dependencies need to be set up appropriately.
        # This is really just aligning the needs of the app with the default library versions
        # that come when a marimo app loads in WASM.
        if running_in_wasm:
            print("Installing via micropip")
            # Downgrade plotly to avoid the use of narwhals
            await micropip.install("plotly<6.0.0")
            await micropip.install("openpyxl")
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
