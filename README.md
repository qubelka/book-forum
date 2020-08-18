## Book forum (Tietokantasovellus 2020 -course project)

Book Forum on Heroku: 

[Heroku link](https://fast-ravine-81652.herokuapp.com/)

### Project status

All the features defined during the first week have been implemented. 
More precise description of each feature can be found below in the section [How to use?](#how-to-use)

### Solved issues and other app improvements since 9.8.

- [x] typing in url `/success/registration` shows a message about
successful registration -> should rewrite built-in flask-login registration function 
- [x] after adding a msg, redirect to the same page where the msg was added, not on the first page of the thread like now

Instructor:
- [x] Typo: "Dicsussion Topics" --> removed
- [x] Käyttöliittymä keskusteluun on jotenkin epäselvä. Keskustelun aloituksessa olisi hyvä voida antaa 
aloitusviesti ja päätyä suoraan siihen keskusteluun.  --> changed
- [x] Kun on kirjoittamassa viestiä, olisi hyvä nähdä aiemmat viestit 
(se voisi olla samalla sivulla viestien kanssa). --> now can add a msg on the same page 
- [x] Alueen keskustelujen lista näyttää jotenkin oudolta. --> buttons changed to table-like view
- [x] Admin-sivulla salasanan (edes hashin) näyttäminen ei ole hyvä idea. --> removed
- [x] Funktiossa result ei ole tarvetta antaa muuttujille arvoa None vaan voi suoraan antaa lopulliset arvot iffin sisällä. --> removed
- [x] Olet käyttänyt vertailuja tyyppiä "if not a == b", luontevampi olisi "if a != b". 
Lisäksi vertailu muotoa "if a == True" on lyhemmin vain "if a". --> updated
- [x] Merkkijonoissa on käytetty sekaisin "- ja '-merkkejä, olisi hyvä valita toinen tapa ja pysyä siinä yhtenäisesti. --> updated

Peer review:
- [x] The character limit of 255 for each message could be expressed more clearly. Now after clicking "Send", 
the user will receive no feedback unless the user then clicks "Add new message" again. --> now 'add message' 
field should not collapse when errors occur

- [ ] It could be nice to have a separate button for returning to the topic view from the /add_thread page.

- [ ] A useful feature might be the option to also delete threads
- [ ] It is now possible to register a user "admin " whose message might be confused with the the messages by the real admin. 
Maybe the characters allowed in the username should be restricted more?
- [x] Currently trying to register a user with an existing username (such as "admin") will cause Internal server error. 
The same seems to happen with other violations of the column data restriction in the User class such as:

- [x] Too long username
- [x] Too long password (This gives an error "Password must be at least 6 characters")
- [x] Deleting a message from an empty Thread redirects the user to "?page=0" and causes "404 Page not found" error

### Problems

* search doesn't show the correct error message if all the found elements
are secret -> should do something with if-checks
* pagination for threads is missing
* ~~there is no error message which would specify the situation when app is trying 
to add to the database two messages with the same slug (duplicates in  message slugs are highly unlikely because now the slug 
is created based on the first 3 characters of the message + random string of 8 characters
including capital letters, small letters and numbers. However, empty messages are allowed, 
and in case of an empty message the slug is formed from 11 character long random 
string. Get the same 11 characters is highly unlikely, but not impossible, so this should be resolved somehow, e.g.
set the min length for messages?)~~ --> this ok

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
which contain the keyword in the message body / thread title / topic title. Conduct
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

Eye icon is used for viewing the record, pen icon is used for editing the record and bin icon for deleting the record. 
Deleting a user means deactivating him (please read the [deletion](#deletion) section for more information about deleting 
items from the database). Admin view is accessible for any user with admin role, so you can create more admin
users via admin view. **However, if you remove all the admin users from the database or the admin role,
you will not be able to access the admin view from Heroku anymore, because the admin role is added to the admin
user during the creation of the database.** 

When creating new objects in the database via admin view, you will have to fill in all the 
fields marked as mandatory (with a red star). For example, a message requires information about 
the thread within which it has to be added. In the same way adding a thread requires information
about the topic it will be added to. Threads and messages added via admin view will
be automatically marked as added by 'admin'. **Specifying the secret users while creating a new thread, 
automatically makes this thread secret (will be visible only to admin and the specified users).** There is
no option to make a secret thread visible only for admin via admin view. However, it is possible to create
such a thread using forum user interface. 

New topics added via admin view will be visible to all the users on the topics page. 
The deletion of threads, topics and messages via admin view is described in [deletion](#deletion) section.

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
