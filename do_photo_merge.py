import numpy as np
import cv2 as cv
 
import argparse
import sys
  
parser = argparse.ArgumentParser(prog='do_photo_merge.py',
                                 description='Merge photos into one')
parser.add_argument('--output', default = 'result.jpg',
    help = 'Resulting image. The default is `result.jpg`.')
parser.add_argument('img', nargs='+', help = 'input images')
 
def main():
    args = parser.parse_args()
 
    # read input images
    imgs = []
    for img_name in args.img:
        img = cv.imread(cv.samples.findFile(img_name))
        if img is None:
            print("can't read image " + img_name)
            sys.exit(-1)
        imgs.append(img)
 
    stitcher = cv.Stitcher.create(cv.Stitcher_PANORAMA)
    status, pano = stitcher.stitch(imgs)
 
    if status != cv.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
        sys.exit(-1)
    
    cv.imwrite(args.output, pano)
 
 
if __name__ == '__main__':
    main()
    cv.destroyAllWindows()
