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

if "prefs" in locals():
    import imp
    imp.reload(prefs)
    imp.reload(refresh)
    imp.reload(save_reload)
    imp.reload(timeline_extra_info)
    imp.reload(frame_current)
    imp_reload(node_editor)
else:
    from . import prefs
    from .scene import refresh, save_reload, current_blend
    from .animation import timeline_extra_info, frame_current
    from . import node_editor

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
           )

widgets = {
    "VIEW3D_MT_object_specials": (refresh.button, frame_current.button),
    "VIEW3D_MT_pose_specials": (frame_current.button, ),
    "INFO_MT_file": (save_reload.button, ),
    "TIME_HT_header": (timeline_extra_info.label, ),
    "NODE_HT_header": (node_editor.templates.pulldown, ),
    "FILEBROWSER_HT_header": (current_blend.button, ),
}

addon_keymaps = []  # [(keymap, [keymap_item, ...]), ...]


def register():
    for c in classes:
        bpy.utils.register_class(c)  # register templates

    # register widgets
    for k, ws in widgets.items():
        for w in ws:
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


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)  # unregister templates

    # unregister widgets
    for k, ws in widgets.items():
        for w in ws:
            getattr(bpy.types, k).remove(w)

    # unregister hotkeys
    for km, items in addon_keymaps:
        for kmi in items:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
