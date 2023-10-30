import random
import tkinter as tk
from PIL import Image, ImageTk

# 建立主視窗
root = tk.Tk()
window_width = 640
window_height = 640
root.geometry(f"{window_width}x{window_height}")

# 打開並顯示背景圖片
bg_image = Image.open("K背景.png")
bg_image = bg_image.resize((window_width, window_height), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)

word_one = ""
file = open('K文件.txt', 'r', encoding='utf-8')
contents = file.read()
file.close()
count = 0
all_list = []
temporary_list = []
word_list = []
chineseword_list = []
labels = []

# 將內容按指定格式分割成不同的列表
for i in contents:
    if i == "#":
        break
    elif ' ' in i:
        temporary_list.append(word_one)
        word_one = ""  # 清空 word_one 變數
    elif '\n' in i:
        temporary_list.append(word_one)
        word_list.append(temporary_list[-1])  # 將最後一項資料加入 word_list
        chineseword_list.append(temporary_list[0])  # 將第一項資料加入 chineseword_list
        all_list.append(temporary_list)
        temporary_list = []  # 清空 temporary_list
        word_one = ""  # 清空 word_one 變數
    else:
        word_one = word_one + i

used_indices = []
random_index_list = []

def open_new_window():
    root.destroy()
    new_window = tk.Tk()
    window_width = 1920
    window_height = 1080
    new_window.geometry(f"{window_width}x{window_height}")
    labels = []

    def start_exam():
        def show_next_question():
            if len(used_indices) < len(word_list):
                random_word_index = random.choice([i for i in range(len(word_list)) if i not in used_indices])
                used_indices.append(random_word_index)
                random_word = word_list[random_word_index]
                corresponding_chinese_value = chineseword_list[random_word_index]
                random_chinese_values = random.sample(chineseword_list, 3)
                random_chinese_index = random.randint(0, 3)
                random_index_list.append(random_chinese_index)
                random_chinese_values.insert(random_chinese_index, corresponding_chinese_value)
                test_list = random_chinese_values

                labels[0].config(text="A. " + test_list[0])
                labels[1].config(text="B. " + test_list[1])
                labels[2].config(text="C. " + test_list[2])
                labels[3].config(text="D. " + test_list[3])
                center_label.config(text=str(len(random_index_list)) + " " + random_word)

                new_window.after(7000, show_next_question)

        show_next_question()

    def calculate_answers():
        # 計算答案並在ANS視窗中列印
        ans_window = tk.Toplevel()
        ans_window.title("ANS")
        ans_window.geometry("400x400")
        points = 100 / int(len(random_index_list))
        ans_label = tk.Label(ans_window, text="每題分數為" + str(points) + "\n答案:", font=("Helvetica", 20))
        ans_label.pack()

        ans_text = tk.Text(ans_window, wrap=tk.WORD, width=40, height=10, font=("Helvetica", 40))
        ans_text.pack()

        # 添加計數器變數
        print_count = 0
        # 創建替換字典
        replacement_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
        # 替換 random_index_list 中的值並添加到 ANS 視窗中
        for idx in random_index_list:
            replaced_value = replacement_dict.get(idx, str(idx))  # 獲取替換值，如果沒有找到則保持原始值

            # 增加計數器並將其添加到文本中
            print_count += 1
            ans_text.insert(tk.END, f"{print_count}. {replaced_value}\n")

    # 打開並顯示新視窗的背景圖片
    bg_image = Image.open('K背景.png')
    bg_image = bg_image.resize((window_width, window_height), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(new_window, width=window_width, height=window_height)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)

    calculate_button = tk.Button(new_window, text="結算", command=calculate_answers, bg='red')
    calculate_button.pack()
    calculate_button.place(x=200, y=20)

    # 創建用於顯示問題的標籤
    for i in range(4):
        label = tk.Label(new_window, text=f"word {i + 1}", relief="solid", bg='white', font=("Helvetica", 80))
        label.place(x=530, y=300 + (i * 126))
        labels.append(label)

    # 創建位於屏幕正中間的標籤
    center_label = tk.Label(new_window, text="word", bg="white", font=("Helvetica", 130))
    center_label.place(x=500, y=50)

    start_button = tk.Button(new_window, text="開始考試", command=start_exam, bg='green')
    start_button.pack()
    start_button.place(x=100, y=20)

    return_button = tk.Button(canvas, text="結束程式", command=new_window.destroy, bg='green')
    return_button.pack()
    return_button.place(x=20, y=20)
    new_window.mainloop()

# 創建一個按鈕以打開新視窗
button = tk.Button(canvas, text="打開考試介面", command=open_new_window)
button.pack()
button.place(x=20, y=20)

# 運行主事件循環
root.mainloop()

