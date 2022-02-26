from docx import Document
import requests

# r = requests.put("http://192.168.1.37/languages/3", params={"lang": "c"})
# print(r)
while False:
    content = open("alllang.txt", "r").read().split("\n")
    for i in content:
        r = requests.put(f"http://192.168.1.37/languages/{content.index(i)}", params={"lang": i})
        print(r)
        print(content)
