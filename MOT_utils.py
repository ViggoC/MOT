import pygame as pg
from MOT_constants import  *
from MOTobj import MOTobj



# Generate random x and y coordinates within the window boundary
boundary_location = ['up', 'down', 'left', 'right']
boundary_coord = [obj_radius, (win_height - obj_radius + 1), obj_radius, (win_width - obj_radius + 1)]
boundary = dict(zip(boundary_location, boundary_coord))

def init_pos(mlist):
    k = len(mlist)
    x_list = sample([n for n in range(int(boundary["left"]+1), int(boundary["right"]-1), obj_radius*2)], k=k)
    y_list = sample([n for n in range(int(boundary["up"]+1), int(boundary["down"]-1), obj_radius*2)], k=k)
    for i in range(k):
        mlist[i].set_position((x_list[i], y_list[i]))
        mlist[i].shuffle_speed()


def generate_list(color):
    """function to generate new list of objects"""
    distractor_list = []
    for nd in range(num_distractor):
        d = MOTobj()
        distractor_list.append(d)

    target_list = []
    for nt in range(num_targ):
        t = MOTobj(color)
        target_list.append(t)

    return distractor_list, target_list


def delay(t):
    """function to stop all processes for a time"""
    pg.time.delay(t)  # multiply by a thousand because the delay function takes milliseconds


def record_response(response_time, response_score, time_out_state, log):
    # record the responses
    header_list = [response_time, response_score, time_out_state]
    # convert to string
    header_str = map(str, header_list)
    # convert to a single line, separated by commas
    header_line = ','.join(header_str)
    header_line += '\n'
    log.write(header_line)

def record_response_judge(response_time, response, label, time_out_state, log):
    # record the responses
    header_list = [response_time, response, label, time_out_state]
    # convert to string
    header_str = map(str, header_list)
    # convert to a single line, separated by commas
    header_line = ','.join(header_str)
    header_line += '\n'
    log.write(header_line)