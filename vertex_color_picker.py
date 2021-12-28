import bpy
import pprint
import bmesh

from mathutils import Color

from collections import defaultdict

def avg_col(cols):
    avg_col = Color((0.0, 0.0, 0.0))

    for col in cols:
        tempcol = Color((col[0], col[1], col[2]))

        avg_col += tempcol/len(cols)
    return avg_col

def vertex_color_picker(self, context):
    tk = defaultdict(list)

    mesh = bpy.context.active_object.data
    color_layer = mesh.vertex_colors['Col']

    i = 0
    for poly in mesh.polygons:
        for idx in poly.loop_indices:
            loop = mesh.loops[idx]
            color = color_layer.data[i].color
            tk[loop.vertex_index].append(color)
            i += 1

    vcol_averages = {k: avg_col(v) for k, v in tk.items()}

    vertices_of_interest = [k for k, v in vcol_averages.items() if v.r < context.scene.color_treshold]


    bpy.ops.object.mode_set(mode='EDIT')


    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    vertices= [e for e in bm.verts]
    oa = bpy.context.active_object

    for vert in vertices:
        if vert.index in vertices_of_interest:
            vert.select_set(True)
        else:
            vert.select_set(False)


    bmesh.update_edit_mesh(me)      

    pprint.pprint(vertices_of_interest)

    # you must cast this as a dict manually like  tk = dict(tk) , 
    # if you need it as a dict, but defaultdict will behave mostly the same

    #pprint.pprint(tk)