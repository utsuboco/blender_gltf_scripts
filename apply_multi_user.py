import bpy

def applyModifierToMultiUser(self, context):
    active = bpy.context.selected_objects[0]
    
    if (active == None):
        print("Select an object")
        return
    if (active.type != "MESH"):
        print("Select an mesh object")
        return
    

    mesh = active.to_mesh(preserve_all_data_layers=False, depsgraph=None)

    linked = []
    selected = []
    
    print(mesh)
    
    for obj in bpy.data.objects:
        if obj.data == active.data:
                linked.append(obj)
    

    bpy.ops.object.make_single_user(object=True, obdata=True, material=False)
    bpy.ops.object.modifier_apply(modifier="Decimate")


    for obj in linked:
        obj.select_set(state=True)
        obj.modifiers.clear()
    

    bpy.ops.object.make_links_data(type='OBDATA')
        
