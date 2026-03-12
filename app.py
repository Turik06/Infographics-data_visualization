from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

num_col = ["pop", "lifeExp", "gdpPercap"]

app.layout = html.Div([

    html.H1('Анализ стран мира', style={'textAlign': 'center'}),

    # 1
    html.Label("Страны:"),
    dcc.Dropdown(df.country.unique(), ['Russia', 'Canada'], id='countries', multi=True),

    html.Label("Ось Y:"),
    dcc.Dropdown(num_col, 'pop', id='y-axis', clearable=False),

    dcc.Graph(id='line-chart'),

    html.Hr(),

    html.Label("Год:"),
    dcc.Slider(
        df['year'].min(), df['year'].max(), step=None,
        value=df['year'].max(), id='year-slider',
        marks={str(y): str(y) for y in df['year'].unique() if y % 5 == 0}
    ),

    # 2
    html.Label("Пузырёк — Ось X:"),
    dcc.Dropdown(num_col, 'gdpPercap', id='bx', clearable=False),

    html.Label("Пузырёк — Ось Y:"),
    dcc.Dropdown(num_col, 'lifeExp', id='by', clearable=False),

    html.Label("Пузырёк — Размер:"),
    dcc.Dropdown(num_col, 'pop', id='bsize', clearable=False),

    dcc.Graph(id='bubble-chart'),

    # 3,4
    html.Div([
        dcc.Graph(id='top15-chart', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='pie-chart',   style={'width': '50%', 'display': 'inline-block'}),
    ])
])


# Колбэк 1
@callback(
    Output('line-chart', 'figure'),
    Input('countries', 'value'),
    Input('y-axis', 'value')
)
def line(countries, y):
    if not countries:
        return px.line(title='Выберите страну')
    dff = df[df.country.isin(countries)]
    return px.line(dff, x='year', y=y, color='country', markers=True)


# Колбэк 2
@callback(
    Output('bubble-chart', 'figure'),
    Input('year-slider', 'value'),
    Input('bx', 'value'),
    Input('by', 'value'),
    Input('bsize', 'value')
)
def bubble(year, x, y, size):
    dff = df[df['year'] == year]
    return px.scatter(dff, x=x, y=y, size=size,
                      color='continent', hover_name='country',
                      size_max=60, title=f'Пузырьки ({year})')


# Колбэк 3
@callback(
    Output('top15-chart', 'figure'),
    Input('year-slider', 'value')
)
def top15(year):
    dff = df[df['year'] == year].nlargest(15, 'pop')
    fig = px.bar(dff, x='pop', y='country', orientation='h',
                 color='continent', title=f'Топ-15 стран ({year})')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig


# Колбэк 4
@callback(
    Output('pie-chart', 'figure'),
    Input('year-slider', 'value')
)
def pie(year):
    dff = df[df['year'] == year]
    return px.pie(dff, values='pop', names='continent',
                  title=f'Население по континентам ({year})', hole=0.3)


if __name__ == '__main__':
    app.run(debug=True)