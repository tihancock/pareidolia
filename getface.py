import numpy as np
import cv2
import cv2.cv as cv
import glob, datetime, os

width = 320
height = 240

class GetFace:
    def __init__(self):
        self.capture = cv.CreateCameraCapture(-1)
        self.cascade = cv.Load('res/haarcascade_frontalface_default.xml')
        self.num_cloud_faces = 0

        date = datetime.datetime.now().strftime("%Y_%m_%d")
        
        self.output_folder = "output/" + date

        if os.path.exists(self.output_folder):
            existing_faces = glob.glob(self.output_folder + "/*.jpg")
            if len(existing_faces) > 0:
                print existing_faces
                im_nums = [int(f.rstrip(".jpg").split("_")[-1]) for f in existing_faces]
                print im_nums
                self.num_cloud_faces = max(im_nums) + 1
        else:
            os.makedirs(self.output_folder)

    def look_for_faces(self):
        image = cv.QueryFrame(self.capture)

        if self.detect_face(image):
            cv.SaveImage(self.output_folder + "/cloudface_%d.jpg" % (self.num_cloud_faces), image)
            self.num_cloud_faces += 1

    def detect_face(self, image):
        min_size = (20,20)
        image_scale = 2
        haar_scale = 1.1
        min_neighbors = 2
        haar_flags = 0

        # Allocate the temporary images
        gray = cv.CreateImage((image.width, image.height), 8, 1)
        smallImage = cv.CreateImage((cv.Round(image.width / image_scale),cv.Round (image.height / image_scale)), 8 ,1)

        # Convert color input image to grayscale
        cv.CvtColor(image, gray, cv.CV_BGR2GRAY)

        # Scale input image for faster processing
        cv.Resize(gray, smallImage, cv.CV_INTER_LINEAR)

        # Equalize the histogram
        cv.EqualizeHist(smallImage, smallImage)

        # Detect the faces
        faces = cv.HaarDetectObjects(smallImage, self.cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)

        return faces

if __name__ == "__main__":
    get_face = GetFace()

    positives = glob.glob('res/test_images/positive/*')
    negatives = glob.glob('res/test_images/negative/*')

    print "Positives"
    for f in positives:
        image = cv.LoadImage(f)
        
        if get_face.detect_face(image):
            print "%s passes" % (f)
        else:
            print "*** FAILED: %s" % (f)

    print "Negatives"
    for f in negatives:
        image = cv.LoadImage(f)
        
        if not get_face.detect_face(image):
            print "%s passes" % (f)
        else:
            print "*** FAILED: %s" % (f)
