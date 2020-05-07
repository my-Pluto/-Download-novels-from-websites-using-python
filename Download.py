import requests
import Header


class Download():
    #   获取页面信息
    @staticmethod
    def download_page(url, referer):
        response = requests.get(url=url, headers=Header.get_header(referer=referer), proxies=Header.get_proxy()[0], verify=False,
                                allow_redirects=False)
        return response

    #   下载信息
    @staticmethod
    def download_text(url, path, referer):
        response = requests.get(url=url, headers=Header.get_header(referer=referer), proxies=Header.get_proxy(),
                                verify=False,
                                allow_redirects=False)
        with open(path, 'wb') as f:
            f.write(response.content)
        f.close()