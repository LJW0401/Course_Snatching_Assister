import base64
import cv2

# 读取图片文件
with open('D:/Projects/Course_Snatching_Assister/PC/test/stop_1.png', 'rb') as image_file:
    # 读取图片文件内容
    image_data = image_file.read()
    
    # 将图片数据编码为Base64
    base64_encoded = base64.b64encode(image_data).decode('utf-8')

# 将Base64编码保存到文件
with open('D:/Projects/Course_Snatching_Assister/PC/test/stop_1.txt', 'w') as output_file:
    output_file.write(base64_encoded)
    
    
    
# 读取图片文件
with open('D:/Projects/Course_Snatching_Assister/PC/test/stop_2.png', 'rb') as image_file:
    # 读取图片文件内容
    image_data = image_file.read()
    
    # 将图片数据编码为Base64
    base64_encoded = base64.b64encode(image_data).decode('utf-8')

# 将Base64编码保存到文件
with open('D:/Projects/Course_Snatching_Assister/PC/test/stop_2.txt', 'w') as output_file:
    output_file.write(base64_encoded)



# 读取图片文件
with open('D:/Projects/Course_Snatching_Assister/PC/test/do.png', 'rb') as image_file:
    # 读取图片文件内容
    image_data = image_file.read()
    
    # 将图片数据编码为Base64
    base64_encoded = base64.b64encode(image_data).decode('utf-8')

# 将Base64编码保存到文件
with open('D:/Projects/Course_Snatching_Assister/PC/test/do.txt', 'w') as output_file:
    output_file.write(base64_encoded)