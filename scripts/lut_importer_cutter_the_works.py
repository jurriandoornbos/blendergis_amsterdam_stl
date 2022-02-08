import bpy
import os
import csv


#function to import the correct .obj files, based on the IDs in a list

def objs_import(ids):

    #2 import the obj files to 3dbag_working dir collection
    #2.1 move them to the correct location
    workdir = os.path.join("C:\\","Users","Jurrian","Documents","3d_printing_locations", "amsterdam", "raw_data", "3dbag_v2")


    files = os.listdir(workdir)
    
    for id in ids:
        
        obj = [item for item in files if item.endswith(str(id)+".obj")][0]
        
        path_to_file = os.path.join(workdir, obj)
        
        bpy.context.view_layer.objects.active = None
        
        bpy.ops.import_scene.obj(filepath = path_to_file, split_mode = "OFF", use_image_search = False, axis_forward =  "Y", axis_up = "Z" )
        
        for ob in bpy.context.selected_objects:
            ob.location[0] = -121649
            ob.location[1] = -485653 
            ob.location[2] = 0
            bpy.data.collections["3dbag_working"].objects.link(ob)
            bpy.context.scene.collection.objects.unlink(ob)


###big section to go down the list from 1:840###
# read CSV file



def csv_parse():
    csv_dir = os.path.join("C:\\","Users","Jurrian","Documents","3d_printing_locations", "amsterdam", "raw_data")

    f = open(os.path.join(csv_dir,"ams_lut.csv"))
    rdr = csv.reader(f, delimiter=';')

    lut = []        
    for ids in rdr:
        sub = []
        
        for id in ids:
            if id == "":
                continue
            
            num = int(id)
            sub.append(num)
            
        lut.append(sub)
    return lut


lut = csv_parse()

i=0
for ids in lut:
    #1 check if the list contains ids (continue)
    id = ids[0]
    bags = ids[1:] 
    print("Working with ID: " + str(id))
    print("Containing tiles: " + str(bags))
        
    if not bags:
        continue
    
    objs_import(bags)
    
    #3 complete join, merge, whatever, these objects into 1 unit
        
    for obj in bpy.data.collections['3dbag_working'].all_objects:
        obj.select_set(True)
    
    bpy.context.view_layer.objects.active = obj
    
    items=bpy.data.collections['3dbag_working'].all_objects.items()
    
    if len(items) != 1:
        bpy.ops.object.join()
        print("### Joined: " + str(items))

    

    
        
    #4 Boolean out this unit based on the cutout/bir_grid ID
    
    diff = obj.modifiers.new("diff", 'BOOLEAN')
    diff.object = bpy.data.objects[str(id)+".003"]
    diff.operation = 'INTERSECT'
    diff.solver = 'EXACT'
    diff.use_hole_tolerant = True
    #diff.use_self = True

    bpy.ops.object.modifier_apply({"object":obj}, modifier=diff.name)
        
    print("### Done with intersection cube + building: " + str(ids) )
        
        
    #5 move it to ams_grid collection and rename it
    bpy.data.collections["ams_grid"].objects.link(obj)
    obj.name = "bag_grid_"+str(id)
    
    #6 reset 3dbag_working
    coll = bpy.data.collections['3dbag_working']
    while coll.objects:
        coll.objects.unlink(coll.objects[0])

    
    #7 clean up work space
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False)
    
    if i == 20:
        bpy.ops.wm.save_mainfile()
        i=0

    
    i+=1
    
        








# start gridded_v3.blend
# join ams_grid to bir_grid
# cut out letters from bir_grid
# cut four square holes from each of the units