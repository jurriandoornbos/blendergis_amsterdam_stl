import bpy
import  os

workdir = os.path.join("C:\\","Users","Jurrian","Documents","3d_printing_locations", "amsterdam", "raw_data", "blender_in", "weg")

files = os.listdir(workdir)

shp_list = [item for item in files if item.endswith(".shp")]

namelist = []

for shp in shp_list[0:10]:
    file = os.path.join(workdir, shp)
    bpy.ops.importgis.shapefile(filepath=file, shpCRS="EPSG:28992",
    fieldExtrudeName="extrusion", 
    extrusionAxis='Z')
    
    obj = bpy.context.active_object
    
    bpy.data.collections['Collection 6'].objects.link(obj)
    
    