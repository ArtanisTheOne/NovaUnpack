import requests
from tqdm import tqdm
import httpx
def download(link, save_path):

    try:
        r = httpx.head(url=link, follow_redirects=True)

        total_size = int(r.headers.get('content-length', 0))
        
        bar = tqdm(
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
                
        )
        with open(save_path, 'wb+') as file, httpx.stream('GET', link, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko)'
                'Version/9.1.2 Safari/601.7.5'
            }, follow_redirects=True) as resp:
            for chunk in resp.iter_bytes(2048 * 1024):
                if bar.total == total_size:
                    bar.total = int(resp.headers.get('content-length', 0))
                if chunk:
                    size = file.write(chunk)
                    bar.update(size)
        
        bar.close()
        print(f"------\nDownloaded file: {save_path}\n")
        
    except Exception as e:
        print(f"------\nERROR - Error downloading file: {e}\nERROR - {link}\nERROR - {save_path}\nERROR - Exiting program.\n")
        exit()
        

def download_apk(app_id, save_path):
    default_download_link = f"https://d.apkpure.com/b/APK/{app_id}?version=latest"

    download(default_download_link, save_path)