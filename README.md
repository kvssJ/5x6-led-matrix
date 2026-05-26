# 5x6-led-matrix
I created an LED matrix that uses multiplexing to play any animations or text. You can either program an animation manually or use a GUI I created to create whatever you want and play them on the LED matrix. I want to use this README to describe the process of making the final LED matrix, explain some cool features, and highlight future plans!



# How I got interested in making LEDs blink

A while ago, I watched a playlist of videos by Kevin Darrah on how he made an 8x8x8 LED cube. I'll add the link to that playlist down below. Just by making different LEDs blink in a particular order, you can get some CRAZY effects. In that playlist, I was introduced to things like multiplexing and Bit Angle Modulation. I knew I wanted to make something like this, but there was one issue.

Kevin Darrah's playlist: https://youtube.com/playlist?list=PL0JWuCHXfJ2zXVRqFRFVq-lNt_xtCYMjx&si=4_hvj407i1M8X7Vf]

An 8x8x8 LED cube needed 512 LEDs. That's a lot of LEDs. This was just the LEDs. I'll need a lot of other components like wires and transistors to make this project work. An alternative I had was to make a 4x4x4 LED cube. However, even this was a huge gamble. Before making any decision, I 
decided to make a simple 4 LED pillar. I knew that if I figured this out, making a 2D or 3D LED project wouldn't be too hard. 

# A 4 LED pillar

I took 4 common cathode RGB LEDs and soldered the Red, green, and blue anode leads together. 

I used multiplexing. Basically, if I select a particular cathode of one of the LEDs and one of the common anode leads, I could turn a particular colour of a specific LED on. This is how LED control is typically done. By changing the order in which I select the anodes or the cathodes, I can create different patterns. 

In fact, even when I need to turn all the LEDs on, I don't actually power all LEDs at once. That just wastes a lot of power. Multiplexing allows me to select one LED after another really fast so that it looks like all of them are on.

# Bit Angle Modulation

<img width="300" height="400" alt="image" src="https://github.com/user-attachments/assets/92113002-f60f-465e-a9b8-2750b7009068" />

I used something called Bit Angle Modulation (shortened to BAM) to control the brightness of the individual LEDs.

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


To understand exactly what's happening, I manually slowed down the switching on and off of the LEDs.The following video demonstrates this well.

![led blink demo](https://youtu.be/wbMBi5V1IEI?si=WqowApnVY7awBI-Y)

Here, you can clearly see that the first LED turns on all 15 times in a single cycle and the last LED turns on only once in a cycle. This is done so fast, that it looks like the last LED is dim and the first LED is bright. In the program, I added a function called LED that takes the number and the brightness of each colour as input. 

```
void LED(int number, int blueBrightness, int greenBrightness, int redBrightness)
```
This simplified the programming a lot. I used just a few simple functions to program the LED pillar.

# Expanding to an LED matrix

<img width="400" height="600" alt="image" src="https://github.com/user-attachments/assets/4ead0361-7183-48bb-9000-56e4d1527f57" />

Since I figured out the multiplexing and the Bit Angle Modulation for a simple LED pillar, it was quite easy to move to an LED matrix. 

## Hardware

I made a simple 5x6 LED matrix using 30 common cathode RGB LEDs. A common cathode RGB LED is grounded from a common lead and powered by seperate leads for seperate colours. Each colour Red, green and blue has a seperate lead. I created six rows, each with five LEDs. I joined the cathodes of the LEDs in each row to create 6 cathodes. I also joined the anodes of six LEDs in each column to create 5 red anodes, 5 blue anodes and 5 green anodes.

<img width="300" height="350" alt="image" src="https://github.com/user-attachments/assets/aa94ac81-d0c4-4d91-8722-940b801095b2" />


Powering multiple LEDs of a column from a single microcontroller can draw too much current from the microcontroller and damage it. Instead, I used transistors for all the cathodes and anodes. I used six NPN transistors for the cathodes and 15 NPN transistors for the anodes. For the cathodes, I connected the collectors to the anodes and the emitters to ground. A low gate voltage from the microcontroller to any of the transistors would short it and ground the cathode. For the anodes, I connected the collectors to an external 5V power supply and the emitters to the anodes.

The arduino would multiplex by selecting each cathode of a row and uploading all the bits to the anodes of that row. For a particular row, depending on what turn of the cycle, it would turn on. 

An arduino doesn't have so many pins to connect to the mulitple transistors. Instead, I used shift registers. Shift registers allow for serial to parallel conversion. Serial data output from a few pins on the arduino can be used to store a bunch of bits in the shift registers and push all the bits out at once. 

## Software

In the program, I used one of the internal hardware timers of the arduino for the multiplexing. I created an Interrupt Service Routine (ISR) and set the timer such that the ISR is called every 3.204 milliseconds.

Every time the ISR is called, the bits are uploaded to a specific row and a variable is updated so that the next ISR call would update the next row. The ISR would iterate from row to row, shifting out the bits to the shift register and out to the anodes and cathodes each time.

For the shift registers, the code uploads a total of 21 bits, the first 6 bits for the cathodes, 5 bits for the red anodes, 5 more bits for the green cathodes, and finally, 5 bits for the blue anodes. I stored all 21 bits as three bytes and used the shiftOut function to shift them out to the shift register.

```
output1 = cathodes[level] | red[level][0][dim] | red[level][1][dim]; 
output2 = red[level][2][dim] | red[level][3][dim] | red[level][4][dim] | green[level][0][dim] | green[level][1][dim] | green[level][2][dim] | green[level][3][dim] | green[level][4][dim]; 
output3 = blue[level][0][dim] | blue[level][1][dim] | blue[level][2][dim] | blue[level][3][dim] |blue[level][4][dim]; 
```

```
//shifting out the bytes
shiftOut(data_pin, clock, MSBFIRST, output3);
shiftOut(data_pin, clock, MSBFIRST, output2);
shiftOut(data_pin, clock, MSBFIRST, output1);
```

For the cathodes, I connected each output of the shift register to each of the cathodes. To select a specific row, I'll just need to make one of the bits a 1 and all other 5 bits 0s.

| 000001  | 1st level |
| -------- | -------- | 
| 000010 | 2nd level | 
| 000100 | 3rd level |
| 001000 | 4th level |
| 010000 | 5th level |
| 100000 | 6th level |

To actually set the colour for each LED, I created a helper function called LED that takes the row, column, and the Red, Green and Blue brightness values as input.

```
void LED(int row, int column, int blueBrightness, int greenBrightness, int redBrightness)
```

I used three 3D arrays to store all the bits for the red, green, and blue anodes. The values of the arrays are initialised in the LED function and shifted out when the ISR is called.

```
byte red[6][5][4]; // SIX rows, FIVE leds each row, FOUR bits for BAM
byte blue[6][5][4];
byte green[6][5][4];
```

# Connecting the matrix to the GUI

In a different repository, I have code for a GUI I made just to create different frames and animations for the LED matrix. I added the python file for the GUI (ledControl.py) in this repo as well. Once I'm done creating multiple frames, all the values would be written to a text file. I still had to figure out how I would read those values and play them on the LED matrix.

To do this, I used serial communication. I wrote a python program called valuesRead.py to read the values from the text file and write them to the LED matrix. I had to try different settings for the timer and speed up the code to ensure that all the bits are uploaded to the LED matrix in the short time interval between two ISR calls.








 

     



