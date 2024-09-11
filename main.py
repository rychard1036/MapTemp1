from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import RoundedRectangle
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout


class RoundedFitImage(FitImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_clip, size=self.update_clip)
        with self.canvas.before:
            self._clip = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(15), dp(15), dp(15), dp(15)])
            self.canvas.before.add(self._clip)

    def update_clip(self, *args):
        self._clip.pos = self.pos
        self._clip.size = self.size


class MainApp(MDApp):
    def build(self):
        return MapScreen()


class MapScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Car ID variable
        car_id = "Plate Number"

        # Add MapView
        mapview = MapView(lat=37.7749, lon=-122.4194, zoom=16)
        #mapview = MapView(lat=37.7749, lon=-122.4194, zoom=15, max_zoom=17, min_zoom=12)

        self.add_widget(mapview)

        # Add custom markers
        marker_data = [
            {"lat": 37.7749, "lon": -122.4194, "price": "$7"},
            {"lat": 37.7849, "lon": -122.4094, "price": "$5"},
            {"lat": 37.7649, "lon": -122.4294, "price": "$4"},
        ]
        for data in marker_data:
            marker = MapMarkerPopup(lat=data["lat"], lon=data["lon"])
            marker.add_widget(MDLabel(text=data["price"], halign="center"))
            mapview.add_widget(marker)

        # Top Right Information Card
        top_right_card = MDCard(
            size_hint=(None, None),
            size=(dp(180), dp(70)),  # Adjusted size to fit the button
            pos_hint={"right": 0.98, "top": 0.98},
            md_bg_color=[1, 1, 1, 1],
            padding=[dp(8), dp(8), dp(8), dp(8)],
            radius=[dp(15), dp(15), dp(15), dp(15)]
        )

        card_layout = MDBoxLayout(orientation='horizontal', spacing=dp(8))
        top_right_card.add_widget(card_layout)

        # Floating Action Button (Car icon)
        car_fab = MDFloatingActionButton(
            icon="truck",
            size_hint=(None, None),
            size=(dp(40), dp(40)),  # Adjusted size
            md_bg_color=[0, 0, 0, 1],  # Black background
            icon_color=[1, 1, 1, 1]  # White icon
        )
        card_layout.add_widget(car_fab)

        # Text Layout
        text_layout = MDBoxLayout(orientation='vertical')
        card_layout.add_widget(text_layout)

        # "My Car" Label
        car_label = MDLabel(
            text="Truck",
            halign="left",
            theme_text_color="Custom",
            text_color=[0.5, 0.5, 0.5, 1],  # Grey color
            font_style="Subtitle1"  # Smaller font size
        )
        text_layout.add_widget(car_label)

        # Car ID Label
        car_id_label = MDLabel(
            text=car_id,
            halign="left",
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1],  # Black color
            font_style="Body1"  # Smaller font size
        )
        text_layout.add_widget(car_id_label)

        self.add_widget(top_right_card)

        # Bottom Information Card
        bottom_card = MDCard(
            size_hint=(0.9, None),
            height=dp(200),  # Reduced height
            pos_hint={"center_x": 0.5, "y": 0.02},
            md_bg_color=[1, 1, 1, 1],
            padding=[dp(8), dp(8), dp(8), dp(8)],
            radius=[dp(15), dp(15), dp(15), dp(15)]
        )

        # Layout for Bottom Card
        bottom_layout = MDBoxLayout(orientation='vertical', spacing=dp(8))
        bottom_card.add_widget(bottom_layout)

        # "pickup Spots" Label
        pickup_spots_label = MDLabel(
            text="Pickup Spots",
            halign="left",
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1],  # Black color
            font_style="H6",  # Smaller font size
            bold=True
        )
        bottom_layout.add_widget(pickup_spots_label)

        # Variable for Address
        address = "255 Main Street"

        # Address Label
        address_label = MDLabel(
            text=address,
            halign="left",
            theme_text_color="Custom",
            text_color=[0.5, 0.5, 0.5, 1],  # Grey color
            font_style="Body2"  # Smaller font size
        )
        bottom_layout.add_widget(address_label)

        # ScrollView for images
        image_scroll_view = ScrollView(bar_width=0, do_scroll_x=True, do_scroll_y=False)
        image_scroll_view.size_hint = (1, None)
        image_scroll_view.height = dp(150)  # Reduced height

        image_container = BoxLayout(
            orientation='horizontal',
            size_hint_x=None,
            height="150dp",
            spacing=dp(10),
            padding=[dp(10), 0]
        )
        image_container.bind(minimum_width=image_container.setter('width'))
        image_scroll_view.add_widget(image_container)

        # Adding larger rounded rectangular images to the container
        for image_source in ["parkng1.jpg", "paking2.jpg", "parkng1.jpg"]:
            card = MDCard(
                size_hint=(None, 1),
                width=dp(200),  # Reduced width
                radius=[dp(15), dp(15), dp(15), dp(15)],
            )
            # Use RoundedFitImage instead of FitImage
            image = RoundedFitImage(source=image_source, size_hint=(1, 1))
            card.add_widget(image)
            image_container.add_widget(card)

        # Add ScrollView to bottom_layout
        bottom_layout.add_widget(image_scroll_view)

        self.add_widget(bottom_card)

        # Floating Action Buttons
        self.add_widget(MDFloatingActionButton(
            icon="menu",
            pos_hint={"center_x": 0.1, "center_y": 0.9},
            md_bg_color=[1, 1, 1, 1],  # White background
            icon_color=[0, 0, 0, 1]  # Black icon
        ))
        self.add_widget(MDFloatingActionButton(
            icon="crosshairs-gps",
            pos_hint={"center_x": 0.9, "center_y": 0.5},
            md_bg_color=[1, 1, 1, 1],  # White background
            icon_color=[0, 0, 0, 1]  # Black icon
        ))
        self.add_widget(MDFloatingActionButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.5},
            md_bg_color=[1, 1, 1, 1],  # White background
            icon_color=[0, 0, 0, 1]  # Black icon
        ))


if __name__ == '__main__':
    MainApp().run()
