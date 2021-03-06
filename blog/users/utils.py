import os
import secrets
from PIL import Image 
from flask import url_for
from blog import app

def save_pic(form_pic):
	ran_hax = secrets.token_hex(8)
	_ , f_ext = os.path.splitext(form_pic.filename)
	pic_fn = ran_hax + f_ext
	pic_path = os.path.join(app.root_path, 'static/IMG', pic_fn)

	size = (80,80)
	i = Image.open(form_pic)
	i.thumbnail(size)
	i.save(pic_path)
	return pic_fn

