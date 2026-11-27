"""ORA — agrandit une petite image (photo de fournisseur) par 4, avec Real-ESRGAN x4plus (licence BSD-3), sur le processeur.
Usage : python3 agrandir_ia.py entree.(png|jpg|webp) sortie.png
Prérequis : ncnn (installé automatiquement s'il manque). Le modèle (~45 Mo, GitHub) est téléchargé au premier usage dans ~/.cache/ora/realesrgan.
L'agrandissement rend net ce qui est flou ; il n'invente pas un autre produit, mais vérifier les détails fins (broches, textes).
"""
import os, sys, time, zipfile, subprocess, urllib.request, numpy as np
try:
    import ncnn
except ImportError:   # absent d'une session neuve : installé à la volée (PyPI)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'ncnn'], check=True); import ncnn
from PIL import Image
CACHE = os.path.expanduser('~/.cache/ora/realesrgan')
ZIP = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip'
M = os.path.join(CACHE, 'models', 'realesrgan-x4plus')
if not os.path.exists(M + '.bin'):
    os.makedirs(CACHE, exist_ok=True); z = os.path.join(CACHE, 'esr.zip')
    urllib.request.urlretrieve(ZIP, z)
    with zipfile.ZipFile(z) as f:
        for n in f.namelist():
            if '/models/realesrgan-x4plus.' in '/' + n or n.startswith('models/realesrgan-x4plus.'):
                os.makedirs(os.path.join(CACHE, 'models'), exist_ok=True)
                open(os.path.join(CACHE, 'models', os.path.basename(n)), 'wb').write(f.read(n))
    os.remove(z)
net = ncnn.Net(); net.opt.use_vulkan_compute = False; net.opt.num_threads = os.cpu_count() or 4
net.load_param(M + '.param'); net.load_model(M + '.bin')
im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32) / 255
H, W, _ = im.shape; T, P = 160, 12; out = np.zeros((H * 4, W * 4, 3), np.float32); t0 = time.time()
for y in range(0, H, T):          # par tuiles (mémoire), avec marge pour éviter les coutures
    for x in range(0, W, T):
        y0, x0, y1, x1 = max(y - P, 0), max(x - P, 0), min(y + T + P, H), min(x + T + P, W)
        ex = net.create_extractor(); ex.input('data', ncnn.Mat(np.ascontiguousarray(im[y0:y1, x0:x1].transpose(2, 0, 1))))
        _, o = ex.extract('output'); o = np.array(o).transpose(1, 2, 0)
        oy, ox = (y - y0) * 4, (x - x0) * 4; h, w = min(T, H - y) * 4, min(T, W - x) * 4
        out[y * 4:y * 4 + h, x * 4:x * 4 + w] = o[oy:oy + h, ox:ox + w]
Image.fromarray((np.clip(out, 0, 1) * 255 + .5).astype(np.uint8)).save(sys.argv[2])
print('OK', sys.argv[2], f'{W}×{H} → {W*4}×{H*4}', round(time.time() - t0, 1), 's')
