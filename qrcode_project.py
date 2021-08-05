import io
import os, sys, shutil, os.path
import qrcode
import cv2

def create_qr(item):
    url = "http://localhost:5000/view-qr/"
    qr_address = url + item
    qr = qrcode.QRCode()
    img = qrcode.make(qr_address)
    return img

def read_qr(qrcode_image):
    d = cv2.QRCodeDetector()
    val, points, straight_qrcode = d.detectAndDecode(cv2.imread(qrcode_image))
    return {'val': val, 'points': points, 'straight_qrcode': straight_qrcode}


