import requests, random, os
from dotenv import load_dotenv

def check_word_exists(word: str, app_key: str) -> bool:
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={app_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Check if the first item in the response is a dictionary with a 'meta' key
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and 'meta' in data[0]:
            return True
        else:
            return False
    elif response.status_code == 404:
        return False
    else:
        response.raise_for_status()

def word_guess(limit = 6):
    game_dic = {"status": False, "attempt": 0, "message": "You have guessed wrong, try again.", "letters_in": [], "letters_out": [], "actual_word": word}
    check = input("\nWould you like to play a game of word guess?\n\n")
    if check.lower() == "yes":
        print(f"\nGuess a 5 letter word, you get 6 attempts.\n")
        while True:
            game(game_dic, limit)
            if game_dic["status"]:
                print(game_dic["message"])
                re_check = input("\nWould you like to play again?\n")
                if re_check.lower() == "yes":
                    word_guess()
                else:
                    print("\nThanks for playing, see you again!")
                    return
            elif game_dic["status"] == False and game_dic["attempt"] >= limit:
                print(f"\nYou have used up your chances. The correct word is {word}, would you like to start a new game?")
                status = input()
                if status.lower() == "yes":
                    word_guess()
                else:
                    print("\nThanks for playing, see you again!")
                    return
            else:
                print(game_dic["message"])
            # print(game_dic)
    else:
        print("Maybe next time.")

def valid_input(input):
    if len(input) != 5:
        return False
    for char in input:
        if ord(char) not in range(97, 122):
            return False
    if not check_word_exists(input, app_key):
        print("Could not find this word!")
        return False
    return True

def game(game_dic, limit):
    guessd_word = input(f"You have {limit - game_dic['attempt']} attempts left.\n\n")
    if not valid_input(guessd_word.lower()):
        game_dic["status"] = False
        game_dic["message"] = "\nNot a valid word, guess again."
        return game_dic
    if guessd_word.lower() == game_dic["actual_word"]:
        game_dic["status"] = True
        game_dic["attempt"] += 1
        game_dic["message"] = f"\nCongradulation you have completed the challenge with {game_dic['attempt']} attempts!!!"
        return game_dic
    else:
        for char in guessd_word.lower():
            if char not in game_dic["actual_word"]:
                game_dic["letters_out"].append(char)
            elif char not in game_dic["letters_in"]:
                game_dic["letters_in"].append(char)
        game_dic["attempt"] += 1
        print(f"""
Attempts:   {game_dic['attempt']}\n
Letters not in the word:    {game_dic['letters_out']}\n
Letters in the word:    {game_dic['letters_in']}\n""")

def get_five_letter_words():
    url = "https://api.datamuse.com/words"
    params = {
        "sp": "?????",  # 5-letter words
        "max": 10,    # you can adjust the number of results as needed
        "md": "p"       # metadata to include parts of speech
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        words = response.json()
        # Filter out phrases, keeping only single words
        single_words = [word['word'] for word in words if ' ' not in word['word']]
        return single_words[random.randint(0,len(single_words)-1)]
    else:
        response.raise_for_status()

load_dotenv()
app_key = os.getenv('APP_KEY')
word = get_five_letter_words()

word_guess()