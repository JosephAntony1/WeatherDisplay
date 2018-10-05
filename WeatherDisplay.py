from bibliopixel.animation import BaseMatrixAnim
from bibliopixel.colors import COLORS as colors
from bibliopixel import font
import pyowm
import threading


"""
This is an example Animation class which has a single field -
`color` with the default value `COLORS.green`.

You can edit this as you like, add and remove fields and
write Python code in general.
"""

class WeatherDisplay(BaseMatrixAnim):
    def __init__(self, *args, text='ScrollText', xPos=0, yPos=0,
                 color=colors.White, bgcolor=colors.Off,
                 font_name=font.default_font, font_scale=1):

        owm = pyowm.OWM('1529be8c1919b4ef1703a9928139940f')
        obs = owm.weather_at_coords(39, -76.9501564922)
        forecast = owm.daily_forecast("Maryland,us")
        print(*args)
        super().__init__(*args)
        self.bgcolor = bgcolor
        self.color = color
        self._text = text
        self.xPos = xPos
        self.orig_xPos = xPos
        self.yPos = yPos
        self.font_name = font_name
        self.font_scale = font_scale
        self._strW = font.str_dim(text, font_name, font_scale, True)[0]
        self._text=(str((obs.get_weather().get_temperature('fahrenheit')['temp_min']))[0:2]+":"+
         str((obs.get_weather().get_temperature('fahrenheit')['temp']))[0:2]+ ":" +
         str((obs.get_weather().get_temperature('fahrenheit')['temp_max']))[0:2])
        self.count = 0
        # Your initialization code goes here.

    def getWeather(self):
        owm = pyowm.OWM('1529be8c1919b4ef1703a9928139940f')
        obs = owm.weather_at_coords(39, -76.9501564922)
        self._text=(str((obs.get_weather().get_temperature('fahrenheit')['temp_min']))[0:2]+":"+
        str((obs.get_weather().get_temperature('fahrenheit')['temp']))[0:2]+ ":" +
        str((obs.get_weather().get_temperature('fahrenheit')['temp_max']))[0:2])
        return  obs

    def step(self, amt=1):
        if (self.count == 84):
            t = threading.Thread(target=self.getWeather, args=())
            t.start()
            self.count = 0

            #self.loop.run_until_complete(self.getWeather())
            #self.count = 0
        self.layout.all_off()
        self.layout.drawText(self._text, self.xPos, self.yPos,
                             color=self.color, bg=self.bgcolor, font=self.font_name,
                             font_scale=self.font_scale)

        self.xPos -= amt
        if self.xPos + self._strW <= 0:
             self.xPos = self.width - 1
             self.animComplete = True

        self.count = self.count + 1
        self._step = 0

    #
    # Everything below here is optional, and you can delete it if you aren't
    # using it.
    #

    # pre_run is called right before the animation starts running.
    def pre_run(self):
        super().pre_run()
        self.xPos = self.orig_xPos

    def cleanup(self, clean_layout=True):
        super().cleanup(clean_layout)
        # Your code goes here.
