 
rpg_items_sheet = ["./resources/rpg_items/Sheet.png"]
rpg_items = [
    "./resources/rpg_items/Item__00.png",
    "./resources/rpg_items/Item__01.png",
    "./resources/rpg_items/Item__02.png",
    "./resources/rpg_items/Item__03.png",
    "./resources/rpg_items/Item__04.png",
    "./resources/rpg_items/Item__05.png",
    "./resources/rpg_items/Item__06.png",
    "./resources/rpg_items/Item__07.png",
    "./resources/rpg_items/Item__08.png",
    "./resources/rpg_items/Item__09.png",
    
    "./resources/rpg_items/Item__10.png",
    "./resources/rpg_items/Item__11.png",
    "./resources/rpg_items/Item__12.png",
    "./resources/rpg_items/Item__13.png",
    "./resources/rpg_items/Item__14.png",
    "./resources/rpg_items/Item__15.png",
    "./resources/rpg_items/Item__16.png",
    "./resources/rpg_items/Item__17.png",
    "./resources/rpg_items/Item__18.png",
    "./resources/rpg_items/Item__19.png",
    
    "./resources/rpg_items/Item__20.png",
    "./resources/rpg_items/Item__21.png",
    "./resources/rpg_items/Item__22.png",
    "./resources/rpg_items/Item__23.png",
    "./resources/rpg_items/Item__24.png",
    "./resources/rpg_items/Item__25.png",
    "./resources/rpg_items/Item__26.png",
    "./resources/rpg_items/Item__27.png",
    "./resources/rpg_items/Item__28.png",
    "./resources/rpg_items/Item__29.png",
    
    "./resources/rpg_items/Item__30.png",
    "./resources/rpg_items/Item__31.png",
    "./resources/rpg_items/Item__32.png",
    "./resources/rpg_items/Item__33.png",
    "./resources/rpg_items/Item__34.png",
    "./resources/rpg_items/Item__35.png",
    "./resources/rpg_items/Item__36.png",
    "./resources/rpg_items/Item__37.png",
    "./resources/rpg_items/Item__38.png",
    "./resources/rpg_items/Item__39.png",
    
    "./resources/rpg_items/Item__40.png",
    "./resources/rpg_items/Item__41.png",
    "./resources/rpg_items/Item__42.png",
    "./resources/rpg_items/Item__43.png",
    "./resources/rpg_items/Item__44.png",
    "./resources/rpg_items/Item__45.png",
    "./resources/rpg_items/Item__46.png",
    "./resources/rpg_items/Item__47.png",
    "./resources/rpg_items/Item__48.png",
    "./resources/rpg_items/Item__49.png",
    
    "./resources/rpg_items/Item__50.png",
    "./resources/rpg_items/Item__51.png",
    "./resources/rpg_items/Item__52.png",
    "./resources/rpg_items/Item__53.png",
    "./resources/rpg_items/Item__54.png",
    "./resources/rpg_items/Item__55.png",
    "./resources/rpg_items/Item__56.png",
    "./resources/rpg_items/Item__57.png",
    "./resources/rpg_items/Item__58.png",
    "./resources/rpg_items/Item__59.png",
    
    "./resources/rpg_items/Item__60.png",
    "./resources/rpg_items/Item__61.png",
    "./resources/rpg_items/Item__62.png",
    "./resources/rpg_items/Item__63.png",
    "./resources/rpg_items/Item__64.png",
    "./resources/rpg_items/Item__65.png",
    "./resources/rpg_items/Item__66.png",
    "./resources/rpg_items/Item__67.png",
    "./resources/rpg_items/Item__68.png",
    "./resources/rpg_items/Item__69.png",
    
    "./resources/rpg_items/Item__70.png",
    "./resources/rpg_items/Item__71.png",
] 

pixel_art = [
    "./resources/bonzai.tif",
    "./resources/link.png",
    "./resources/mario.png",
]
pixel_art.extend(rpg_items)

test_images = [
    "./resources/circle.png",                   # 0
    "./resources/diagonal_left_100x100.tif",    # 1
    "./resources/disks_256.png",                # 2
    "./resources/grayscale_test_1.png",         # 3
    "./resources/multi_grayscale_1_100x100.tif",# 4
    "./resources/plus_100x100.tif",             # 5
    "./resources/stripes.png",                  # 6

    # Original HQX test images
    "./resources/test_original.png",            
    "./resources/mailbox_original.png",         
    "./resources/randam_orig.png",              
    "./resources/sq_orig.png",             
]

real_life_gray = [
    "./resources/cameraman.tif",
    "./resources/house.tif",
    "./resources/jetplane.tif",
    "./resources/lake.tif",
    "./resources/lena_gray_256.tif",
    # "./resources/lena_gray_512.tif",
    "./resources/livingroom.tif",
    "./resources/mandril_gray.tif",
    "./resources/peppers_gray.tif",
    "./resources/pirate.tif",
    "./resources/walkbridge.tif",
    "./resources/woman_blonde.tif",
    "./resources/woman_darkhair.tif"
]

real_life_color = [
    "./resources/lena_color_256.tif",
    # "./resources/lena_color_512.tif",
    "./resources/mandril_color.tif",
    "./resources/peppers_color.tif",
]
real_life = []
real_life.extend(real_life_gray)
real_life.extend(real_life_color)

all = []
all.extend(pixel_art)    
all.extend(test_images)    
all.extend(real_life)