

__all__ = ['propagator', 'image_converter']

if __name__ == "__main__":
    import image_converter
    import propagator
    import numpy as np
    from sys import argv
    _object = image_converter.convert_image(argv[1])
    z = propagator.z_const(_object, float(argv[3]))
    if len(argv) == 8:
        hologram = propagator.reholo_arr(_object, z, float(argv[4]), float(argv[4]), float(argv[5]))
    else:
        hologram = propagator.holo_arr(_object, z, float(argv[4]), float(argv[4]), float(argv[5]))
    propagator.save_holo(hologram, argv[2], float(argv[4]))



