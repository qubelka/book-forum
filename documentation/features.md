## Book forum
Book forum is a web-application, which by default provides 4 discussion topics:

* Bestsellers
* New Releases
* What Should I Read Next?
* Authors

(Only admin user can modify the default topics list.)

### Features

#### 1. Registration 

- [x] Users can register. 

#### 2. Authorization

- [x] Registered users can log in.

#### 3. Adding a new thread

- [x] Authorised users can add new threads within the topics. 

#### 4. Adding messages

 - [x] Authorised users can add new messages within threads. 

#### 5. Removing messages

 - [x] Authorised users can remove the messages they have added.

#### 6. Editing messages

 - [x] Authorised users can edit the messages they have added.

#### 7. Search

All users can conduct keyword search. Search will return all messages
which contain the keyword in the 
- [x] message body (only perfect matches) /
- [ ] ~~within the tag~~ (?) / 
- [x] thread title / 
- [x] topic title

#### 8. Admin mode

- [x] There is a role associated with each user. Admin role gives more privileges to the user:
admin has access to all information in the database and can make any modifications.

- [x]  Navigation between admin & user view. 

#### 9. Secret threads

- [x] Possibility to add secret threads which are visible only to the specified users.