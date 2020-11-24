import binascii
import sys
import pymysql as pymysql
import serial  # 导入模块
import serial  # 导入模块
import serial.tools.list_ports
from tkinter import *

port_list = list(serial.tools.list_ports.comports())
print(port_list)
ans = ""
# **********************************
# 测试是否有可用得串口，有的话就进行打印
if len(port_list) == 0:
    print('无可用串口')
else:
    for i in range(0, len(port_list)):
        print(port_list[i])

# **********************************
win = Tk()


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.start = Button(frame, text="开始读卡", fg="red" ,font="楷体",pady="20px", command=self.start_)
        self.start.pack(side=LEFT)

    def start_(self):
        w = Label(win, text="正在读取...", pady="20")
        w.pack(side=TOP)
        try:
            str2 = ""
            ser = serial.Serial('COM3', '19200', timeout=1)
            print("串口详情参数：", ser)

            # 写数据，发送寻卡指令
            ser.write(bytes([0x02, 0x00, 0x00, 0x04, 0x46, 0x52, 0x9C, 0x03]))
            # # 发送寻卡（唯一ID指令）
            sys.stdout.flush()
            serial.time.sleep(0.5)
            result2 = ser.write(bytes([0x02, 0x00, 0x00, 0x04, 0x47, 0x04, 0x4F, 0x03]))

            while True:
                if ser.in_waiting:
                    # 因为这个就是缓冲区（前面返回的10个字节的数据，后面返回的是12个字节的数据）
                    if (ser.in_waiting == 22):
                        str1 = ser.read(ser.in_waiting)
                        str2 = str(binascii.b2a_hex(str1))[2:-1]
                        break
            ans = str2
            # print("this is : ", ans)
            # 32--39
            lastAnswer = ans[32:40]
            print("卡号:", lastAnswer)

            ser.close()  # 关闭串口
            print("!!!", lastAnswer)
            db = pymysql.connect("localhost", "root", "cuiwenxuan", "csustnet", charset='utf8')

            cursor = db.cursor()  # 数据库操作
            sql = "insert into medicineintroduce(medicineIntroId,medicineName,medicineIntroduce,isOTC,dosage,img,isD) values ('%s','%s','%s','%d','%s','%s','%d')" % (
                lastAnswer, "严迪", "yes", 0, "一天两次", "sdfwedwe", 0)
            cursor.execute(sql)
            db.commit()
            print("提交成功!!!!")
            x = Label(win, text="提交成功！",fg="blue", pady="5")
            x.pack(side=TOP)
        except Exception as e:
            print("---异常---：", e)
            t = Label(win, text=e, fg="red", pady="5")
            tt = Label(win, text="提交失败！", fg="red", pady="5")
            tt.pack()
            t.pack(side=TOP)
        # *****



app = App(win)
win.geometry('800x300')
win.mainloop()
# ***************

# print(ser.read())#读一个字节
# print(ser.read(10).decode("gbk"))#读十个字节
# print(ser.readline().decode("gbk"))#读一行
# print(ser.readlines())#读取多行，返回列表，必须匹配超时（timeout)使用
# print(ser.in_waiting)#获取输入缓冲区的剩余字节数
# print(ser.out_waiting)#获取输出缓冲区的字节数

# 寻卡指令02 00 00 04 47 04 4F 03
# 循环接收数据，此为死循环，可用线程实现
