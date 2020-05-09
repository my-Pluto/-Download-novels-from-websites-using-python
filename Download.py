import os
import requests
import Header

cmd_path = "D:\SoftwareData\Wget\\"
http_proxy = "http_proxy=\"127.0.0.1:10809\""

# ??????
def download_page(url, referer):
    response = requests.get(url=url, headers=Header.get_header(referer=referer), proxies=Header.get_proxy()[0],
                            verify=False,
                            allow_redirects=False)
    return response



def download_img(url, path, referer):
    response = requests.get(url=url, headers=Header.get_header_not_proxy(referer=referer),
                            verify=False,
                            allow_redirects=False)
    with open(path, 'wb') as f:
        f.write(response.content)
    f.close()

def download_text(url, path):
    cmd = cmd_path + "wget -P " + path + " -e "+ http_proxy + " " + url
    os.system(cmd)
