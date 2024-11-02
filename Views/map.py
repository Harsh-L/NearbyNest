from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
import random
import flet as ft
import flet.map as map
from flet_core.connection import Connection

class Map_Location(ft.Page):
    def __init__(self):
        super().__init__()

    def build(self):
        self.marker_layer_ref = ft.Ref[map.MarkerLayer]()
        # self.circle_layer_ref = ft.Ref[map.CircleLayer]()

        MapView = ft.View(
            "/map",
            [
                map.Map(
                    expand=True,
                    configuration=map.MapConfiguration(
                        initial_center=map.MapLatitudeLongitude(15, 10),
                        initial_zoom=4.2,
                        interaction_configuration=map.MapInteractionConfiguration(
                            flags=map.MapInteractiveFlag.ALL
                        ),
                        on_init=lambda e: print(f"Initialized Map"),
                        on_tap=handle_tap,
                        # on_secondary_tap=handle_tap,
                        # on_long_press=handle_tap,
                        on_event=handle_event,
                    ),
                    layers=[
                        map.TileLayer(
                            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                            on_image_error=lambda e: print("TileLayer Error"),
                        ),
                        map.RichAttribution(
                            attributions=[
                                map.TextSourceAttribution(
                                    text="OpenStreetMap Contributors",
                                    on_click=lambda e: e.page.launch_url(
                                        "https://openstreetmap.org/copyright"
                                    ),
                                ),
                            ]
                        ),
                        map.MarkerLayer(
                            ref=self.marker_layer_ref,
                        ),
                    ],
                ),
            ]
        )

        self.views.clear()
        self.views.append(MapView)
        self.go('/map')

        def handle_tap(e: map.MapTapEvent):
            print(f"Name: {e.name} - coordinates: {e.coordinates} - Local: ({e.local_x}, {e.local_y}) - Global: ({e.global_x}, {e.global_y})")
            
            if e.name == map.MapEventSource.TAP:
                self.marker_layer_ref.current.markers.clear()
                self.marker_layer_ref.current.markers.append(
                    map.Marker(
                        content=ft.Icon(
                            ft.icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED
                        ),
                        coordinates=e.coordinates,
                    )
                )
            self.update()

        def handle_event(e: map.MapEvent):
            print(
                f"{e.name} - Source: {e.source} - Center: {e.center} - Zoom: {e.zoom} - Rotation: {e.rotation}"
            )