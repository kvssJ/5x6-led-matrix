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

<img width="300" height="400" alt="image" src="https://github.com/user-attachments/assets/92113002-f60f-465e-a9b8-2750b7009068" />

I used something called Bit Angle Modulation (shortened to BAM) to control the brightness of the LEDs. 

Typically, to control the brightness of an LED using an Arduino, an easy method is using Pulse Width Modulation. For stuff like LEDs or motors, I can use the analog pins and inbuilt functions like analogWrite(). PWM works by sending multiple high and low pulses, kind of like turning a switch on and off really fast. 

For an LED, when I use PWM, I can control it such that it's on half of the time and off half of the time. Something like this is called a 50% duty cycle. Different duty cycles have different levels of brightness. 

Although PWM is easy to use with an Arduino, it's still computationally complex. It's the best option for high levels of precision control. I felt this level of precision was unnecessary to  control a couple of LEDs. This is why I used BAM. It's much simpler to implement in a program. I only need 4 bits to create 16 varying levels of brightness. BAM uses the fundamental idea behind binary numbers.

If I use a 4 bit binary number, each position can be expressed as 2 to the power of the corresponding position. If we take a number like 1001,

| 1  | 0 | 0 | 1 |
| -------- | -------- | -------- | -------- |
| $2^3$ | $2^2$ | $2^1$ | $2^0$ |
| 8 | 4 | 2 | 1 |

The maximum decimal number that can be expressed this way is 15. Therefore, if I use 4 bit Bit Angle Modulation, I can create 16 varying levels of brightness ranging from 0 to 15 (both included). In my LED pillar, this means that I would iterate through the pillar 15 times, each time moving from the last LED to the first LED. If an LED is set to brightness 0, it'll stay off all 15 times. If an LED has brightness 1111 (that's 15 in binary), it'll turn on all 15 times. What if I set the brightness to something like 9.

In binary, a 7 is 0111.

| 0  | 1 | 1 | 1 |
| -------- | -------- | -------- | -------- |
| $2^3$ | $2^2$ | $2^1$ | $2^0$ |
| 8 | 4 | 2 | 1 |

Since the first three bits are all 1s, this means that in a cycle, the LED will turn on the first time, the next two times, and even the next four times but it'll stay off the next 8 times.

This is equivalent to a 50% duty cycle. To show how BAM works with the LED pillar, I set the first LED to a brightness of 15 (fully bright) and the last LED to a 1 (dim). The following image shows how this would look like in real time.


<img width="300" height="500" alt="image" src="https://github.com/user-attachments/assets/a4925bf9-552e-4fc3-a9c8-41474762a36d" />


To understand exactly what's happening, I manually slowed down the switching on and off of the LEDs. Since the first LED is set to a 15, it'll turn on all 15 times in a single cycle, but the last LED turns on only one time in a single cycle. The following video demonstrates this well.

![](https://youtube.com/shorts/2p29_jpqs7A?feature=share)


![[led demo](https://youtube.com/shorts/2p29_jpqs7A?feature=share)](https://youtube.com/shorts/2p29_jpqs7A?feature=share)

 

     



