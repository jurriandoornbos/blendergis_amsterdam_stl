import bpy


base_tiles = bpy.data.collections["bir_grid"].all_objects.items()

alfabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
"o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "aa", "bb", "cc", "dd", "ee", "ff"]

num = 1
ctr = 0
s = 70

for i in range(len(base_tiles)):

    if num >28:
        
        num = 1
        ctr+=1

       
    letter = alfabet[ctr]
    id = letter + str(num)
    item = base_tiles[i][0]
    obj = bpy.data.objects.get(item)
    bpy.ops.object.text_add()
    ob=bpy.context.object
    ob.data.body = id
    ob.data.size = s
    ob.location[0] = obj.location[0]
    ob.location[1] = obj.location[1]
    ob.location[2] = -16
    ob.data.extrude = 1.5
    ob.rotation_euler[1] = 3.14159
    
    ob.name = id
    num+=1
    
    #1 Convert to mesh
    bpy.ops.object.convert(target="MESH")
    
    #2 boolean difference with obj (bir_grid) using ob (text) as tool
    mod = obj.modifiers.new("diff", 'BOOLEAN')
    mod.object = ob
    mod.operation = 'UNION'
    mod.solver = 'FAST'

    bpy.ops.object.modifier_apply({"object":obj}, modifier=mod.name)
    print("done with: " + str(i))
    