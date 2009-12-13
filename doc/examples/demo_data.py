import supreme.io
import os

def chelsea(grey=False):
    return supreme.io.imread(os.path.join(os.path.dirname(__file__),
                                          './data/chelsea.jpg'), grey)
