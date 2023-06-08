import cv2
import numpy as np

class Rect:  
  def __init__(self,
            a,
            b,
            c,
            d):
        self.a=a
        self.b=b
        self.c=c
        self.d=d

def merge_rectangles(r_1, r_2):

    a_m= min(r_1.a, r_2.a)
    b_m= min(r_1.b, r_2.b)
    c_M= max(r_1.c, r_2.c)
    d_M= max(r_1.d, r_2.d)

    return Rect(a_m, b_m, c_M, d_M)


def nearRects(rect_1,
        rect_2,
        tol_w=20,
        tol_h=60):
    
    b0 = (np.abs(rect_1.a - rect_2.a) < tol_w ) and (np.abs(rect_1.c - rect_2.c) < tol_w)

    h1 = np.abs(rect_1.d - rect_1.b)
    h2 = np.abs(rect_2.d - rect_2.b)
    b1 = np.abs(h1-h2) < tol_h

    return b0 and b1


def unionRects(contours):
  candidate_rectangles=[]
  for c in contours:
      x,y,w,h = cv2.boundingRect(c)
      candidate_rectangles.append(Rect(x,y,x+w,y+h))

  kept=np.ones(len(candidate_rectangles))
  new_rectangles=[]
  for i in range(len(candidate_rectangles)):
      for j in range(i+1,len(candidate_rectangles)):
          b=nearRects(candidate_rectangles[i], candidate_rectangles[j])
          if b:
              new_rect=merge_rectangles(candidate_rectangles[i], candidate_rectangles[j])
              new_rectangles.append(new_rect)
              kept[i]=0
              kept[j]=0

  rectangles = []
  for i in range(len(kept)):
      if kept[i]:
          rect=candidate_rectangles[i]
          rectangles.append(rect)

  for rect in new_rectangles:
      rectangles.append(rect)

  return rectangles

def preprocess_img(image):
    scale_percent = 60
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    denoised = cv2.fastNlMeansDenoising(image, None, 15, 7, 21)
    ret, thresh = cv2.threshold(denoised, 127, 255, cv2.THRESH_BINARY_INV)
  
    return thresh


def img_to_lst(image_file):
    image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    output = image.copy()
    prep_img = preprocess_img(image)
    contours, _ = cv2.findContours(prep_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    rectangles = unionRects(contours)
    cropped = []

    for rect in rectangles:
        cv2.rectangle(output, (rect.a, rect.b), (rect.c, rect.d), color=(0, 0, 0), thickness=1)
        x = rect.a
        y = rect.b
        w = rect.c - rect.a
        h = rect.d - rect.b
        crop = cv2.bitwise_not(prep_img)[y:y+h, x:x+w]
        size_max = max(w, h)
        square = 255 * np.ones(shape=[size_max, size_max], dtype=np.uint8)
        if w>h:
            y_pos = size_max//2 - h//2
            square[y_pos:y_pos+h, 0:w] = crop
        elif w < h:
            x_pos = size_max//2 - w//2
            square[0:h, x_pos:x_pos+w] = crop
        else:
            square = crop
        cropped.append((x, w, cv2.resize(square, (45, 45), interpolation=cv2.INTER_AREA)))


    cropped.sort(key=lambda x: x[0], reverse=False)
    
    return cropped