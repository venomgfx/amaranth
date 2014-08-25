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
from . import vectorblur, vignette


# Node Templates Menu
class Templates(bpy.types.Menu):
    bl_idname = 'AMTH_NODE_MT_amaranth_templates'
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Templates"
    bl_description = "List of Amaranth Templates"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            vectorblur.Vectorblur.bl_idname,
            text="Vector Blur",
            icon='FORCE_HARMONIC')
        layout.operator(
            vignette.Vignette.bl_idname,
            text="Vignette",
            icon='COLOR')


def pulldown(self, context):
    if context.space_data.tree_type == 'CompositorNodeTree':
        layout = self.layout
        row = layout.row(align=True)
        row.scale_x = 1.3
        row.menu("AMTH_NODE_MT_amaranth_templates",
                 icon="NODETREE")
