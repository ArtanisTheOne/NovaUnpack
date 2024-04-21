import argparse
import os
from src.apkpure import download_apk
from src.unpack import main_container
from threading import Thread
from datetime import datetime
from zipfile import ZipFile
import shutil

parser = argparse.ArgumentParser(description="Download Nova Empire APK and extract Unity Texture2D asssets.")
parser.add_argument("-force_download", "--force_download", action="store_true", help="Redownload APK File. If not set, the script will scan the directory for latest version of .apk file and use it.", default=False)
parser.add_argument("-d_path", "--download_path", type=str, help="Path to download the APK files. If not set, the script will download the APK file to the current directory.", default=os.getcwd())
parser.add_argument("-apk", "--apk_path", type=str, help="Path to the APK file. If not set, the script will follow the logic of the 'force_download' parameter.", default=None)
parser.add_argument("-app_id", "--app_id", type=str, help="App ID of the APK file to download.", default="com.gamebeartech.nova")

args = parser.parse_args()




# file loc of apk_path

preset_apk_valid = bool(args.apk_path and os.path.exists(args.apk_path) and args.apk_path.endswith(".apk"))
apk_path = args.apk_path if preset_apk_valid else os.path.join(args.download_path, f"{args.app_id}_{datetime.now().date()}.apk")

# sets the download path to ../ of the apk_path the apk_path is set
download_path = args.download_path if not preset_apk_valid else os.path.dirname(apk_path)

force_download = args.force_download
app_id = args.app_id

apk_found = False


if not force_download:
    print("------\nScanning current directory for latest APK file...\n")
    apk_files = [f for f in os.listdir(download_path) if f.endswith(".apk") and f.startswith(app_id)]    
    
    # sort from newest to oldest
    apk_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_path, x)), reverse=True)
    mtimes = [os.path.getmtime(os.path.join(download_path, f)) for f in apk_files]
    
    if len(apk_files) > 0:
        apk_path = os.path.join(download_path, apk_files[0])
        print(f"------\nLatest APK file found: {apk_path} - {round(mtimes[0] / 86400, 5)} days old\nSkipping fresh download.\n")
        apk_found = True
    else:
        print(f"------\nNo APK files found in the current directory for {app_id}\nDownloading fresh version...\n")

if not apk_found:
    download_apk("com.gamebeartech.nova", apk_path)
    
if not os.path.exists(apk_path):
    print(f"------\nERROR - APK file not found: {apk_path}\nERROR - Exiting program.\n")
    exit()


print(f"------\nExtracting APK file: {os.path.join(download_path, 'apk_extracted')}")

if os.path.exists(os.path.join(download_path, "apk_extracted")):
    shutil.rmtree(os.path.join(download_path, "apk_extracted"), ignore_errors=True)

if not os.path.exists(os.path.join(download_path, "apk_extracted")):
    os.mkdir(os.path.join(download_path, "apk_extracted"))
else:
    print(f"------\nWARNING - Directory already exists and may interfere with the extraction process: {os.path.join(download_path, 'apk_extracted')}\n")


ZipFile(apk_path).extractall(os.path.join(download_path, "apk_extracted"))

print('------\nExtracted APK file to folder: ' + os.path.join(download_path, 'apk_extracted') + '\nStarting Unity extraction\n')

bin = Thread(target=main_container, args=(os.path.join(download_path, "apk_extracted", "assets", "bin", "Data"), os.path.join(download_path, "EXTRACTED_MEDIA", "misc"), 1))
main = Thread(target=main_container, args=(os.path.join(download_path, "apk_extracted", "assets", "asset_bundles", "android"), os.path.join(download_path, "EXTRACTED_MEDIA", "main"), 2))

bin.start()
main.start()