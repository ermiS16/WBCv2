from base64 import b64decode
import datetime



class Output:

    EXT_PNG = ".png"
    EXT_CSV = ".csv"

    def __init__(self, dest):
        self = self
        self.output_dir = dest


    def saveSrcAsImage(self, imgSrc):
        imageFileName = self.generateFileName(self.EXT_PNG)

        # decode the img-src into an actual image
        header, encoded = imgSrc.split(",", 1)
        data = b64decode(encoded)


        # save decoded image as .png
        with open(imageFileName, "wb") as f:
            f.write(data)


    def saveArrayAsCSV(self, arr):
        imageFileName = self.generateFileName(self.EXT_CSV)
        print(imageFileName)


    def generateFileName(self, extension):
        if(self.dest[-1] != '/'):
            self.dest = self.dest + '/'

        print(self.dest)

        #outputDirectory = "Output/Pr0"
        #fileExtension = ".png"
        date = datetime.datetime.now()
        currentDate = date.strftime("%Y%m%d%H%M%S%f")

        filename = self.dest + currentDate + extension
        return filename
