# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 18:22:41 2025

@author: sheng
@name: Computational Geometry Practice

@description:
    
    Kind of taken some from here:
        https://github.com/dreilly369/AppliedMathForSecurityBook/blob/main/Chapter%207%20-%20Computational%20Geometry%20Theory/Computational_Geometry.ipynb
        
    Others from book
"""
import math
from shapely.geometry import Point, LineString, Polygon, LinearRing
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PolyPatch

#%%
point_a = Point((2.0, 4.0))
point_b = Point((4.0, 0.0))
origin = Point((0, 0))

line_a = LineString([(2.0, 4.0), (4.0, 0.0)])
line_b = LineString([point_a, point_b])
line_c = LineString([(3.3,5.0), origin])

print(line_a.area, line_a.length)
print(line_b.area, line_b.length)
print(line_c.area, line_c.length)

ring_a = LinearRing([origin, (4.0,6.0), (6.0, 6.0), origin]) # explicit close
ring_b = LinearRing([(-4.0, -1.0), (3.0,-2.0), (-1.0, -3.0)]) # implicit close

print(ring_a.area, ring_a.length)
print(ring_b.area, ring_b.length)

poly_a = Polygon([(2.0,2.0), (4.0,1.0), (5.0,5.0), (2.0,2.0)]) # explictly closed polygon made of raw values
poly_b = Polygon([origin, point_b, point_a]) # implicitly closed polygon made of points
poly_c = Polygon([origin, (-4.0, 3.2), point_a, (5.1, 3.5)]) # Polygon made of mixed points and raw tuples

print(poly_a.area, poly_a.length)
print(poly_b.area, poly_b.length)
print(poly_c.area, poly_c.length)

poly_a_fill = PolyPatch(list(poly_a.exterior.coords), fill=True, facecolor="Blue")
poly_b_fill = PolyPatch(list(poly_b.exterior.coords), fill=True, facecolor="Green")
poly_c_fill = PolyPatch(list(poly_c.exterior.coords), fill=True, facecolor="Red")

fig, ax = plt.subplots(ncols=3, nrows=1)
ax[0].plot(*poly_a.exterior.xy, color="Black", alpha=0.7, linewidth=1, solid_capstyle="round", zorder=2)
ax[0].add_patch(poly_a_fill)

ax[1].plot(*poly_b.exterior.xy, color="Black", alpha=0.7, linewidth=1, solid_capstyle="round", zorder=2)
ax[1].add_patch(poly_b_fill)

ax[2].plot(*poly_c.exterior.xy, color="Black", alpha=0.7, linewidth=1, solid_capstyle="round", zorder=2)
ax[2].add_patch(poly_c_fill)

fig.tight_layout()
plt.show()

#%%
park = Polygon([(0,0), (4.5, 0.5), (9, 3), (14,7), (12,9), (5,9)])
info_booth = Polygon([(4,2), (5,2), (5,3), (4,3)])
stage = Polygon([(6,7), (9,7), (9,8), (6,8)])

park_fill = PolyPatch(list(park.exterior.coords), fill=True, facecolor="#00FF5A")
info_fill = PolyPatch(list(info_booth.exterior.coords), fill=True, facecolor="White")
stage_fill = PolyPatch(list(stage.exterior.coords), fill=True, facecolor="White")

fig, ax = plt.subplots(ncols=1, nrows=1)
ax.plot(*park.exterior.xy, color="Black", alpha=0.7,
    linewidth=1, solid_capstyle="round", zorder=2, marker="*")
ax.plot(*info_booth.exterior.xy, color="Black", alpha=0.7,
    linewidth=1, solid_capstyle="round", zorder=2, marker=".")
ax.plot(*stage.exterior.xy, color="Black", alpha=0.7,
    linewidth=1, solid_capstyle="round", zorder=2, marker=".")
ax.add_patch(park_fill)
ax.add_patch(info_fill)
ax.add_patch(stage_fill)
ax.set_title("Event Park")
ax.set_xlabel("x10 meters")
ax.set_ylabel("x10 meters")
#fig.tight_layout()
plt.savefig("Figure_7-3.png")
plt.savefig("Figure_7-3.svg", format="svg")
plt.show()

#%% scale of 1 to 10 for map
event_area = (park.area - (info_booth.area + stage.area)) * 10
print ("%.2f m^2 park area" % (park.area * 10))
print ("%.2f m^2 info booth area" % (info_booth.area * 10))
print ("%.2f m^2 stage area" % (stage.area * 10))
print ("%.2f m^2 usable area" % event_area)

safe_capacity = int(math.floor(event_area / 0.75)) # 8ft sq
max_capacity = int(math.floor(event_area / 0.37)) # 4ft sq
print("Comfortable capacity: %d people" % safe_capacity)
print("Maximum safe capacity: %d people" % max_capacity)