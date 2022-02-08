import bpy
import os

workdir = os.path.join("C:\\","Users","Jurrian","Documents","3d_printing_locations", "amsterdam", "raw_data", "3dbag_v2")

files = os.listdir(workdir)

obj_list = [item for item in files if item.endswith(".obj")]

collection_name = "3dbag_v2"


for obj in obj_list:
    path_to_file = os.path.join(workdir, obj)
    bpy.context.view_layer.objects.active = None
    
    bpy.ops.import_scene.obj(filepath = path_to_file, split_mode = "OFF", use_image_search = False, axis_forward =  "Y", axis_up = "Z" )
    
    for ob in bpy.context.selected_objects:
        ob.location[0] = -121649
        ob.location[1] = -485653 
        ob.location[2] = 0
        bpy.data.collections[collection_name].objects.link(ob)
        bpy.context.scene.collection.objects.unlink(ob)