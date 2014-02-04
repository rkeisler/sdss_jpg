
def demo():  
    '''
    Get jpg image for UGC 01962, view it, 
    and remove temporary jpg file.
    '''
    jpg = SdssJpg(37.228, 0.37)
    jpg.show()
    jpg.clean_up()



class SdssJpg(object):

    '''
    Class for an SDSS jpg image.
    See http://skyservice.pha.jhu.edu/dr10/imgcutout/imgcutout.asmx
    for more info.

      RA, DEC - J2000, degrees
      SCALE - plate scale in arsec per pixel
      WIDTH, HEIGHT - size of image in pixels
      SAVENAME - if none provided, defaults to 'sdss.jpg'
      DR - integer value for SDSS data release.
    '''

    def __init__(self, ra, dec, 
                 scale=0.3515625, width=512, height=512,
                 savename=None, DR=10, init_download=True):
        self.ra = ra
        self.dec = dec
        self.scale = scale
        self.width = width
        self.height = height
        self.DR = DR
        if savename==None:
            savename = 'sdss.jpg'
        self.savename = savename
        if init_download: self.download()

        
    def download(self):
        from urllib import urlretrieve
        url = 'http://skyservice.pha.jhu.edu/dr%i/ImgCutout/getjpeg.aspx?'%self.DR
        url += 'ra=%0.5f&dec=%0.5f&'%(self.ra, self.dec)
        url += 'scale=%0.5f&'%self.scale
        url += 'width=%i&height=%i'%(self.width, self.height)
        urlretrieve(url, self.savename)


    def data(self):
        from PIL import Image
        import numpy as np
        return np.array(Image.open(self.savename), dtype=np.uint8)

    def show(self):
        import matplotlib.pylab as pl
        pl.imshow(self.data())

    def clean_up(self):
        from os import system
        system('rm '+self.savename)



