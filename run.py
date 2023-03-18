import Test

from Test.finalGrader import export
import os
from Test.pdfToJPG import convertToImg
import argparse

pdf_name = "png2pdf.pdf" #<- where to parse questions from

startValue = 8 #starting question value

options = 27 #how many bubbles per row, warning: tweaking this may break the code if you aren't careful

numQuestions = 3 #how many long response questions are there

outputFileName = 'results.csv' # <- this is the file the information will go to. If you want to add to an existing csv, use the name of the csv.
                                #if you want to make a new csv, name it whatever you want, the code will automatically generate and populate the csv.

directory = "images" #where you want the images to be stored, they will however be deleted after the code runs, so there is no real need to change this
#do not modify anything below this line

ap = argparse.ArgumentParser()

args = {"pdf_name": "png2pdf.pdf", "startValue": 8, "options": 27, "numQuestions": 3, "outputFileName": 'results.csv'}

ap.add_argument("-p", "--pdf", required=True,
	help="path to the input pdf")

ap.add_argument("-s", "--startValue", required=False,
	help="starting question value")

ap.add_argument("-o", "--options", required=False,
	help="number of options")

ap.add_argument("-q", "--numQuestions", required=False,
	help="starting question value")

ap.add_argument("-r", "--outputFileName", required=False,
	help="path to the output csv")

args2 = vars(ap.parse_args())

for k in args2:
    if(args2[k] is not None):
        args[k] = args2[k]



convertToImg(args["pdf_name"], directory) #<- converts the pdf by pages into jpgs



file_names = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))] #gets every individual file in an array

for fileName in file_names: #parses through array, runs csv generator on array.
    export(file_name="images/"+fileName, options=args["options"], startValue=args["startValue"], numQuestions=args["numQuestions"], 
           outputFileName=args["outputFileName"])

for f in os.listdir(directory):
     os.remove(os.path.join(directory, f))