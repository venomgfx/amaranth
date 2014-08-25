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


class Refresh(bpy.types.Operator):

    """Refresh the current scene"""
    bl_idname = "scene.refresh"
    bl_label = "Refresh!"

    def execute(self, context):
        preferences = context.user_preferences.addons["amaranth"].preferences
        scene = context.scene

        if preferences.use_scene_refresh:
            # Changing the frame is usually the best way to go
            scene.frame_current = scene.frame_current
            self.report({"INFO"}, "Scene Refreshed!")

        return {'FINISHED'}


def button(self, context):
    preferences = context.user_preferences.addons["amaranth"].preferences

    if preferences.use_scene_refresh:
        self.layout.separator()
        self.layout.operator(Refresh.bl_idname,
                             text="Refresh!",
                             icon='FILE_REFRESH')
