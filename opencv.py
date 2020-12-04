
#!/usr/bin/env python
#在python中绑定OpenCV
import cv2
#使用图片的方法：在同一个文件夹下有"test.jpg"图片
fn="test.jpg"

if __name__ == '__main__':
    img = cv2.imread('test.jpg')
    cv2.imshow('a frame', img)  # a frame 是显示窗口的的标题名称
    cv2.waitKey(0)
    cv2.destroyAllWindows()