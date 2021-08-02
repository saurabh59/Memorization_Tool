from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)


Base.metadata.create_all(engine)


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
                practice_questions()
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
                add()
            elif i == 2:
                break
            else:
                print(f'{i} is not an option')
        except ValueError:
            print(f'{i} is not an option')


def practice_questions():
    result_list = session.query(flashcard).all()
    if result_list:
        counter = 0
        for _x in result_list:
            print()
            print(f'Question: {result_list[counter].question}')
            choice = input('Please press "y" to see the answer or press "n" to skip:')
            if choice == 'y':
                print()
                print(f'Answer: {result_list[counter].answer}')
                counter += 1
            elif choice == 'n':
                counter += 1
                continue
            else:
                print(f'{choice} is not an option')
    else:
        print('There is no flashcard to practice!')


def add():
    print()
    print("Question:")
    question = input()
    while question.isspace() or not question:
        print("Question:")
        question = input()
    print()
    print("Answer:")
    answer = input()
    while answer.isspace() or not answer:
        print("Answer:")
        answer = input()
    new_data = flashcard(question=question, answer=answer)
    session.add(new_data)
    session.commit()


main_menu()