from math import pi, sin, cos
from panda3d.core import *
from pandac.PandaModules import ActorNode, ForceNode, LinearVectorForce
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Shader
from direct.filter.CommonFilters import CommonFilters
from direct.interval.IntervalGlobal import Sequence
import sys

loadPrcFile('robolove.prc')

class MainApp(ShowBase):
    

    def __init__(self):
        ShowBase.__init__(self)

        # Load shaders. If this fails, quit.
        if(not self.loadShaders()):
            return
        #Make some floors for us :)
        floorTex=loader.loadTexture('maps/envir-ground.jpg')
        cm=CardMaker('')
        cm.setFrame(-2,2,-2,2)
        floor = render.attachNewNode(PandaNode("floor"))
        for y in range(12):
            for x in range(12):
                nn = floor.attachNewNode(cm.generate())
                nn.setP(-90)
                nn.setPos((x-6)*4, (y-6)*4, 0)
        floor.setTexture(floorTex)
        floor.flattenStrong()

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
        
        # Models
        #Tron
        self.pandaActor = Actor("models/tron")
        self.pandaActor.setScale(0.3, 0.3, 0.3)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.setPos(10, 0, 4.2)

        #Panda
        # Load the "panda" model.  Loading a model returns a
        # NodePath object.
        ##self.panda = loader.loadModel("panda")
        # Remember, loaded objects start out hidden!  If we want to
        # see the panda, it must be reparented to the "render" node.
        ##self.panda.reparentTo(render)
        # By default, position is specified relative to a node's
        # parent.Position is specified as "x,y,z" or "right, forward, up"
        # Since panda's parent is the root node (render),
        # this command moves panda to the global position (0, 30, -5).
        ##self.panda.setPos(0, 0, 0)
        # Alternately, the position can be given relative to any other
        # NodePath.  Here, we set the position to be 30 feet in front
        # of the camera, and slightly to the right.  Note the use of
        # 'camera', another pre-defined NodePath object.
        ##self.panda.setX(camera, 10)








        # Text
        self.text = TextNode('node name')
        self.textNodePath = aspect2d.attachNewNode(self.text)
        self.textNodePath.setScale(0.05)
        self.text.setTextColor(1, 1, 1, 1)
      
        # enable physics
        base.enableParticles()
        self.physicsNode=NodePath(PandaNode("PhysicsNode"))
        self.physicsNode.reparentTo(render)

        # set up camera with physics
        self.cameraActorNode=ActorNode("camera-physics")
        self.cameraActorNodeParent=self.physicsNode.attachNewNode(self.cameraActorNode)
        base.physicsMgr.attachPhysicalNode(self.cameraActorNode)
        self.camera.reparentTo(self.cameraActorNodeParent)

        # set up camera and mouse settings
        self.camera.setPos(6.27662, -48.9656, 26.0119)
        self.camera.setHpr(7.30458, -27.7855, 3.34447)
        self.cameraInterval = self.camera.posInterval(10,
                                                        Point3(10,10,20),
                                                        startPos=Point3(camera.getPos()))
        self.cameraPace = Sequence(self.cameraInterval)
        self.cameraForwardThrottleEnabled = False
        #self.cameraPace.start()

        # disable debug mode for starters
        self.setDebugMode(False)

        # event handling
        self.accept("space", self.toggleGlow)
        self.accept("escape", sys.exit, [0])
        self.accept('o', self.toggleDebugMode)
        
        self.accept('p', self.pauseSequence)
        self.accept('w', self.moveForward)
        self.accept('a', self.moveLeft)
        self.accept('d', self.moveRight)
        self.accept('s', self.moveBack)

        self.accept('arrow_up', self.enableCameraForwardThrottle)
        self.accept('arrow_up-up', self.disableCameraForwardThrottle)

        # add tasks
        self.taskMgr.add(self.doLogic, "DoLogic")
#        self.taskMgr.add(self.refreshGUI, "RefreshGUI")

    def enableCameraForwardThrottle(self):
        self.cameraForwardThrottleEnabled = True

    def disableCameraForwardThrottle(self):
        self.cameraForwardThrottleEnabled = False

    def refreshGUI(self, task):
        string = str(self.pandaActor.getPos())
        self.text.setText(string)
        self.text.setCardColor(0, 0, 0, 0.5)
        self.text.setCardAsMargin(0, 0, 0, 0)
        return task.cont

    def moveForward(self):
        currentPosition = self.pandaActor.getPos()
        newPosition = Point3(0,2,0) + currentPosition
        pandaMoveForwardInterval = self.pandaActor.posInterval(0.1,
                                                        Point3(newPosition),
                                                        startPos=Point3(currentPosition))
        self.pandaPace = Sequence(pandaMoveForwardInterval)
        self.pandaPace.start()
        return currentPosition
    def moveBack(self):
        currentPosition = self.pandaActor.getPos()
        newPosition = Point3(0,-2,0) + currentPosition
        pandaMoveForwardInterval = self.pandaActor.posInterval(0.1,
                                                        Point3(newPosition),
                                                        startPos=Point3(currentPosition))
        self.pandaPace = Sequence(pandaMoveForwardInterval)
        self.pandaPace.start()
        return currentPosition

    def moveLeft(self):
        currentPosition = self.pandaActor.getPos()
        newPosition = Point3(-2,0,0) + currentPosition
        pandaMoveForwardInterval = self.pandaActor.posInterval(0.1,
                                                        Point3(newPosition),
                                                        startPos=Point3(currentPosition))
        self.pandaPace = Sequence(pandaMoveForwardInterval)
        self.pandaPace.start()
        return currentPosition

    def moveRight(self):
        currentPosition = self.pandaActor.getPos()
        newPosition = Point3(2,0,0) + currentPosition
        pandaMoveForwardInterval = self.pandaActor.posInterval(0.1,
                                                        Point3(newPosition),
                                                        startPos=Point3(currentPosition))
        self.pandaPace = Sequence(pandaMoveForwardInterval)
        self.pandaPace.start()
        return currentPosition

    def pauseSequence(self):
        self.pandaPace.pause()

    def doLogic(self, task):
        dt = globalClock.getDt()
        # this method is a placeholder to test if differnt stuff has occured
        # like checking wether the robot is ready for a new command, etc.
        if self.cameraForwardThrottleEnabled:
            currentVelocity = self.cameraActorNode.getPhysicsObject().getVelocity()
            newVelocity = currentVelocity + Vec3(dt*250,0,0)
            self.cameraActorNode.getPhysicsObject().setVelocity(newVelocity)

        # slow down camera ("friction")
        self.cameraActorNode.getPhysicsObject().setVelocity(self.cameraActorNode.getPhysicsObject().getVelocity() * 0.92)


        return Task.cont

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

    def loadShaders(self):
        # Check video card capabilities for shaders.
        if (base.win.getGsg().getSupportsBasicShaders() == 0):
            addTitle("Glow Filter: Video driver reports that shaders are not supported.")
            return False

        # Load filters
        self.filters = CommonFilters(base.win, base.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat=-0.5, intensity=3.0, size="small")
        if (filterok == False):
            addTitle("Toon Shader: Video card not powerful enough to do image postprocessing")
            return False
        self.glowSize=1

        # Shadow shaders
        # TODO: Implement shadows
        
        return True

app = MainApp()
app.run()
