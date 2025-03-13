import os
import shutil
import src.getCard
import src.generate
import src.html2pdf_selenium
import src.mergePdf
import tkinter as tk
from tkinter import ttk, scrolledtext

class App:
    def __init__(self, root):
        self.root = root
        root.title("邦邦明信片生成器")
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 卡面ID输入
        ttk.Label(main_frame, text="卡面编号:").grid(row=0, column=0, sticky=tk.W)
        self.card_id = ttk.Entry(main_frame)
        self.card_id.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # 特训状态选择
        ttk.Label(main_frame, text="特训状态:").grid(row=1, column=0, sticky=tk.W)
        self.training_status = tk.StringVar(value="normal")
        ttk.Radiobutton(main_frame, text="特训前", variable=self.training_status, 
                       value="normal").grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(main_frame, text="特训后", variable=self.training_status, 
                       value="trained").grid(row=1, column=2, sticky=tk.W)
        
        # 生成按钮
        ttk.Button(main_frame, text="开始生成", command=self.generate).grid(row=2, column=0, 
                                                                      columnspan=3, pady=10)
        
        # 日志显示区域
        self.log_area = scrolledtext.ScrolledText(main_frame, height=10, width=50)
        self.log_area.grid(row=3, column=0, columnspan=3, pady=5)

    def log(self, message):
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.see(tk.END)
        self.root.update()

    def generate(self):
        try:
            card_id = int(self.card_id.get())
            after_training = self.training_status.get() == "trained"
            
            self.log("开始生成...")
            
            os.makedirs("cache", exist_ok=True)
            cardInfo = src.getCard.getCard(card_id, afterTraining=after_training)

            if cardInfo is None:
                self.log("卡面数据获取失败")
                return
            else:
                self.log("卡面数据获取成功")

            src.generate.generateHtml(cardInfo)
            self.log("HTML生成完成")
            
            src.html2pdf_selenium.html_to_pdf("cache/front.html", "cache/front.pdf")
            src.html2pdf_selenium.html_to_pdf("cache/back.html", "cache/back.pdf")
            self.log("PDF转换完成")

            os.makedirs("output", exist_ok=True)
            output_filename = "output/{}_{}_{}.pdf".format(
                cardInfo["characterChineseName"], 
                card_id, 
                "after-training" if after_training else "normal"
            )
            src.mergePdf.mergePdf("cache/front.pdf", "cache/back.pdf", output_filename)
            self.log(f"PDF合并完成，已保存至: {output_filename}")

            if os.path.exists("cache"):
                shutil.rmtree("cache")
                self.log("临时文件已清理")
                
        except Exception as e:
            self.log(f"生成明信片出错: {str(e)}")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()