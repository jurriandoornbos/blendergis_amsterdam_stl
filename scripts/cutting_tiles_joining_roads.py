import bpy

base_tiles = bpy.data.collections["bir_grid"].all_objects.items()

#road_tiles = bpy.data.collections["bir_weg_600"].all_objects.items()
#road_l = [e for l in road_tiles for e in l]
water_tiles= bpy.data.collections["water_fixed_600"].all_objects.items()
water_l = [e for l in water_tiles for e in l]


j = len(base_tiles)
fails = [543, 544]
for i in fails:
    item = base_tiles[i][0]
    obj = bpy.data.objects.get(item)
    #bpy.context.view_layer.objects.active =ob
    
    #obj = bpy.context.active_object
    water = item+".002"
    if water in water_l:
        
    
        diff = obj.modifiers.new("diff", 'BOOLEAN')
        diff.object = bpy.data.objects[water]
        diff.operation = 'DIFFERENCE'
        diff.solver = 'EXACT'
        diff.use_hole_tolerant = True
        #diff.use_self = True

        bpy.ops.object.modifier_apply({"object":obj}, modifier=diff.name)
        
        print(water +  " - Done I got " + str(i) + "/" + str(j) + "to go")
        
    else:
        pass
    '''
    road = item+".002"
        
    if road in road_l:
        
    
        un = obj.modifiers.new("join", 'BOOLEAN')
        un.object = bpy.data.objects[road]
        un.operation = 'UNION'
        un.solver = 'EXACT'
        un.use_hole_tolerant = True
        un.use_self = True

        bpy.ops.object.modifier_apply({"object":obj}, modifier=un.name)
        print(road +  " - Done I got " + str(i) + "/" + str(j) + "to go")
    else:
        pass
    '''
    
    



