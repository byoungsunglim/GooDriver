from traffic_light import traffic_light
from stop_line import stop_line


while True:
    lights = traffic_light("http://10.16.128.66:8080/video")
    print(lights)