# Based on the original https://www.reddit.com/r/deepfakes/ code sample + contribs

import cv2

from lib.aligner import get_align_mat

class Extract(object):
    @staticmethod
    def extract(image, face, size):
        if face.landmarks == None:
            print("Warning! landmarks not found. Switching to crop!")
            return cv2.resize(face.image, (size, size))

        alignment = get_align_mat( face )
        return Extract.transform( image, alignment, size, 48 )

    @staticmethod
    def transform( image, mat, size, padding=0 ):
        mat = mat * (size - 2 * padding)
        mat[:,2] += padding
        return cv2.warpAffine( image, mat, ( size, size ) )
