from pickle import FALSE
import pytesseract
import cv2
import os
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

dirname = os.path.dirname(__file__)
#print(dirname)
#quit()
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


def check_drawing(image_path, image_name):
    image_name_2 = image_path + str("\\") + image_name
    img_cv = cv2.imread(image_name_2)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    converted_string = pytesseract.image_to_string(img_rgb)
    all_text_list = converted_string.strip().split('\n')
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
            

    with open(image_name + ".txt", "w") as text_file:
        text_file.write("Here is the Part Numbers in this drawing:" + '\n')
        for found_numeric in only_part_numbers:
            text_file.write(found_numeric+ '\n')

        text_file.write('\n' + "***Note that these results are not validated with more than 100 drawings***")
        # text_file.write("ALL Text Info from tesseract: %s" % all_text_list)

#Make it get global path for deployment

if __name__ == "__main__":
    # execute only if run as a script
    image_path = path_of_images
    image_list = os.listdir(dirname + r"\drawings\.")
    print(image_list)
    for image in image_list:
        check_drawing(image_path + str("\\"), image)