import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

global vertices
global normals
global texcoords
global faces

# vertices = []
# normals = []
# texcoords = []
# faces = []

def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError, "mtl file doesn't start with newmtl stmt"
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = pygame.image.load(mtl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, image)
        else:
            mtl[values[0]] = map(float, values[1:])
    return contents

class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
        for face in self.faces:
            vertices, normals, texture_coords, material = face
            # vertices, normals, texcoords
            # mtl = self.mtl[material]
            # if 'texture_Kd' in mtl:
            #     # use diffuse texmap
            #     glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            # else:
            #     # just use diffuse colour
            #     glColor(*mtl['Kd'])
            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(normals[normals[i] - 1])
                # if texture_coords[i] > 0:
                #     glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(vertices[vertices[i] - 1])
            glEnd()        
        # print "..."
    # def get_vertices(self):
    #     return self.vertices
    # def get_normals(self):
    #     return self.normals
    # def get_texcoords(self):
    #     return self.texcoords
    # def get_faces(self):
    #     return self.faces        
        # self.gl_list = glGenLists(1)
        # glNewList(self.gl_list, GL_COMPILE)
        # glEnable(GL_TEXTURE_2D)
        # glFrontFace(GL_CW)
        # for face in faces:
        #     vertices, normals, texture_coords, material = face
        #     # mtl = self.mtl[material]
        #     # if 'texture_Kd' in mtl:
        #     #     # use diffuse texmap
        #     #     glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
        #     # else:
        #     #     # just use diffuse colour
        #     #     glColor(*mtl['Kd'])
        #     glBegin(GL_POLYGON)
        #     for i in range(len(vertices)):
        #         if normals[i] > 0:
        #             glNormal3fv(self.normals[normals[i] - 1])
        #         # if texture_coords[i] > 0:
        #         #     glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
        #         glVertex3fv(self.vertices[vertices[i] - 1])
        #     glEnd()
        # # glDisable(GL_TEXTURE_2D)
        # glEndList()


def room():
    # print faces
    for face in faces:
        vertices, normals, texture_coords, material = face
        vertices, normals, texcoords
        mtl = self.mtl[material]
        if 'texture_Kd' in mtl:
            # use diffuse texmap
            glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
        else:
            # just use diffuse colour
            glColor(*mtl['Kd'])
        glBegin(GL_POLYGON)
        for i in range(len(vertices)):
            if normals[i] > 0:
                glNormal3fv(normals[normals[i] - 1])
            if texture_coords[i] > 0:
                glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
            glVertex3fv(vertices[vertices[i] - 1])
        glEnd()


def main():
    # global vertices, normals, texcoords, faces
    # obj = OBJ(sys.argv[1], swapyz=True)
    # vertices = obj.get_vertices()
    # normals = obj.get_normals()
    # texcoords = obj.get_texcoords()
    # faces = obj.get_faces()
    # room()
    pygame.init()
    viewport = (800,600)
    hx = viewport[0]/2
    hy = viewport[1]/2
    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
    glEnable(GL_DEPTH_TEST)
    clock = pygame.time.Clock()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(90.0, width/float(height), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    rx, ry = (0,0)
    tx, ty = (0,0)
    zpos = 30
    rotate = move = False
    while 1:
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4: zpos = max(1, zpos-1)
                elif e.button == 5: zpos += 1
                elif e.button == 1: rotate = True
                elif e.button == 3: move = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1: rotate = False
                elif e.button == 3: move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry += j
                if move:
                    tx += i
                    ty -= j
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
            # RENDER OBJECT
        glTranslate(tx/20., ty/20., - zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        obj = OBJ(sys.argv[1], swapyz=True)
        # glCallList(obj.gl_list)
        # print obj.gl_list
        pygame.display.flip()
main()    