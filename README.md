# CSN 291 OOAD Lab Group Activity

## Group Members (in alphabetical order):

1. Anant Jain
2. Dhas Aryan Satish
3. Divij Rawal
4. Pratyaksh Bhalla
5. Parit Gupta
6. Roopam Taneja


# Introduction

This Python utility provides two main functions for password management:

   1. check_password_pwned: This function checks if a given password has been involved in any known data breaches using the "Have I Been Pwned" API. It does so by hashing the password using SHA-1 and searching the database for breaches.

2. password_strength: This function evaluates the strength  of a password based on predefined criteria,     categorizing it as very weak, weak, medium, or strong.

# Usage

### 1. check_password_pwned

* This function checks if a password has been pawned in known data breaches.

### 2. password_strength

* This function evaluates the strength of a password based on predefined patterns. 

#### *Password Strength Criteria*

The password_strength function uses the following criteria to judge the strength of a password:

* Very Weak: 1 to 5 characters
*    Weak: At least 6 characters, including at least one letter and one digit
*    Medium: At least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit
*    Strong: At least 8 characters, including at least one lowercase letter, one uppercase letter, one digit, and one special character (@, #, $, %, ^, &, +, =)
