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


class NoOperation(bpy.types.Operator):
    bl_idname = "object.no_operation"
    bl_label = "NOOP"
    bl_description = "Do Nothing"

    def execute(self, context):
        return {"FINISHED"}


class Reset2DCursor(bpy.types.Operator):
    bl_idname = "object.reset_2d_cursor"
    bl_label = "Reset 2D Cursor"
    bl_description = "Reset 2D Cursor"

    def execute(self, context):
        bpy.ops.uv.cursor_set(location=(0.0, 0.0))
        return {'FINISHED'}


class XYZDistanceToBoundBoxCenter(bpy.types.Operator):
    """todashuta_toolbox XYZ Distance To Bounding Box Center"""
    bl_idname = "object.todashuta_toolbox_xyz_distance_to_boundbox_center"
    bl_label = "xyzDistanceToBoundBoxCenter"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len([o for o in context.scene.objects if o.select]) == 1

    def execute(self, context):
        # 参考:
        # https://blenderartists.org/t/calculating-bounding-box-center-coordinates/546894/2
        # https://blender.stackexchange.com/questions/717/is-it-possible-to-print-to-the-report-window-in-the-info-view
        # https://blender.stackexchange.com/questions/6155/how-to-convert-coordinates-from-vertex-to-world-space

        active_object = context.active_object
        center = sum((active_object.matrix_world * Vector(v) for v in active_object.bound_box), Vector())
        center /= 8

        # center - bpy.context.scene.cursor_location
        # bpy.context.scene.cursor_location - center

        diff = center - context.scene.cursor_location
        s = "X: {0:.3f},  Y: {1:.3f},  Z: {2:.3f}".format(*[abs(x) for x in diff])
        self.report({'INFO'}, s)
        return {'FINISHED'}


class ToggleTranslatedUI(bpy.types.Operator):
    # 参考:
    # https://blender.jp/modules/newbb/index.php?post_id=7549

    """Toggle Translated UI"""
    bl_idname = "object.todashuta_toolbox_toggle_translated_ui"
    bl_label = "Toggle Translated UI"

    @classmethod
    def poll(cls, context):
        return context.user_preferences.system.use_international_fonts

    def execute(self, context):
        context.user_preferences.system.use_translate_interface ^= 1
        return {'FINISHED'}


class ToggleTranslatedTooltips(bpy.types.Operator):
    """Toggle Translated Tooltips"""
    bl_idname = "object.todashuta_toolbox_toggle_translated_tooltips"
    bl_label = "Toggle Translated Tooltips"

    @classmethod
    def poll(cls, context):
        return context.user_preferences.system.use_international_fonts

    def execute(self, context):
        context.user_preferences.system.use_translate_tooltips ^= 1
        return {'FINISHED'}


class ToggleMyKeymaps(bpy.types.Operator):
    """Toggle My Keymaps"""
    bl_idname = "object.todashuta_toolbox_toggle_mykeymaps"
    bl_label = "Toggle My Keymaps"

    def execute(self, context):
        if enabled_my_keymaps():
            disable_my_keymaps()
            self.report({'INFO'}, "my keymaps are disabled")
        else:
            enable_my_keymaps()
            self.report({'INFO'}, "my keymaps are enabled")
        return {'FINISHED'}


class CustomMenu(bpy.types.Panel):
    bl_label = "todashuta toolbox"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator(ToggleTranslatedUI.bl_idname, text=ToggleTranslatedUI.bl_label)
        layout.operator(ToggleTranslatedTooltips.bl_idname, text=ToggleTranslatedTooltips.bl_label)
        layout.operator(ToggleMyKeymaps.bl_idname, text=ToggleMyKeymaps.bl_label)
        layout.operator(XYZDistanceToBoundBoxCenter.bl_idname, text=XYZDistanceToBoundBoxCenter.bl_label)


def kmi_props_setattr(kmi_props, attr, value):
    try:
        setattr(kmi_props, attr, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (attr, kmi_props.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)


addon_keymaps = []


def enabled_my_keymaps():
    return len(addon_keymaps) > 0


def enable_my_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    if not kc:
        return

    # PauseキーでToggle Translated UI
    km = kc.keymaps.new(name="Window", space_type="EMPTY")
    kmi = km.keymap_items.new(ToggleTranslatedUI.bl_idname, 'PAUSE', 'PRESS')
    addon_keymaps.append((km, kmi))

    # QでxyzDistanceToBoundBoxCenter
    km = kc.keymaps.new("3D View", space_type="VIEW_3D", region_type="WINDOW", modal=False)
    kmi = km.keymap_items.new(XYZDistanceToBoundBoxCenter.bl_idname, 'Q', 'PRESS')
    addon_keymaps.append((km, kmi))

    # 3Dカーソルの移動を Alt-左クリック に変更する
    #km = kc.keymaps.new("3D View", space_type="VIEW_3D", region_type="WINDOW", modal=False)
    #kmi = km.keymap_items.new('view3d.cursor3d', 'ACTIONMOUSE', 'PRESS', alt=True)
    #addon_keymaps.append((km, kmi))

    # 左クリック操作を無効化する
    #km = kc.keymaps.new("3D View", space_type="VIEW_3D", region_type="WINDOW", modal=False)
    #kmi = km.keymap_items.new(NoOperation.bl_idname, 'ACTIONMOUSE', 'PRESS')
    #addon_keymaps.append((km, kmi))

    # ビューの回転を Shift-中ボタン に変更する
    #km = kc.keymaps.new("3D View", space_type="VIEW_3D", region_type="WINDOW", modal=False)
    #kmi = km.keymap_items.new('view3d.rotate', 'MIDDLEMOUSE', 'PRESS', shift=True)
    #addon_keymaps.append((km, kmi))

    # ビューのパンを 中ボタン に変更する (Shift押下不要にする)
    #km = kc.keymaps.new("3D View", space_type="VIEW_3D", region_type="WINDOW", modal=False)
    #kmi = km.keymap_items.new('view3d.move', 'MIDDLEMOUSE', 'PRESS')
    #addon_keymaps.append((km, kmi))

    # UV Editor の2Dカーソル移動を Alt+左クリック に変更する
    #km = kc.keymaps.new('UV Editor', space_type='EMPTY', region_type='WINDOW', modal=False)
    #kmi = km.keymap_items.new('uv.cursor_set', 'ACTIONMOUSE', 'PRESS', alt=True)
    #addon_keymaps.append((km, kmi))

    # UV Editor の左クリック操作を 色を採取 に変更する
    #km = kc.keymaps.new('UV Editor', space_type='EMPTY', region_type='WINDOW', modal=False)
    #kmi = km.keymap_items.new('image.sample', 'ACTIONMOUSE', 'PRESS')
    #addon_keymaps.append((km, kmi))

    # Shift-C で UV Editor の2Dカーソルをリセットする
    km = kc.keymaps.new('UV Editor', space_type='EMPTY', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new(Reset2DCursor.bl_idname, 'C', 'PRESS', shift=True)
    addon_keymaps.append((km, kmi))

    # 選択のCの操作をCを押してる間だけ有効にする
    #km = kc.keymaps.new('View3D Gesture Circle', space_type='EMPTY', region_type='WINDOW', modal=True)
    #kmi = km.keymap_items.new_modal('CANCEL', 'C', 'RELEASE')
    #addon_keymaps.append((km, kmi))

    # 選択のBの操作をCを押してる間だけ有効にする
    #km = kc.keymaps.new('Gesture Border', space_type='EMPTY', region_type='WINDOW', modal=True)
    #kmi = km.keymap_items.new_modal('CANCEL', 'B', 'RELEASE')
    #addon_keymaps.append((km, kmi))

    # Console Ctrl-A 行頭
    km = kc.keymaps.new('Console', space_type='CONSOLE', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('console.move', 'A', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'type', 'LINE_BEGIN')
    addon_keymaps.append((km, kmi))
    # Console Ctrl-E 行頭
    km = kc.keymaps.new('Console', space_type='CONSOLE', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('console.move', 'E', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'type', 'LINE_END')
    addon_keymaps.append((km, kmi))
    # Console Ctrl-B 前の文字
    km = kc.keymaps.new('Console', space_type='CONSOLE', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('console.move', 'B', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'type', 'PREVIOUS_CHARACTER')
    addon_keymaps.append((km, kmi))
    # Console Ctrl-F 次の文字
    km = kc.keymaps.new('Console', space_type='CONSOLE', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('console.move', 'F', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'type', 'NEXT_CHARACTER')
    addon_keymaps.append((km, kmi))
    # Console Ctrl-H 前の文字を削除
    km = kc.keymaps.new('Console', space_type='CONSOLE', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('console.delete', 'H', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'type', 'PREVIOUS_CHARACTER')
    addon_keymaps.append((km, kmi))
    # Console Ctrl-U 行をクリア
    km = kc.keymaps.new('Console', space_type='CONSOLE', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('console.clear_line', 'U', 'PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))
    # Console Ctrl-P 履歴(一つ前)
    km = kc.keymaps.new('Console', space_type='CONSOLE', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('console.history_cycle', 'P', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'reverse', True)
    addon_keymaps.append((km, kmi))
    # Console Ctrl-N 履歴(一つ次)
    km = kc.keymaps.new('Console', space_type='CONSOLE', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('console.history_cycle', 'N', 'PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))


def disable_my_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def register():
    bpy.utils.register_module(__name__)
    enable_my_keymaps()


def unregister():
    bpy.utils.unregister_module(__name__)
    disable_my_keymaps()


if __name__ == "__main__":
    register()
