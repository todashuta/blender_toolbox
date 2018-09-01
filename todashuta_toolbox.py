import bpy
from mathutils import Vector


bl_info = {
    "name": "todashuta_toolbox",
    "author": "todashuta",
    "version": (1, 0, 0),
    "blender": (2, 60, 0),
    "location": "command menu (spacebar)",
    "description": "todashuta_toolbox",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}


class XYZDistanceToBoundBoxCenter(bpy.types.Operator):
    """todashuta_toolbox XYZ Distance To Bounding Box Center"""
    bl_idname = "object.todashuta_toolbox_xyz_distance_to_boundbox_center"
    bl_label = "xyzDistanceToBoundBoxCenter"

    def execute(self, context):
        # 参考:
        # https://blenderartists.org/t/calculating-bounding-box-center-coordinates/546894/2
        # https://blender.stackexchange.com/questions/717/is-it-possible-to-print-to-the-report-window-in-the-info-view
        # https://blender.stackexchange.com/questions/6155/how-to-convert-coordinates-from-vertex-to-world-space

        active_object = bpy.context.active_object
        center = sum((active_object.matrix_world * Vector(v) for v in active_object.bound_box), Vector())
        center /= 8

        # center - bpy.context.scene.cursor_location
        # bpy.context.scene.cursor_location - center

        diff = center - bpy.context.scene.cursor_location
        s = "X: {0:.3f},  Y: {1:.3f},  Z: {2:.3f}".format(*[abs(x) for x in diff])
        self.report({'INFO'}, s)
        return {'FINISHED'}


class TranslatedUI_toggle(bpy.types.Operator):
    # 参考:
    # https://blender.jp/modules/newbb/index.php?post_id=7549

    """Toggle Translated UI"""
    bl_idname = "object.todashuta_toolbox_translatedui_toggle"
    bl_label = "Toggle Translated UI"

    def execute(self, context):

        if not bpy.context.user_preferences.system.use_international_fonts:
            self.report({'WARNING'}, "[todashuta_toolbox] ローカライズを有効にしてください")
            return {'CANCELLED'}

        b = bpy.context.user_preferences.system.use_translate_interface
        bpy.context.user_preferences.system.use_translate_interface = not b
        return {'FINISHED'}


class TranslatedTooltips_toggle(bpy.types.Operator):
    """Toggle Translated Tooltips"""
    bl_idname = "object.todashuta_toolbox_translatedtooltips_toggle"
    bl_label = "Toggle Translated Tooltips"

    def execute(self, context):

        if not bpy.context.user_preferences.system.use_international_fonts:
            self.report({'WARNING'}, "[todashuta_toolbox] ローカライズを有効にしてください")
            return {'CANCELLED'}

        b = bpy.context.user_preferences.system.use_translate_tooltips
        bpy.context.user_preferences.system.use_translate_tooltips = not b
        return {'FINISHED'}


def register():
    bpy.utils.register_class(XYZDistanceToBoundBoxCenter)
    bpy.utils.register_class(TranslatedUI_toggle)
    bpy.utils.register_class(TranslatedTooltips_toggle)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Window", space_type="EMPTY")
        kmi = km.keymap_items.new('object.todashuta_toolbox_translatedui_toggle', 'PAUSE', 'PRESS')


def unregister():
    bpy.utils.unregister_class(XYZDistanceToBoundBoxCenter)
    bpy.utils.unregister_class(TranslatedUI_toggle)
    bpy.utils.unregister_class(TranslatedTooltips_toggle)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps["Window"]
        for kmi in km.keymap_items:
            if kmi.idname == 'object.todashuta_toolbox_translatedui_toggle':
                km.keymap_items.remove(kmi)
                break


if __name__ == "__main__":
    register()
