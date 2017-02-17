# -*- coding: utf-8 -*-
__author__ = 'liaoben'


from PIL import Image
import os
import cv2



def isCrust(pix):
    # return sum(pix) < 25
    #print pix
    return pix == (26,26,26)

def hCheck(img, y, step = 50):
    count = 0
    width = img.size[0]
    for x in xrange(0, width, step):
        if isCrust(img.getpixel((x, y))):
            #print '1111'
            count += 1
        if count > width / step / 2:
            return True
    return False

def vCheck(img, x, step = 50):
    count = 0
    height = img.size[1]
    for y in xrange(0, height, step):
        if isCrust(img.getpixel((x, y))):
            count += 1
        if count > height / step / 2:
            return True
    return False

def boundaryFinder(img,crust_side,core_side,checker):
    if not checker(img,crust_side):
        return crust_side
    if checker(img,core_side):
        return core_side

    mid = (crust_side + core_side) / 2
    while  mid != core_side and mid != crust_side:
        if checker(img,mid):
            crust_side = mid
        else:
            core_side = mid
        mid = (crust_side + core_side) / 2
    return core_side


def boundary_find(img):
    img = Image.open(img)
    if img.mode != "RGB":
        img = img.convert("RGB")
    width, height = img.size
    print width,height
    for i in range(0,width/2,1):
        rgb = img.getpixel((i, height/2-1))
        if not isCrust(rgb):
            left = i
            break

    for i in range(width-1,width/2,-1):
        rgb = img.getpixel((i, height/2))
        if not isCrust(rgb):
            right = i
            break

    for i in range(0,height/2,1):
        rgb = img.getpixel((width/2-1, i))
        if not isCrust(rgb):
            top = i
            break
    for i in range(height-1,height/2,-1):
        rgb = img.getpixel((width/2, i))
        if not isCrust(rgb):
            bottom = i
            break
    box = (left,top,right,bottom)
    #print box
    return box

def handleImage2(filename,tar):
    #img = Image.open(os.path.join(src_folder,filename))
    img = Image.open(filename)
    if img.mode != "RGB":
        img = img.convert("RGB")
    width, height = img.size
    box = boundary_find(filename)
    region = img.crop(box)
    #print tar,filename
    p = os.path.join(tar,os.path.split(filename)[1])
    print p
    #region.show()
    region.save(p)
    return box

def handleImage(filename,tar):
    #img = Image.open(os.path.join(src_folder,filename))
    img = Image.open(filename)
    if img.mode != "RGB":
        img = img.convert("RGB")
    width, height = img.size
    print width,height
    left = boundaryFinder(img, 0, width/2, vCheck)
    right = boundaryFinder(img, width-1, width/2, vCheck)
    top = boundaryFinder(img, 0, height/2, hCheck)
    bottom = boundaryFinder(img, height-1, width/2, hCheck)

    rect = (left,top,right,bottom)
    print rect
    region = img.crop(rect)
    #print tar,filename
    p = os.path.join(tar,os.path.split(filename)[1])
    print p
    #region.show()
    region.save(p)
    pass

def folderCheck(foldername):
    if foldername:
        if not os.path.exists(foldername):
            os.mkdir(foldername)
            print "Info: Folder \"%s\" created" % foldername
        elif not os.path.isdir(foldername):
            print "Error: Folder \"%s\" conflict" % foldername
            return False
    return True
    pass

def main():
    if folderCheck(tar_folder) and folderCheck(src_folder) and folderCheck(backup_folder):
        for filename in os.listdir(src_folder):
            if filename.split('.')[-1].upper() in ("JPG","JPEG","PNG","BMP","GIF"):
                handleImage(filename,tar_folder)
                os.rename(os.path.join(src_folder,filename),os.path.join(backup_folder,filename))
        pass

class CnvHandler:

    def __init__(self,driver,pic_width,pic_height,mode=1):
        self.driver = driver
        self.pic_width = pic_width
        self.pic_height = pic_height
        self.mode = mode
        self.screen_width = self.driver.get_window_size()['width']
        self.screen_height = self.driver.get_window_size()['height']
        self.slide_range = 13
        self.pic_range = 5



    def calculator(self):
        if self.mode == 1:
            if self.pic_width > self.pic_height:
                return self.calculator1()
            if self.pic_width < self.pic_height:
                return self.calculator2()
            if self.pic_height == self.pic_width:
                return self.caclulator5()
        if self.mode == 9:
            if self.pic_width > self.pic_height:
                return self.calculator3()
            if self.pic_width < self.pic_height:
                return self.calculator4()
            if self.pic_height == self.pic_width:
                return self.caclulator6()

    #单横图
    def calculator1(self):
        h0 = self.screen_width*7/15
        w1 = self.pic_width*h0/self.pic_height
        request_h = h0
        q=70
        if w1>=1200:
            request_w=1200
        elif w1<1200:
            request_w=w1
        return request_w,request_h,q

    #单竖图
    def calculator2(self):
        w0 = self.screen_width*7/15
        h1 = self.pic_height*w0/self.pic_width
        request_w = w0
        q=70
        if h1>=1600:
            request_h=1600
        elif h1<1200:
            request_h=h1
        return request_w,request_h,q

    #九宫横图
    #测试可以搜索：九宫格横图缩放后小于1200
    def calculator3(self):
        h0 = (self.screen_width-self.slide_range*2-self.pic_range*2)/3
        w1 = self.pic_width*h0/self.pic_height
        q=70
        request_h = h0
        if w1>=1200:
            request_w=1200
        elif w1<1200:
            request_w=w1
        return request_w,request_h,q

    #九宫竖图
    def calculator4(self):
        w0 = (self.screen_width-self.slide_range*2-self.pic_range*2)/3
        h1 = self.pic_height*w0/self.pic_width
        request_w = w0
        q=70
        if h1>=1600:
            request_h=1600
        elif h1<1200:
            request_h=h1
        return request_w,request_h,q

    #单方图
    def caclulator5(self):
        return 480,480,70

    #九宫方图
    def caclulator6(self):
        w0 = (self.screen_width-self.slide_range*2-self.pic_range*2)/3
        h0 = w0
        return w0,h0,70

if __name__ == '__main__':
    #main()
    # fn = 'g:/music/1.png'
    # fn2 = 'g:/music/2.png'
    # im1 = Image.open(fn)
    # rgb_im1 = im1.convert('RGB')
    # im2 = Image.open(fn2)
    # rgb_im2 = im2.convert('RGB')
    # for i in range(im1.size[0]):
    #     for j in range(im1.size[1]):
    #         x = rgb_im1.getpixel((i, j))
    #         y = rgb_im2.getpixel((i, j))
    #         if x !=y:
    #             print i,j
    #             print x,y
    handleImage('g:/toast.tiff','g:/')