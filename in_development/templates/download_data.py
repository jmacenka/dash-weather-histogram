import base64
import io
import dash
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    html.A(
        'Download Excel Data',
        id='excel-download',
        download="data.xlsx",
        href="",
        target="_blank"
    )
])

@app.callback(Output('excel-download', 'href'),
             [Input(...)])
def update_dashboard(...):
    df = pd.DataFrame(...)
    xlsx_io = io.BytesIO()
    writer = pd.ExcelWriter(xlsx_io, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=period)
    writer.save()
    xlsx_io.seek(0)
    # https://en.wikipedia.org/wiki/Data_URI_scheme
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    data = base64.b64encode(xlsx_io.read()).decode("utf-8")
    href_data_downloadable = f'data:{media_type};base64,{data}'
    return href_data_downloadable 