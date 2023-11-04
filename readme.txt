CSN 291 OOAD Lab Group Project

Group Members (in alphabetical order)

S.No. | Name              | Enrollment no
----- | ----------------- | -------------
1.    | Anant Jain        | 22114005      
2.    | Dhas Aryan Satish | 22117046      
3.    | Divij Rawal       | 22114031      
4.    | Parit Gupta       | 22117100      
5.    | Pratyaksh Bhalla  | 22115119      
6.    | Roopam Taneja     | 22125030      

Requirements
- Nodejs (https://nodejs.org/en/download)
- Python (https://www.python.org/downloads/)

Installation

1. Clone the repository and go to project directory
   git clone https://github.com/Project-Group-CSE/CSN-291-OOAD-Lab.git
   cd CSN-291-OOAD-Lab

2. Create a virtual environment
   python -m venv env

3. Activate the virtual environment
    - On Windows, run:
      .\env\Scripts\activate
    - On Unix or MacOS, run:
      source env/bin/activate

4. Install the dependencies
   pip install -r requirements.txt
 
5. Do necessary migrations
   cd hashed
   python manage.py makemigrations
   python manage.py migrate

6. Open another terminal and install node dependencies
   cd ..\h4-h3d\
   npm install

Running the project

1. Start Django server
   cd hashed
   python manage.py runserver

2. Start node server
   cd ..\h4-h3d\
   npm start

3. Go to home page:
   Type localhost:3000 in browser window to reach home page of our application.
