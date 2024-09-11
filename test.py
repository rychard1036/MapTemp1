from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import RoundedRectangle
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime, date
from plyer import gps
from kivy.clock import Clock

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
        # Start GPS location service
        self.start_gps()
        return MapScreen()

    def start_gps(self):
        # Start GPS for mobile or simulate for desktop
        try:
            # Configure GPS settings (this works only on mobile platforms)
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start(minTime=1000, minDistance=0)
        except NotImplementedError:
            # Simulate location for unsupported platforms (like desktop)
            print("GPS is not supported on this platform.")
            # Simulate a location after a delay to mimic GPS update
            Clock.schedule_once(lambda dt: self.simulate_location(), 2)

    def simulate_location(self):
        # Simulating GPS coordinates for a desktop platform
        lat, lon = 37.7749, -122.4194  # San Francisco coordinates
        print(f"Simulated Location: lat={lat}, lon={lon}")
        self.on_location(lat=lat, lon=lon)

    def on_location(self, **kwargs):
        # Called when a new GPS location is received
        lat = kwargs.get('lat', 37.7749)
        lon = kwargs.get('lon', -122.4194)
        print(f"New Location: lat={lat}, lon={lon}")

        # Access the MapScreen and update the map position
        map_screen = self.root
        map_screen.update_map_to_location(lat, lon)
    def on_status(self, status):
        # Handle GPS status (e.g., enabled, disabled, etc.)
        print(f"GPS Status: {status}")

class MapScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Car ID variable
        car_id = "Plate Number"

        # Create a MapView instance and store it as an attribute
        self.mapview = MapView(lat=37.7749, lon=-122.4194, zoom=16)
        self.add_widget(self.mapview)

        # Other widget setups like cards, markers, etc.
        self.setup_markers_and_widgets()

    def update_map_to_location(self, lat, lon):
        # Update the map's center to the new GPS location
        self.mapview.center_on(lat, lon)

    def setup_markers_and_widgets(self):
        # Add custom markers and other widgets here
        marker_data = [
            {"lat": 37.7749, "lon": -122.4194, "name": "Tegeta"},
            {"lat": 37.7849, "lon": -122.4094, "name": "Ubungo"},
            {"lat": 37.7649, "lon": -122.4294, "name": "Posta"},
        ]
        for data in marker_data:
            marker = MapMarkerPopup(lat=data["lat"], lon=data["lon"])
            marker.add_widget(MDLabel(text=data["name"], halign="center"))
            self.mapview.add_widget(marker)

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

        # Floating Action Button (Truck icon)
        truck_fab = MDFloatingActionButton(
            icon="truck",
            size_hint=(None, None),
            size=(dp(40), dp(40)),  # Adjusted size
            md_bg_color=[0, 0, 0, 1],  # Black background
            icon_color=[1, 1, 1, 1]  # White icon
        )
        truck_fab.bind(on_release=self.show_request_popup)
        card_layout.add_widget(truck_fab)

        # Text Layout
        text_layout = MDBoxLayout(orientation='vertical')
        card_layout.add_widget(text_layout)

        # "My Truck" Label
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
            text="car_id",
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

        # "Pickup Spots" Label
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
        address = "Main Street"

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

    def show_request_popup(self, *args):
        # Initialize the selected date with today's date
        self.selected_date = datetime.today().strftime('%Y-%m-%d')

        # Date button to display the selected date
        self.date_button = MDRaisedButton(
            text=self.selected_date,
            size_hint=(1, None),
            height=dp(60),
            md_bg_color=[0.5, 0.5, 0.5, 1],  # Grey background color
            text_color=[1, 1, 1, 1],  # White text color for better contrast
            on_release=self.show_date_picker
        )

        # Create a custom layout for the dialog
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(10)],  # Add padding for spacing
            size_hint_y=None,
            height=dp(250)  # Adjust height as needed
        )

        # Add the date button to the dialog's content layout at the center
        content_layout.add_widget(BoxLayout(size_hint_y=None, height=dp(40)))  # Spacer for top
        content_layout.add_widget(self.date_button)
        content_layout.add_widget(BoxLayout(size_hint_y=None, height=dp(40)))  # Spacer for bottom

        # Create the button layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50),  # Height of the button layout
            padding=[dp(10), dp(10), dp(10), dp(10)],
        )

        # Add buttons to the button layout
        cancel_button = MDRaisedButton(
            text="CANCEL",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            on_release=lambda x: self.dialog.dismiss(),
        )
        confirm_button = MDRaisedButton(
            text="CONFIRM",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            on_release=lambda x: self.process_request(self.selected_date),
        )

        # Add buttons to the layout
        button_layout.add_widget(cancel_button)  # Bottom left button
        button_layout.add_widget(BoxLayout())  # Spacer to push buttons apart
        button_layout.add_widget(confirm_button)  # Bottom right button

        # Add the button layout to the content layout
        content_layout.add_widget(button_layout)

        # Create the dialog with the custom content layout
        self.dialog = MDDialog(
            title="Request Service",
            type="custom",
            content_cls=content_layout,
            size_hint=(None, None),
            size=(dp(400), dp(300))  # Adjust size of the dialog
        )

        self.dialog.open()

    def show_date_picker(self, *args):
        # Create a date picker dialog
        date_picker = MDDatePicker(
            min_date=date.today(),  # Set minimum date to today
            max_date=date(2100, 12, 31),  # Set maximum date to a far future date
        )

        # Function to handle the date selection
        def on_date_selected(instance, value, date_range):
            # Update the selected date
            self.selected_date = value.strftime('%Y-%m-%d')

            # Update the text on the date button to reflect the selected date
            if hasattr(self, 'date_button'):
                self.date_button.text = self.selected_date

        # Bind the on_date_selected function to the date picker
        date_picker.bind(on_save=on_date_selected)

        # Open the date picker dialog
        date_picker.open()

    def process_request(self, selected_date):
        # Handle the request here
        print("Selected Date:", selected_date)
        self.dialog.dismiss()


if __name__ == '__main__':
    MainApp().run()
