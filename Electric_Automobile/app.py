from shiny import App, render, ui, reactive
from shinywidgets import output_widget, register_widget, reactive_read
import ipyleaflet as L
from userInfo import UserInfo
from station import Station
from settings import *
import numpy as np
service = Station()
user = UserInfo.geocoding(default_add)

app_ui = ui.page_fluid(
    ui.div(
        ui.input_text("add", "", placeholder='현재 주소'),
        ui.output_text_verbatim("txt")
    ),
    output_widget('map')
)


def server(input, output, session):

    map = L.Map(center = (user.loc['lat'], user.loc['lng']),
                zoom=12, color='bw', scroll_wheel_zoom=True)
    map.add_control(L.leaflet.ScaleControl(position = 'bottomleft'))
    register_widget("map", map)
    # map.

    @output
    @render.text
    def txt():
        try:
            add = np.where(input.add() == '', default_add, input.add())
            user.set_add(add)
            return f'add: "{user.address}" \nloc: "{user.loc}"'
        except:
            return '위치 정보 오류!'

    @reactive.Effect
    def _():
        add = np.where(input.add() == '', default_add, input.add())
        user.set_add(add)
        map.center = (user.loc['lat'], user.loc['lng'])

app = App(app_ui, server, debug=True)
