def demo():  
    '''
    Get jpg image for UGC 01962, view it, 
    and remove temporary jpg file.
    '''
    jpg = SdssJpg(37.228, 0.37)
    jpg.show()


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

    def __del__(self):
        from os import system
        # remove the temporary jpg file
        system('rm '+self.savename)
        
    def download(self):
        from urllib import urlretrieve
        from PIL import Image
        from numpy import array, uint8
        url = 'http://skyservice.pha.jhu.edu/dr%i/ImgCutout/getjpeg.aspx?'%self.DR
        url += 'ra=%0.5f&dec=%0.5f&'%(self.ra, self.dec)
        url += 'scale=%0.5f&'%self.scale
        url += 'width=%i&height=%i'%(self.width, self.height)
        urlretrieve(url, self.savename)
        self.data = array(Image.open(self.savename), dtype=uint8)

    def show(self):
        import matplotlib.pylab as pl
        pl.imshow(self.data)


def study25():
    '''
    Dumb function for viewing images of 25 galaxies
    whose (RA, DEC) positions are in tmp.csv
    '''
    from pandas.io.parsers import read_csv
    import matplotlib.pylab as pl
    pl.ion()
    x=read_csv('tmp.csv')
    pl.figure(1)
    pl.clf()
    for i in range(25):
        pl.subplot(5,5,i+1)
        jpg=SdssJpg(x.ra[i],x.dec[i], width=64, height=64)
        pl.axis('off');
        pl.imshow(jpg.data)
        pl.title('%0.2f'%x.z[i])
        
