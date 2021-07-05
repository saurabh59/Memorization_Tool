# write your code here
def main_menu():
    while True:
        print("""1. Add flashcards
2. Practice flashcards
3. Exit""")
        option = input()
        try:
            option = int(option)
            if option == 1:
                print()
                sub_menu()
            elif option == 2:
                practice_questions(bank)
            elif option == 3:
                print("Bye!")
                break
            else:
                print(f'{option} is not an option')
        except ValueError:
            print(f"{option} is not an option")


def sub_menu():
    while True:
        print("""1. Add a new flashcard
2. Exit""")
        i = input()
        try:
            i = int(i)
            if i == 1:
                add(bank)
            elif i == 2:
                break
            else:
                print(f'{i} is not an option')
        except ValueError:
            print(f'{i} is not an option')


def practice_questions(a_dict):
    if a_dict:
        for key, value in a_dict.items():
            print()
            print(f'Question: {key}')
            choice = input('Please press "y" to see the answer or press "n" to skip:')
            if choice == 'y':
                print()
                print(f'Answer: {value}')
            elif choice == 'n':
                continue
            else:
                print(f'{choice} is not an option')
    else:
        print('There is no flashcard to practice!')


def add(b_dict):
    print()
    print("Question:")
    question = input()
    while not question:
        print("Question:")
        question = input()
    print()
    print("Answer:")
    answer = input()
    while not answer:
        print("Answer:")
        answer = input()
    b_dict[question] = answer


bank = {}

main_menu()