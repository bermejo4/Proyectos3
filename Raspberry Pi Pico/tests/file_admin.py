import os
import json

#print(os.listdir())
#file = open("init_page.html", "r")
# html_array=[]
# html_code=" "
# while True:
#     if not html_code:
#         break
#     else:
#         html_code=file.read(2048)
#         html_array.append(html_code)
#     
# #print(html_code.replace("\n",""))
# file.close()
# print(html_array[8])
# #print(html_code.partition(':')[0])

file = open("conf_file.txt", "r")
configuration=file.read()
conf=json.loads(configuration)
print(conf["Server_ip"])