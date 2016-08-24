import bpy
import time
import os.path

start_time = time.time()



# SETTINGS:

collums = 80
rows = 5
#rows must be uneven#

mid = int((rows +1)/2)

maxheight = 6

spectrum_Start = 10
spectrum_End = 21000
#in Hz# 

#path to musicfile#
path = os.path.abspath("C:\\Users\Hoxxel\Desktop\The Chainsmokers - Don t Let Me Down (Illenium Remix).mp3")

# </ SETTINGS>

l = 1
h = spectrum_Start

base = ( spectrum_End / spectrum_Start ) ** ( 1 / collums )



print("STARTED (Cubes_Spectrum=" + str(collums) + ", Cubes_Vertical=" + str(rows) + ", Cube_Height=" + str(maxheight) + ", Cube_Count=" + str(collums*rows) + ")")

bpy.ops.screen.frame_jump(end=False)

def funktion(x, y, zmax, lo, hi): 
        
    bpy.ops.mesh.primitive_cube_add(location = (x, y, 0))
    bpy.context.scene.cursor_location = bpy.context.active_object.location
    bpy.context.scene.cursor_location.z -= 1
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    ####
	#to have a gap between the cubes#
    bpy.context.active_object.scale.x = 0.4
    bpy.context.active_object.scale.y = 0.4
    bpy.context.active_object.scale.z = zmax
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bpy.ops.anim.keyframe_insert_menu(type='Scaling')
    bpy.context.active_object.animation_data.action.fcurves[0].lock = True
    bpy.context.active_object.animation_data.action.fcurves[1].lock = True
    
    
    bpy.context.area.type = 'GRAPH_EDITOR'
    
    
    bpy.ops.graph.sound_bake(filepath=path, low=lo, high=hi)
    
    
    
    bpy.context.active_object.animation_data.action.fcurves[2].lock = True
    
    
    
for i in range(0, collums):
    
	#exponetial course of frequency#
    l = h
    h = round(spectrum_Start * base ** (i + 1), 2)
    
    
    print("     c: " + str(i) + "   l: " + str(l) + " Hz    h: " + str(h) + " Hz")
    
	#exponetial drop to sides#
    for n in range(0, mid):
        hoehe = maxheight * (10**(-1*(n/(mid-1))))
        funktion(n, i, hoehe, l, h)
        
    for n in range(1, mid):
        hoehe = maxheight * (10**(-1*(n/(mid-1))))
        funktion((-1*n), i, hoehe, l, h)
        
    print(str(round(((i+1)/collums)*100, 1)) + "%   done in " + (str(round((time.time() - start_time)/60, 2))) + " minutes")
    
    
#change it back to the text editor.
bpy.context.area.type = 'TEXT_EDITOR'
print("FINISHED")