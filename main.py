import random
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, select
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# Database setup
engine = create_engine(DATABASE_URL, echo=False)

metadata = MetaData()


scores = Table(
    'scores',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('score', Integer, nullable=False),
    Column('created_at', DateTime, default=datetime.now)
)

metadata.create_all(engine)


def display_welcome_message():
    print('*** Welcome To Number Guesser ***')
    print('Choose which level you want to play:')
    print('1. Easy: Guess number between 1 to 100 with unlimited tries')
    print('2. Medium: Guess number between 1 to 100 with 10 tries')
    print('3. Hard: Guess number between 1 to 100 with 5 tries')
    print('4. Custom level')
    print('********************************************')


def get_user_choice():
    while True:
        try:
            choice = int(input('Enter your choice: '))
            if choice in [1, 2, 3, 4]:
                return choice
            else:
                print('Invalid choice. Please enter a valid option.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')


def set_level(choice):
    if choice == 1:
        return 100, float('inf')
    elif choice == 2:
        return 100, 10
    elif choice == 3:
        return 100, 5
    elif choice == 4:
        while True:
            try:
                range_limit = int(input('Enter the upper limit: '))
                max_tries = int(input('Enter the maximum number of tries: '))
                return range_limit, max_tries
            except ValueError:
                print('Invalid input. Please enter a valid number.')



def game_play(range_limit, max_tries):
    secret_number = random.randint(1, range_limit)
    tries = 0

    while True:
        try:
            guess = int(input(f'Guess the number between 1 and {range_limit}: '))
            tries += 1
            max_tries -= 1

            if guess == secret_number:
                print(f'Congratulations! You guessed the number in {tries} tries.')
                break
            elif guess < secret_number:
                print('Too low! Try again.')
                print(f'You have {max_tries} tries left.')
            elif guess > secret_number:
                print('Too high! Try again.')
                print(f'You have {max_tries} tries left.')
            else:
                print('Invalid input. Please enter a valid number.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')

        if max_tries == 0:
            print('Game over! You have no more tries left.')
            break

    return tries

def save_score(username, score):
    with engine.connect() as conn:
        conn.execute(scores.insert().values(username=username, score=score))
        conn.commit()


def calculate_score(tries):
    score = 1000 - (tries * 100)
    if score < 0:
        return 0
    return score


def get_highest_score():
    with engine.connect() as conn:
        result = conn.execute(select(scores).order_by(scores.c.score.desc()).limit(1))
        row = result.fetchone()
        return row.score if row else 0, row.username if row else 'Anonymous'




def main():
    while True:
        display_welcome_message()
        choice = get_user_choice()
        range_limit, max_tries = set_level(choice)
        tries = game_play(range_limit, max_tries)

        score = calculate_score(tries)
        print(f'Your score is {score}')
        highest_score, highest_score_username = get_highest_score()

        if score > highest_score:
            print('Congratulations! You have the highest score!')
            print(f'The highest score was {highest_score} by {highest_score_username}')
        try:
            username = input('Enter your username to save your score: ')
            save_score(username, score)
        except ValueError:
            print('Invalid input. Please enter a valid username.')

        

        try:
            play_again = input('Do you want to play again? (yes/no): ').lower()
            if play_again != 'yes':
                print('Thank you for playing!')
                break

        
        except ValueError:
            print('Invalid input. Please enter a valid option.')




if __name__ == '__main__':
    main()