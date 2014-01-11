#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
蘇武牧羊
Persi Diaconis "Magical Mathematics" によると、
『中外戯法図説』という本に収録されていた
とのこと
"""

import sys

def prompt_for_input(prompt = ""):
    sys.stdout.write(prompt)
    return sys.stdin.readline().strip()

def ask_yes_or_no(message):
    res = prompt_for_input(message)
    res = res.lower()
    if res in ("y", "yes", "1", "true", "t"):
        return True
    elif res in ("n", "no", "0", "false", "f"):
        return False
    raise ValueError, "A yes or no response is required"

class SoBuBokuYou:
    def __init__(self,):
        self.chars = {
            1: "平", #flat
            2: "求", #search
            3: "王", #king
            4: "元", #formerly
            5: "斗", #pint
            6: "非", #non-
            7: "半", #half
            8: "米", #rice
        }

        self.question_target_chars = {
            1: [3,4,7,8], # 王、元、半、米
            2: [1,2,3,4], # 平、求、王、元
            3: [1,3,5,7], # 平、王、斗、半
        }

        self.pic = SoBuBokuYouPicture()
        self.QA = SoBuBokuYouQA()

    def map_answers_to_int(self, answers):
        res = 0
        if answers[1] == True:
            res += pow(2,1)
        if answers[2] == False:
            res += pow(2,2)
        if answers[3] == False:
            res += pow(2,0)
        # [0, 7] to [1, 8]
        res += 1
        return res

    def show_answer(self, answer_int):
        answer_int = int(answer_int)
        sys.stdout.write("あなたの選んだ文字は %s です！！\n" %self.chars[answer_int])
        return

    def update_answer_picture(self, ith_question, answer):
        self.pic.update(ith_question, answer)
    def finalize_answer_picture(self, answer_int):
        answer_int = int(answer_int)
        self.pic.finalize(answer_int)
    def output_answer_picture(self,):
        self.pic.output()

    def ask_first_question(self,):
        return self.QA.ask_first_question(self.chars)
    def ask_questions(self, ith_question):
        question_target_chars = self.question_target_chars[ith_question]
        return self.QA.ask_questions(self.chars, question_target_chars)
    def ask_final_question(self,):
        return self.QA.ask_final_question()

class SoBuBokuYouQA:
    def __init__(self,):
        return
    def ask_first_question(self, chars):
        answer = False
        while answer == False:
            sys.stdout.write("以下のうちから一文字選んでください:\n")
            for i,c in chars.items():
                sys.stdout.write("%s\n" %c)
            sys.stdout.write("\n")
            answer = ask_yes_or_no("決めましたか？ (y/n)\n")
        return answer
    def ask_questions(self, chars, question_target_chars):
        sys.stdout.write("あなたが選んだ文字はこの中にありますか？\n")
        for ith_char in question_target_chars:
            sys.stdout.write("%s\n" %chars[ith_char])
        answer = ask_yes_or_no("(y/n)\n")
        return answer
    def ask_final_question(self,):
        answer = ask_yes_or_no("あなたの選んだ文字はこれですか？ (y/n)\n")
        return answer

class SoBuBokuYouPicture:
    def __init__(self, row_num = 13, col_num = 15):
        self.row_num = row_num
        self.col_num = col_num
        self.init_picture()

        # i番目の質問でこの行を更新する
        self.target_row = {
            1: 5,
            2: 2,
            3: 8,
        }
        # この列を更新する（白く塗りつぶす）
        self.target_col = {
            True: [2,3,4,5,6,7,8,9,10,11,12], # answer = y の場合
            False:  [3,4,          10,11],    # answer = n の場合
        }
        # 最後にこの列を直線で塗りつぶす
        self.final_target = {
            1:{
                "r": range(2, self.row_num),
                "c": [7],
                },
            2:{
                "r": range(self.row_num -2),
                "c": [7],
                },
            3:{
                "r": range(3, self.row_num -4),
                "c": [7],
                },
            4:{
                "r": range(5,self.row_num -4),
                "c": [4,10],
                },
            5:{
                "r": range(self.row_num -1),
                "c": [10,11],
                },
            6:{
                "r": range(self.row_num -1),
                "c": [5,9],
                },
            7:{
                "r": range(self.row_num -1),
                "c": [7],
                },
            8: {
                "r": range(1, self.row_num -2),
                "c": [7],
                },
        }
        return

    def init_picture(self,):
        self.picture = {}
        for i in range(self.row_num):
            self.picture[i] = "#" * self.col_num

    def update(self, ith_question, answer):
        target_col = self.target_col[answer]
        target_row = self.target_row[ith_question]
        new_row = ""
        for c in range(self.col_num):
            if c in target_col:
                new_row += " "
            else:
                new_row += "#"
        self.picture[target_row] = new_row

    def finalize(self, answer_int):
        target = self.final_target[answer_int]
        for r in range(self.row_num):
            new_row = ""
            for c in range(self.col_num):
                if c in target["c"] and r in target["r"]:
                    new_row += " "
                else:
                    new_row += self.picture[r][c]
            self.picture[r] = new_row
        return

    def output(self,):
        sys.stdout.write("\n")
        for i, row in self.picture.items():
            sys.stdout.write("[%02d] %s\n" %(i,row))
        sys.stdout.write("\n")

def main():
    sbby = SoBuBokuYou()
    # 選んでもらう
    sbby.ask_first_question()
    sbby.output_answer_picture()

    # 3つの質問
    answers = {}
    for ith_question in range(1, 3+1):
        answer = sbby.ask_questions(ith_question)
        answers[ith_question] = answer
        sbby.update_answer_picture(ith_question, answer)
        sbby.output_answer_picture()

    # 最後に
    answer_int = sbby.map_answers_to_int(answers)
    sbby.show_answer(answer_int)
    
    sbby.finalize_answer_picture(answer_int)
    sbby.output_answer_picture()
    answer = sbby.ask_final_question()
    if answer == True:
        sys.stdout.write("Grazie!!")
    else:
        sys.stdout.write("Noooooo!!")

if __name__ == '__main__':
    main()
