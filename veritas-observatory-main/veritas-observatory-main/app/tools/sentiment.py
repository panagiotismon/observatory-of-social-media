from flask import render_template
from bokeh.plotting import figure
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
import requests
import pandas as pd

from tools.env import DOMAIN_NAME, EUNOMIA_USER

def sentiment_results(request):
    req = request.form
    mtoken = req["mtoken"]
    htq = req["hashtagquery"]
    htq2 = req["hashtagquery2"]
    startdate = req["startdate"]
    enddate = req["enddate"]

    url = f"https://{DOMAIN_NAME}/eunomia/api/credentials"

    params = {"sn": "mastodon", "sn_url": f"https://{DOMAIN_NAME}/", "sn_token": mtoken}

    response = requests.request("GET", url, params=params)
    if not response:
        return render_template("error.html")

    euntoken=response.json()['eunomia_token']

    url2 = f"https://{DOMAIN_NAME}/eunomia/api/posts/mastodon"

    headers = {
        "accept": "application/json",
        "X-EUNOMIA-TOKEN": euntoken,
        "X-SN-TOKEN": mtoken,
        "X-SN-URL": f"https://{DOMAIN_NAME}/",
        "X-ACCOUNT-URL": f"https://{DOMAIN_NAME}/@{EUNOMIA_USER}",
    }
    params2 = {
        "keys": ["created_at", "created_at"],
        "comparisons": ["gt", "lt"],
        "values": [startdate, enddate],
        "extra_fields": "original_post",
    }
    response2 = requests.request("GET", url2, params=params2, headers=headers)
    data = response2.json()
    tm = [i["created_at"] for i in data if htq in i["text"]]
    tm2 = [i["created_at"] for i in data if htq2 in i["text"]]
    votes1_p = [i["votes"]["trusts"] for i in data if htq in i["text"]]
    votes2_p = [i["votes"]["trusts"] for i in data if htq2 in i["text"]]
    votes1_n = [i["votes"]["mistrusts"] for i in data if htq in i["text"]]
    votes2_n = [i["votes"]["mistrusts"] for i in data if htq2 in i["text"]]
    votes1_psum = 0
    votes2_psum = 0
    votes1_nsum = 0
    votes2_nsum = 0

    if htq2 == "":
        tm2 = []

    if not tm:
        return render_template("noresult.html")

    for i in range(0, len(votes1_p)):
        votes1_psum = votes1_psum + votes1_p[i]
    for i in range(0, len(votes2_p)):
        votes2_psum = votes2_psum + votes2_p[i]
    for i in range(0, len(votes1_n)):
        votes1_nsum = votes1_nsum + votes1_n[i]
    for i in range(0, len(votes2_n)):
        votes2_nsum = votes2_nsum + votes2_n[i]

    dates = []
    dates2 = []

    for y in tm:
        dates.append(
            y[0] + y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7] + y[8] + y[9]
        )
    se = []
    for y in tm2:
        dates2.append(
            y[0] + y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7] + y[8] + y[9]
        )
    se2 = []

    for i in data:
        se = [
            i["sentiment_class"] * i["sentiment_confidence"]
            for i in data
            if htq in i["text"]
        ]
    if htq2 != "":
        for i in data:
            se2 = [
                i["sentiment_class"] * i["sentiment_confidence"]
                for i in data
                if htq2 in i["text"]
            ]
    dataframe1 = pd.DataFrame({"dates": dates, "se": se})
    df = dataframe1.groupby("dates").mean()
    df.index = pd.to_datetime(df.index)
    df.index.name = "dates"
    df.sort_index(inplace=True)
    source = ColumnDataSource(df)
    
    if htq2 != "":
        dataframe2 = pd.DataFrame({"dates2": dates2, "se2": se2})
        df2 = dataframe2.groupby("dates2").mean()
        df2.index = pd.to_datetime(df2.index)
        df2.index.name = "dates2"
        df2.sort_index(inplace=True)
        source2 = ColumnDataSource(df2)

    plot = figure(
        title="Sentiment analysis over time",
        x_axis_type="datetime",
        plot_width=600,
        plot_height=350,
        x_axis_label="date",
        y_axis_label="sentiment analysis",
    )
    _=plot.line('dates', 'se', source=source, legend_label=htq)
    if htq2 != "":
        _=plot.line('dates2', 'se2', source=source2, color="red", legend_label=htq2)
    script, div = components(plot, wrap_plot_info=True)

    barplot = ["Trusted", "No trusted"]
    fill_color = ["blue", "red"]
    plot2 = figure(
        x_range=barplot,
        plot_height=250,
        title="Trusted and no trusted votes for " + htq,
    )
    plot2.vbar(
        x=barplot, top=[votes1_psum, votes1_nsum], width=0.6, fill_color=fill_color
    )
    script2, div2 = components(plot2)

    if htq2 != "":
        barplot2 = ["Trusted", "No trusted"]
        fill_color2 = ["blue", "red"]
        plot3 = figure(
            x_range=barplot2,
            plot_height=250,
            title="Trusted and no trusted votes for " + htq2,
        )
        plot3.vbar(
            x=barplot2,
            top=[votes2_psum, votes2_nsum],
            width=0.6,
            fill_color=fill_color2,
        )
        script3, div3 = components(plot3, wrap_plot_info=True)
        kwargs = {
            "script": script,
            "div": div,
            "script2": script2,
            "div2": div2,
            "script3": script3,
            "div3": div3,
        }
        
    else:
        kwargs = {"script": script, "div": div, "script2": script2, "div2": div2}

    kwargs["title"] = "Sentiment Analysis of hashtags"
    return render_template(
        "sentimentanalysis_results.html",
        **kwargs,
    )
