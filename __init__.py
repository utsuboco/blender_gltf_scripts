# context.area: VIEW_3D
# by Renaud Rohlinger
# https://github.com/RenaudRohlinger/blender_gltf_scripts

import os
import bpy
from bpy_extras.io_utils import ExportHelper

bl_info = {
    "name": "GLTF Scripts",
    "author": "Renaud Rohlinger <renaudrohlinger@gmail.com>",
    "version": (1, 3),
    "blender": (2, 92, 0),
    "description": "GLTF script utilities",
    "category": "",
    "location": "3D Viewport",
    "doc_url": "https://github.com/RenaudRohlinger/blender_gltf_scripts",
    "tracker_url": "https://github.com/RenaudRohlinger/blender_gltf_scripts"
}

loading = False


def main(self, context):
    bpy.context.window.cursor_set("WAIT")
    loading = True
    # preevent the undo to not work
    bpy.ops.object.mode_set(mode="OBJECT")

    bpy.ops.object.select_all(action='DESELECT')

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

    if context.scene.filename_path:
        name = context.scene.filename_path

    if not name:
        context.scene.filename_path = 'scene'
        name = 'scene'

    fn = os.path.join(basedir, name) + "_camera.glb"
    # Auto bake with first and last frame
    bpy.ops.nla.bake(frame_start=frame_start, frame_end=frame_end,
                     visual_keying=True, clear_constraints=True, bake_types={'OBJECT'})
    self.report({'INFO'}, 'Bake camera from frame ' +
                str(frame_start) + ' to frame ' + str(frame_end))

    wm = bpy.types.WindowManager
    props = wm.operator_properties_last("export_scene.gltf")
    dic = {}
    for k, v in props.items():
        dic[k] = v

    useAdvanced = False
    if context.scene.advanced_mode:
        useAdvanced = True
        if props:
            fn = dic['filepath'][:-4] + "_camera.glb"

    bpy.ops.export_scene.gltf(
        filepath=fn,
        check_existing=True,
        export_format='GLB',
        ui_tab='GENERAL',
        use_selection=True,
        export_draco_mesh_compression_level=context.scene.draco_level,
        export_draco_mesh_compression_enable=False)
    self.report({'INFO'}, 'GLTF Export completed')

    bpy.ops.ed.undo()

    bpy.context.window.cursor_set("DEFAULT")
    loading = False
    pass


def main_gltf(self, context):
    # name of the glb generated based on the name of the .blend file
    basedir = os.path.dirname(bpy.data.filepath)
    # add user basedir path if available
    if context.scene.dir_path:
        basedir = bpy.path.abspath(context.scene.dir_path)

    name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]

    if context.scene.filename_path:
        name = context.scene.filename_path

    if not name:
        context.scene.filename_path = 'scene'
        name = 'scene'

    fn = os.path.join(basedir, name)

    wm = bpy.types.WindowManager
    props = wm.operator_properties_last("export_scene.gltf")
    dic = {}
    for k, v in props.items():
        dic[k] = v

    if props and context.scene.advanced_mode:
        fn = dic['filepath'][:-4]
        dic['export_draco_mesh_compression_enable'] = False if context.scene.instance or context.scene.unlit else dic['export_draco_mesh_compression_enable']
        bpy.ops.export_scene.gltf(**dic)
        self.report({'INFO'}, 'GLTF Export completed')
    else:
        bpy.ops.export_scene.gltf(
            filepath=fn + ".glb",
            check_existing=True,
            export_format='GLB',
            ui_tab='GENERAL',
            export_draco_mesh_compression_level=context.scene.draco_level,
            export_draco_mesh_compression_enable=False if context.scene.instance or context.scene.unlit else context.scene.draco)
        self.report({'INFO'}, 'GLTF Export completed')

    if context.scene.unlit:
        import subprocess
        try:
            subprocess.run(['gltf-transform',
                           'unlit', fn + ".glb", fn + ".glb"])
            self.report({'INFO'}, 'KHR_Unlit compression applied')
        except:
            print('gltf-transform',
                  'unlit', fn + ".glb", fn + ".glb")
            self.report({'ERROR'}, 'KHR_Unlit failed')

    if context.scene.instance:
        import subprocess
        try:
            subprocess.run(['gltf-transform',
                           'instance', fn + ".glb", fn + ".glb"])
            self.report({'INFO'}, 'EXT_GPU_Instancing applied')
        except:
            self.report({'ERROR'}, 'EXT_GPU_Instancing failed')

    if (context.scene.instance or context.scene.unlit) and context.scene.draco:
        import subprocess
        try:
            subprocess.run(['gltf-transform', 'draco',
                            fn + ".glb", fn + ".glb"])
            self.report({'INFO'}, 'Draco compression applied')
        except:
            self.report({'ERROR'}, 'Draco failed')

    pass


class SimpleGLTF(bpy.types.Operator):
    bl_idname = "object.simple_gltf"
    bl_label = "Quick Scene Export"

    def execute(self, context):
        try:
            self.report(
                {'INFO'}, '----- ----- ----- GLTF Scripts ----- ----- -----')
            self.report(
                {'INFO'}, 'Quick GLB Export processing')
            bpy.context.window.cursor_set("WAIT")
            loading = True
            main_gltf(self, context)
            bpy.context.window.cursor_set("DEFAULT")
            loading = False
            return {'FINISHED'}
        except Exception as e:
            print("Something went wrong")
            self.report({'ERROR'}, 'Something went wrong')
            # raise the exception again
            raise e


class BakeCamera(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Camera Bake Export"
    # bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            self.report(
                {'INFO'}, '----- ----- ----- GLTF Scripts ----- ----- -----')
            self.report({'INFO'}, 'Camera Bake processing')
            bpy.ops.ed.undo_push(message="Camera Bake")
            main(self, context)
            bpy.ops.ed.undo()

            return {'FINISHED'}
        except Exception as e:
            print("Something went wrong")
            self.report({'ERROR'}, 'Something went wrong')
            # raise the exception again
            raise e


class WMConfig(bpy.types.Operator):
    bl_idname = "object.use_wm_config"
    bl_label = "Use last gltf export config"

    def execute(self, context):
        bpy.ops.export_scene.gltf()
        return {'FINISHED'}


class GLTF_PT_Panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = 'GLTF Export'
    bl_idname = "GLTF_PT_Panel"
    bl_label = "Quick GLTF Export"

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        wm = bpy.types.WindowManager
        props = wm.operator_properties_last("export_scene.gltf")

        row = layout.row()
        label = "Advanced mode ON" if context.scene.advanced_mode else "Advanced mode OFF"
        row.prop(context.scene, 'advanced_mode', text=label, toggle=True)
        col = layout.column()

        box = layout.box()
        col = box.column()
        row = col.row()

        if context.scene.advanced_mode:
            if props:
                if scn.show_options_01:
                    row.prop(scn, "show_options_01",
                             icon="DOWNARROW_HLT", text="", emboss=False)
                else:
                    row.prop(scn, "show_options_01",
                             icon="RIGHTARROW", text="", emboss=False)

                row.label(text='Configuration')
                if scn.show_options_01:
                    for k, v in props.items():
                        col.label(text=k + ': ' + str(v))
        else:
            col.prop(context.scene, 'dir_path')
            col.prop(context.scene, 'filename_path')
            col.prop(context.scene, 'draco')
            col.prop(context.scene, 'draco_level')

        col2 = layout.column(align=True)
        if context.scene.advanced_mode and not props.items():
            col.label(
                text='-export once required-', icon='GHOST_DISABLED')
        else:
            col2.prop(context.scene, 'unlit')
            col2.prop(context.scene, 'instance')

            layout.operator('object.simple_operator',
                            icon='VIEW_CAMERA', depress=loading)
            layout.operator('object.simple_gltf',
                            icon='SORTTIME' if loading else 'SHADERFX', depress=loading)


blender_classes = [
    BakeCamera,
    SimpleGLTF,
    GLTF_PT_Panel,
    WMConfig


]


def register():
    bpy.types.Scene.show_options_01 = bpy.props.BoolProperty(
        name='Show advanced panel', default=True)

    bpy.types.Scene.dir_path = bpy.props.StringProperty(
        name="Path",
        default="",
        description="Define the glb path of the project",
        subtype='DIR_PATH'
    )
    bpy.types.Scene.filename_path = bpy.props.StringProperty(
        name="Name",
        default="",
        description="Define the filename of the exported glb",
    )
    bpy.types.Scene.draco = bpy.props.BoolProperty(
        name="Use Draco Compression",
        description="Use Draco Compression",
        default=False
    )
    bpy.types.Scene.advanced_mode = bpy.props.BoolProperty(
        name="Use Advance mode",
        description="Advanced mode",
        default=False
    )
    bpy.types.Scene.gltf_sys = bpy.props.BoolProperty(
        name="Use Last GLTF Config",
        description="Use the last GLTF config of blender",
        default=False
    )
    bpy.types.Scene.draco_level = bpy.props.IntProperty(
        name="Compression level",
        description="Draco compression level",
        default=10,
        min=0,
        max=10
    )
    bpy.types.Scene.unlit = bpy.props.BoolProperty(
        name="Use KHR Unlit",
        description="Convert materials from metal/rough to unlit",
        default=False
    )
    bpy.types.Scene.instance = bpy.props.BoolProperty(
        name="Use EXT_mesh_gpu_instancing",
        description="Create GPU instances from shared Mesh references ",
        default=False
    )

    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)


def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)
    del bpy.types.Scene.dir_path
    del bpy.types.Scene.filename_path
    del bpy.types.Scene.draco
    del bpy.types.Scene.draco_level
    del bpy.types.Scene.unlit
    del bpy.types.Scene.instance
    del bpy.types.Scene.gltf_sys
