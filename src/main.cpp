#include <Arduino.h>
#include <SPI.h>
#include <SD.h>
#define latch_pin 4

#define clock 13
#define data_pin 11

File myFile;

volatile int bamCounter = 0;
volatile int level = 0;
volatile byte cathodes[6];
volatile byte output;
boolean uploadFlag = true;
boolean okay = false;
String input1 = "";
byte red[6][5][4]; // SIX rows, FIVE leds each row, FOUR bits for BAM
byte blue[6][5][4];
byte green[6][5][4];
byte output1;
byte output2;
byte output3;
byte line[16];
volatile boolean clearFrame = false;
int  lineUpload[16];

int dim;
int count = 1;
int check = 1;
int checkPrev = 0;
int inputLength = 0;
int rows = 0;
String temp = "";
volatile boolean upload = true;
boolean valueSent = true;
int uploadLevel = 0;
boolean frameUpload = true;


int seconds = 0;

int numValues = 0;

int mapToSmall(int value){
    int mappedValue = (value * 15)/255;
    return mappedValue;
}

void LED(int row, int column, int blueBrightness, int greenBrightness, int redBrightness){ 
    

    green[row][column][0]|= ((greenBrightness >> 0)&1) << (column+3);
    green[row][column][1]|=((greenBrightness >> 1)&1) << (column+3);
    green[row][column][2]|= ((greenBrightness >> 2)&1) << (column+3);
    green[row][column][3]|= ((greenBrightness >> 3)&1) << (column+3);
    

    if(column<=1){
        red[row][column][0]|= ((redBrightness >> 0)&1) << (column+6);
        red[row][column][1]|=((redBrightness >> 1)&1) << (column+6);
        red[row][column][2]|= ((redBrightness >> 2)&1) << (column+6);
        red[row][column][3]|= ((redBrightness >> 3)&1) << (column+6);
    }
    else{
        red[row][column][0]|= ((redBrightness >> 0)&1) << (column-2);
        red[row][column][1]|= ((redBrightness >> 1)&1) << (column-2);
        red[row][column][2]|= ((redBrightness >> 2)&1) << (column-2);
        red[row][column][3]|= ((redBrightness >> 3)&1) << (column-2);
        
    }

    blue[row][column][0]|= ((blueBrightness >> 0)&1) << column;
    blue[row][column][1]|= ((blueBrightness >> 1)&1) << column;
    blue[row][column][2]|= ((blueBrightness >> 2)&1) << column;
    blue[row][column][3]|= ((blueBrightness >> 3)&1) << column;

    }


  
void setup() {
      
    Serial.begin(115200);
    noInterrupts();
    SPI.setBitOrder(MSBFIRST);
    SPI.setDataMode(SPI_MODE0);
    SPI.setClockDivider(SPI_CLOCK_DIV2);
    TCCR1A = B00000000;
    TCCR1B = B00001011;
    TIMSK1 = B00000010;
    OCR1A = 800;
    cathodes[0]= B00000001;
    cathodes[1]= B00000010;
    cathodes[2] = B00000100;
    cathodes[3]= B00001000;
    cathodes[4]= B00010000;
    cathodes[5]= B00100000;
    pinMode(3, OUTPUT);
    pinMode(10,OUTPUT);
    pinMode(latch_pin, OUTPUT);

    pinMode(clock, OUTPUT);
    pinMode(data_pin, OUTPUT);
    
    // initialising all LEDs to a 0 (off).
    for(int i = 0; i<=5; i+=1){
                for(int j =0; j<5; j++){
                    LED(i, j, 0,0, 0);
                }
            }
         
        
        seconds = 3;
      
        
        
        interrupts();
   

}


void loop() {

if(clearFrame){ //resets the frame 
    memset(red, 0, sizeof(red));
    memset(green, 0, sizeof(green));
    memset(blue, 0, sizeof(blue));
    clearFrame = false;
}
   
if(upload && (seconds<= 0)){
        
    if(valueSent){
        Serial.println("S");
        valueSent = false;
    }
        
        if(Serial.available()>=17){
            if(Serial.read()==0xAA){
                uploadLevel = Serial.read(); 
                
                level = uploadLevel;
                count = uploadLevel+1;
                 numValues = Serial.readBytes(line, 16);
            
           
            if(uploadLevel==5){
                seconds = line[15] * 1; // stores the number of times the count has to be 90. 4  times count is 90 is one second. 
            }
           
            LED(uploadLevel, 0, mapToSmall(line[0]), mapToSmall(line[1]), mapToSmall(line[2]));
            LED(uploadLevel, 1, mapToSmall(line[3]), mapToSmall(line[4]), mapToSmall(line[5]));
            LED(uploadLevel, 2, mapToSmall(line[6]), mapToSmall(line[7]), mapToSmall(line[8]));
            LED(uploadLevel, 3, mapToSmall(line[9]), mapToSmall(line[10]), mapToSmall(line[11]));
            LED(uploadLevel, 4, mapToSmall(line[12]), mapToSmall(line[13]), mapToSmall(line[14]));

            upload = false;
            valueSent = true;
            }
           
                    
        }
        
    }


}


ISR(TIMER1_COMPA_vect){

    
//Bit Angle Modulation
// dim goes other way cause  we need to take the bits from LSB to MSB
    if(count <= 6){
        dim = 3;
    }
    if(count > 6 && count<=18){
        dim = 2;
    }
    if(count > 18 && count<=42){
        dim = 1;
    }
    if(count > 42 && count <= 90){
        dim = 0;
    }
    //creates the three bytes for all 21 bits
    output1 = cathodes[level] | red[level][0][dim] | red[level][1][dim]; 
    output2 = red[level][2][dim] | red[level][3][dim] | red[level][4][dim] | green[level][0][dim] | green[level][1][dim] | green[level][2][dim] | green[level][3][dim] | green[level][4][dim]; 
    output3 = blue[level][0][dim] | blue[level][1][dim] | blue[level][2][dim] | blue[level][3][dim] |blue[level][4][dim]; 
    digitalWrite(latch_pin, LOW);
    //shifts out the bytes to the three shift registers
    shiftOut(data_pin, clock, MSBFIRST, output3);
    shiftOut(data_pin, clock, MSBFIRST, output2);
    shiftOut(data_pin, clock, MSBFIRST, output1);
    digitalWrite(latch_pin, HIGH);

    count++;
    if(count == 90){
        count = 1;
        if(seconds>0){
            seconds = seconds-1;
            
        }
        if(seconds==0){
            clearFrame = true;
        }
       
        
    }
    level++; // increments the level/row

    
    upload = true;
    
    
    if(level ==6){ //resets the level
        level = 0;
        
    }
    
}


