"""
Joe Howes' Conway's Life Generator
Official website: http://josephhowes.com/
Author: Joe Howes (rjak) joeh@foldingrain.com
Licence: you can modify and reditribute this file as you wish.
"""

import bpy

from .goldriver import GOLDriver

bl_info = {
    "name": "Conway's Life Generator",
    "author": "Joe Howes (rjak)",
    "version": (0,9,1),
    "blender": (2, 7, 0),
    #"api": 45996,
    #"location": "View3D > Tool Shelf > 3D Nav",
    "description": "Generates a Game of Life simulation.",
    "category": "Object"}

class ObjectGenerateConwayLife(bpy.types.Operator):
    """Conway's Life Generator"""
    bl_idname = "object.conway_life"
    bl_label = "Generate Conway's Life"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        driver = GOLDriver()
        driver.go()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ObjectGenerateConwayLife)

def unregister():
    bpy.utils.unregister_class(ObjectGenerateConwayLife)

if __name__ == "__main__":
    register()
