from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageFilter
import os.path, sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)

originalImagesPath = ""

def Crop():
    statusLabel.config(text = "Cropping...", foreground = "black")
    root.update_idletasks()
    root.update()
    
    try:
        if i.get() == 1:
            CropQuestions()
        else:
            CropAnswers()
    except:
        statusLabel.config(text = "There was an error broh. Make sure the folder you chose is correct broh.", foreground = "red")	

def CropQuestions():        
    croppedImagesPath = originalImagesPath + "\\Cropped_Questions\\"
    originalImages = os.listdir(originalImagesPath)

    if not os.path.exists(croppedImagesPath):
        os.makedirs(croppedImagesPath)

    for item in originalImages:
        imagePath = os.path.join(originalImagesPath, item)
        if os.path.isfile(imagePath):
            originalFile = os.path.basename(imagePath)
            originalFileName, originalFileExtension = os.path.splitext(originalFile)
            originalImage = Image.open(imagePath)
            width, height = originalImage.size

            # Crops the image with the pixel coordinates defined as (left, upper, right, lower). Keep the 
            # left and upper coords to "0, 0" so that it crops the image from the upper left most corner.
            croppedImage = originalImage.crop((165, 0, 1500, 1015))

            croppedImage.filter(ImageFilter.MedianFilter(3))
            colorArray = numpy.array(croppedImage.convert('RGB'))                        
            firstLetterY, firstLetterX = numpy.where(numpy.all(colorArray==[229,230,231], axis=2))  #Finds the coords for the first black pixel (should be the top of the first letter)
            answerBoxBorderY, answerBoxBorderX = numpy.where(numpy.all(colorArray==[85,144,204], axis=2)) #Finds the coords for the last teal pixel (should be the bottom of the answer box)
            headerY, headerX = numpy.where(numpy.all(colorArray==[56, 82, 164], axis=2))  #Blue header/footer                     

            #If the answerBoxBorderY length is less than 2000 then we know that the answer box is cut off or is not in the picture
            #at all. Therefore, we want the top and bottom coords to be different to fit everything in the cropped image.
            if len(answerBoxBorderY) > 2000:
                top = 90   
                bottom = answerBoxBorderY[-1] + 10
            else:
                top = headerY[-1] + 1
                bottom = height

            right = 1250         
            left = 0   
            
            finishedImage = colorArray[top:bottom, left:right]
            finishedImageName = croppedImagesPath + originalFileName + "_Question_Cropped.png"
            Image.fromarray(finishedImage).save(finishedImageName)

    statusLabel.config(text = "Crop Complete", foreground = "green")

def CropAnswers():
    croppedImagesPath = originalImagesPath + "\\Cropped_Answers\\"
    originalImages = os.listdir(originalImagesPath)

    if not os.path.exists(croppedImagesPath):
        os.makedirs(croppedImagesPath)

    for item in originalImages:
        imagePath = os.path.join(originalImagesPath, item)
        if os.path.isfile(imagePath):
            originalFile = os.path.basename(imagePath)
            originalFileName, originalFileExtension = os.path.splitext(originalFile)
            originalImage = Image.open(imagePath)            
            width, height = originalImage.size
       
            #Crops the image with the pixel coordinates defined as (left, upper, right, lower). Keep the 
            #left and upper coords to "0, 0" so that it crops the image from the upper left most corner.
            croppedImage = originalImage.crop((165, 65, width, 1015))

            croppedImage.filter(ImageFilter.MedianFilter(3))
            colorArray = numpy.array(croppedImage.convert('RGB'))                            
            blueY, blueX = numpy.where(numpy.all(colorArray==[56, 82, 164], axis=2))  #Blue header/footer
            imageBorderY, imageBorderX = numpy.where(numpy.all(colorArray==[255, 255, 255], axis=2))              
            
            #If the image is a picture then we need to crop it differently
            if len(blueY) > 0 and len(blueX) > 0:          
                top = blueY[0]
                right = imageBorderX[-1] - 200
                bottom = blueY[-1] - 10
                left = blueX[0] + 100

                secondCrop = colorArray[top:bottom, left:right]
                blueY, blueX = numpy.where(numpy.all(secondCrop==[56, 82, 164], axis=2))
                whiteAreaY, whiteAreaX = numpy.where(numpy.all(secondCrop==[255, 255, 255], axis=2))                   
                top = blueY[-1] + 5                    
                bottom = whiteAreaY[-1] - 5

                finishedImage = secondCrop[top:bottom, left:right]
                finishedImageName = croppedImagesPath + originalFileName + "_Answer_Cropped.png"
                Image.fromarray(finishedImage).save(finishedImageName)
            #This is for cropping explanation text images
            else:                
                top = 1
                right = 1250
                bottom = croppedImage.size[1]
                left = 0

                finishedImage = colorArray[top:bottom, left:right]
                finishedImageName = croppedImagesPath + originalFileName + "_Answer_Cropped.png"
                Image.fromarray(finishedImage).save(finishedImageName)  

    statusLabel.config(text = "Crop Complete", foreground = "green")              

def RadioButtonSelected():
    folderPath.set("")
    cropButton.pack_forget()
    statusLabel.config(text = "", foreground = "black")
    statusLabel.pack_forget()

    if i.get() == 1:
    	uncroppedHeader.config(text = "Choose the Folder With the Mo Fuckin' Uncropped Questions")		
    else:
    	uncroppedHeader.config(text = "Choose the Folder With the Mo Fuckin' Uncropped Answers")

    textBox.pack(side=LEFT, ipady = 6)
    browseButton.pack(side=LEFT, padx = 10)    

def FolderPathSelected():
    global originalImagesPath
    filename = filedialog.askdirectory()
    folderPath.set(filename.replace('/', "\\"))    
    originalImagesPath = str(filename.replace('/', "\\"))
    cropButton.pack(anchor=N, pady = 20)
    statusLabel.pack(anchor=N)

root = Tk()

header = Label(master=root, text = "What You Croppin' Bih?")
header.pack(anchor=N, pady = 5)
header.config(font=("bold", 20))

radioButtonGroup = Frame(root)
i = IntVar()
r1 = Radiobutton(radioButtonGroup, text = "Questions", value = 1, variable = i, font=("bold", 12), command = RadioButtonSelected)
r2 = Radiobutton(radioButtonGroup, text = "Answers", value = 2, variable = i, font=("bold", 12), command = RadioButtonSelected)
r1.pack(side = LEFT)
r2.pack(side = LEFT)
radioButtonGroup.pack(anchor=N)

uncroppedHeader = Label(master=root)
uncroppedHeader.pack(anchor=N, pady = 10)
uncroppedHeader.config(font=("bold", 15))

folderPath = StringVar()
browseFrame = Frame(root)
browseFrame.pack(anchor=N)
textBox = Entry(browseFrame, width = 72, textvariable = folderPath, state = "disabled")
browseButton = Button(browseFrame, text = "Browse", command = FolderPathSelected, font=("bold", 12))

cropButton = Button(root, text = "Friggen Crop It up Bitch!", command=Crop, font=("bold", 15))
statusLabel = Label(master=root)
statusLabel.config(font=("bold", 15))

root.geometry("715x280")
root.mainloop()