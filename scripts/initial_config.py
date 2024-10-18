from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import nmcli
import requests
import os

API_KEY = os.environ['OCTOPRINT_API_KEY']

class ConfigPage:
    def __init__(self):
        self.ssid = ""
        self.password = ""

def is_wifi_connected():
    for dev in nmcli.device():
        if dev.device == "wlan0":
            # there can be a variety of connected tags e.g. connected (managed) and the word connected
            # is in disconnected
            if "connected" in dev.state and not "disconnected" in dev.state:
                return True
    return False

def send_octopi_lcd_text(text):
    api_url = f"http://octoUrl/api/printer/command?apikey={API_KEY}"
    lcd_command = {
        "command": f"M117 {text}"
    }
    response = requests.post(api_url, json=lcd_command)

def serve(wifinames):
    # TODO(Heidt) should rescan on dropdown
    config = ConfigPage()

    def show(event: ValueChangeEventArguments):
        name = type(event.sender).__name__
        ui.notify(f"attempting to connect to {config.ssid}")
        nmcli.device.wifi_connect(ssid=config.ssid, password=config.password, wait=10)
        # TODO(Heidt) probably want to make sure it's the right wifi!
        if is_wifi_connected():
            ui.notify("Connected to wifi")
        else:
            ui.notify("Failed to connect to wifi")

    ui.select(wifinames, value=wifinames[0]).bind_value(config, "ssid")
    ui.input("password", password=True).bind_value(config, "password")
    ui.button("Button", on_click=show)

    ui.run()


def main():
    nearby_ssids = [network.ssid for network in nmcli.device.wifi()]
    print(f"Found nearby SSIDs")
    for ssid in nearby_ssids:
       print(f"{ssid}")

    serve(nearby_ssids)

if __name__ in {"__main__", "__mp_main__"}:
    main()
