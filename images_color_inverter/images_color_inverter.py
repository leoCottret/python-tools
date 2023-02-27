from PIL import Image
import pathlib

# START OPTIONS
IN_PATH = 'in'
OUT_PATH = 'out'
# if you want to add some string before every inverted images, to better differantiate them. Can be an empty string
OUT_PREFIX = 'inv_'
# END OPTIONS

# FUNCTIONS

# revert a color channel
# each possible channel value can be defined independantly, from 0 to 255
# here we just want to revert the image color, so 0 becomes 255, 1 becomes 254 etc. until 255 becomes 0
def revert_channel(i):
	return 255 - i

# create inverted image from an image, with image_out_name as name
def create_inverted_image(image_in, image_out_name):
	# separate channels
	r, g, b = image_in.split()
	# revert red channel
	r = r.point(lambda i: revert_channel(i))
	# revert green channel
	g = g.point(lambda i: revert_channel(i))
	# revert blue channel
	b = b.point(lambda i: revert_channel(i))
	# create the new image by merging the 3 channels
	image_out = Image.merge('RGB', (r, g, b))
	# save the new image
	image_out.save(f'{OUT_PATH}/{image_out_name}')

# MAIN
# get all files in the "in" folder
files_in = pathlib.Path(f'{IN_PATH}').glob('**/*')
# iterate through the files
for f in files_in:
	# get an image in "in" folder
	image_in = Image.open(f.resolve()).convert('RGB')
	image_out_name = f'{OUT_PREFIX}{f.name}'
	create_inverted_image(image_in, image_out_name)