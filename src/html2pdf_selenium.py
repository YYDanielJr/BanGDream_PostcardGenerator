import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import base64  # 添加 base64 模块

def html_to_pdf(html_path, output_path):
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 配置Chrome选项
    chrome_options = Options()
    if sys.platform == 'win32':
        chrome_path = os.path.join("drivers", "Chrome", "chrome.exe")
    else:
        chrome_path = os.path.join("drivers", "Chrome", "chrome")
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument('--headless')  # 无界面模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    if sys.platform == 'win32':
        service = Service(executable_path=os.path.join("drivers", "chromedriver.exe"))
    else:
        service = Service(executable_path=os.path.join("drivers", "chromedriver"))

    # 设置固定尺寸（单位：毫米）
    page_width_mm = 296
    page_height_mm = 200

    try:
        driver = webdriver.Chrome(options=chrome_options, service=service)

        html_absolute_path = os.path.abspath(html_path)
        driver.get(f"file:///{html_absolute_path}")

        # 设置打印选项
        print_options = {
            'printBackground': True,
            'landscape': False,  # 改为纵向打印
            'paperWidth': 8.7406225,  # 交换宽高
            'paperHeight': 5.905826,
            'margin': {
                'top': 0,
                'bottom': 0,
                'left': 0,
                'right': 0
            },
            'scale': 1.0,
            # 'preferCSSPageSize': True,  # 使用CSS定义的页面大小
        }
        
        # 打印为PDF并处理返回的base64数据
        result = driver.execute_cdp_cmd('Page.printToPDF', print_options)
        pdf_data = base64.b64decode(result['data'])
        
        # 保存PDF文件
        with open(output_path, 'wb') as file:
            file.write(pdf_data)
            
        print(f"PDF已成功生成: {output_path}")
        return True

    except Exception as e:
        print(f"生成PDF时出错: {str(e)}")
        return False
        
    finally:
        if 'driver' in locals():
            driver.quit()