## Book forum (Tietokantasovellus 2020 -course project)

Book Forum on Heroku: 

[Heroku link](https://fast-ravine-81652.herokuapp.com/)

### Intro

Book forum is a web application which has the basic forum functionality: there are some predefined
topics within which users can add and remove threads and messages.  

### Good to know about this app 
#### Protection against CSRF

Please notice that in this project I use FlaskForms which have built-in protection against CSRF attacks. 
Miguel Grinberg's blog (which was refernced in our course material) says the following:

> The form.hidden_tag() template argument generates a hidden field that includes a token that is used to protect the form against CSRF attacks. All you need to do to have the form protected is include this hidden field and have the SECRET_KEY variable defined in the Flask configuration. If you take care of these two things, Flask-WTF does the rest for you.

[The Flask Mega-Tutorial Part III: Web Forms](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms/page/3)

#### Deletion

- The owner of a thread or message (i.e. the user that has created the thread or the message) can delete this specific thread or message. 

- Admin user can delete all topics / threads and messages via admin view. 

Topic and thread models implement the cascade rule according to which:

- Deletion of a topic removes all the threads and messages associated with that topic. 
- Deletion of a thread removes all the messages associated with that thread. 
 
Admin user can also remove users from the database. 
This means deactivating a user by setting his active-feature to False. 
Default Flask-admin library uses deactivation for a different purpose, 
so in this app there is no user deactivation feature. Instead, when deactivated user tries to log in, 
he gets the message 'Specified user does not exist.' and won't be able to use the app. 
Admin can restore the user from the database by setting his status back to active. 
Thus, removing a user does not affect the messages or threads that he owns.  

### How to use? 

By default app has 2 users in the db: 
* user@test.com 
* admin@test.com (admin)

Both have the same password: 'password'. 

All the topics, threads and messages on the forum can be viewed by anyone without logging in. 
The exception from this rule are secret threads and the messages within these threads which can be viewed only by the registered
users who have been given access to these threads. However, all the operations on threads and messages, 
such as adding a new thread or removing a message, require logging in.

#### Authorization

Sign in by clicking "Sign in" button on the right side of the navigation bar. 
Use the default users credentials or register a new user. Please notice that some features 
are available only for the admin user (e.g. admin view).  

#### Registration 

Register a new user by clicking "Register" button on the right side of the navigation bar. Registration
requires an email which will be used for signing in. The username, on the other hand, will identify the creator of 
a particular message and will be visible for anyone on the forum. 

#### Adding a new thread

After signing in choose one of the topics to add a new thread. There are 4 predefined topics:
Bestsellers, New Releases, What Should I Read Next? and Authors. Only admin can modify the list
of topics. More on modifying the topics in [admin mode](#admin-mode). 

Within the chosen topic click button "Add new discussion" and enter the discussion name. 
The discussion name should be 4-70 characters long. Click "Create discussion" button to create
the discussion. 

* Creating secret discussion

Check the box "Make this thread secret" to create a secret discussion which will be visible only
for the specified users. From the list of existing users choose the users who will be able to view, add 
and modify messages within this thread. If you do not choose any users, the thread will be visible only 
for you.

#### Adding messages

Click on the thread inside which you want to add a new message. Click button "Add new message". If you 
are not already signed in, the application will ask you to sign in. After signing in,
type in your message and click "Add message". Message has no minimum character number requirements, but
it can be max 255 characters long. 

#### Editing messages

The signed in users can edit the messages they have added. Go to the thread inside which you want
to edit a message. The messages that you have added should have a yellow "edit" button on the right
side. Click the "edit" button, make any required modifications and then click "Edit message" to complete your actions. 
Click "Go back" if you do not want to modify the message. 

#### Removing messages

The signed in users can delete the messages they have added. Go to the thread inside which you want
to remove a message. The messages that you have added should have a red "delete" button on the right
side. Click the "delete" button, you will be redirected to the confirmation page. Confirm the deletion by
clicking "Yes, delete message." or go back by clicking "No, go back".

#### Search

All users can conduct keyword search. The search results from the secret threads will be visible
only for the users who has access rights to these threads. Search will return all messages / threads / topics
which contain the keyword in the message body / thread title / topic title (only perfect matches). Conduct
the search by typing the keyword into the search field on the right side of the navigation bar. Click 
"Search" button to show the results.

#### Admin mode

There is a role associated with each user. Admin role gives more privileges to the user:
admin has access to all information in the database and can make almost any modifications on the forum. By
default there is an admin user which has admin privileges. To access the admin view, sign in as admin user (email: 
admin@test.com, password: password). Click "Admin view" button on the right side of the navigation bar. 

You should be redirected to the flask-admin view with all the tables from the database, i.e. 
User, Role, Topic, Thread, Message. To return back to the main page click "Back to book forum main page"
on the right side of the navigation bar. To modify the database tables click on the specific table.   

Pen icon is used for editing the record and bin icon for deleting the record. Deleting a user
means deactivating him (please read the [deletion](#deletion) section for more information about deleting 
items from the database). Admin view is accessible for any user with admin role, so you can create more admin
users via admin view. **However, if you remove all the admin users from the database or the admin role,
you will not be able to access the admin view from Heroku anymore, because the admin role is added to the admin
user during the creation of the database.** 

When creating new objects in the database via admin view, you will have to fill in all the 
fields marked as mandatory (with red star). For example, a message requires information about 
the thread within which it has to be added. In the same way adding a thread requires information
about the topic it will be added to. Threads and messages added via admin view will
be automatically marked as added by 'admin'. New topics will be accessible by all the users
on the topics page. The deletion of threads, topics and messages via admin view is described in
 [deletion](#deletion) section.

### Cloning the project

If you don't want to use Heroku, and instead want to pull this project on your computer, you can use the 
following command to create the database before running the app: 

`~/book-forum$ flask create_db`

This will create the database with 2 default users and 4 default topics. You can modify the 
functionality of this command by modifying `application/commands.py` file. To work correctly, besides
the initialized database, the application requires 4
`.env` variables: `DATABASE_URL`, `SECRET_KEY`, `SECURITY_PASSWORD_HASH` and `SECURITY_PASSWORD_SALT`. Modify the 
 `application/config.py` if you don't want to use the `.env` file. 

---

##### (First assignment 26.7.) Original list of features for implementation :
[Features](/documentation/features.md)
