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

# Imports
import bpy

if locals().get("prefs") is not None:
    from imp import reload
    reload(prefs)
    reload(refresh)
    reload(save_reload)
    reload(timeline_extra_info)
    reload(frame_current)
    reload(node_editor)
    reload(border_camera)
    reload(meshlights)
    reload(passepartout)
    reload(stats)
    reload(only_render)
    reload(unsimplify)
    reload(utils)
else:
    from . import prefs, utils
    from .scene import refresh, save_reload, current_blend, stats
    from .animation import timeline_extra_info, frame_current
    from . import node_editor
    from .render import border_camera, meshlights, passepartout, only_render, unsimplify

# Addon info
bl_info = {
    "name": "Amaranth Toolset",
    "author": "Pablo Vazquez, Bassam Kurdali, Sergey Sharybin, Lukas Tönne",
    "version": (0, 9, 6),
    "blender": (2, 71),
    "location": "Everywhere!",
    "description": "A collection of tools and settings to improve productivity",
    "warning": "",
    "wiki_url": "http://pablovazquez.org/amaranth",
    "tracker_url": "",
    "category": "Scene"}

# Registration

classes = (prefs.AmaranthToolsetPreferences,
           refresh.AMTH_SCENE_OT_refresh,
           save_reload.AMTH_WM_OT_save_reload,
           node_editor.templates.AMTH_NODE_MT_amaranth_templates,
           node_editor.templates.AMTH_NODE_OT_AddTemplateVectorBlur,
           node_editor.templates.AMTH_NODE_OT_AddTemplateVignette,
           current_blend.AMTH_FILE_OT_directory_current_blend,
           node_editor.id_panel.AMTH_NODE_PT_indices,
           border_camera.AMTH_VIEW3D_OT_render_border_camera,
           meshlights.AMTH_OBJECT_OT_select_meshlights,
           only_render.AMTH_VIEW3D_OT_show_only_render,
           )

widgets = {
    "VIEW3D_MT_object_specials": (refresh.button,
                                  border_camera.button,
                                  passepartout.button,
                                  frame_current.button
                                  ),
    "VIEW3D_MT_pose_specials": (frame_current.button, ),
    "INFO_MT_file": (save_reload.button, ),
    "TIME_HT_header": (timeline_extra_info.label, ),
    "INFO_HT_header": (stats.label, ),
    "NODE_HT_header": (node_editor.templates.pulldown, ),
    "FILEBROWSER_HT_header": (current_blend.button, ),
    "VIEW3D_MT_select_object": (meshlights.button, ),
    "CyclesScene_PT_simplify": (unsimplify.checkbox, ),
    "SCENE_PT_simplify": (unsimplify.checkbox, ),
}

addon_keymaps = []  # [(keymap, [keymap_item, ...]), ...]


def register():
    # register panels
    unsimplify.register()
    for c in classes:
        bpy.utils.register_class(c)

    # register widgets
    for k, ws in widgets.items():
        for w in ws:
            if "cycles" in k.lower() and not utils.cycles_exists():
                continue
            getattr(bpy.types, k).append(w)

    # register hotkeys
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window')
        items = list()
        items.append(km.keymap_items.new(
            'scene.refresh', 'F5', 'PRESS', shift=False, ctrl=False))
        items.append(km.keymap_items.new(
            'wm.save_reload', 'W', 'PRESS', shift=True, ctrl=True))
        addon_keymaps.append((km, items))

        km = kc.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
        kmi.properties.name = "AMTH_NODE_MT_amaranth_templates"
        addon_keymaps.append((km, [kmi]))

        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            'view3d.show_only_render', 'Z', 'PRESS', shift=True, alt=True)
        addon_keymaps.append((km, [kmi]))


def unregister():
    # unregister panels
    unsimplify.unregister()
    for c in classes:
        bpy.utils.unregister_class(c)

    # unregister widgets
    for k, ws in widgets.items():
        for w in ws:
            if "cycles" in k.lower() and not utils.cycles_exists():
                continue
            getattr(bpy.types, k).remove(w)

    # unregister hotkeys
    for km, items in addon_keymaps:
        for kmi in items:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
