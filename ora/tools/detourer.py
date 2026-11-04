# Détourage d'un produit photographié sur fond blanc pur : matting contre le blanc.
import sys, numpy as np
from PIL import Image
from scipy import ndimage
src, out = sys.argv[1], sys.argv[2]
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 2
im = Image.open(src).convert('RGB')
im = im.resize((int(im.width*scale), int(im.height*scale)), Image.LANCZOS)
a = np.asarray(im).astype(np.float32)
L = a.mean(axis=2)
near_white = L > 238
lab, _ = ndimage.label(near_white)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
# bande de transition autour du fond
band = ndimage.binary_dilation(bg, iterations=int(3*scale)) & ~bg
alpha = np.ones_like(L)
alpha[bg] = 0
# dans la bande : alpha = écart au blanc, normalisé sur la couleur produit (sombre)
dark = 40.0
alpha[band] = np.clip((255 - L[band]) / (255 - dark), 0, 1)
# dé-mélange du blanc : C = (I - (1-a)*255) / a
aa = np.clip(alpha, 1e-3, 1)[..., None]
rgb = np.clip((a - (1 - aa) * 255) / aa, 0, 255)
rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
img = Image.fromarray(rgba, 'RGBA')
img = img.crop(img.getbbox())
img.save(out)
print(img.size)
