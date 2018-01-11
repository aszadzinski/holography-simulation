import matplotlib as mlp
mlp.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib_scalebar.scalebar import ScaleBar

def f_fresnel(z_arr, x_res, y_res, wavelenght, reconstruct=False):
    s = np.zeros(z_arr.shape)
    x_px, y_px = s.shape[0], s.shape[1]
    pm = 1
    if reconstruct:
        pm = -1
    for i in range(x_px):
        for j in range(y_px):
            #s[i][j] = np.exp(pm*1j*np.pi*wavelenght*z_arr[i][j]*(((i-x_px/2-1)/x_res)**2 + ((j-y_px/2-1)/y_res)**2))
            s[i][j] = np.exp(pm*2j * np.pi * 1/wavelenght * z_arr[i][j] * (1-wavelenght**2*((i - x_px / 2 - 1) / x_res) ** 2 - wavelenght**2*((j - y_px / 2 - 1) / y_res) ** 2)**0.5)
            
    s[np.isnan(s)] = 0
    return s

def holo_arr(_object, z_arr, x_res, y_res, wavelenght):
    shape = _object.shape
    #hologram = np.fft.ifft2(np.fft.fft2(_object)*f_fresnel(z_arr, x_res, y_res, wavelenght,True))
    hologram = _ifft(_fft(_object)*f_fresnel(z_arr, x_res, y_res, wavelenght,True))
    hologram = np.abs(hologram)**2
    return hologram

def reholo_arr(_object, z_arr, x_res, y_res, wavelenght):
    shape = _object.shape
    img = _ifft(_fft(_object)*f_fresnel(z_arr, x_res, y_res, wavelenght, True))
    img = np.abs(img)**2
    return img


def z_const(_object, cz):
    z = np.full(_object.shape, cz)
    return z

def _ifft(_object):
    size = _object.shape
    fft = np.zeros(size)
    for i in range(size[0]):
        for j in range(size[1]):
            fft[i][j] = np.exp(-1j*np.pi*(i + j))
    return np.fft.ifft2(fft*_object)

def _fft(_object):
    size = _object.shape
    fft = np.zeros(size)
    for i in range(size[0]):
        for j in range(size[1]):
            fft[i][j] = np.exp(1j*np.pi*(i + j))
    return np.fft.fft2(fft*_object)

def save_holo(_object, path, n, label='Interference pattern'):
    plt.imshow(_object, cmap='gray',  interpolation='lanczos')
    plt.title(label)
    plt.xlabel('px')
    plt.ylabel('px')
    scalebar = ScaleBar(n/500,'m', box_alpha=0.2)
    plt.gca().add_artist(scalebar)
    plt.savefig(path, bbox_inches='tight', pad_inches=0)
    plt.clf()
    return None

