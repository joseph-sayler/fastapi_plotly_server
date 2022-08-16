from fastapi import FastAPI
import pandas as pd
import plotly, json
import plotly.graph_objects as go
import plotly.express as px

app = FastAPI()


@app.get("/barchart")
async def bar_graph():
    data = pd.read_csv(
        "/home/jsayler/Projects/fastapi_plotly/data/popular_movies_data.csv"
    )
    data.released = pd.to_datetime(data.released, infer_datetime_format=True)
    parsed_data = data.loc[(data.average_stars > 0) & (data.total_votes > 0)].dropna()
    # bar chart
    p = parsed_data.loc[parsed_data.average_stars > 3]
    custom_data = p.loc[:, ("title", "released")]
    custom_data.loc[:, "released"] = custom_data.loc[:, "released"].dt.strftime(
        "%B %-d, %Y"
    )

    fig = go.Figure(
        go.Bar(
            x=p.average_stars,
            y=p.popularity,
            customdata=custom_data,
            hovertemplate="Title: '%{customdata[0]}'<br>Release Date: %{customdata[1]}<br>Average Stars: %{x}<br>Popularity: %{y}<extra></extra>",
        )
    )
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return {"plot": graph_json}

@app.get("/treemap")
async def tree_map():
    data = pd.read_csv(
        "/home/jsayler/Projects/fastapi_plotly/data/popular_movies_data.csv"
    )
    data.released = pd.to_datetime(data.released, infer_datetime_format=True)
    parsed_data = data.loc[(data.average_stars > 0) & (data.total_votes > 0)].dropna()
    # treemap plot
    p = parsed_data.loc[(parsed_data.average_stars > 4) & (parsed_data.released >= "2021-01-01")]
    t = p.copy()
    t.loc[:, "release_date"] = p.loc[:, "released"].dt.strftime("%B %-d, %Y")
    t.loc[:, "release"] = p.loc[:, "released"].dt.strftime("%B %Y")
    t.loc[:, "popularity"] = p.loc[:, "popularity"].round(decimals=1)
    fig = px.treemap(
        t,
        path=[px.Constant("Movie scores"), "release", "average_stars", "title"],
        values="total_votes",
        color="average_stars",
    )
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return {"plot": graph_json}