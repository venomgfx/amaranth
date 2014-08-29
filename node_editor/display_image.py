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

# FEATURE: Display Active Image Node on Image Editor
# Made by Sergey Sharybin, tweaks from Bassam Kurdali
image_nodes = {"CompositorNodeImage",
               "CompositorNodeViewer",
               "CompositorNodeComposite",
               "ShaderNodeTexImage",
               "ShaderNodeTexEnvironment"}


class AMTH_NODE_OT_show_active_node_image(bpy.types.Operator):

    """Show active image node image in the image editor"""
    bl_idname = "node.show_active_node_image"
    bl_label = "Show Active Node Node"
    bl_options = {'UNDO'}

    def execute(self, context):
        preferences = context.user_preferences.addons["amaranth"].preferences
        if preferences.use_image_node_display:
            if context.active_node:
                active_node = context.active_node

                if active_node.bl_idname in image_nodes:
                    for area in context.screen.areas:
                        if area.type == "IMAGE_EDITOR":
                            for space in area.spaces:
                                if space.type == "IMAGE_EDITOR":
                                    if active_node.bl_idname == 'CompositorNodeViewer':
                                        space.image = bpy.data.images[
                                            'Viewer Node']
                                    elif active_node.bl_idname == 'CompositorNodeComposite':
                                        space.image = bpy.data.images[
                                            'Render Result']
                                    elif active_node.image:
                                        space.image = active_node.image
                            break

        return {'FINISHED'}
# // FEATURE: Display Active Image Node on Image Editor
