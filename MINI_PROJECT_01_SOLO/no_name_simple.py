## 기능 함수들 모듈/파일 로딩 --------------------
import datetime
import no_name_simple_func

## 윈도우 창 만들기
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from functools import partial # functools 추가
import os # os모듈을 사용하여 특정 디렉터리에서 .txt 파일 목록을 가져오고, 그 목록을 tkinter의 listbox에 표시

win = Tk()

# 다이어리 파일이 저장된 경로
diary_dir = './' # 현재 디렉토리에서 파일을 읽을 경우 './'을 사용


## 창크기 조절과 제목 넣기기
win.title("No_Name_simple_Diary")
win.geometry("1500x780+10+0")

# 현재 날짜 구하기
today=datetime.datetime.now()
print(today)

# 날짜를 'YYYY-MM-DD' 형식으로 표시
today_str=today.strftime("%Y년 %m월 %d일")
# print(today_str)

# 라벨 넣기
t1 = Label(win, text=f'🌟🌟🌟🌟🌟   {today_str}   🌟🌟🌟🌟🌟',
           font=("Malgun Gothic", 20, "bold"))
t1.pack()

t2 = Label(win, text="=======   Diary List   =======",
           font=("Malgun Gothic", 16, "bold"))
t2.place(x=100, y=100)

t3 = Label(win, text="==========  ✨💕Content✨💕  ==========",
           font=("Malgun Gothic", 16, "bold"))
t3.place(x=500, y=100)


# ------------------------------------------------
# 파일을 읽고 텍스트 위젯에 출력하는 함수
# ------------------------------------------------
def load_diary(file_name):
    try:
        # 파일 열기
        with open(os.path.join(diary_dir, file_name), 'r', encoding='utf-8') as file:
            content = file.read()
            text_entry.delete(1.0, tk.END) # 기존 내용을 삭제
            text_entry.insert(tk.END, content) # 파일 내용을 입력
    except Exception as e:
        messagebox.showerror("오류", f"파일을 읽는 데 실패했습니다. : {e}")

# 파일 목록을 불러오는 함수
def load_file_list():
    try:
        # diary_dir 경로에 있는 모든 .txt 파일 목록을 가져옴
        files = [f for f in os.listdir(diary_dir) if f.endswith('.txt')]
        listbox.delete(0, tk.END) # 기존 목록 삭제
        
        # 파일 목록을 Listbox에 추가
        if len(files) == 0:
            listbox.insert(tk.END, "파일 없음") # 파일이 없으면 메시지 표시
        else:
            for file in files:
                listbox.insert(tk.END, file) # 파일 목록을 listbox에 추가
    except Exception as e:
        messagebox.showerror("오류", f"파일 목록을 불러오는 데 실패했습니다: {e}")
        
# 선택된 파일을 읽어서 텍스트 위젯에 표시
def on_file_select(event):
    try:
        selected_file_index = listbox.curselection()
        if selected_file_index:
            selected_file = listbox.get(selected_file_index)
            load_diary(selected_file)
        else:
            messagebox.showwarning("선택 오류", "파일을 선택해주세요.")
    except Exception as e:
        messagebox.showerror("오류", f"파일을 선택하는 데 실패했습니다.: {e}")
                

# prt1 = StringVar()
# lbl = Label(win, textvariable=prt1).pack()
# --------------------------------------------------------
# 메인 윈도우 설정
# 다이어리 파일 목록을 표시할 Listbox
# --------------------------------------------------------
listbox = tk.Listbox(win, width=50, height=30)
listbox.place(x=100,y=150)

# listbox에서 파일을 선택하면 내용을 표시하도록 이벤트 바인딩
listbox.bind('<<ListboxSelect>>', on_file_select)

# 파일 내용 표시를 위한 Text 위젯
text_entry = tk.Text(win, width=59, height=22.5,
                     font=("Malgun Gothic", 12))
text_entry.place(x=500,y=150)

# "파일 목록 새로고침" 버튼
refresch_button = tk.Button(win, text="새로고침",
                            font=("Malgun Gothic", 40),
                            fg='white', bg='sky blue',
                            command=load_file_list)
refresch_button.place(x=1100, y=300)

# 처음에 파일 목록을 로드
load_file_list()




# -------------------------------------------------------------------    
# 페이지 전환 함수
# -------------------------------------------------------------------
second_window=None # 변수를 밖에도 줘야지 나중에 찾아보고 없으면 global 붙은 곳까지 찾아줌
third_window=None
def open_second_window():
    # win.withdraw() # 첫 번째 창 숨기기
    create_second_window()
    
def open_third_window():
    # win.withdraw()
    create_third_window()

    

# ---------------------------------------------------------------------
# 실행 부분 (글 작성 / 수정 / 삭제)
# --------------------------------------------------------------------- 
# 다이어리 작성하기(파일 저장)

def write_diary(date):
    
    diary_content = text_entry.get("1.0", "end-1c") # Text 위젯에서 내용을 가져옴
    if len(diary_content) != 0: #  내용이 비어있지 않으면 저장
        # 다이어리 내용을 파일에 저장
        
        with open(f'diary_{date}.txt', "w", encoding="utf-8") as file: 
            file.write(diary_content)
        messagebox.showinfo("저장", "다이어리가 저장되었습니다.") # 저장 성공 메시지
    else:
        messagebox.showwarning("경고", "내용을 입력해 주세요.") # 내용이 없으면 경고 메시지

# -----------------------------------------------------------------
#
# -----------------------------------------------------------------


# --------------------------------------------------------------------
# 두 번째 창(win2)    
# --------------------------------------------------------------------
def create_second_window():
    global text_entry # 전역 변수를 사용하여 text_entry를 참조조
    
    global second_window # 전역함수로 사용할 것을 선언(반대는 지역함수)
    # 새 창 생성
    second_window = tk.Toplevel(win)
    second_window.title("To Do List")
    second_window.geometry("1500x780+10+0")
    
    label_01 = tk.Label(second_window, text=f"To Do List",
                     font=("Malgun Gothic", 35, "bold"))
    label_02 = tk.Label(second_window, text=today,
                     font=("Malgun Gothic", 10, "bold"))
    label_01.pack(pady=10)
    label_02.pack()
    
    # 다이어리 작성 기능 추가
    diary_label = Label(second_window, text=f'다이어리 작성 - {today_str}',
                        font=("Malgun Gothic", 15, "bold"))
    diary_label.pack(pady=10) # 세로로 여백을 10 줄게게
    
    # Text 위젯 : 다이어리 내용을 입력할 수 있게 함
    text_entry = Text(second_window, width=50, height=20,
                      font=("Malgun Gothic", 12))
    text_entry.pack(pady=10)
    
    # 저장 버튼 : 작성한 내용을 파일에 저장
    save_button = Button(second_window, text="저장", 
                         font=("Malgun Gothic", 15, "bold"),
                         fg="white", bg="sky blue", command=partial(write_diary, today_str)) # partial로 인자 전달
    save_button.pack(pady=20)                                                                # today_str 날짜가 제대로 안 불러와져서 partial을 쓰긴 함함
    
    # 두 번째 페이지 Button [1] : 종료
    btn2_1 = Button(second_window, text="종   료",
                font=("Malgun Gothic", 10, "bold"),
                fg="white", bg="grey",
                command=exit_btn)
    btn2_1.place(x=1430, y=15)
    
    # 두 번째 페이지 Button [2] : 작   성 
    # btn2_2 = Button(win, text="작   성",
    #               font=("Malgun Gothic", 40, "bold"),
    #               fg="white", bg="sky blue",
    #               command=btn1_press)
    # btn2_2.place(x=1100, y=100)
    
    # # 두 번째 페이지 Button [3] : 수   정 
    # btn2_3 = Button(win, text="수   정",
    #               font=("Malgun Gothic", 40, "bold"),
    #               fg="white", bg="sky blue",
    #               command=btn1_press)
    # btn2_3.place(x=1100, y=250)
    
    # # 두 번째 페이지 Button [4] : 삭   제 
    # btn2_4 = Button(win, text="삭   제",
    #               font=("Malgun Gothic", 40, "bold"),
    #               fg="white", bg="sky blue",
    #               command=btn1_press)
    # btn2_4.place(x=1100, y=400)

    # 두 번째 페이지 Button [4] : Back / 뒤로가기
    btn2_5 = Button(second_window, text="Back",
                font=("Malgun Gothic", 10, "bold"),
                fg="white", bg="blue",
                command=go_back_to_main_win)
    btn2_5.place(x=1430, y=700)
    
# 세 번째 창(win3)    
def create_third_window():
    global third_window
    # 새 창 생성
    third_window = tk.Toplevel(win)
    third_window.title("✨💕✨💕")
    third_window.geometry("1500x780+10+0")
    
    label_01 = tk.Label(third_window, text=f"✨💕✨💕",
                        font=("Malgun Gothic", 35, "bold"))
    label_02 = tk.Label(third_window, text=today,
                        font=("Malgun Gothic", 10, "bold"))
    label_01.pack(pady=20)
    label_02.pack()
    
    # 세 번째 페이지 Button [1] : 종료
    btn3_1 = Button(third_window, text="종   료",
                font=("Malgun Gothic", 10, "bold"),
                fg="white", bg="grey",
                command=exit_btn)
    btn3_1.place(x=1430, y=15)
    
    # 두 번째 페이지 Button [2] : 작   성 
    # btn3_2 = Button(win, text="작   성",
    #               font=("Malgun Gothic", 40, "bold"),
    #               fg="white", bg="sky blue",
    #               command=btn1_press)
    # btn3_2.place(x=1100, y=100)
    
    # # 두 번째 페이지 Button [3] : 수   정 
    # btn3_3 = Button(win, text="수   정",
    #               font=("Malgun Gothic", 40, "bold"),
    #               fg="white", bg="sky blue",
    #               command=btn1_press)
    # btn3_3.place(x=1100, y=250)
    
    # # 두 번째 페이지 Button [4] : 삭   제 
    # btn3_4 = Button(win, text="삭   제",
    #               font=("Malgun Gothic", 40, "bold"),
    #               fg="white", bg="sky blue",
    #               command=btn1_press)
    # btn3_4.place(x=1100, y=400)
    
    # 세 번째 페이지 Button [5] : Back / 뒤로가기
    btn3_5 = Button(third_window, text="Back",
                font=("Malgun Gothic", 10, "bold"),
                fg="white", bg="blue",
                command=go_back_to_main_win)
    btn3_5.place(x=1430, y=700)

    

# -------------------------------------------------------------------------
# 종료 함수
# -------------------------------------------------------------------------
def exit_btn():
    win.quit()
    win.destroy()
    
# -------------------------------------------------------------------------
# 두 번째 페이지 Button [2] : Back / 종료 
# -------------------------------------------------------------------------
def go_back_to_main_win():
    global second_window
    if second_window:
        second_window.destroy() # 두 번째 창을 닫고
    win.deiconify() # 메인 창(win)을 다시 보이게 함
    
# -------------------------------------------------------------------------

# -------------------------------------------------    
# 첫 번째 페이지 Button [1]
btn_to_do_list = Button(win, text="✨💕✨💕",
                        font=("Malgun Gothic", 35, "bold"),
                        fg="white", bg="sky blue",
                        command=open_second_window)
btn_to_do_list.place(x=1100, y=150)

# 첫 번째 페이지 Button [2]
# btn_note = Button(win, text="✨💕✨💕",
#                         font=("Malgun Gothic", 35, "bold"),
#                         fg="white", bg="sky blue",
#                         command=open_third_window)
# btn_note.place(x=1100, y=400)

# 첫 번째 페이지 Button [3] : 종료
btn1_4 = Button(win, text="종   료",
              font=("Malgun Gothic", 10, "bold"),
              fg="white", bg="grey",
              command=exit_btn)
btn1_4.place(x=1430, y=15)




    
    































































win.mainloop()

# 실행 부분
# no_name_simple_func.daily_list(today_str)
# if __name__=="__main__":  # 다이어리가 스크립트에 저장되고 있기 때문에 그 파일을 불러주기 위해 사용
#     # 오늘 날짜의 다이어리를 먼저 출력
#     # no_name_simple_func.write_diary(today_str)
#     no_name_simple_func.daily_list(today_str)
    
#     # 다이어리를 작성할지 물어보는 메시지
#     user_input = input("\n오늘의 다이어리를 작성하시겠습니까? ( Yes or No ) : ")
#     if user_input.lower() in 'yes':
#         no_name_simple_func.write_diary(today_str)
#         print("다이어리가 저장되었습니다.")
#     else:
#         print("다이어리 작성을 종료합니다.")
    
    
    
    
    
    
# ----------------------------------------------
# To Do List 프로그램
# ----------------------------------------------
# while True:
#     # 메뉴출력 및 선택
#     choice=no_name_simple_func.printMenu()
    
#     # 종료 조건문
#     if choice=='5':
#         print('프로그램을 종료합니다.')
#         break
    
#     # 메뉴에 따른 기능 코드 실행
#     elif choice=='1':
#         print("Monthly")
    
#     elif choice=='2':
#         print("Weekly")
        
#     elif choice=='3':
        
#         print("Daily")
    
#     elif choice=='4':
#         print("Back")
        
#     else:
#         print("존재하지 않는 메뉴입니다.")