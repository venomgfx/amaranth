import bpy


class Save_reload(bpy.types.Operator):

    """Save and Reload the current blend file"""
    bl_idname = "wm.save_reload"
    bl_label = "Save & Reload"

    def save_reload(self, context, path):
        if not path:
            bpy.ops.wm.save_as_mainfile("INVOKE_AREA")
        else:
            bpy.ops.wm.save_mainfile()
        bpy.ops.wm.open_mainfile("EXEC_DEFAULT", filepath=path)
        self.report({'INFO'}, "Saved & Reloaded")

    def execute(self, context):
        path = bpy.data.filepath
        self.save_reload(context, path)
        return {'FINISHED'}


def button(self, context):
    preferences = context.user_preferences.addons["amaranth"].preferences

    if preferences.use_file_save_reload:
        self.layout.separator()
        self.layout.operator(
            Save_reload.bl_idname,
            text="Save & Reload",
            icon='FILE_REFRESH')
