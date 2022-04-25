import cv2
import os
import sys
import shutil
from shutil import copyfile
import tkinter as tk
import exifread
from send2trash import send2trash
from os import listdir
from os.path import isfile, join

def get_photo_original_datetime(path_image, filename):
	file_path = path_image
	b = open(file_path, 'rb')
	tags = exifread.process_file(b)
	# print(tags.keys)
	for tag in tags.keys():
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
	return ('', '') # empty stands for something wrong

def show_image_by_index(root, files, index):
	# print('index %d, len(files): %d' % (index, len(files)))
	f = files[index]
	# print(os.path.join(root, f))

	tkobj = tk.Tk()
	screen_width = tkobj.winfo_screenwidth()
	screen_height = tkobj.winfo_screenheight()
	# print(screen_width, screen_height)

	if 'jpg' in f or 'jpeg' in f or 'JPG' in f or 'JPEG' in f:
		cv2.namedWindow('show', cv2.WINDOW_NORMAL)
		image = cv2.imread(os.path.join(root, f))

		#
		max_h = int(screen_height * 0.8)
		if image.shape[0] > max_h:
			ratio = image.shape[0] / float(max_h)
			imS = cv2.resize(image, (int(image.shape[1] / ratio), max_h))
		else:
			imS = image
		cv2.imshow("show", imS)
		return 0
	else: 
		return -1


if __name__ == '__main__':

	# default path for convenient 
	# TODO: fine-tune w/ gui or force to bring argvs
	# path_develop = '/Users/casper/Desktop/proj_dslr_pys/_dev_volume_5_20190731'
	path_develop = os.path.join(os.getcwd(), 'profolio')
	path_stock = os.path.join(os.getcwd(), 'stock')
	# path_stock = '/Users/casper/Desktop/proj_dslr_pys/_photo_by_py/2019/20190623'

	if len(sys.argv) >= 2:
		path_stock = sys.argv[1]
		print('path_stock: %s' % path_stock)

	for root, dirs, files in os.walk(path_stock):
		# print('root: ', root)
		files.sort()

	index = 0

	while True:
		res = show_image_by_index(root, files, index)
		if res == -1:
			index += 1
			continue
		c = cv2.waitKey()
		# print(c)
		if c == 32 or c == 1: # key.space or key.down
			cv2.destroyAllWindows()
			index += 1
			# if index >= len(files):
			#   index = len(files) - 1 # to the last file
			index = min(index, len(files)-1)
		elif c == 0: # key.up
			cv2.destroyAllWindows()
			index -= 1
			index = max(index, 0)
		elif c == ord('q'):
			sys.exit()
		elif c == ord('d'): # delete this file
			f = files[index]
			src = os.path.join(root, f)
			if src != '':
				if os.path.isfile(src):
					send2trash(src)
					# index += 1
					files = [f for f in listdir(path_stock) if isfile(join(path_stock, f))]
					files.sort()
					index = min(index, len(files) - 1)
		elif c == ord('s'):

			# check if folder existed, otherwise mkdir it. 
			if not os.path.isdir(os.path.join(os.getcwd(), 'selected')):
				try:
					os.mkdir(os.path.join(os.getcwd(), 'selected'))
					print(f"folder selected has been created.")
				except Exception as e:
					print(e)

			# cp file into selected folder
			f = files[index]
			src = os.path.join(root, f)
			dst = os.path.join('./selected', f)
			# copyfile(src, dst)
			# print('copyfile from %s to %s' % (src, dst))

			# move file instead of copy
			shutil.move(src, dst)
			# reload file list after moving picture
			files = [f for f in listdir(path_stock) if isfile(join(path_stock, f))]
			files.sort()
			index = min(index, len(files) - 1)

		elif c == ord('p'):

			# check if folder existed, otherwise mkdir it. 
			if not os.path.isdir(os.path.join(os.getcwd(), 'profolio')):
				try:
					os.mkdir(os.path.join(os.getcwd(), 'profolio'))
					print(f"folder selected has been created.")
				except Exception as e:
					print(e)


			# cp file into profolio folder (profolio means enough to sharing or development :) )
			f = files[index]
			src = os.path.join(root, f)

			#dst = os.path.join('./profolio', f)

			# get captured date in exif
			y, create_date = get_photo_original_datetime(src, f)
			if create_date != '':
				dst = os.path.join(path_develop, create_date+'_'+f)
			# give a new name

			copyfile(src, dst)
			print('copyfile from %s to %s' % (src, dst))
		else:
			print ('you press %s, do nothing' % chr(c))


'''
Upkey : 0
DownKey : 1
LeftKey : 2
RightKey: 3
Space : 32
Delete : 40
esc:27
'''



