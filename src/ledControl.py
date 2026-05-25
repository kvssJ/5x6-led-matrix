from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import ttk


red_arr = [[0 for _ in range(5)] for _ in range(6)]
green_arr = [[0 for _ in range(5)] for _ in range(6)]
blue_arr = [[0 for _ in range(5)] for _ in range(6)]
brightnessList = [[15 for _ in range(5)] for _ in range(6)]
frameTime = [] #stores all the frames 
row = 0
column = 0
rowPrev = 0
columnPrev = 0
buttonList = []
original_colour = ""
count = 0
currentFrame = 0
frameRetrieve = 0
state = False
timeUpdateFrame = 0

def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def clearAll():
     for x in range(0,6,1):
        for y in range(0,5,1):
            buttonList[x][y].config(bg = original_colour)
            red_arr[x][y] = 0
            green_arr[x][y] =0
            blue_arr[x][y] = 0
            brightnessList[x][y] = 15

def loadPreviousNext(b):
    
    global currentFrame
    global frameRetrieve
    global original_colour
    global state
    global timeUpdateFrame
    
    if not entry.get().strip().isdigit():
        messagebox.showerror(title = "wrong input", message = "the value entered for time is not acceptable!")

    if (b == 1 or b==2) and state:
        clearAll()
   
    if b==2:
        if currentFrame == len(frameTime)-2:            
            clearAll()
            entry.delete(0, 'end')
            entry.insert(0 ,"1")
            frameNext.config(state = DISABLED)
            currentFrame+=1
            frameRetrieve = -1
        else:
            currentFrame+=1
            frameRetrieve = currentFrame + 1
    elif b==1:
        frameRetrieve = currentFrame 
    
    if frameRetrieve>=0:
        if not frameNext.cget("state")=="disabled":
            if b ==1 :
                timeUpdateFrame = frameRetrieve +1
            else:
                timeUpdateFrame = frameRetrieve-1
            timeValue = entry.get().strip()

            for i in range(0, 6, 1):
                changedStr = frameTime[timeUpdateFrame][i].strip()[:-1]
                changedStr = changedStr + str(timeValue) + " "
                frameTime[timeUpdateFrame][i] = changedStr
           

            
        for i in range(0, len(frameTime[frameRetrieve]), 1):
            line = frameTime[frameRetrieve][i] #here i is each line
            allValues = [int(x) for x in line.strip().split(" ")]
            for j in range(0, 17, 4):
                if not(rgbtohex(allValues[j], allValues[j+1], allValues[j+2]) == "#000000"):                
                    buttonList[i][int(j/4)].config(bg = rgbtohex(allValues[j], allValues[j+1], allValues[j+2]))
                    state = True
        
            print(allValues)
        entry.delete(0, 'end')
        entry.insert(0,str(allValues[len(allValues)-1]))
  
    
    if b==1:
        currentFrame -=1
        frameRetrieve = currentFrame
    
    if currentFrame == len(frameTime)-1:
        frameNext.config(state = DISABLED)
    else:
        frameNext.config(state = ACTIVE)
    if currentFrame<0:
        framePrevious.config(state = DISABLED)
    else:
        framePrevious.config(state = ACTIVE)
 
    

def uploadAll():
    if len(frameTime) == 0:
        messagebox.showwarning(title = "no upload", message = "WARNING - No data was entered!")
    else:
        file = open("src\led_matrix_information.txt",  'a')
        for i in range(0, len(frameTime),1):
            for j in range(0, len(frameTime[i]),1):
                file.write(frameTime[i][j] + '\n')
        file.close()
        done.config(state =DISABLED)
        

def uploadFrame():
    global count
    global original_colour
    global frameTime
    global currentFrame

    if frameNext.cget("state") == "disabled":
    
        if count==0 or not entry.get().strip().isdigit():
            messagebox.showerror(title ="invalid input",message  = "invalid input!")
        else:
            if int(entry.get().strip())==0:
                messagebox.showerror(title = "invalid input", message = "invalid input! time can't be 0")
            else:
                time = int(entry.get().strip())
                for x in range(0,6,1):
                    for y in range(0,5,1):
                        buttonList[x][y].config(bg = original_colour)
                lineUpload = []
                for i in range(0, 6, 1):
                    lineWrite = ""
                    lineWrite = str(red_arr[i][0]) + " " + str(green_arr[i][0]) + " " + str(blue_arr[i][0]) + " " + str(brightnessList[i][0]) + " " + str(red_arr[i][1]) + " " 
                    lineWrite = lineWrite + str(green_arr[i][1]) + " " + str(blue_arr[i][1]) + " " + str(brightnessList[i][1]) + " " + str(red_arr[i][2]) + " " + str(green_arr[i][2])+ " "
                    lineWrite = lineWrite + str(blue_arr[i][2]) + " " + str(brightnessList[i][2]) + " " + str(red_arr[i][3]) + " " + str(green_arr[i][3]) + " " + str(blue_arr[i][3]) + " "
                    lineWrite = lineWrite + str(brightnessList[i][3]) + " " + str(red_arr[i][4]) + " " + str(green_arr[i][4]) + " " + str(blue_arr[i][4]) + " " + str(brightnessList[i][4]) + " "
                    lineWrite = lineWrite + str(time) + " "
                    lineUpload.append(lineWrite)    
                frameTime.append(lineUpload)
                for i in range(0, 6, 1):
                    print(lineUpload[i])

                clearAll()
                entry.delete(0, "end")
                entry.insert(0, "1")
                currentFrame = len(frameTime)-1
                frameRetrieve = currentFrame
                framePrevious.config(state = ACTIVE)
                scale.set(15)
                listbox.selection_clear(0, 'end')
    else:
        messagebox.showerror(title = "no upload", message = "Data was automatically saved")



def buttonFunc(event):
    global row
    global column
    global rowPrev
    global columnPrev
    global original_colour
    global timeUpdateFrame

    frameButton = Frame(bg = 'black', bd = 1)
    widget = event.widget
    info = widget.grid_info()
    row = int(f"{info['row']}")
    column = int(f"{info['column']}")

    if not frameNext.cget("state")=="disabled":
          
            line = frameTime[frameRetrieve][row]
            allValues = [int(x) for x in line.strip().split(" ")]
            scale.set(allValues[column*4 + 3])
    else:
            
            scale.set(brightnessList[row][column])    
        
    if buttonList[rowPrev][columnPrev].cget("background")=="#ffffff":
        buttonList[rowPrev][columnPrev].config(bg = original_colour)
    if buttonList[row][column].cget("background")==original_colour:
        buttonList[row][column].config(bg = "#ffffff")
    rowPrev = row
    columnPrev = column

   
    listbox.selection_clear(0, 'end')

def valueSubmit():
     global count
     global red_arr
     global blue_arr
     global green_arr
     global row
     global column
     global original_colour
     count = count + 1
     
     red = 0
     green = 0
     blue = 0
     brightness = scale.get()
         
   
     if not listbox.curselection() or  listbox.get(listbox.curselection()) == "(None, None)":
        messagebox.showerror(title = "Wrong selection", message = "No colour was selected!")
     elif listbox.get(listbox.curselection()).strip() == "default":
        buttonList[row][column].config(bg=original_colour)
        red_arr[row][column] = 0
        green_arr[row][column] = 0
        blue_arr[row][column] = 0
        brightnessList[row][column] = 0
     else:
        color = listbox.get(listbox.curselection()).strip()
        if color=="red":
            red = 255
            green = 0
            blue = 0
        elif color == "blue":
            red = 0
            green = 0
            blue = 255
        elif color == "green":
            red = 0
            green = 255
            blue = 0
        elif color == "yellow":
            red = 255
            green = 255
            blue = 0
        elif color == "orange":
            red = 255
            green = 165
            blue = 0
        else:
            temp = color.removeprefix("((")
            red = int(temp[0: temp.find(',')])
            temp = temp.removeprefix(temp[0 :temp.find(',')+2])
            green = int(temp[0: temp.find(',')])
            temp = temp.removeprefix(temp[0:temp.find(',')+2])
            blue = int(temp[0: temp.find(')')])
            temp = temp.removeprefix(temp[0: temp.find(',')+2])

            # below code just turns the RGB values to the closest multiples of 15. This gives way more accurate colours and there's no glitching. Works well
            

            if((red%15)<=7):
                red = red - red%15
            else:
                red = red + (15-red%15)
            
            if((green%15)<7):
                green = green - green%15
            else:
                green = green + (15-green%15)
            
            if((blue%15)<7):
                blue = blue - blue%15
            else:
                blue = blue + (15-blue%15)

            
        
        if not(frameNext.cget("state")=="disabled"):
       
            buttonList[row][column].config(bg = rgbtohex(red, green, blue))
            column2 = column * 4
            line = frameTime[frameRetrieve+1][row]
            allValues = [int(x) for x in line.strip().split(" ")]
            allValues[column2] = red
            allValues[column2+1] = green
            allValues[column2+2] = blue
            allValues[column2+3] = brightness
            line = ""
            for i in range(0, len(allValues), 1):
                line = line + str(allValues[i]) + " "
         
            frameTime[frameRetrieve+1][row] = line


            
        else:

            red_arr[row][column] = red
            green_arr[row][column] = green
            blue_arr[row][column] = blue
            buttonList[row][column].config(bg = rgbtohex(red, green, blue))
            brightnessList[row][column] = brightness       
     #scale.set(0)
     #listbox.selection_clear(0, 'end')
        

def colourChoose():
    if(listbox.size()>6):
        for i in range(listbox.size()-1,4,-1):
            listbox.delete(i)
    listbox.selection_clear(0, 'end')
    color2 = str(colorchooser.askcolor())
    listbox.insert(listbox.size(),  color2)
    listbox.selection_set(listbox.size()-1)
   



window = Tk()
window.title("led matrix")
window.geometry("800x800")
iconImage = PhotoImage(file = 'src\logo.png')

window.iconphoto(True, iconImage)
coloursArr = ["red", "green", "blue", "yellow", "orange", "default"]
# create the 5x6  grid where each cell is a button. Clicking the button allows me to enter options.
frameFinal = Frame(window, bd = 3, relief = "sunken")
framePrevious = Button(frameFinal, text = "Previous", font = ("sans serif", 16))
framePrevious.config(width = 7, command = lambda :loadPreviousNext(1), state = DISABLED)
framePrevious.pack(side = "left", padx = 8, pady =5)
frameNext = Button(frameFinal, text = "Next", font = ("sans serif", 16), command = lambda : loadPreviousNext(2))
frameNext.config(width = 7, state = DISABLED)
frameNext.pack(side = "left", padx = 8, pady = 5)
frameSubmit = Button(frameFinal, text = "Submit", font = ("sans_serif", 16))
frameSubmit.config(width = 9, command = uploadFrame)
frameSubmit.pack(side = "left", padx = 8, pady = 5)
done = Button(frameFinal, text = "Done!", font = ("sans serif", 16) )
done.config(width = 7, command = uploadAll)
done.pack(side = "left", padx = 8, pady = 5)
frameFinal.place(x = 220, y = 680)
timeFrame = Frame(window, bd = 3, relief = "sunken")
timeLabel = Label(timeFrame,  text = "time")
timeLabel.config(padx = 1, pady = 1)
timeLabel.pack()
entry = Entry(timeFrame, width = 10)
entry.insert(0, "1")
entry.config(font = ('monospace', 10))
entry.pack(padx = 5,pady = 5)

timeFrame.place(x = 42, y = 82)
   
frame = Frame(window, bd = 3, relief = "sunken")

frame2 = Frame(window, bd = 3, relief = "raised")
brightLabel = Label(frame2, text = "Brightness", font = ("monospace",10,"bold")).pack()
scale = Scale(frame2, from_=0, to=15, orient = VERTICAL, length = 200)
scale.set(15)
scale.pack()
colorLabel = Label(frame2, text = "Colours", font = ("monospace", 10, "bold"), pady = 10).pack()
listbox = Listbox(frame2)
for i in range(0,6,1):
    listbox.insert(i, "             " + coloursArr[i])
listbox.config(height = listbox.size())
listbox.config(bd = 5)
listbox.pack()
otherButton = Button(frame2, text = "other", width =10 )
otherButton.config(command = colourChoose)
otherButton.pack()
listbutton = Button(frame2, text = "choose", font = ("monospace", 12) )
listbutton.config(command = valueSubmit, pady = 5, width =10)
listbutton.pack()

frame2.place(x = 20,  y = 150)
# for the buttons of the beautiful grid
for i in range(0,6,1):
    buttonTemp = []
    for j in range(0,5,1):
       button = Button(frame, height = 5, width = 13, bd = 4, relief = RAISED)
       original_colour = button.cget("background")   
       if i==0 and j==0:
           button.config(bg = "#ffffff")
       button.grid(row = i, column =  j)
       buttonTemp.append(button)
       button.bind('<Button-1>', buttonFunc)

    buttonList.append(buttonTemp)
    
    
frame.place(x = 470, y=  350, anchor = "center")
window.mainloop()