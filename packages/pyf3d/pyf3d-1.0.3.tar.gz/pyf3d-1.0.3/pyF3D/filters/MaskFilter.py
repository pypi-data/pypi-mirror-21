import numpy as np
import pkg_resources as pkg
import pyopencl as cl
import pyF3D.FilterClasses as fc

class MaskFilter:

    """
    Class for applying mask to an image

    Parameters
    ----------
    maskChoice: str, optional
        type of mask - can only be 'mask3D' currently
    mask: {sr, ndarray}, optional
        Mask must be same shape as image. Can be one of the following string values:

        'StructuredElementL'
        ''Diagonal3x3x3'
        ''Diagonal10x10x4'
        ''Diagonal10x10x10'

        Can also be ndarray that will be used directly as a mask
    L: int, optional
        Radius for 'StructuredElementL' mask
    """

    allowedMasks = ['StructuredElementL', 'Diagonal3x3x3', 'Diagonal10x10x4',
                          'Diagonal10x10x10']
    maskChoices = ['mask3D']

    def __init__(self, maskChoice='mask3D', mask='StructuredElementL', L=3):

        self.name = 'MaskFilter'

        self.maskChoice = maskChoice
        self.mask = mask
        self.L = L
        self.clattr = None
        self.atts = None

        if type(self.mask) is str:
            if self.mask not in self.allowedMasks: raise TypeError('Mask does not match any of allowed choices')
        else:
            try:
                self.mask = np.array(self.mask).astype(np.uint8)
            except ValueError:
                raise TypeError('Mask must be able to be converted to np.uint8')

    def toJSONString(self):
        result = "{ \"Name\" : \"" + self.getName() + "\" , "
        result += "\"selectedMaskChoice\" : \"" + self.maskChoice + "\" , "

        mask = {"maskImage" : self.mask if self.mask in self.allowedMasks else 'customMask'}
        if self.mask == 'StructuredElementL':
            mask["maskLen"] = "{}".format(int(self.L))

        result += "\"Mask\" : " + "{}".format(mask) + " }"
        return result

    def clone(self):
        return MaskFilter(maskChoice=self.maskChoice, mask=self.mask, L=self.L)

    def getName(self):
        return "MaskFilter"

    def getInfo(self):
        info = fc.FilterInfo()
        info.name = self.getName()
        info.memtype = bytes
        info.overlapX = info.overlapY = info.overlapZ = 0
        return info

    def loadKernel(self):
        try:
            filename = "../OpenCL/Mask3D.cl"
            self.program = cl.Program(self.clattr.context, pkg.resource_string(__name__, filename)).build()
        except Exception:
            return False

        self.kernel = cl.Kernel(self.program, self.maskChoice)
        return True

    def runFilter(self):
        mask = self.atts.getMaskImages(self.mask, self.L)[0]

        if self.atts.width*self.atts.height*self.atts.slices != np.product(mask.shape):
            print "Mask dimensions not equal to original image's"
            return False

        globalSize = [0]
        localSize = [0]

        self.clattr.computeWorkingGroupSize(localSize, globalSize, [self.atts.width, self.atts.height,
                                                self.clattr.maxSliceCount + self.atts.overlap[self.index]])
        self.maskBuffer = self.atts.getStructElement(self.clattr.context, self.clattr.queue, mask, globalSize[0])

        try:
            self.kernel.set_args(self.clattr.inputBuffer, self.maskBuffer, self.clattr.outputBuffer,
                                 np.int32(self.atts.width), np.int32(self.atts.height),
                                 np.int32(self.clattr.maxSliceCount + self.atts.overlap[self.index]))

            cl.enqueue_nd_range_kernel(self.clattr.queue, self.kernel, globalSize, localSize)

        except Exception as e:
            raise e

            # write results
        cl.enqueue_copy(self.clattr.queue, self.clattr.inputBuffer, self.clattr.outputBuffer)
        self.clattr.queue.finish()

        return True

    def setAttributes(self, CLAttributes, atts, index):
        self.clattr = CLAttributes
        self.atts = atts
        self.index = index



