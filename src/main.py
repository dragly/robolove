from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Shader
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import AntialiasAttrib
from panda3d.core import TextNode,Point3,Vec4
from panda3d.core import loadPrcFile
import sys
#dette er en test

loadPrcFile('robolove.prc')

class MainApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Check video card capabilities for shaders.
        if (base.win.getGsg().getSupportsBasicShaders() == 0):
            addTitle("Glow Filter: Video driver reports that shaders are not supported.")
            return

        # Load filters
        self.filters = CommonFilters(base.win, base.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat=-0.5, intensity=3.0, size="small")
        if (filterok == False):
            addTitle("Toon Shader: Video card not powerful enough to do image postprocessing")
            return
        self.glowSize=1

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # set up shaders and anti alias
        self.render.setShaderAuto()
        self.render.setAntialias(AntialiasAttrib.MAuto)
        
        # set up lights
        dlight = DirectionalLight('dlight')
        alight = AmbientLight('alight')
        dlnp = render.attachNewNode(dlight)
        alnp = render.attachNewNode(alight)
        dlight.setColor(Vec4(1.0, 0.7, 0.2, 1))
        alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)
        render.setLight(alnp)
        
        # set up model
        self.pandaActor = Actor("models/tron")
        self.pandaActor.setScale(0.3, 0.3, 0.3)
        self.pandaActor.reparentTo(self.render)

        # set up camera and mouse settings
        self.camera.setPos(6.27662, -48.9656, 26.0119)
        self.camera.setHpr(7.30458, -27.7855, 3.34447)

        # disable debug mode for starters
        self.setDebugMode(False)

        # event handling
        self.accept("space", self.toggleGlow)
        self.accept("escape", sys.exit, [0])
        self.accept('d', self.toggleDebugMode)

    def toggleGlow(self):
        self.glowSize = self.glowSize + 1
        if (self.glowSize == 4): self.glowSize = 0
        self.filters.setBloom(blend=(0,0,0,1), desat=-0.5, intensity=3.0, size=self.glowSize)
        print "Glow size set to", self.glowSize
        
    def printCameraPosition(self):
        print self.camera.getPos()
        print self.camera.getHpr()
    def toggleDebugMode(self):
        if(self.debugMode):
            self.setDebugMode(False)
        else:
            self.setDebugMode(True)
    def setDebugMode(self, enabled):
        self.debugMode = enabled
        if(enabled):
            self.enableMouse()
            self.accept('c', self.printCameraPosition)
        else:
            self.disableMouse()
            self.ignore('c')

app = MainApp()
app.run()
