from shiny import App, render, ui
from userInfo import UserInfo
from station import Station
from settings import *

service = Station()
user = UserInfo.geocoding(default_add)

app_ui = ui.page_fluid(
    ui.input_text("add", "Text input", placeholder=user.address),
    ui.output_text_verbatim("txt"),
)


def server(input, output, session):
    @output
    @render.text
    def txt():

        return f'add: "{input.add()}" \nloc: "{}"'


app = App(app_ui, server, debug=True)
