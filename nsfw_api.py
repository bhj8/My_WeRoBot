from nsfw_detector import predict

model = predict.load_model('./mobilenet_v2_140_224')

# Predict single image
# print(predict.classify(model, 'N1.png'))
# {'2.jpg': {'sexy': 4.3454722e-05, 'neutral': 0.00026579265, 'porn': 0.0007733492, 'hentai': 0.14751932, 'drawings': 0.85139805}}

# Predict multiple images at once
# predict.classify(model, ['/Users/bedapudi/Desktop/2.jpg', '/Users/bedapudi/Desktop/6.jpg'])
# {'2.jpg': {'sexy': 4.3454795e-05, 'neutral': 0.00026579312, 'porn': 0.0007733498, 'hentai': 0.14751942, 'drawings': 0.8513979}, '6.jpg': {'drawings': 0.004214506, 'hentai': 0.013342537, 'neutral': 0.01834045, 'porn': 0.4431829, 'sexy': 0.5209196}}

# Predict for all images in a directory
def is_safe(img_path):
    print("zhengzai sheng he !!!!!!")
    a = predict.classify(model, img_path)
    t = a['hentai']*2 + a['porn']*2 +a['sexy']
    if t > 0.6:
        return False
    return True




# for i in a.keys() :
#      t = a[i]['hentai']*2 + a[i]['porn']*2 +a[i]['sexy']
#      if t > 0.6:
#         print(a[i]['hentai']*3)
#         print(a[i]['porn']*3 )
#         print(a[i]['sexy'])
#         #先取i的文件名
#         i = i.split('\\')[-1]
#         #复制到t1文件夹下
#         shutil.copyfile('./images/'+i, './images/t1/'+i)
#         print(i, t)