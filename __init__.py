import bpy
import json
import os
from os.path import expanduser, splitext, split

bl_info = {
    "name": "Collect Material IDs",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0),
    "author": "Hierosoft LLC",
    "description": "Collects and saves material IDs for objects containing a search term in their name.",
}

class MaterialIDCollector(bpy.types.Operator):
    bl_idname = "object.collect_mat_ids"
    bl_label = "Collect Material IDs"

    def execute(self, context):
        ids_path = expanduser(context.scene.mat_id_path)
        known_mat_ids = {}

        # Load existing material IDs if file exists
        if os.path.exists(ids_path):
            with open(ids_path, 'r') as file:
                try:
                    known_mat_ids = json.load(file)
                except json.JSONDecodeError:
                    self.report({'WARNING'}, f"Failed to parse {ids_path}, starting with an empty dictionary.")

        # Iterate through objects in the scene
                # Set initial error and found status
        error = None
        found = False

        for obj in context.scene.objects:
            if context.scene.obj_name_filter.lower() in obj.name.lower():
                suffix = None
                if found:
                    error = "More than one object matches"
                    suffix = ".{}".format(obj.name)
                found = True
                self.collect_mat_ids(obj, known_mat_ids, ids_path, suffix=suffix)

        # Save updated material IDs back to file
        with open(ids_path, 'w') as file:
            json.dump(known_mat_ids, file, indent=4)

        if not found:
            error = "Object with '{}' in name not found".format(context.scene.obj_name_filter)

        if error:
            self.report({'ERROR'}, error)
        else:
            self.report({'INFO'}, f"Material IDs saved to {ids_path}")
        return {'FINISHED'}

    def collect_mat_ids(self, obj, known_mat_ids, ids_path, suffix=None):
        if obj.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        filename = bpy.data.filepath if bpy.data.filepath else ids_path
        cache_key = splitext(split(filename)[1])[0]
        if suffix:
            cache_key += suffix
        known_mat_ids.setdefault(cache_key, {})

        # Collect material indices
        for index, mat_slot in enumerate(obj.material_slots):
            if mat_slot.material:
                material_name = mat_slot.material.name
                known_mat_ids[cache_key][material_name] = index

class MaterialIDPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_collect_mat_ids"
    bl_label = "Material ID Collector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Material IDs'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "mat_id_path")
        layout.prop(context.scene, "obj_name_filter")
        layout.operator(MaterialIDCollector.bl_idname)

# Register property for file path configuration
bpy.types.Scene.obj_name_filter = bpy.props.StringProperty(
        name="Object Name Filter",
        description="Filter for object names to include in material ID collection",
        default="body"
    )

def register():
    bpy.utils.register_class(MaterialIDCollector)
    bpy.utils.register_class(MaterialIDPanel)
    bpy.types.Scene.mat_id_path = bpy.props.StringProperty(
        name="Material ID Path",
        description="Path to save material IDs",
        default="~/mat_ids.json",
        subtype='FILE_PATH'
    )


def unregister():
    bpy.utils.unregister_class(MaterialIDCollector)
    bpy.utils.unregister_class(MaterialIDPanel)
    del bpy.types.Scene.mat_id_path


if __name__ == "__main__":
    register()
