import asyncio

from nicegui import ui, app

from use_thread import COMListen


class Data:
    def __init__(self):
        self.value = ""


def start_up():
    data = Data()
    new_loop = asyncio.new_event_loop()
    listen = COMListen(new_loop,
                       "This is a demo that use nicegui to send data to com port and receive data from com port!")
    listen.start()
    ui.label().bind_text_from(listen, "value")
    ui.input(label='input').bind_value(data, "value")
    ui.button("发送", on_click=lambda: listen.send(data.value))


app.on_startup(start_up)

ui.run(title="COM IO Demo")
