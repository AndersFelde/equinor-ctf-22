import cv2
import numpy as np
from matplotlib import pyplot as plt
import PIL

colors = {
    "brown": [165, 42, 42],
    "purple": [128, 0, 128],
    "white": [255, 255, 255],
    "yellow": [255, 255, 0],
    "blue": [0, 0, 255],
    "green": [0, 128, 0],
    "red": [255, 0, 0],
}

colorsHSV = {
    "black": [[180, 255, 30], [0, 0, 0]],
    "white": [[180, 18, 255], [0, 0, 231]],
    # "red": [[180, 255, 255], [159, 50, 70]],
    "brown": [[0, 193, 166], [0, 188, 158]],
    "red": [[9, 255, 255], [0, 50, 70]],
    "green": [[89, 255, 255], [36, 50, 70]],
    "blue": [[128, 255, 255], [90, 50, 70]],
    "yellow": [[35, 255, 255], [25, 50, 70]],
    "purple": [[158, 255, 255], [129, 50, 70]],
    "orange": [[24, 255, 255], [10, 50, 70]],
    "gray": [[180, 18, 230], [0, 0, 40]],
    # "brown": [[10, 100, 20], [20, 255, 200]],
}


def getColor(filename, x, y):
    red_image = PIL.Image.open(filename)
    red_image_rgb = red_image.convert("RGB")
    rgb_pixel_value = red_image_rgb.getpixel((x, y))
    return rgb_pixel_value


# reading image
def findShape(filename, shape):
    colorMode = False
    if " " in shape:
        colorMode = True
        color = shape.split(" ")[0].strip()
        shape = shape.split(" ")[1].strip()
        print("COLOR: ", color)
        print("SHAPE: ", shape)
    img = cv2.imread(filename)

    # converting image into grayscale image
    if not colorMode:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # setting threshold of gray image
        _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # using a findContours() function
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
    else:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        upper = np.array(colorsHSV[color][0])
        lower = np.array(colorsHSV[color][1])
        print("APPLYER MASK MED", lower, upper)
        # er egt ikke d
        gray = cv2.inRange(hsv, lower, upper)
        _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # using a findContours() function
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

    i = 0

    # list for storing names of shapes
    def getPos(x, y):
        out = ""
        if y > 300:
            out += "S"
        else:
            out += "N"

        if x > 300:
            out += "E"
        else:
            out += "W"

        return out

    poses = []
    joemama = ""
    if colorMode:
        joemama = []
    for contour in contours:

        # here we are ignoring first counter because
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        # using drawContours() function
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

        # finding center point of shape
        M = cv2.moments(contour)
        if M["m00"] != 0.0:
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])

        # putting shape name at center of each shape
        if len(approx) == 3:
            cv2.putText(
                img,
                "triangle",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )
            if shape == "triangle":
                print("FANT TRIANGLE")
                print(x, y)
                if colorMode:
                    joemama.append(getPos(x, y))
                else:
                    joemama = getPos(x, y)
                    break

        elif len(approx) == 4:
            cv2.putText(
                img,
                "rectangle",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )
            if shape == "rectangle":
                print("FANT RECTANGLE")
                print(x, y)
                if colorMode:
                    joemama.append(getPos(x, y))
                else:
                    joemama = getPos(x, y)
                    break

        elif len(approx) == 5:
            cv2.putText(
                img,
                "Pentagon",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )
            if shape == "pentagon":
                print("FANT PENTAGON")
                print(x, y)
                if colorMode:
                    joemama.append(getPos(x, y))
                else:
                    joemama = getPos(x, y)
                    break

        elif len(approx) == 6:
            cv2.putText(
                img,
                "Hexagon",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )
            if shape == "hexagon":
                print("FANT HEXAGON")
                print(x, y)
                if colorMode:
                    joemama.append(getPos(x, y))
                else:
                    joemama = getPos(x, y)
                    break

        else:

            cv2.putText(
                img, "circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
            )
            if shape == "circle":
                print("FANT CIRCLE")
                print(x, y)
                if colorMode:
                    joemama.append(getPos(x, y))
                else:
                    joemama = getPos(x, y)
                    break
        if colorMode:
            print("DID NOT FIND")
        poses.append(getPos(x, y))

    if not colorMode:
        if joemama == "":
            print("JEG FANT IKKE")
            for pos in ["NW", "NE", "SW", "SE"]:
                if pos not in poses:
                    joemama = pos
                    break
    else:
        if len(joemama) == 0:
            for pos in ["NW", "NE", "SW", "SE"]:
                if pos not in poses:
                    joemama.append(pos)

        if len(joemama) == 1:
            joemama = joemama[0]
        else:
            print("FLERE MULIGE: ", joemama)
            for coords in joemama:
                # if y > 300:
                #     out += "S"
                # else:
                #     out += "N"

                # if x > 300:
                #     out += "E"
                # else:
                #     out += "W"
                RED = (165, 42, 42)
                PURPLE = (128, 0, 128)
                WHITE = (255, 255, 255)
                if coords[0] == "S":
                    y = 380
                else:
                    y = 127

                if coords[1] == "E":
                    x = 380
                else:
                    x = 127

                foundCol = getColor(filename, x, y)
                print(foundCol)
                if color in colors and colors[color] == list(foundCol):
                    joemama = coords[0] + coords[1]
                    break

    # cv2.imshow("shapes", img)
    cv2.imwrite("cv2.png", img)
    cv2.imwrite("gray.png", gray)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return joemama


# displaying the image after drawing contours
