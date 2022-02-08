# Blender GIS used for Amsterdam 3D files

My mess of files and ideas, and some info to get started on printing your own city. This is more usable as a general idea and what problems you need to solve, Do not think this is automated in any way, there is a lot of manual work and thinking required to get everything to work nicelty with eachother.

This deals with how you can get some of the nice data and visualizations to print. I delved more into the Netherlands side of it, because we have lovely data to work with and I know which government data is available. 

The broad idea here is to get your data all nicely aligned to a grid of squares which will fit the printerbed. Then cut the data out to that area, attach it to the square and export as stl's.

This project was a lot more than expected, trying to add cubes to buildings at a small scale is doable, but this was slightly (read, a lot) more effort than initially thought. There were two problems, the first is trying to improve a lot on the exisitng method I created by adding roads and water, which is actaully a big improvement for Amsterdam. The second is using a mahusive dataset. It consists of around 800 tiles, which is a lot. Due to it being a square grid, it increases *2 instead of +2 for each tile in x or y.

However for Amsterdam alone, I have done most of the hard work, here are the 840 stl files of Amsterdam:
[Onedrive Download of .zip file](https://1drv.ms/u/s!AufxGaH9C4-Vgcx30R7lSQ14FjmNdA?e=1tjdWh)
This also contains the map from which to select your preferred tiles, and some simple info on the tiles.


# Other countries 
There is probably better ways to go about this, but I did not research it, and this is probably good enough for some basic prints.

## Pre-requisites
- Install Blender + BlenderGIS (Preferably with GDAL)

# Netherlands
There is a million ways to go about this ofcourse, I present here a few steps to get (for NL): 
You can of course do only a single step of these.

1. Buildings
2. Roads 
3. Water

## Pre-requisites
- Install Blender + BlenderGIS (Preferably with GDAL also installed, see their [Github page](https://github.com/domlysz/BlenderGIS/wiki/Install-and-usage) about that).
- Figure out where the data-files from your government/state/municipality are (they have a LOT of info/data about their areas, so dive into that).

Read up on the projection and geometry of your data, work in a single system, this will make blenderGIS play nice with you.

For the buildings downloading I created a .txt file with all the 3DBAG tiles I wanted, and let python do the work for me, downloading, extracting and only selecting the LOD2.2
    download_bag.py

### theory and executing for Q-GIS
The tiles are made in QGIS with the grid-tool, creating polygons, these polygons will have a value, to extrude in blenderGIS. This grid will chop the water pieces and the roads. 

I used a grid of around 600x600meters, covering most of Amsterdam and adding a few height features, to extrude on later in blenderGIS.

    create grid -> 600x600 meters -> bake a few height values for the thiccness of the tile (15 seems aight for the main tiles, 7 as a filler, 200 for the cutter) -> export as .shp

The water dataset is imported, and intersected with the grid, The individual grid-numbers are then dissolved, creating a water section corresponding to the tile, then I added a new entry on the data-table, with a value of -6, this cut out of the grid in blenderGIS later. Exported the water a .shp files (blenderGIS GeoJSON when?)

    import waterdata -> intersect with grid -> dissolve on grid_id ->  add new feature with -8 -> export as .shp

This oughtta work for roads, but it did not. Internal tesselation in blenderGIS makes some shapes impossible, joining multiple faces together, terrible. 
This requires plan B. Plan B is skipping the dissolve step. and exporting every single road section individually, taking around 36h for the 100k road-features.

    import roads -> fix geometry -> simplify -> intersect with grid -> fix geometry -> add features (poly_id = to_string(@row_number) + '_' to_string(id_2) ; extrude = 7)-> split vector layer (.shp, based on the poly_id name, to folder 'weg')

In the case of the Amsterdam road network, there is a conflict between the grid and the .shp datastructure. multi-shape shapefiles are not supported in BlenderGIS, and any other dataformat will not import correctly, creating terrible results. So this does not really work.

### theory and executing for BlenderGIS

The main goal is to create actual STLs for printing. This requires the tiling process, based on the QGIS-created-grid. I like to save and copy the .blend file every so often, as some changes might make everything fail.

This requires cutting the buildings to the tile-extents and joining them to the tiles. Subtracting water from these tiles. Joining the roads to the tiles.

Tiles are imported from the .shp grid file. And imported as collection of individual pieces, extruded based on feature main_height.

This is repeated once more for the cutter feature, and once more for the filler feature. Leaving the user with three different sets of tiles. Save.

    import grid shp -> extrude on main 
    import grid shp -> extrude on filler
    import grid shp -> extrude on cutter
    save .blend
Most of this is done in the following files:


The water is cut from the tiles by using a boolean, difference operation, the errored tiles are then filled in with the fill-tiles. 
This is done by first importing the water .shp files as individual things, based on the grid_id, and extracting them based on the extrusion feature. Align the water models to the main_tiles based on what looks good to be subtracted. 
Then run the water_cutter.py file, adjusting the parameters. This executes the boolean operation between the tiles and the water, one by one. Save.

    import_water_shps.py
    water_cutter.py for cutting out the water tiles based on the qgis-grid
    cutting_tiles_joining_roads.py might also serve some use in figuring out what codes to use.


Finally, the buildings need to be imported, cut to tiles size, joined to the tiles. Problematically,  we do not know which 3Dbag tiles align to which qgis-generated tiles. This required some manual work, by importing everything and counting the overlaps for each. The result is in ams_lut.csv, this forms the basis for the cutting out of the 840 tiles.
So for each tile, the correct 3Dbag tiles are imported, joined, and then removed with booleaan intersection. All 840 tiles are done, and takes a long time, for me around 14 hours on a Ryzen 4800H. Main limiter for this stuff is memory, 16GB in my case.

    For just importing all the tiles:
    import_3dbag.py
    
    For all the processing, and therefore also importing:

    lut_import_cutter_theworks.py
       
    save .blend

Let's make it harder for ourselves, and add a naming-scheme, which is nice for grid,localizatoin on a larger scale. 0:inf for the longitude/X, a-z for lat/y (aa, ab,ac, after z has been used.)
runnnig .py scripts! These names, pieces of text are placed on the bottom of the tile, centered, and join to the grid.

    physical_id_adder.py

    save .blend

I also added some connectors to make the individual tiles combineable, this is based around the dimensions of the grid.

    conn_box_theworks.py


This is it, project done. Time to export all the tiles as nice stls, but we first have to join them to the the grid, this is all done in join_export.py

    join_export.py

Good luck!