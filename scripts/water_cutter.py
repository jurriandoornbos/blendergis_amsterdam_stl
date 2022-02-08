import bpy

wateritems = bpy.data.collections["Water"].all_objects.items()

tots = len(wateritems)
i=1


obj = bpy.context.active_object

for i in range(10):
    item = wateritems[i]
    mod = obj.modifiers.new("diff", 'BOOLEAN')
    mod.object = bpy.data.objects[item[0]]
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'

    bpy.ops.object.modifier_apply({"object":obj}, modifier=mod.name)

    print(item[0] +  " - Done I got " + str(i) + "/" + str(tots) + "to go")
    
    i+=1

3
