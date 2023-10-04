import requests
import hashlib
import re
def get_pass(num):
    api = "https://random-word-api.herokuapp.com/word"
    parameters = {"number": num}
    response = requests.get(f"{api}", params=parameters)
    if response.status_code != 200:
        return Exception("Error in fetching data")
    else:
        result = response.json()
        s = ""
        for i in range(num - 1):
            s += result[i] + "-"
        s += result[num - 1]
        return s

def check_password_pwned_api(password):
    # Hash the password using SHA-1 hash algorithm
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    api_url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(api_url)
    if response.status_code == 200:
        
        for line in response.text.splitlines():
            if line.startswith(suffix):
                count = int(line.split(":")[1])
                return f"The password has been found {count} times and is compromised."
        return "The password has not been found in any known breaches."
    elif response.status_code == 404:
        return "Invalid API endpoint or no data found."
    else:
        return "Error occurred while checking the password."



def password_strength(password):
    
    very_weak_pattern = r'^.{1,5}$' 
    weak_pattern = r'^(?=.*[a-zA-Z])(?=.*\d).{6,}$'
    medium_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    strong_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$'  

   
    if re.match(strong_pattern, password):
        return "Strong"
    elif re.match(medium_pattern, password):
        return "Medium"
    elif re.match(weak_pattern, password):
        return "Weak"
    elif re.match(very_weak_pattern, password):
        return "Very Weak"
    else:
        return "Invalid"



