# by Renaud ROHLINGER
import bpy
import os

def main(context):
    # Auto select all cameras
    objects = bpy.context.scene.objects
    for obj in objects:
        obj.select_set(obj.type == "CAMERA")
        ad = obj.animation_data

    # check if actions is empty
    if bpy.data.actions:
        # get all actions
        action_list = [action for action in bpy.data.actions]
        # sort, remove doubles and create a set
        keys = (sorted(set([item for sublist in action_list for item in sublist.frame_range])))
        # print first and last keyframe
        #print ("{} {}".format("first keyframe:", keys[0]))
        #print ("{} {}".format("last keyframe:", keys[-1]))
    else:
        print ("no actions")

    # name of the glb generated based on the name of the .blend file
    basedir = os.path.dirname(bpy.data.filepath)
    name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
    fn = os.path.join(basedir, name)
    print(basedir, name, fn)

    # Auto bake with first and last frame
    bpy.ops.nla.bake(frame_start=keys[0], frame_end=keys[-1], visual_keying=True, clear_constraints=True, bake_types={'OBJECT'})
    
    #export glb in the same folder as the blend file
    bpy.ops.export_scene.gltf(
        filepath=fn + ".glb",
        export_format='GLB',
        ui_tab='GENERAL',
        export_copyright="",
        export_image_format='AUTO',
        export_texture_dir="",
        export_texcoords=True,
        export_normals=True,
        export_draco_mesh_compression_enable=False,
        export_draco_mesh_compression_level=6,
        export_draco_position_quantization=14,
        export_draco_normal_quantization=10,
        export_draco_texcoord_quantization=12,
        export_draco_generic_quantization=12,
        export_tangents=False,
        export_materials=True,
        export_colors=True,
        export_cameras=True,
        export_selected=False,
        export_extras=False,
        export_yup=True,
        export_apply=False,
        export_animations=True,
        export_frame_range=True,
        export_frame_step=1,
        export_force_sampling=True,
        export_nla_strips=True,
        export_def_bones=False,
        export_current_frame=False,
        export_skins=True,
        export_all_influences=False,
        export_morph=True,
        export_morph_normal=True,
        export_morph_tangent=False,
        export_lights=False,
        export_displacement=False,
        will_save_settings=False,
        check_existing=True,
        filter_glob="*.glb;*.gltf"
    )
    pass


class SimpleOperator(bpy.types.Operator):
        bl_idname = "object.simple_operator"
        bl_label = "Simple Object Operator"
       
        def execute(self, context):
                main(context)
                return {'FINISHED'}

bpy.utils.register_class(SimpleOperator)


try:

    bpy.ops.object.simple_operator()
    #undo bake script
    bpy.ops.ed.undo()
except Exception as e:
    print("something went wrong")
    #raise the exception again
    raise e


