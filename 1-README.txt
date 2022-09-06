RUN:
1-catalog.py
2-driverMotionCreator.py *
3-telegramBot.py (http://t.me/driver_awareness_bot type /start)
4-EC_subscriber.py
5-EC_ThingSpeakSGET.py
6-publisher.py
7-Thingspeak.py

* For the sake of testing the system it is set to generate "Sleepy" condition with high rate with respect to "Normal" one. Could be modified for a more realstic scenario.