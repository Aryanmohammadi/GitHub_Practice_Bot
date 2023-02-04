import cv2
import numpy as np
import scipy
from scipy.interpolate import UnivariateSpline



def spreadLookupTable(x, y):
        spline = UnivariateSpline(x, y)
        return spline(range(256))



class ImageEdit:
    def __init__(self,image):
        self.image = image

    def focus_on_nearest_object(image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply a Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply Canny edge detection to find edges in the image
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours in the image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort the contours by area and choose the largest one
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_contour = contours[0] if len(contours) > 0 else None
        
        # Create a mask that covers everything except the largest contour
        mask = np.zeros(image.shape, dtype=np.uint8)
        if largest_contour is not None:
            cv2.drawContours(mask, [largest_contour], 0, (255, 255, 255), -1)
        
        # Apply a Gaussian blur to everything outside the largest contour
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        blurred[mask == 0] = 0
        return blurred


    def beautify_photo(image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply a Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply histogram equalization to enhance the contrast
        equalized = cv2.equalizeHist(blurred)
        
        # Convert back to color
        color = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
        
        # Normalize the image to improve brightness and saturation
        norm_image = cv2.normalize(color, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC3)
        
        return norm_image



    def warmImage(image):
        increaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 50, 100, 256])
        red_channel, green_channel, blue_channel = cv2.split(image)
        red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
        return cv2.merge((red_channel, green_channel, blue_channel))
    
    def coldImage(self,image):
        increaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 50, 100, 256])
        red_channel, green_channel, blue_channel = cv2.split(self.image)
        red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
        return cv2.merge((red_channel, green_channel, blue_channel)) & cv2.imwrite("img/coldimage.jpg",self.image)

# We only have one main function in our project because it indicates that the file which contains our main function is our main script to run
'''def main():
    image = cv2.imread("img/img.jpg")
    operation = ImageEdit(image)
    operation.coldImage(image)

    



if __name__ == '__main__':
    main()
'''