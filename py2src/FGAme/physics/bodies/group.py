# -*- coding: utf8 -*-
from __future__ import division
from FGAme.mathtools import null2D, shapes
from FGAme.physics.bodies.body import Body

inf = float('inf')
__all__ = ['Circle']


class Group(Body):

    '''Define um grupo de objetos físicos ligados rigidamente entre si.'''

    __slots__ = ()

    def __init__(self, objects, pos=(0, 0), vel=(0, 0), theta=0, mass=None, **kwds):
        
        if 'density' in kwds:
            raise TypeError('must set the density of each object separately')
        if 'inertia' in kwds and float(kwds['inertia']) != float('inf'):
            raise TypeError('cannot set the inerta of a group object')
        
        # Find center of mass position
        objects = list(objects)
        mass = sum(obj.mass for obj in objects)
        denom = sum(obj.mass * obj.pos for obj in objects)
        if mass == inf:
            mass = sum(obj.area for obj in objects)
            denom = sum(obj.area * obj.pos for obj in objects)
        pos_cm = denom / mass
         
        # Compute center of inertia
        if mass == inf:
            inertia = inf
        else:  
            inertia = sum(obj.inertia + obj.mass * (obj.pos - pos_cm).norm_sqr())
        
        # Compute the radius for the CBB
        R = 0
        for obj in objects:
            R = max(R, (obj.pos - pos).norm() + obj.cbb_radius)
        cbb_radius = float(R)
        
        # Super call
        super(Group, self).__init__(
            pos, vel, mass=mass, density=None, inertia=inertia,
            baseshape=None, cbb_radius=cbb_radius, **kwds)
        
        # Save object list
        self.objects = []
        for obj in self:
            obj.theta += theta
            obj.pos -= pos_cm
            self.objects.append(obj)
    
    def __iter__(self):
        return iter(self.objects)
    
    def __getitem__(self, idx):
        return self.objects[idx]
    
    def add(self, obj):
        raise NotImplementedError
        
    @Body.mass.setter
    def mass(self, value):
        total = self.mass
        ratio = value / total
        for obj in self:
            obj.mass *= ratio 
        super(Group, self).mass = value
    
    @property
    def bb(self):
        return None

    @property
    def xmin(self):
        return self.pos.x - self.cbb_radius

    @property
    def xmax(self):
        return self.pos.x + self.cbb_radius

    @property
    def ymin(self):
        return self.pos.y - self.cbb_radius

    @property
    def ymax(self):
        return self.pos.y + self.cbb_radius


if __name__ == '__main__':
    from doctest import testmod
    testmod()
    from FGAme import Group, Circle
    L = [Circle(10), Circle(10, pos=(10, 10), color='red')]
    g = Group(L)
