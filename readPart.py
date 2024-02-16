#Tesseract Python packages
import pytesseract
#OpenCV
import cv2
#Python OS
import os
#Python REGEX
import re

#Am I the same repo

#Tesseract Installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

dirname = os.path.dirname(__file__)
#Checks if a string is only numbers? If it is all letters, neglected
def isNumbers(someString):
    #first check if it only letters
    #Is this necessary?
    isIt = False
    #print(someString)
    #if character is a number, pass true, othervise proceed for other characters, if None number, skip that someString
    for character in someString:
        if character.isnumeric():
            #print("this element has numbers")
            isIt = True
        elif character:
            pass
    return isIt
#Check if a string with numbers fit in "Part Number" definition: "DD.DDDDD-DDDD"
def isPartNumber(stringWNumbers):
    #everyPartNumber Starts w/ 2 digits then .
    partNumRegex = re.compile(r'\d\dA\d\d\d\d\dA\d\d\d\d')
    #Might be part number, each one has - & . in them
    if  "." in stringWNumbers:
        if "-" in stringWNumbers:
            #print("Original String w/ Number:    " + stringWNumbers)
            noLetters = re.sub('[a-zA-Z]','', stringWNumbers)
            # Letters Gone
            #print("Letters Gone:    " + noLetters)
            noSpaces = noLetters.replace(" ","")
            digitsandAs = noSpaces.replace(".","A")
            digitsandAs = digitsandAs.replace("-","A")
            #print("Digits:    " + digitsandAs)
            part_nums = re.sub('[^A-Za-z0-9]+', '', digitsandAs)
            # Spaces Gone

            #If it is a perfect partnum:
            if partNumRegex.match(part_nums):
                #print(part_nums)
                return part_nums

    return None
  
path_of_images =dirname + r"\drawings"
#This function reads the .tif file, runs Tesseract and then checks elements
def check_drawing(image_path, image_name):
    image_name_2 = image_path + str("\\") + image_name
    img_cv = cv2.imread(image_name_2)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    converted_string = pytesseract.image_to_string(img_rgb)
    all_text_list = converted_string.strip().split('\n')
    #print(all_text_list)
    only_part_numbers = []
    for element in all_text_list:
        if isNumbers(element) == False:
            pass
        elif isNumbers(element) == True:
            if isPartNumber(element) != None:
                partNoFormatted = isPartNumber(element)
                #Check if first A is in place:
                if partNoFormatted[2] == "A":
                    print(partNoFormatted + " is aligned from the beginning")
                    if len(partNoFormatted)>13:
                        print("Cleaning the unnecessary characters from the end")
                        partNoFormatted = partNoFormatted[0:13:]
                #Getting rid of if it has 
                elif partNoFormatted[3] == "A":
                    if len(partNoFormatted)>13:
                        print("Cleaning the unnecessary characters from the beginning")
                        partNoFormatted = partNoFormatted[1:13:]
                    
                    
                only_part_numbers.append(partNoFormatted)

#Every Part Number found is in a list and with this, written into a text file
    with open(image_name + ".txt", "w") as text_file:
        text_file.write("Here is the Part Numbers in this drawing:" + '\n')
        for found_numeric in only_part_numbers:
            text_file.write(found_numeric+ '\n')

        text_file.write('\n' + "***Experimental Code Results***")

#Main Function, repeats all steps above for EACH .tiff file in \drawings folder        
if __name__ == "__main__":
    # execute only if run as a script
    image_path = path_of_images
    image_list = os.listdir(dirname + r"\drawings\.")
    print(image_list)
    for image in image_list:
        check_drawing(image_path + str("\\"), image)


        