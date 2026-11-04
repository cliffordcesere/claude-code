import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA')
a = np.asarray(im).astype(np.float32)
al = a[..., 3] / 255
# 1. garder la plus grande composante (supprime les taches isolées)
lab, n = ndimage.label(al > 0.5)
if n > 1:
    sizes = ndimage.sum(np.ones_like(al), lab, range(1, n + 1))
    keep = lab == (1 + int(np.argmax(sizes)))
    keep = ndimage.binary_dilation(keep, iterations=3)
    al = al * keep
# 2. bords : léger rognage puis adoucissement
m = Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
al = np.asarray(m).astype(np.float32) / 255
al = np.clip((al - 0.15) / 0.7, 0, 1)
# 3. débruitage de l'image (médiane 5 px, puis flou léger)
rgb = Image.fromarray(a[..., :3].astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(0.6))
res = np.dstack([np.asarray(rgb), (al * 255).astype(np.uint8)])
img = Image.fromarray(res, 'RGBA'); img = img.crop(img.getbbox()); img.save(out); print(out, img.size)
