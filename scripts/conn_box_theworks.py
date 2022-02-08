import bpy

base_tiles = bpy.data.collections["bir_grid"].all_objects.items()


ctr =0
for i in range(len(base_tiles)):
    item = base_tiles[i][0]
    obj = bpy.data.objects.get(item)

    boxdims = [60, 60, 15]
    x = obj.location[0]
    y = obj.location[1]
    z = obj.location[2]
    h= -21
    bpy.ops.mesh.primitive_cube_add(location=(x-240,y-240,h))
    ob = bpy.context.object
    ob.dimensions = boxdims
    ob.name = "a" + str(i+1)
    mod = obj.modifiers.new("diff", 'BOOLEAN')
    mod.object = ob
    mod.operation = 'UNION'
    mod.solver = 'EXACT'

    bpy.ops.object.modifier_apply({"object":obj}, modifier=mod.name)
    
    bpy.ops.mesh.primitive_cube_add(location=(x+240,y-240,h))
    bpy.context.object.dimensions = boxdims
    ob = bpy.context.object
    ob.dimensions = boxdims
    ob.name = "b" + str(i+1)
    mod = obj.modifiers.new("diff", 'BOOLEAN')
    mod.object = ob
    mod.operation = 'UNION'
    mod.solver = 'EXACT'

    bpy.ops.object.modifier_apply({"object":obj}, modifier=mod.name)
    
    bpy.ops.mesh.primitive_cube_add(location=(x-240,y+240,h))
    bpy.context.object.dimensions = boxdims
    ob = bpy.context.object
    ob.dimensions = boxdims
    ob.name = "c" + str(i+1)
    mod = obj.modifiers.new("diff", 'BOOLEAN')
    mod.object = ob
    mod.operation = 'UNION'
    mod.solver = 'EXACT'

    bpy.ops.object.modifier_apply({"object":obj}, modifier=mod.name)
    
    bpy.ops.mesh.primitive_cube_add(location=(x+240,y+240,h))
    bpy.context.object.dimensions = boxdims
    ob = bpy.context.object
    ob.dimensions = boxdims
    ob.name = "d" + str(i+1)
    mod = obj.modifiers.new("diff", 'BOOLEAN')
    mod.object = ob
    mod.operation = 'UNION'
    mod.solver = 'EXACT'

    bpy.ops.object.modifier_apply({"object":obj}, modifier=mod.name)
    
    if ctr == 20:
        bpy.ops.wm.save_mainfile()
        ctr = 0
        
    ctr+=1
    
    print("Done with " +str(i+1))