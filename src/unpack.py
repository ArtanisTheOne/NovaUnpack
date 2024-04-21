import os
import UnityPy
from tqdm import tqdm






def main_container(source_folder : str, destination_folder : str, row_n = 1):
    global main_loop 
    
    main_loop = True
    
    
    

    def unpack_all_assets(source_folder : str, destination_folder : str, row_n = 1):
    
        print_counter = False
        count = 0
        if main_loop:
            if not os.path.exists(destination_folder):
                if not os.path.exists(os.path.dirname(destination_folder)):
                    os.mkdir(os.path.dirname(destination_folder))
                os.mkdir(destination_folder)
            print_counter = True
            main_loop = False
        folder_name = destination_folder
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        for file_name in os.listdir(source_folder):
            if os.path.isdir(os.path.join(source_folder, file_name)):
                # /android/icon
                number_added = unpack_all_assets(os.path.join(source_folder, file_name), os.path.join(destination_folder, file_name))
                if print_counter:
                    count += number_added
                continue
                
            if file_name.endswith(".manifest") or file_name.endswith(".json") or file_name.endswith(".xml"):
                continue
        
            unity_obj = UnityPy.load(os.path.join(source_folder, file_name))
            
            for obj in unity_obj.objects:
                if obj.type.name not in ["Texture2D", "Texture2DArray"]:
                    continue
                
                if obj.type.name == "Texture2D":
                    image = obj.read()
                    try:
                        image.image.save(os.path.join(destination_folder, (image.m_Name + ".png").replace(" ", "_")))
                        if print_counter:
                            count += 1
                    except:
                        pass
                else:
                    for i, image in enumerate(obj.read()):
                        try:
                            image.image.save(os.path.join(destination_folder, (image.m_Name + str(i) + ".png").replace(" ", "_")))
                            if print_counter:
                                count += 1
                        except:
                            pass
        
        if len(os.listdir(destination_folder)) == 0:
            try:
                os.rmdir(destination_folder)
            except: 
                pass
        
        if print_counter:
            print("Total images exported: " + str(count))
        
        return count
    
    unpack_all_assets(source_folder, destination_folder, row_n)