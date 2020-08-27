### Solved issues and other app improvements since 9.8.

- [x] typing in url `/success/registration` shows a message about
successful registration -> built-in flask-login registration function changed a bit
- [x] after adding a msg, redirect to the same page where the msg was added, not on the first page of the thread like now --> done
- [x] search doesn't show the correct error message if all the found elements
are secret -> should work now
- [x] ~~there is no error message which would specify the situation when app is trying 
to add to the database two messages with the same slug (duplicates in  message slugs are highly unlikely because now the slug 
is created based on the first 3 characters of the message + random string of 8 characters
including capital letters, small letters and numbers. However, empty messages are allowed, 
and in case of an empty message the slug is formed from 11 character long random 
string. Get the same 11 characters is highly unlikely, but not impossible, so this should be resolved somehow, e.g.
set the min length for messages?)~~ --> this ok

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

- [x] It could be nice to have a separate button for returning to the topic view from the /add_thread page. --> button added

- [x] A useful feature might be the option to also delete threads --> delete option added
- [x] It is now possible to register a user "admin " whose message might be confused with the the messages by the real admin. 
Maybe the characters allowed in the username should be restricted more? --> username validation added
- [x] Currently trying to register a user with an existing username (such as "admin") will cause Internal server error. 
The same seems to happen with other violations of the column data restriction in the User class such as: --> error messages added

- [x] Too long username
- [x] Too long password (This gives an error "Password must be at least 6 characters")
- [x] Deleting a message from an empty Thread redirects the user to "?page=0" and causes "404 Page not found" error 
--> should now redirect to page 1