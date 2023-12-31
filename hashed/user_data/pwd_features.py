import requests
import hashlib
import re
import secrets
import string


def shuffle_string(s):  # Fisher-Yates shuffle algo
    alphabet = list(s)
    for i in range(len(alphabet)):
        j = secrets.randbelow(i + 1)
        alphabet[i], alphabet[j] = alphabet[j], alphabet[i]
    return "".join(alphabet)


def get_random_pass(pwd_length, nos, symbols):
    # Generating random password
    if pwd_length < 6:
        return Exception("Error : Minimum length should be 6")
    limit = pwd_length // 5
    limit_no = 0
    limit_sym = 0
    if nos == True:
        # add nos <= 20% of length
        limit_no = 1 + secrets.randbelow(limit)
        pwd_length = pwd_length - limit_no

    if symbols == True:
        # add symbols <= 20% of length
        limit_sym = 1 + secrets.randbelow(limit)
        pwd_length = pwd_length - limit_sym

    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    pwd = ""
    while True:  # ensure one upper and lowercase letters
        for i in range(pwd_length):
            pwd += "".join(secrets.choice(letters))
        if any(c.islower() for c in pwd) and any(c.isupper() for c in pwd):
            break
    for i in range(limit_no):
        pwd += "".join(secrets.choice(digits))
    for i in range(limit_sym):
        pwd += "".join(secrets.choice(special_chars))
    # shuffle the pwd randomly
    pwd = shuffle_string(pwd)
    return pwd


def hackify(text):  # replace few characters with nos
    leet_dict = {
        "a": "4",
        "A": "4",
        "e": "3",
        "E": "3",
        "o": "0",
        "O": "0",
        "s": "5",
        "S": "5",
    }
    return "".join(leet_dict.get(char, char) for char in text)


def get_pass(num, caps, cryptify):
    # generate memorable password
    api = "https://random-word-api.herokuapp.com/word"
    parameters = {"number": num}
    response = requests.get(f"{api}", params=parameters)
    if response.status_code != 200:
        return Exception("Error in fetching data")
    else:
        result = response.json()
        s = ""
        for i in range(num - 1):
            if caps == True:  # capitalize first letter
                result[i] = result[i].capitalize()
            s += result[i] + "-"
        if caps == True:
            result[num - 1] = result[num - 1].capitalize()
        s += result[num - 1]
        if cryptify == True:
            s = hackify(s)
        return s


def check_password_pwned(password):  # check breach data
    if len(password) == 0:
        return "No Password Entered"
    # Hash the password using SHA-1 hash algorithm
    sha1_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    # call the api with first 5 characters
    api_url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(api_url)
    if response.status_code == 200:
        for line in response.text.splitlines():
            if line.startswith(suffix):  # search for entered pwd in response
                count = int(line.split(":")[1])
                return f"The password has been found {count} times and is compromised."
        return "The password has not been found in any known breaches."
    elif response.status_code == 404:
        return "Invalid API endpoint or no data found."
    else:
        return "Error occurred while checking the password."


def password_strength(password):  # Patterns to find pwd strength
    weak_pattern = r"^(?=.*[a-zA-Z])(?=.*\d).{6,}$"
    weak2 = r"^(?=.*[a-zA-Z])(?=.*[\W]).{6,}$"
    medium_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
    medium2 = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,}$"
    medium3 = r"^(?=.*[a-zA-Z])(?=.*[\W])(?=.*\d).{8,}$"
    strong_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W]).{8,}$"
    possibly_strong = r"^.{20,}$"

    if len(password) == 0:
        return "Invalid"
    elif re.match(strong_pattern, password):
        return "Strong"
    elif re.match(possibly_strong, password):
        return "Possibly strong due to length"
    elif (
        re.match(medium_pattern, password)
        or re.match(medium2, password)
        or re.match(medium3, password)
    ):
        return "Medium"
    elif re.match(weak_pattern, password) or re.match(weak2, password):
        return "Weak"
    else:
        return "Poor"
