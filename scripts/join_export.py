import bpy
import os

base_tiles = bpy.data.collections["bir_grid"].all_objects.items()
ams_tiles = bpy.data.collections["ams_grid"].all_objects.items()

alfabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
"o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "aa", "bb", "cc", "dd", "ee", "ff"]
num =1 
ctr= 0
ams_ctr = 0
for i in range(len(base_tiles)):
    
    if num >28:
        
        num = 1
        ctr+=1
    
    letter = alfabet[ctr]
    id = letter + str(num) 
    fp = workdir = os.path.join("C:\\","Users","Jurrian","Documents","3d_printing_locations", "amsterdam", "stl_out", id+".stl")   
    
    bir_item = base_tiles[i][0]
    bir = bpy.data.objects.get(bir_item)
    
    ams_item = ams_tiles[ams_ctr][0]
    ams = bpy.data.objects.get(ams_item)
    if str(ams_item).endswith(str(i+1)):
    
        ams.select_set(True)
        
        bpy.context.view_layer.objects.active = ams
        bir.select_set(True)
        bpy.context.view_layer.objects.active = bir
        
        bpy.ops.object.join()
        
        print("joined ams + bir: " + str(bir_item) + "  "+ str(ams_item)+" --- " + id)
        ams_ctr+=1
    
   
    
    

        
    else:
        bir.select_set(True)
        
    bpy.ops.export_mesh.stl(filepath=fp, check_existing=False, filter_glob='*.stl', use_selection=True, global_scale=0.15, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OFF', axis_forward='Y', axis_up='Z')
    
    
    bpy.ops.object.select_all(action='DESELECT') 
    print("exported ams + bir: " + str(i+1) + " --- " + id)
    num+=1
    
    
    
    
    