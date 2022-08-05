def qemu_img(cijoe, args=[]):
    """Helper function wrapping around 'qemu_img'"""

    return cijoe.run(f"{cijoe.config['qemu']['img_bin']} " + " ".join(args))

def qemu_system(cijoe, args=[]):
    """Wrapping the qemu system binary"""

    return cijoe.run(f"{cijoe.config['qemu']['system_bin']" + " ".join(args))
