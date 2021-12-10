import bpy

def apply_all_modifier(self, context):
    is_select, is_mod = False, False
    message_a, message_b = "", ""
    # collect names for objects failed to apply modifiers
    collect_names = []

    for obj in bpy.context.selected_objects:
        is_select = True

        # copying context for the operator's override
        contx = bpy.context.copy()
        contx['object'] = obj

        for mod in obj.modifiers[:]:
            contx['modifier'] = mod
            is_mod = True
            try:
                bpy.ops.object.modifier_apply(
                                    contx,
                                    modifier=contx['modifier'].name
                                    )
            except:
                obj_name = getattr(obj, "name", "NO NAME")
                collect_names.append(obj_name)
                message_b = True
                pass

    if is_select:
        if is_mod:
            message_a = "Applying modifiers on all Selected Objects"
        else:
            message_a = "No Modifiers on Selected Objects"
    else:
        self.report({"INFO"}, "No Selection. No changes applied")
        return {'CANCELLED'}

    # applying failed for some objects, show report
    message_obj = (",".join(collect_names) if collect_names and
                    len(collect_names) < 8 else "some objects (Check System Console)")

    self.report({"INFO"},
                (message_a if not message_b else
                "Applying modifiers failed for {}".format(message_obj)))

    if (collect_names and message_obj == "some objects (Check System Console)"):
        print("\n[Modifier Tools]\n\nApplying failed on:"
                "\n\n{} \n".format(", ".join(collect_names)))

    return {'FINISHED'}

