# context.area: VIEW_3D
# by Renaud Rohlinger
# https://github.com/RenaudRohlinger/blender_gltf_scripts

import os
import bpy
from bpy_extras.io_utils import ExportHelper

bl_info = {
    "name": "GLTF Scripts",
    "author": "Renaud Rohlinger <renaudrohlinger@gmail.com>",
    "version": (1, 0),
    "blender": (2, 83, 0),
    "description": "GLTF script utilies",
    "category": "",
    "location": "3D Viewport",
    "doc_url": "https://github.com/RenaudRohlinger/blender_gltf_scripts",
    "tracker_url": "https://github.com/RenaudRohlinger/blender_gltf_scripts"
}


def main(context):

    # Select object view
    # bpy.ops.object.mode_set(mode="OBJECT")

    # Auto select the camera
    objects = bpy.context.scene.objects
    for obj in objects:
        obj.select_set(obj.type == "CAMERA")

    # select the camera and get the first and last animation frame
    a = bpy.context.selected_objects[0].animation_data.action
    frame_start, frame_end = map(int, a.frame_range)

    # name of the glb generated based on the name of the .blend file
    basedir = os.path.dirname(bpy.data.filepath)

    # add user basedir path if available
    if context.scene.dir_path:
        basedir = bpy.path.abspath(context.scene.dir_path)

    name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
    fn = os.path.join(basedir, name)
    # Auto bake with first and last frame
    bpy.ops.nla.bake(frame_start=frame_start, frame_end=frame_end,
                     visual_keying=True, clear_constraints=True, bake_types={'OBJECT'})

    # Export glb in the same folder as the blend file
    bpy.ops.export_scene.gltf(
        filepath=fn + "_camera.glb",
        check_existing=True,
        export_format='GLB',
        ui_tab='GENERAL',
        use_selection=True,
        export_draco_mesh_compression_enable=context.scene.draco)

    # reselect a context to trigger undo
    for obj in objects:
        obj.select_set(obj.type == "CAMERA")

    pass


def main_gltf(context):
    # name of the glb generated based on the name of the .blend file
    basedir = os.path.dirname(bpy.data.filepath)
    # add user basedir path if available
    if context.scene.dir_path:
        basedir = bpy.path.abspath(context.scene.dir_path)

    name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
    fn = os.path.join(basedir, name)

    bpy.ops.export_scene.gltf(
        filepath=fn + ".glb",
        check_existing=True,
        export_format='GLB',
        ui_tab='GENERAL',
        export_draco_mesh_compression_enable=context.scene.draco)
    pass


class SimpleGLTF(bpy.types.Operator):
    bl_idname = "object.simple_gltf"
    bl_label = "Quick Scene Export"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            main_gltf(context)
            return {'FINISHED'}
        except Exception as e:
            print("something went wrong")
            # raise the exception again
            raise e


class BakeCamera(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Camera Bake Export"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            main(context)
            # undo bake script
            bpy.ops.ed.undo_push()
            return {'FINISHED'}
        except Exception as e:
            print("something went wrong")
            # raise the exception again
            raise e


class GLTF_PT_Panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = 'GLTF Export'
    bl_idname = "GLTF_PT_Panel"
    bl_label = "Quick GLTF Export"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        col = layout.column()
        col.prop(context.scene, 'dir_path')

        col2 = layout.column()
        col2.prop(context.scene, 'draco')

        layout.operator('object.simple_operator', icon='VIEW_CAMERA')
        layout.operator('object.simple_gltf', icon='SHADERFX')


blender_classes = [
    BakeCamera,
    SimpleGLTF,
    GLTF_PT_Panel
]


def register():
    bpy.types.Scene.dir_path = bpy.props.StringProperty(
        name="Path",
        default="",
        description="Define the glb path of the project",
        subtype='DIR_PATH'
    )
    bpy.types.Scene.draco = bpy.props.BoolProperty(
        name="Use Draco compression",
        description="Use Draco Compression",
        default=False
    )
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)


def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)
    del bpy.types.Scene.dir_path
    del bpy.types.Scene.draco
