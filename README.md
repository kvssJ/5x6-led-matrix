# 5x6-led-matrix
I created an LED matrix that uses multiplexing to play any animations or text. You can either program an animation manually or use a GUI I created to create whatever you want and play them on the LED matrix. I want to use this README to describe the process of making the final LED matrix, explain some cool features, and highlight future plans!



# How I got interested in making LEDs blink

A while ago, I watched a playlist of videos by Kevin Darrah on how he made an 8x8x8 LED cube. I'll add the link to that playlist down below. Just by making different LEDs blink in a particular order, you can get some CRAZY effects. In that playlist, I was introduced to things like multiplexing and Bit Angle Modulation. I knew I wanted to make something like this, but there was one issue.

Kevin Darrah's playlist: https://youtube.com/playlist?list=PL0JWuCHXfJ2zXVRqFRFVq-lNt_xtCYMjx&si=4_hvj407i1M8X7Vf]

An 8x8x8 LED cube needed 512 LEDs. That's a lot of LEDs. This was just the LEDs. I'll need a lot of other components like wires and transistors to make this project work. An alternative I had was to make a 4x4x4 LED cube. However, even this was a huge gamble. Before making any decision, I 
decided to make a simple 4 LED pillar. I knew that if I figured this out, making a 2D or 3D LED project wouldn't be too hard. 

# A 4 LED pillar

I took 4 common cathode RGB LEDs and soldered the Red, green, and blue cathode leads together. 
