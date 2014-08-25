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
else:
    from . import prefs
    from .scene import refresh, save_reload
    from .animation import timeline_extra_info, frame_current

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

modules = ("prefs",
           "refresh",
           "save_reload",
           )

addon_keymaps = []  # [(keymap, [keymap_item, ...]), ...]


# Registration
def register():
    for m in modules:
        if not hasattr(globals()[m], m.capitalize()):
            continue
        c = getattr(globals()[m], m.capitalize())
        bpy.utils.register_class(c)

    bpy.types.VIEW3D_MT_object_specials.append(refresh.button)
    bpy.types.VIEW3D_MT_object_specials.append(frame_current.button)
    bpy.types.VIEW3D_MT_pose_specials.append(frame_current.button)
    bpy.types.INFO_MT_file.append(save_reload.button)

    bpy.types.TIME_HT_header.append(timeline_extra_info.label)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window')
        items = list()
        items.append(km.keymap_items.new('scene.refresh', 'F5', 'PRESS',
                                         shift=False, ctrl=False))
        items.append(km.keymap_items.new('wm.save_reload', 'W', 'PRESS',
                                         shift=True, ctrl=True))
        addon_keymaps.append((km, items))


def unregister():
    for m in modules:
        c = getattr(globals()[m], m.capitalize())
        bpy.utils.unregister_class(c)

    bpy.types.VIEW3D_MT_object_specials.remove(refresh.button)
    bpy.types.VIEW3D_MT_object_specials.remove(frame_current.button)
    bpy.types.VIEW3D_MT_pose_specials.remove(frame_current.button)
    bpy.types.INFO_MT_file.remove(save_reload.button)

    bpy.types.TIME_HT_header.remove(timeline_extra_info.label)

    for km, items in addon_keymaps:
        for kmi in items:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
