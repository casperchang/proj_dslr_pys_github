import os,sys
# from PIL import Image
# from PIL.ExifTags import TAGS
import exifread

def get_field (exif,field) :
  for (k,v) in exif.iteritems():
     if TAGS.get(k) == field:
        return v

# image = Image.open('didi.JPG')
# exif = image._getexif()
# print(exif)
# print (get_field(exif,'ExposureTime'))


# Open image file for reading (binary mode)
f = open('./test/DSC01015.JPG', 'rb')

# Return Exif tags
tags = exifread.process_file(f)
# print(tags)
for tag in tags.keys():
    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        if 'DateTimeOriginal' in tag:
        	print ("Key: %s, value %s" % (tag, tags[tag]))
        	print('datatime: ', tags[tag])
        	str_datetime = str(tags[tag])

        	y = str_datetime.split(' ')[0].split(':')[0]
        	m = str_datetime.split(' ')[0].split(':')[1]
        	d = str_datetime.split(' ')[0].split(':')[2]

        	print('target folder: %s-%s-%s' % (y, m, d))
