# aREST-Unauthenticated-Websocket-PoC
# NOTE: This vulnerability no longer exists and has been patched out
aREST is a framework for making homebrew IoT devices on boards such as Raspberry Pi's and arduinos. I first heard about aREST from a popular infosec youtuber in February 2019 and began tinkering with it on an ESP8266 shortly there after. At the end of March 2019 after trying to investigate how the API key system worked I identified a vulnerability in the aREST framework. 

At sign up you were given a 6 digit code or could choose one yourself. In a way this acts as the username for interacting with your IoT device. The API key acted like the password part of the authentication. At the time the aREST framework worked in 2 options for how to interact with the device if you were utilizing an API key. The first way was to use a URL crafted to do send the command. An example would look like this:

https://cloud.arest.io/272925/digital/5/1id?key=h3mcbz71juajak8x

In this example the "user" is 272925 and it is enabling pin 5 in a digital fashion and is also providing the API key to authenticate. The problem with this is that the site was partially vulnerable to SSL stripping though it was never consistent. It was possible to expose the API key and "user" information by forcing an insecure connection and capturing the traffic.

The second way was to sign in to your aREST account on their main website and use their dashboard controller which claimed to utilize your API key for you. Much simpler for the user to use and you could have buttons, switches etc. The communication method for issuing commands to your IoT device after a dashboard element had been used was websockets and MQTT. A sample message might look like this:

["{\"msg\":\"method\",\"method\":\"digitalWrite\",\"params\":[\"272925\",4,1,{\"_id\":\"HfNGZqXqPh7Aw6ddS\",\"emails\   [{\"address\":\"sample@gmail.com\",\"verified\":false}]}],\"id\":\"5\"}"]

A clever eye might notice that there seems to be some missing information there. After some fuzzing the smallest message to succesfully control a device looks like this

["{\"msg\":\"method\",\"method\":\"digitalWrite\",\"params\":[\"272925\",4,1],\"id\":\"0\"}"]

The above message enables pin 4 in a digital fashion for "user" 272925. As you can see the above message does not contain the API key that should be there. This meant that you could interact with an API key enabled device running aREST without providing the API key, which basically boils down to unauthenticated access should someone figure out what your 6 digit "user" code is. Looking at it somewhat differently you could also brute force 6 digit codes fairly easily and cause havoc on the majoritiy of the user base by randomly controlling their devices. 

As a live demo I hooked my ESP8266 up to my garage door and ran my PoC exploit script to show that I could activate my device without knowing the API key. You can view that here: https://www.youtube.com/watch?v=cXhRW67ypsM

Much thanks to Marco for working fast to get this vulnerability fixed.


