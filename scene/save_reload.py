#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import bpy


class AMTH_WM_OT_save_reload(bpy.types.Operator):

    """Save and Reload the current blend file"""
    bl_idname = "wm.save_reload"
    bl_label = "Save & Reload"

    def save_reload(self, context, path):
        if not path:
            bpy.ops.wm.save_as_mainfile("INVOKE_AREA")
            return
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
            AMTH_WM_OT_save_reload.bl_idname,
            text="Save & Reload",
            icon='FILE_REFRESH')
