from datetime import datetime, timedelta
from models import db, Thread, Comment
personal_pronouns = ['I', 'me', 'my', 'we', 'us', 'our', 'your', 'you']

#helper functions:

#helper function to determine if input is grabage or valid
def is_valid_input(input) -> bool:
    # Check if input is empty or just whitespace
    if not input.strip():
        return False

    # Check if input contains at least one alphabetic character
    has_letters = any(char.isalpha() for char in input)

    # Return True if it has at least one letter, otherwise False
    return has_letters 

#check thread
#make sure the input is valid (not all nums)
#Threads that are older than one week should not be shown (but should still be stored in the database).
#Threads and comments should be automatically deleted after 30 days.
#check for personal pronouns
#return bool
def checkThread(inputTitle, inputContent, inputAuthor) -> bool:
    #Check content is not garbage (i.e. not all nums)
    if not is_valid_input(inputContent):
        print("\ninputCONTENT is NOT valid. Change this input: %s \n", inputContent)
        #NOTE what else do we wanna do when input isnt valid?
        return False

    #Check if content has personal pronouns 
    if any(pronoun in inputContent for pronoun in personal_pronouns):
        print("\nThread contains personal pronouns. Rejected.\n")
        # session.delete(thread)
        # session.commit()
        return False

    # checks if this thread already exists
    #we dont want too many of the same threads
    existing_thread = Thread.query.filter(Thread.title == inputTitle).first()
    if existing_thread:
        print("\nThread title already exists!\n")
        return False

    #Check if posted one week ago   
    one_week_ago = datetime.utcnow() - timedelta(weeks=1)
    if existing_thread and existing_thread.created_at < one_week_ago:
        print("\nThreads older than a week will not be shown!\n")
        return False
        #DO NOT SHOW TO USER
    

    #Check if a month old 
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    if existing_thread and existing_thread.created_at < one_month_ago:
        db.session.delete(existing_thread)
        db.session.commit()
        print("\nThread was deleted because it was older than 30 days!!\n")
        return False

    #check daily thread limit for the author (3 per day)
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    threadCount = Thread.query.filter(Thread.author == inputAuthor, Thread.created_at >= one_day_ago).count()
    if threadCount >= 3:
        print("\nAuthor has reached daily thread limit of 3.\n")
        #REDIRECT TO ERROR PAGE 
        return False

    return True  # Thread passes all checks!!!
    

#check comment 
#make sure the input is valid (not all nums)
#Comments that are older than 24 hours should not be shown (but should still be stored in the database).
#Threads and comments should be automatically deleted after 30 days.
#check for personal pronouns
#run this helper function every time someone runs the home page
#return bool
def checkComment(inputContent, author) -> bool:

    #Check content is not garbage (i.e. not all nums)
    if not is_valid_input(inputContent):
        print(f"\nInvalid comment content: {inputContent}\n")
        return False

     #Check if content has personal pronouns 
    if any(pronoun in inputContent for pronoun in personal_pronouns):
        print("\nComment contains personal pronouns. Rejected.\n")
        # session.delete(comment)
        # session.commit()
        return False

    #Check if posted one day ago / dont show it
    one_day_ago = datetime.utcnow() - timedelta(hours=24)
    existing_comment = Comment.query.filter(Comment.content == inputContent).first()
    if existing_comment and existing_comment.created_at < one_day_ago:
        print("\nComments older than 24 hours won't be displayed!\n")
        return False
    #make sure it is still stored in the database

    # check if month old (delete it)
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    if existing_comment and existing_comment.created_at < one_month_ago:
        db.session.delete(existing_comment)
        db.session.commit()
        print("\nComments older than a month will be deleted.\n")
        return False

    #check for daily comment limit for author (5 per day)
    comment_count = Comment.query.filter(Comment.author == author, Comment.created_at >= one_day_ago).count()
    if comment_count >= 5:
        print("\nAuthor has reached the daily comment limit!\n")
        return False

    return True
       
