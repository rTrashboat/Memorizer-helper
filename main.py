import os
import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import random
import os

def Memorize_lesson_func(chosen_lesson):
    correct_words_string = ""
    wrong_words_string = ""
    missing_words_string = ""
    memorize_lesson_layout = [
        [sg.Multiline("",expand_x= True, key = "input_memorizelesson",size = (80,15))],
        [sg.Button("Check", expand_x = True, key = "button_check")],
        [sg.Text("Correct words: N/A", key = "text_correct")],
        [sg.Text("Wrong words: N/A", key = "text_wrong")],
        [sg.Text("Missing words: N/A", key = "text_missing")]
    ]
    memorize_lesson_window = sg.Window('Memorizer helper', memorize_lesson_layout, finalize = True)
    sealed = False
    while True:
        event, values = memorize_lesson_window.read()
        if event == "button_check":
            correct_words = []
            correct_words_string = ""
            wrong_words_string = ""
            missing_words_string = ""
            memorize_attempt = values["input_memorizelesson"].lower()
            memorize_attempt_list = list(memorize_attempt.split(" "))
            chosen_lesson_list = list(chosen_lesson.split(" "))
            print(chosen_lesson_list)
            if memorize_attempt_list == chosen_lesson_list:
                print("cool")
            for lesson_word in chosen_lesson_list:
                print(lesson_word) 
                for memorized_word in memorize_attempt_list:
                    if lesson_word == memorized_word:
                        #print(lesson_word)
                        correct_words.append(lesson_word)
            for correct_word in correct_words:
                chosen_lesson_list.remove(correct_word)
                memorize_attempt_list.remove(correct_word)
                correct_words_string += f"{correct_word}, "
            
            for wrong_word in memorize_attempt_list:
                wrong_words_string += f"{wrong_word}, "

            for missing_word in chosen_lesson_list:
                missing_words_string += f"{missing_word}, "


            if correct_words_string:
                memorize_lesson_window["text_correct"].update(f"Correct words: {correct_words_string}")
            else : memorize_lesson_window["text_correct"].update(f"Correct words: None );")

            if correct_words_string:
                memorize_lesson_window["text_wrong"].update(f"Wrong words: {wrong_words_string}")
            else : memorize_lesson_window["text_wrong"].update(f"Wrong words: None ;)")

            if correct_words_string:
                memorize_lesson_window["text_missing"].update(f"Missing words: {missing_words_string}")
            else : memorize_lesson_window["text_missing"].update(f"Missing words: None ;)")

            print(f"Correct words:{correct_words}")
            print(f"Wrong words:{memorize_attempt_list}")
            print(f"missing words:{chosen_lesson_list}")



        if event == sg.WIN_CLOSED:
            memorize_lesson_window.close()
            sealed = True
            break
    if not sealed:
        main_thing()

def Read_lesson_func(chosen_lesson):
    read_lesson_layout = [
        [sg.Text(str(chosen_lesson))],
        [sg.Button("Memorize", expand_x = True, key = "Button_memorize")],
        [sg.Button("Go back", expand_x = True, key = "Button_back")]
    ]
    sealed = True
    read_lesson_window = sg.Window('Memorizer helper', read_lesson_layout, finalize = True)
    while True:
        event, values = read_lesson_window.read()
        
        if event == "Button_memorize":
            sealed = False
            goback = False
            memorize = True
            read_lesson_window.close()
            break

        if event == "Button_back":
            sealed = False
            goback = True
            memorize = False
            read_lesson_window.close()
            break

        if event == sg.WIN_CLOSED:
            read_lesson_window.close()
            sealed = True
            break
    if not sealed:
        if goback:
            main_thing()
        elif memorize:
            Memorize_lesson_func(chosen_lesson)


def New_lesson_func():
    new_lesson_layout = [
        [sg.Text("New lesson!",expand_x = True, justification = "center", key = "text_newlesson")],
        [sg.Text("Title :",expand_x = True, justification = "left")],
        [sg.Input("", expand_x = True, key = "input_title")],
        [sg.Text("Lesson :",expand_x = True, justification = "left")],
        [sg.Multiline("",expand_x= True, key = "input_lesson",size = (80,15))],
        [sg.Button("Save",expand_x= True, key = "button_save")]
    ]
    new_lesson_window = sg.Window('Memorizer helper', new_lesson_layout, finalize = True)
    sealed = False

    while True:
        event, values = new_lesson_window.read()
        if event == "button_save":
            new_lesson_title = values["input_title"]
            new_lesson_core = values["input_lesson"]
            Save_data(f"{new_lesson_title}/{new_lesson_core}")
            break
        if event == sg.WIN_CLOSED:
            sealed = True
            break
    new_lesson_window.close()
    if not sealed:
        main_thing()

def Save_data(data):
    try:
        saved_data = open(f"dataenclosure/data.bin", "a")
    except Exception:
        saved_data = open(f"dataenclosure/data.bin", "w")
    saved_data.write((str(data) + ",").lower())
    saved_data.close()

def overwrite(data):
    saved_data = open(f"dataenclosure/data.bin", "w")
    saved_data.write((str(data)).lower())
    saved_data.close()

def main_thing():
    sg.theme('DarkTeal1')
    try:
        sg.set_options(font = ("qualy",16), icon = "dataenclosure/icon.ico")
    except Exception:
        pass
    try:
        loaded_data = open(f"dataenclosure/data.bin", "r")
    except FileNotFoundError:
        loaded_data = open(f"dataenclosure/data.bin", "w")
        loaded_data.close()
        loaded_data = open(f"dataenclosure/data.bin", "r")
    loaded_data = loaded_data.read()
    layout = [
        [sg.Text("Choose a lesson to memorize or make a new one!",expand_x = True, justification = "center")],
        [sg.Button("+", expand_x = True, key = "Add_button")]
    ]
    choosing_window = sg.Window('Memorizer helper', layout, finalize = True)
    lessons = list(loaded_data.split(","))
    cycles = 0
    sealed = True
    New_lesson = False
    Read_lesson = False
    for lesson in lessons:
        if lesson:
            lesson = list(lessons[cycles].split("/"))
            cycles += 1
            lesson_element = sg.Button(f"{lesson[0]}",expand_x=True, key = int(cycles))
            remove_elemnt = sg.Button(f"❌", key = f"R{cycles}")
            lesson_list = [[lesson_element,remove_elemnt]]
            choosing_window.extend_layout(choosing_window,lesson_list)
    cycles = 0
    
    while True:
        event, values = choosing_window.read()
        if event == "Add_button":
            sealed = False
            New_lesson = True
            Read_lesson = False
            break
        if isinstance(event, int):
            lesson_number = event - 1
            chosen_lesson_list = list(lessons[lesson_number].split("/"))
            chosen_lesson = chosen_lesson_list[1]
            sealed = False
            New_lesson = False
            Read_lesson = True
            break
        try:
            if event[0] == "R":
                rawdata = open("dataenclosure/data.bin", "r")
                rawdata_text = rawdata.read()
                removed_string_number = int(event[1]) - 1
                removed_string = lessons[removed_string_number]
                rawdata_text =rawdata_text.replace(f"{removed_string},", "")
                rawdata.close()
                overwrite(rawdata_text)
                sealed = False
                break
        except TypeError:
            print("TypeError")

        if event == sg.WIN_CLOSED:
            break
    choosing_window.close()
    if not sealed:
        if New_lesson:
            New_lesson_func()
        elif Read_lesson:
            Read_lesson_func(chosen_lesson)
        else:
            main_thing()

if __name__ == '__main__':
    main_thing()