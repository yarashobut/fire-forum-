#Fire Forum: simple (anonymous) forum site to share ideas 

Fire Forum is a lightweight, moderated forum designed to foster thoughtful discussions, academic inquiries, and philosophical debates. Unlike other anonymous platforms, it encourages users to focus on ideas rather than personal opinions, ensuring a more engaging and respectful discussion space. Users cannot
personalize content, and should remain neutral in their language!

Installation & Setup:

1. Set Up Your Virtual Environment: uv venv 

To activate your virtual environment, type source .venv/bin/activate. You should see your shell change to have a (folder name) prefix.

To deactivate your virtual environment, type deactivate.

Check that your virtual environment is using the correct version of Python:

(.venv) $ which python
<path_to_directory>/.venv/bin/python

2. Install Flask and Flask-SQLAlchemy and other required Python libraries:
uv pip install flask flask-cors Flask-SQLAlchemy jupyter
#OR 
uv pip install -r requirements.txt

3. Run Your Flask App
If your main flask application is set up in a file called app.py, you can start your flask web server using the following command:

flask run --debug --reload

The --debug and --reload flags will automatically restart your sever if you make changes to files.

Content Moderation Rules:
Fire Forum is built for thoughtful questions, academic inquries, and philosophical discussions.
This is not a personal platform and, as such, users' ability to talk about
themselves is limited. Comments/Threads with words like "I, me, my, we, us, our, your, you, ect..." 
will be deleted as they do not follow the general mission of Fire Forum.

