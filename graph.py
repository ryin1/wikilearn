# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
from plotly.graph_objs import *
from app import *

title, origin_url, urls, count = setup('machine learning')
output, link_score, keyw_score = rank_links(origin_url, urls, count)

py.sign_in("ryin", "dyg27kojki")


trace1 = Bar(
    x=[x[0] for x in output],
    y=link_score,
    name='Link score',
    marker=Marker(color='rgb(55, 83, 109)'
    )
)
trace2 = Bar(
    x=[x[0] for x in output],
    y=keyw_score,
    name='China',
    marker=Marker(
        color='rgb(26, 118, 255)'
    )
)
data = Data([trace1, trace2])
layout = Layout(
    title='US Export of Plastic Scrap',
    xaxis=XAxis(
        tickfont=Font(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=YAxis(
        title='USD (millions)',
        titlefont=Font(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=Font(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    legend=Legend(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
)
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='style-bar')