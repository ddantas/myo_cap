from PIL import Image
import PIL 

def pattern(localUp, localDown):

	wsize = 310	 
   	hsize = 370
	img = PIL.Image.open(localUp)
	    
	img = img.resize((wsize, hsize), PIL.Image.ANTIALIAS)
	img.save(localDown)	


def gray_scale(localUp, localDown):

   	img = Image.open(localUp).convert('L')
	img.save(localDown)	
