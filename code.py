from adafruit_clue import clue
import time

import adafruit_dht
import board

import storage

log_to_file = True

if log_to_file:
    storage.remount("/", False)

dht = adafruit_dht.DHT22(board.D2)


# Set desired temperature range in degrees Celsius.
min_temperature = 24
max_temperature = 30

# Set desired humidity range in percent.
min_humidity = 40
max_humidity = 65

# Set to true to enable audible alarm tone.
alarm_enable = False


start_time = time.monotonic()
clue_display = clue.simple_text_display(text_scale=3, colors=(clue.WHITE,))

clue_display[0].text = "Box Tester"
# clue_display[1].text = "Humidity"



#     fp.write("OutsideTemp;OutsideHumidity;BoxTemp;BoxHumidity;\n"


while True:
    alarm = False

    temperature = clue.temperature
    humidity = clue.humidity

    temperature_box = dht.temperature
    humidity_box = dht.humidity

    clue_display[3].text = "Temp: {:.1f} C".format(temperature)
    clue_display[5].text = "Humi: {:.1f} %".format(humidity)

    clue_display[2].text = "Temp B: {:.1f} C".format(temperature_box)
    clue_display[4].text = "Humi B: {:.1f} %".format(humidity_box)
    clue_display[1].text = "Minute: {:.0f}".format((time.monotonic() - start_time) / 60)

    if temperature < min_temperature:
        clue_display[3].color = clue.BLUE
        alarm = True
    elif temperature > max_temperature:
        clue_display[3].color = clue.RED
        alarm = True
    else:
        clue_display[3].color = clue.WHITE

    if humidity < min_humidity:
        clue_display[5].color = clue.BLUE
        alarm = True
    elif humidity > max_humidity:
        clue_display[5].color = clue.RED
        alarm = True
    else:
        clue_display[5].color = clue.WHITE
    clue_display.show()

    if alarm and alarm_enable:
        clue.start_tone(2000)
    else:
        clue.stop_tone()
    if log_to_file:
        with open("/templog.csv", "a") as fp:
            fp.write("{:.0f};".format((time.monotonic() - start_time) / 60))
            fp.write("{:.1f};".format(temperature))
            fp.write("{:.1f};".format(humidity))
            fp.write("{:.1f};".format(temperature_box))
            fp.write("{:.1f};\n".format(humidity_box))

    time.sleep(60)
