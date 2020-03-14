import math
from random import randint, choice, sample, random
import time
import sys

# == Directory to save file to ==
save_directory = "data"
# 'judge' the alternative object 
# or 'select' all target object
mode = 'judge'
# == Trial variables ==
n_real = 120
n_prac = 20

# == Processing power or frames per second ==
FPS = 60

# Define the object class attributes
obj_radius = 35  # size of balls in pixels
num_distractor = 4  # number of distractor objects
num_targ = 4  # number of target objects
num_total = num_distractor + num_targ


# Define the speed range from min_spd to max_spd
# fix the speed if min_spd = None
min_spd = None
max_spd = 6

# Define the times and durations in SECONDS
fix_draw_time = Tfix = 1 # time to present fixation cross and objects

flash_time = Tfl = fix_draw_time + 1  # time for targets to flash

animation_time = Tani = flash_time + 5  # time for objects to move around in seconds


if mode == 'judge':
    answer_time = Tans = animation_time + 2
else:
    answer_time = Tans = animation_time + 6  # time limit to make answer
feedback_time = 1
"""
Define the project display window
"""
title = "Multiple Object Tracking Experiment"
# windows 下可自动获取分辨率
# 非windows用户请注释以下3行，自行设定相应的屏幕分辨率
# if not in Windows, comment 3 lines below and set the resolution manually 
import ctypes
user32 = ctypes.windll.user32
win_width, win_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# win_width, win_height = 2560, 1440  # pixels; width of screen

win_dimension = (win_width, win_height)

"""
Define instruction texts
"""

start_text = "屏幕上将出现位于中央的十字和 {dist:d} 个随机分布的圆点，请注视十\n" \
             "字。随后其中 {targ:d} 个会发生闪烁。\n" \
             "接着，十字将消失，所有圆点开始运动。请你跟踪发生过闪烁的 {targ:d} 个目标圆点。\n\n" \
             "当圆点停止运动，你将有 6 秒钟点击你跟踪的所有目标圆点，并\n" \
             "按空格键确认。\n\n" \
             "若已经准备好，请按 F 键继续。如有疑问请咨询实验人员。"\
    .format(dist=num_total, targ=num_targ)


fix_text = "首先你将看到这个十字，请注视它。 \n\n按 F 继续。"

present_text = "{total:d} 个圆点会随机分布在屏幕上。其中 {targ:d} 个会发生闪烁。\n" \
               "圆点停止闪烁后，十字消失时，所有圆点开始运动，请跟踪闪烁过\n"\
               "的目标圆点。" \
               "\n\n按 F 继续。"\
    .format(total=num_total, targ=num_targ)

submit_ans_txt = "当圆点停止运动请用鼠标选择你跟踪的目标圆点。\n" \
                 "你将有 {:d} 秒钟时间进行选择。\n\n" \
                 "按空格键提交你的选择\n" \
                 "目前为暂停状态，按 F 键继续".format(int(answer_time-animation_time))



prac_finished_txt = "练习结束\n\n若已经准备好，请按 F 键进入正式实验。\n" \
                    "请尽可能快地选择目标并提交选择。\n\n" \
                    "按 F 继续。".format(num_targ)
if mode == 'judge':
    start_text = "屏幕上将出现位于中央的十字和 {dist:d} 个随机分布的圆点，请注视十\n" \
                "字。随后其中 {targ:d} 个会发生闪烁。\n" \
                "接着，十字将消失，所有圆点开始运动。请你跟踪发生过闪烁的 {targ:d} 个目标圆点。\n\n" \
                "当圆点停止运动，请判断待定高亮圆点是否为目标圆点。\n" \
                "J 键表示是，K 键表示否。\n\n" \
                "若已经准备好，请按 F 键继续。如有疑问请咨询实验人员。"\
        .format(dist=num_total, targ=num_targ)
    
    submit_ans_txt = "当圆点停止运动，请判断待定高亮圆点是否为目标圆点。\n" \
                 "你将有 {:d} 秒钟时间进行选择。\n\n" \
                 "J 键表示是，K 键表示否。\n" \
                 "目前为暂停状态，按 F 键继续".format(int(answer_time-animation_time))

    prac_finished_txt = "练习结束\n\n若已经准备好，请按 F 键进入正式实验。\n" \
                    "请尽可能快地做出判断并按键。\n\n" \
                    "按 F 继续。".format(num_targ)

experim_fin_txt = "实验结束，感谢你参与。" \
                  "\n\n按 F 退出"

guide_fin_txt = "实验介绍结束，接下来将进入练习环节。\n" \
                "练习环节的流程与正式实验相同，但你的成绩不会被记录。练习\n结束后将进入正式实验。" \
                "\n\n按 F 进入练习环节。"

guide_submit_txt = "提交成功"

guide_timeup_txt = "时间到，实验将自动继续。"

exm_timeup_txt = "时间到，进入下一轮！"

need_select_txt = "请选 {targ:d} 个！".format(targ=num_targ)

# == Font size ==
large_font = 72
med_font = 42
small_font = 12

"""
Define some colours
"""
# == Greyscale ==
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREY = [128, 128, 128]
SLATEGREY = [112, 128, 144]
DARKSLATEGREY = [47, 79, 79]

# == Yellows ==
YELLOW = [255, 255, 0]
OLIVE = [128,128,0]
DARKKHAKI = [189,183,107]

# == Greens ==
GREEN = [0, 128, 0]
GREENYELLOW = [173, 255, 47]

RED = [220, 20, 60]

# == Define colors ==
background_col = GREY
hover_col = DARKSLATEGREY
click_col = GREENYELLOW
select_col = YELLOW


"""
Define session information for recording purposes
"""
session_info = {'Observer': '', 'Participant': sys.argv[1]}
date_string = time.strftime("%b_%d_%H%M", time.localtime())  # add the current time

