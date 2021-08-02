import os

from hstest.check_result import CheckResult
from hstest.exceptions import WrongAnswerException
from hstest.stage_test import StageTest
from hstest.test_case import TestCase

MAIN_MENU = """
1. Add flashcards
2. Practice flashcards
3. Exit"""
SUB_MENU = """
1. Add a new flashcard
2. Exit"""
FIRST_QUESTION = "What is the Capital city of Germany?"
FIRST_ANSWER = "Berlin"
SECOND_QUESTION = "What is the Capital city of Italy?"
SECOND_ANSWER = "Rome"
Q_S = 'Please press "y" to see the answer or press "n" to skip:'
if os.path.exists('flashcard.db'):
    os.remove('flashcard.db')


class FlashCardTest(StageTest):
    def generate(self):
        return [TestCase(stdin=[self.test1_input1,
                                self.test1_input2,
                                self.test1_input3,
                                self.test1_input4,
                                self.test1_input5,
                                self.test1_input6,
                                self.test1_input7,
                                self.test1_input8,
                                self.test1_input9,
                                self.test1_input10,
                                self.test1_input11,
                                self.test1_input12,
                                ])
            , TestCase(stdin=[self.test2_input1,
                              self.test2_input2,
                              self.test2_input3])
            , TestCase(stdin=['1',
                              '4',
                              self.test3_input1,
                              self.test3_input2])
            , TestCase(stdin=['1',
                              '1',
                              ' ',
                              self.test4_input4,
                              self.test4_input5])
            , TestCase(stdin=['1',
                              '1',
                              'What is the capital city of Peru?',
                              ' ',
                              self.test5_input5,
                              self.test5_input6])
            , TestCase(stdin=['2',
                              self.test1_input10,
                              self.test1_input11,
                              self.test1_input12
                              ])]

    def check_main_menu(self, out):
        main_menu_list = MAIN_MENU.strip().split('\n')
        out_list = out.strip().split('\n')
        if len(out_list) > 4 or len(out_list) < 3:
            raise WrongAnswerException(f'The main menu has "3" lines and it must be like this:\n{MAIN_MENU}')
        for index, action in enumerate(main_menu_list):
            if not action == out_list[index]:
                raise WrongAnswerException(f'the line no.{index + 1} of main menu must be like this:\n {action}')
        return True

    def check_sub_menu(self, out):
        sub_menu_list = SUB_MENU.strip().split('\n')
        out_list = out.strip().split('\n')
        if len(out_list) > 3 or len(out_list) < 2:
            raise WrongAnswerException(f'The sub_menu has "2" lines and it must be like this:\n{SUB_MENU}')
        for index, content in enumerate(sub_menu_list):
            if not content == out_list[index]:
                raise WrongAnswerException(f'The line no.{index + 1} must be like this:\n{sub_menu_list[index]}')
        return True

    def check_question(self, out):
        if not "Question:" in out:
            raise WrongAnswerException(f'the word {out} spelling is wrong, it should be like this:\nQuestion:')
        return True

    def check_answer(self, out):
        if not "Answer:" in out:
            raise WrongAnswerException(f'the word {out} spelling is wrong it should be like this:\nAnswer:')
        return True

    def check_practice_question(self, out, question):
        out_list = out.strip().split('\n')
        out_first_line = out_list[0].split(':')
        if not 'Question' == out_first_line[0]:
            raise WrongAnswerException(f'{out_first_line[0]} is wrong!\nplease check extra spaces, misspelling or ":"')
        if not question == out_first_line[1].strip():
            raise WrongAnswerException('wrong question is printed')
        if not Q_S == out_list[1]:
            raise WrongAnswerException(f'{out_list[1]} is wrong\n{Q_S} is correct')
        return True

    def check_practice_answer(self, out, answer):
        out_list = out.strip().split('\n')
        first_part = out_list.pop(0).strip().split(':')
        if not 'Answer' == first_part[0]:
            raise WrongAnswerException('Answer:\n is missing or misspelling!')
        if not answer == first_part[1].strip():
            raise WrongAnswerException('The answer is not printed correctly')
        if Q_S.strip() in out_list:
            return True
        raise WrongAnswerException(f'{Q_S}\n should be printed after answer')

    def test1_input1(self, out):
        if not os.path.exists("flashcard.db"):
            raise WrongAnswerException("Please, make sure that your program creates a database and names it \"flashcard\".")
        if self.check_main_menu(out):
            return '1'

    def test1_input2(self, out):
        if self.check_sub_menu(out):
            return '1'

    def test1_input3(self, out):
        if self.check_question(out):
            return FIRST_QUESTION

    def test1_input4(self, out):
        if self.check_answer(out):
            return FIRST_ANSWER

    def test1_input5(self, out):
        if self.check_sub_menu(out):
            return '1'
        # if result == 1 or result == 2:
        #     raise WrongAnswerException('after entering answer the sub_menu must be printed')

    def test1_input6(self, out):
        if self.check_question(out):
            return SECOND_QUESTION

    def test1_input7(self, out):
        if self.check_answer(out):
            return SECOND_ANSWER

    def test1_input8(self, out):
        if self.check_sub_menu(out):
            return '2'
        # if result == 1 or result == 2:
        #     raise WrongAnswerException('after entering answer the sub_menu must be printed')

    def test1_input9(self, out):
        if self.check_main_menu(out):
            return '2'
        # if result == 1 or result == 2:
        #     raise WrongAnswerException('by press no.2 it should return to main menu')

    def test1_input10(self, out):
        if self.check_practice_question(out, FIRST_QUESTION):
            return 'y'

    def test1_input11(self, out):
        question = out.strip().split('\n')
        if len(question) == 0:
            raise WrongAnswerException("The output can't be empty")
        else:
            question.pop(0)
            question = '\n'.join(question)
            if self.check_practice_question(question.strip(), SECOND_QUESTION):
                if self.check_practice_answer(out, FIRST_ANSWER):
                    return 'n'

    def test1_input12(self, out):
        if self.check_main_menu(out.strip()):
            return '3'

    def check(self, reply: str, attach):
        all_output = reply.strip().split('\n')
        if not 'Bye!' == all_output[-1]:
            raise WrongAnswerException('Bye! is missing or misspelling!')
        return CheckResult.correct()

    def test2_input1(self, out):
        if self.check_main_menu(out):
            return '5'

    def test2_input2(self, out):
        out_list = out.strip().split('\n')
        if len(out_list) < 2:
            raise WrongAnswerException("The output is not printed correctly")
        else:
            if not out_list[0] == '5 is not an option':
                raise WrongAnswerException('5 is not an option\nshould be printed in output')
            out_list.pop(0)
            if self.check_main_menu('\n'.join(out_list)):
                return 'we'

    def test2_input3(self, out):
        out_list = out.strip().split('\n')
        if len(out_list) < 2:
            raise WrongAnswerException("The output is not printed correctly")
        else:
            if not out_list[0] == 'we is not an option':
                raise WrongAnswerException('we is not an option\nshould be printed')
            out_list.pop(0)
            if self.check_main_menu('\n'.join(out_list)):
                return CheckResult.correct()

    def test3_input1(self, out):
        out_list = out.strip().split('\n')
        if len(out_list) < 2:
            raise WrongAnswerException("The output is not printed correctly")
        else:
            if not out_list[0] == '4 is not an option':
                raise WrongAnswerException('4 is not an option\nshould be printed')
            out_list.pop(0)
            if self.check_sub_menu('\n'.join(out_list)):
                return 'Rome'

    def test3_input2(self, out):
        out_list = out.strip().split('\n')
        if len(out_list) < 2:
            raise WrongAnswerException("The output is not printed correctly")
        else:
            if not out_list[0] == 'Rome is not an option':
                raise WrongAnswerException('Rome is not an option\nshould be printed')
            out_list.pop(0)
            if self.check_sub_menu('\n'.join(out_list)):
                return CheckResult.correct()

    def test4_input4(self, out):
        output = out.strip().split('\n')
        if not 'Question:' in output:
            raise WrongAnswerException("the question can't be empty!")
        return ''

    def test4_input5(self, out):
        output = out.strip().split('\n')
        if not 'Question:' in output:
            raise WrongAnswerException("the question can't be empty!")
        return CheckResult.correct()

    def test5_input5(self, out):
        output = out.strip().split('\n')
        if not 'Answer:' in output:
            raise WrongAnswerException("the answer can't be empty!")
        return ''

    def test5_input6(self, out):
        output = out.strip().split('\n')
        if not 'Answer:' in output:
            raise WrongAnswerException("the answer can't be empty!")
        return CheckResult.correct()


if __name__ == '__main__':
    FlashCardTest().run_tests()
