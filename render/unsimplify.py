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


def register():
    scene = bpy.types.Scene
    scene.use_unsimplify_render = bpy.props.BoolProperty(
        default=False,
        name="Unsimplify Render",
        description="Disable Simplify during render")
    scene.simplify_status = bpy.props.BoolProperty(default=False)


def unregister():
    wm = bpy.context.window_manager
    for p in ("use_unsimplify_render", "simplify_status"):
        if wm.get(p):
            del wm[p]


@bpy.app.handlers.persistent
def unsimplify_render_pre(scene):
    render = scene.render
    scene.simplify_status = render.use_simplify

    if scene.use_unsimplify_render:
        render.use_simplify = False


@bpy.app.handlers.persistent
def unsimplify_render_post(scene):
    render = scene.render
    render.use_simplify = scene.simplify_status


def checkbox(self, context):
    scene = bpy.context.scene
    self.layout.prop(scene, 'use_unsimplify_render')
