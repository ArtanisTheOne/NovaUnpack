import os
import UnityPy
from tqdm import tqdm

global count, last_run
last_run = 0
count = 0

def get_new_count():
    global count, last_run
    
    count_val = count
    
    to_add = count_val - last_run
    last_run = count_val
    
    return to_add

def get_count():
    global count
    return count

def unpack_all_assets(source_folder : str, destination_folder : str):
    global count
    
    folder_name = destination_folder
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for file_name in os.listdir(source_folder):
        if os.path.isdir(os.path.join(source_folder, file_name)):
            # /android/icon
            number_added = unpack_all_assets(os.path.join(source_folder, file_name), os.path.join(destination_folder, file_name))
            continue
            
        if file_name.endswith(".manifest") or file_name.endswith(".json") or file_name.endswith(".xml"):
            continue
    
        unity_obj = UnityPy.load(os.path.join(source_folder, file_name))
        
        for obj in unity_obj.objects:
            if obj.type.name not in ["Texture2D", "Texture2DArray", "Sprite"]:
                continue
            
            if obj.type.name == "Texture2D":
                image = obj.read()
                try:
                    image.image.save(os.path.join(destination_folder, (image.m_Name + ".png").replace(" ", "_")))
                    count += 1
                except:
                    pass
            elif obj.type.name == "Texture2DArray":
                for i, image in enumerate(obj.read()):
                    try:
                        image.image.save(os.path.join(destination_folder, (image.m_Name + str(i) + ".png").replace(" ", "_")))
                        count += 1
                    except:
                        pass
            elif obj.type.name == "Sprite":
                image = obj.read()
                try:
                    save_path = os.path.join(destination_folder, image.m_Name + ".png")
                    image.image.save(save_path)
                    count += 1
                except:
                    pass
    
    if len(os.listdir(destination_folder)) == 0:
        try:
            os.rmdir(destination_folder)
        except: 
            pass