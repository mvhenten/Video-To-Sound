
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time

class GLWindow(object):
    _window             = None
    _full_screen         = True
    _set_mode_callback  = None
    _image_callback     = None;
    
    def __init__( self, image_callback ):
        self._image_callback = image_callback
        newArgv = glutInit(sys.argv)
    
        glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )

#        glutInitWindowSize(1600,900)
#        glutInitWindowPosition(100, 100)
        
        self._window = glutCreateWindow("hello")
    
        glutDisplayFunc( self.display )        
        glutKeyboardFunc( self.keyboard )    
        glutIdleFunc(self.idle )

        #glutReshapeFunc(reshape)
        #glutMouseFunc(printFunction( 'Mouse' ))
        #glutEntryFunc(printFunction( 'Entry' ))
        #glutKeyboardUpFunc( printFunction( 'KeyboardUp' ))
        #glutMotionFunc( printFunction( 'Motion' ))
        #glutPassiveMotionFunc( printFunction( 'PassiveMotion' ))
        #glutVisibilityFunc( printFunction( 'Visibility' ))
        #glutWindowStatusFunc( printFunction( 'WindowStatus' ))
        #glutSpecialFunc( printFunction( 'Special' ))
        #glutSpecialUpFunc( printFunction( 'SpecialUp' ))
        #glutTimerFunc( 1000, ontimer, 23 )
        glutMainLoop()
        
    def get_image( self ):
        return self._image_callback();
        
    def display( self ):        
        glutSetWindow( self._window )
        glClearColor (0.0, 0.0, 1.0, 0.0)
        glClear (GL_COLOR_BUFFER_BIT)
        
        #get out dimenstions
        screen_w = float(glutGet(GLUT_WINDOW_WIDTH))
        screen_h = float(glutGet(GLUT_WINDOW_HEIGHT))
        
        #dit is nodig
        glLoadIdentity();
        glOrtho(0.0, screen_w, 0.0, screen_h, -1.0, 1.0)        
        frame = self.get_image()
        
        #set fullscreen or not    
        if self._full_screen:
                glutFullScreen()
        else:
                glutReshapeWindow(frame.width,frame.height)
    
        #scale the frame    
        scale_w = screen_w/float(frame.width)
        scale_h = screen_h/float(frame.height)
        glPixelZoom(scale_w, -scale_h);
        
        #paint op de juist plek
        glRasterPos2d(0,frame.height);
        glBitmap (0, 0, 0, 0, 0, screen_h - frame.height , 0); #move the bitmap
        
        if frame.nChannels==1:
                glDrawPixels(frame.width, frame.height, GL_LUMINANCE, GL_UNSIGNED_BYTE, frame.tostring())
        else:
                glDrawPixels(frame.width, frame.height, GL_BGR, GL_UNSIGNED_BYTE, frame.tostring())
        
        glFlush ()
        glutSwapBuffers()
    
    def reshape( self, *args ):
        glViewport( *( (0,0)+args) )
        self.display()
    
    def idle( self ):
        glutPostRedisplay()
           
    def keyboard( self, key,x,y):        
        if( key == 'q' ):
            exit();
            
        if( key == 'f' ):
            self._full_screen = not self._full_screen
