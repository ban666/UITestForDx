# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from PIL import Image

def make_regalur_image(img, size = (256, 256)):

    return img.resize(size).convert('RGB')


def split_image(img, part_size = (64, 64)):

    w, h = img.size

    pw, ph = part_size

    assert w % pw == h % ph == 0
    return [img.crop((i, j, i+pw, j+ph)).copy() for i in xrange(0, w, pw) for j in xrange(0, h, ph)]


def hist_similar(lh, rh):

    assert len(lh) == len(rh)

    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)



def calc_similar(li, ri):

    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0


def calc_similar_by_path(lf, rf):

    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))

    return calc_similar(li, ri)

def calc_similar_by_percent(lf, rf,percent):

    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))

    result = True if calc_similar(li, ri)>percent else False

    return result

if __name__ == '__main__':
    path = 'g:/doc/pic/*.jpg'
    import os.path
    import glob
    for f in glob.glob(path):
        t = Image.open(f)
        print os.path.split(f)[1],'{:.2f}'.format(os.path.getsize(f)/1024/1024.0),t.height,t.width