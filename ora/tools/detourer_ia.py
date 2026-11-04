import sys
from rembg import remove, new_session
from PIL import Image
model, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
s = new_session(model)
im = Image.open(src).convert('RGB')
r = remove(im, session=s, alpha_matting=False)
r.save(out); print(out, r.size)
