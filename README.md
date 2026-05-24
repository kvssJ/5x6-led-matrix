# 5x6-led-matrix
I created an LED matrix that uses multiplexing to play any animations or text. You can either program an animation manually or use a GUI I created to create whatever you want and play them on the LED matrix. I want to use this README to describe the process of making the final LED matrix, explain some cool features, and highlight future plans!



# How I got interested in making LEDs blink

A while ago, I watched a playlist of videos by Kevin Darrah on how he made an 8x8x8 LED cube. I'll add the link to that playlist down below. Just by making different LEDs blink in a particular order, you can get some CRAZY effects. In that playlist, I was introduced to things like multiplexing and Bit Angle Modulation. I knew I wanted to make something like this, but there was one issue.

Kevin Darrah's playlist: https://youtube.com/playlist?list=PL0JWuCHXfJ2zXVRqFRFVq-lNt_xtCYMjx&si=4_hvj407i1M8X7Vf]

An 8x8x8 LED cube needed 512 LEDs. That's a lot of LEDs. This was just the LEDs. I'll need a lot of other components like wires and transistors to make this project work. An alternative I had was to make a 4x4x4 LED cube. However, even this was a huge gamble. Before making any decision, I 
decided to make a simple 4 LED pillar. I knew that if I figured this out, making a 2D or 3D LED project wouldn't be too hard. 

# A 4 LED pillar

I took 4 common cathode RGB LEDs and soldered the Red, green, and blue cathode leads together. 

I used multiplexing. Basically, if I select a particular anode of one of the LEDs and one of the common cathode leads, I could turn a particular colour of a specific LED on. This is how LED control is typically done. By changing the order in which I select the anodes or the cathodes, I can create different patterns. 

In fact, even when I need to turn all the LEDs on, I don't actually power all LEDs at once. That just wastes a lot of power. Multiplexing allows me to select one LED after another really fast so that it looks like all of them are on.

# Bit Angle Modulation

I used something called Bit Angle Modulation (shortened to BAM) to control the brightness of the LEDs. 

Typically, to control the brightness of an LED using an Arduino, an easy method is using Pulse Width Modulation. For stuff like LEDs or motors, I can use the analog pins and inbuilt functions like analogWrite(). PWM works by sending multiple high and low pulses, kind of like turning a switch on and off really fast. 

For an LED, when I use PWM, I can control it such that it's on half of the time and off half of the time. Something like this is called a 50% duty cycle. Different duty cycles have different levels of brightness. 

Although PWM is easy to use with an Arduino, it's still computationally complex. It's the best option for high levels of precision control. I felt this level of precision was unnecessary to  control a couple of LEDs.

This is why I used BAM. It's much simpler to implement in a program. I only need 4 bits to create 16 varying levels of brightness. We're just using 4 bit binary numbers. Being binary numbers, every bit has a place value. 

Generally, for binary numbers, the place value is 2 raised to the position. For example, if we take 1001