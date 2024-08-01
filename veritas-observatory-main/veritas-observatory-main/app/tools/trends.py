from flask import render_template
import pandas as pd
import html2text
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS, Slider, Column
from bokeh.layouts import column
import requests
import json

from tools.env import DOMAIN_NAME, EUNOMIA_USER

def trend_results(request):
    req = request.form
    mtoken = req["mtoken"]
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
    data3 = response2.json()
    reblogs1 = []
    posttext1 = []
    postdate1 = []
    postid1 = []
    trust1 = []
    mistrust1 = []
    numberofvotes1 = []
    for i in data3:
        reblogs1.append(i["original_post"]["reblogs_count"])
        posttext1.append(i["text"])
        postdate1.append(i["original_post"]["created_at"])
        postid1.append(i["original_post"]["id"])
        trust1.append(i["votes"]["trusts"])
        mistrust1.append(i["votes"]["mistrusts"])
        numberofvotes1.append(i["votes"]["trusts"] + i["votes"]["mistrusts"])
    dataframe3 = pd.DataFrame(
        {
            "reblogs_count": reblogs1,
            "post_id": postid1,
            "created_at": postdate1,
            "post_text": posttext1,
            "trusts": trust1,
            "mistrusts": mistrust1,
            "nov": numberofvotes1,
        }
    )
    dfs5 = dataframe3.sort_values(by="reblogs_count", ascending=False)
    # ?
    # dfs.to_csv("sharedall.csv")
    dfs5 = dfs5.head()
    # dfs5.to_csv("shared5.csv", encoding="utf-8")
    xplot = dfs5["post_id"].values.tolist()
    yplot = dfs5["reblogs_count"].values.tolist()
    posttext2 = dfs5["post_text"].values.tolist()
    postdates = dfs5["created_at"].values.tolist()
    trustsvotes = dfs5["trusts"].values.tolist()
    mistrustsvotes = dfs5["mistrusts"].values.tolist()
    totalvotes = dfs5["nov"].values.tolist()
    trustper = []
    mistrustper = []
    novotes = []
    for i in range(len(trustsvotes)):
        if (trustsvotes[i] + mistrustsvotes[i]) == 0:
            trustper.append(0)
            mistrustper.append(0)
            novotes.append(yplot[i])

        else:
            trustper.append(
                (yplot[i] * trustsvotes[i]) / (trustsvotes[i] + mistrustsvotes[i])
            )
            mistrustper.append(
                (yplot[i] * mistrustsvotes[i]) / (trustsvotes[i] + mistrustsvotes[i])
            )
            novotes.append(0)

    dateofpost = []
    i = 0
    for y in postdates:
        i = i + 1
        dateofpost.append(
            "#"
            + str(i)
            + " "
            + y[0]
            + y[1]
            + y[2]
            + y[3]
            + y[4]
            + y[5]
            + y[6]
            + y[7]
            + y[8]
            + y[9]
        )
    colorf = []
    legendlabel = []
    for i in range(len(trustsvotes)):

        if trustsvotes[i] > mistrustsvotes[i]:
            colorf.append("green")

        if trustsvotes[i] < mistrustsvotes[i]:
            colorf.append("red")

        if trustsvotes[i] == mistrustsvotes[i] and trustsvotes[i] != 0:
            colorf.append("blue")

        if trustsvotes[i] == 0 and mistrustsvotes[i] == 0:
            colorf.append("grey")

    df6 = pd.DataFrame(
        {
            "post_id": xplot,
            "reblogs_count": yplot,
            "post_text": posttext2,
            "created_at": dateofpost,
            "trusts": trustsvotes,
            "mistrusts": mistrustsvotes,
            "trust%": trustper,
            "mistrust%": mistrustper,
            "novotes": novotes,
            "colors": colorf,
            "totalvotes": totalvotes,
        }
    )
    posttext3 = []
    h = html2text.HTML2Text()
    h.ignore_links = True
    for i in posttext2:
        posttext3.append(h.handle(i))
    # df6.to_csv("final.csv")
    source9 = ColumnDataSource(
        data=dict(
            created_at=dateofpost,
            post_id=xplot,
            reblogs_count=yplot,
            colors=colorf,
            totalvotes=totalvotes,
            posttext=posttext3,
        )
    )
    TOOLTIPS = [("Number of votes", "@totalvotes"), ("Post", "@posttext")]
    plotf = figure(
        x_range=dateofpost,
        title="The most shared posts",
        tools="hover",
        tooltips=TOOLTIPS,
        x_axis_label="Date",
        y_axis_label="Number of reshares",
        plot_width=500,
        plot_height=400,
    )
    plotf.vbar(
        x="created_at", top="reblogs_count", width=0.5, color="colors", source=source9
    )
    source8 = ColumnDataSource(
        data=dict(
            created_at=dateofpost,
            reblogs_count=yplot,
            colors=colorf,
            totalvotes=totalvotes,
        )
    )
    callback = CustomJS(
        args=dict(source9=source9, source8=source8),
        code="""
        var data = source9.data;
        var initialdata = source8.data;
        var colors = data['colors'];
        var colors2 = initialdata['colors']
        var totalvotes=data['totalvotes'];
        var f = cb_obj.value;
        for (var i = 0; i <= 5; i++) {
                if (totalvotes[i] <= f) {     
                        colors[i]=['grey'];
                      }
                else {
                        colors[i]=colors2[i];
                        }
        }
        source9.change.emit();
    """,
    )
    slider = Slider(start=0, end=5, value=0, step=1, title="Number of votes")
    slider.js_on_change("value", callback)
    controls = Column(slider)
    layout = column(controls, plotf)
    script4, div4 = components(layout, wrap_plot_info=True)
    kwargs = {"script4": script4, "div4": div4}
    kwargs["title"] = "Trends and Trustworthiness"
    return render_template(
        "trend_results.html", **kwargs
    )
    
