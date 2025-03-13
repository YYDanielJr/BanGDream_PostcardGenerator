# BanG Dream!明信片生成器
你还在因为参加各种邦o或者邦邦live印无料，发现制作流程繁琐而心烦意乱吗？<br>
本程序的诞生是因为自己在印制明信片卡面时，因为修改卡面过程重复且繁琐，从而产生了自动化操作的想法。

## 环境配置
目前本程序仅在Windows环境，python版本3.11.11（conda）下成功运行。<br>
对于Windows用户，我建议直接下载release下的包含二进制文件的压缩包。压缩包包含了Chrome二进制文件和Real-ESRGAN二进制文件，可以直接使用。<br>
在解压所有文件之后，运行`main.exe`即可。<br>
对于macOS和Linux用户，需要下载**相同版本的**Chrome二进制文件和chromedriver二进制文件，以及Real-ESRGAN二进制文件。<br>
Chrome下载位置：https://googlechromelabs.github.io/chrome-for-testing/#stable<br>
Real-ESRGAN下载位置：https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases/tag/v0.2.0<br>
下载完成之后，将chromedriver二进制文件放置在`drivers`目录下，chrome二进制文件的整个目录放置在`drivers/Chrome`目录下，将整个`Real-ESRGAN`目录放置在RealEsrgan目录下。<br>
你的程序应当有如下的目录结构：
```
BanGDream_PostcardGenerator
├─drivers
│  ├─chromedriver
│  └─Chrome
│     └─chrome
├─RealEsrgan
│  └─realesrgan-ncnn-vulkan
```
建议在conda等虚拟环境下运行程序。<br>
安装依赖：
```
pip install -r requirements.txt
```
安装依赖之后，运行main.py即可：
```
python main.py
```

## 使用方法
在打开程序之后，按照提示输入想要制作的卡面ID，选择花前或花后，在output目录下会自动生成可供印刷的pdf文件。pdf文件为296mm * 200mm，尺寸按照我上一次在某家淘宝店印刷明信片时的148mm * 100mm设计。

## 程序流程
1. 从Bestdori!获取卡面数据和卡面图片
2. 下载好的卡面和pico服装使用real-esrgan算法超分
3. 将信息填写到位于pageTemplate目录下的模板html内
4. 将html渲染为pdf

## 远期规划
- 明信片模板提供更多样式（现在你可以通过移动模板html中的元素位置来修改明信片卡面）
- 一个GUI
- 批量生成
- 压缩生成的图片大小，减小pdf尺寸

## 使用到的第三方库
- Real-ESRGAN二进制文件：https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan
- Selenium：https://github.com/SeleniumHQ/selenium