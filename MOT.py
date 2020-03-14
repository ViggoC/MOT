import sys, os
from MOT_utils import *
from messagescreens import *

def guide_user(master_list, distractor_list, target_list):

    # -- Welcome message --
    guide_screen("start", master_list)
    wait_key()

    # -- Fixation cross screen
    guide_screen("focus", master_list)
    wait_key()

    # -- Present cross and circles screen
    guide_screen("present", master_list)
    wait_key()

    real_trials(master_list, distractor_list, target_list, 0, 1, round='guide')


def real_trials(master_list, distractor_list, target_list, CRT, n_trails, round='real', recorder=None):
    """function for real trials to record answer score, time and timed out state; same as practice trial except
    the user responses are recorded"""

    completed_practice_trial_count = CRT

    reset = False
    submitted = False
    need_to_select_4 = False
    timeup = False
    wait_ans = False
    t_pause = 0
    t0 = pg.time.get_ticks()
    candi = choice(master_list)
    label = 1 if candi in target_list else 0
    while True:
        pg.time.Clock().tick_busy_loop(FPS)  # =Set FPS

        win.fill(background_col)  # =fill background with background color
        mx, my = pg.mouse.get_pos()  # =get x and y coord of mouse cursor on window

        selected_list = []  # - list for all selected objects
        selected_targ = []  # - list for all SELECTED TARGETS

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if wait_ans:
                    t_keypress = pg.time.get_ticks() - t_pause
                    if event.key == pg.K_j:
                        response = 1
                        submitted = True
                    if event.key == pg.K_k:
                        response = 0
                        submitted = True

        t1 = pg.time.get_ticks() - t_pause
        dt = (t1 - t0)/1000

        if completed_practice_trial_count < n_trails:
            if not reset:
                if dt <= Tfix:
                    fixation_screen(master_list)
                elif Tfix < dt <= Tfl:
                    flash_targets(distractor_list, target_list)
                elif Tfl < dt <= Tani:
                    for targ in target_list:
                        targ.state_control("neutral")
                    animate(distractor_list, target_list, master_list)
                elif Tani < dt <= Tans:
                    candi.state_control("selected")
                    wait_ans = True
                    static_draw(master_list)
                    pg.display.flip()
                    if round == 'guide':
                        round = None
                        guide_screen("answer", master_list)
                        pause_start = pg.time.get_ticks()
                        wait_key() 
                        t_pause = pg.time.get_ticks()-pause_start
                    # t_stop = pg.time.get_ticks()
                elif Tans < dt:
                    timeup = True

            if submitted:
                win.fill(background_col)
                msg = 'Right' if response == label else 'Wrong'
                msg_to_screen_centered(msg, BLACK, large_font)
                if recorder:
                    t_sub = ((t_keypress - t0)/1000) - animation_time
                    # record_response(t_sub, correct, False, recorder)
                    record_response_judge(t_sub,response,label, False, recorder)
                pg.display.flip()
                wait_time = int(Tans*1000 - (t_keypress - t0) + 1000)
                delay(wait_time)
                reset = True

            if timeup:
                if recorder:
                    record_response_judge(Tans-Tani, -1, label, True, recorder)
                message_screen("timeup")
                delay(feedback_time*1000)
                reset = True

            if reset:
                print(completed_practice_trial_count)
                candi = choice(master_list)
                label = 1 if candi in target_list else 0
                init_pos(master_list)
                for obj in master_list:
                    obj.state_control("neutral")
                completed_practice_trial_count += 1
                submitted = timeup = wait_ans = reset = False
                t_pause = 0
                t0 = pg.time.get_ticks()

        else:
            win.fill(background_col)
            if round == 'real':
                recorder.close()
                message_screen("exp_finished")
            elif round == 'prac':
                message_screen("prac_finished")
            else:
                guide_screen("finished", master_list)
            pg.display.flip()
            wait_key()
            break



def main():
    """Main loop"""

    # == Variables to count how many trials have been completed ==
    completed_real_trials = 0
    completed_practice_trials = 0

    # == Generate a list of objects ==
    list_d, list_t = generate_list(WHITE)
    list_m = list_d + list_t
    init_pos(list_m)
    # == Dialogue box to enter participant information ==
    # dlg_box = DlgFromDict(session_info, title="Multiple Object Tracking", fixed=["date"])

    print(session_info)

    # == Prepare a CSV file ==
    mot_log = date_string + ' pcpnt_' + session_info['Participant']
    save_file = os.path.join(save_directory + "\\" + mot_log + '.csv')
    log = open(save_file, 'w')
    header = ["response_time", "response", "label", "timed_out"]
    delim = ",".join(header)
    delim += "\n"
    log.write(delim)

    # == Initiate pygame ==
    pg.init()

    # == Start guide ==
    guide_user(list_m, list_d, list_t)

    # == Start practice ==
    real_trials(list_m, list_d, list_t, completed_practice_trials, n_prac, 'prac')

    # == Start real trials, recording responses ==
    real_trials(list_m, list_d, list_t, completed_real_trials, n_real, 'real', log)
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
