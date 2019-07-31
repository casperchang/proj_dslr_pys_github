import os
import exifread
import shutil
from shutil import copyfile


def get_photo_original_datetime(path_image, filename):
    # get the datetime
    file_path = path_image
    b = open(file_path, 'rb')
    tags = exifread.process_file(b)
    # print(tags.keys)
    # print('loop++')
    for tag in tags.keys():
        # print(tag)
        if 'DateTimeOriginal' in tag:
            # print(str(tags[tag]))
            try:
                str_datetime = str(tags[tag])
            except:
                print(Exception)
            finally:
                # print('str_datetime: ', str_datetime.split(' ')[0])
                # print('len: ', len(str_datetime))
                if len(str_datetime.split(' ')[0].split(':')) == 3:
                    # print(str_datetime)
                    y = str_datetime.split(' ')[0].split(':')[0]
                    m = str_datetime.split(' ')[0].split(':')[1]
                    d = str_datetime.split(' ')[0].split(':')[2]
                    create_date = '%s%2s%s' % (y, m, d)
                    # print(create_date)
                    # break
                    return y, create_date
                else:
                    print('datatime format error len: %d' % len(str_datetime.split(' ')[0].split(':')))
    return ('', '')


if __name__ == '__main__':

    src_folder = './_to_process'
    output_folder = '_photo_by_py'

    specified_date = ''
    specified_folder_note = ''
    # specified_date = '20170825'
    # specified_folder_note = ''

    for root, dirs, files in os.walk(src_folder):
        for i, f in enumerate(files):
            print('... %d/%d' % (i, len(files)))
            if 'jpg' in f or 'jpeg' in f or 'JPG' in f or 'JPEG' in f:

                file_path = os.path.join(root, f)

                if specified_date != '':
                    y = specified_date[:4]
                    # print('y: ', y)
                    create_date = specified_date
                    folder_y = os.path.join(output_folder, y)
                    folder_name = os.path.join(output_folder, y, '%s_%s' % (specified_date, specified_folder_note))
                else:
                    y, create_date = get_photo_original_datetime(file_path, f)
                    # print(y, create_date)
                    if create_date == '': # fail, won't move anything
                        print('no datetime info')
                        continue
                    else:
                        folder_y = os.path.join(output_folder, y)
                        folder_name = os.path.join(output_folder, y, create_date)

                # do move

                # folder exited checking, if not, create it.
                if not os.path.isdir(folder_y):
                    try:
                        os.mkdir(folder_y)
                    except Exception as e:
                        print(e)
                if not os.path.isdir(folder_name):
                    try:
                        os.mkdir(folder_name)
                    except Exception as e:
                        print(e)

                # check if file already existed in dist path
                if os.path.isfile(os.path.join(folder_name, f)):
                    print('file already existed, skip (%s)' % f)
                else:
                    # copy file
                    # copyfile(os.path.join(root, f), os.path.join(folder_name, f))

                    # move file
                    shutil.move(os.path.join(root, f), os.path.join(folder_name, f))

                print(folder_name)

        print(len(files))



'''
# Open image file for reading (binary mode)
f = open('../didi.JPG', 'rb')

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

        	print('folder: %s-%s-%s' % (y, m, d))
        else: # find alternative
        	pass
'''