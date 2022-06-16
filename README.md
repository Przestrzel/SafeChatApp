# SafeChatApp
Local safe chat application that enable user to send encrypted messages to another user by P2P network. 
GUI provided by Kivy library.

# Features
- generation of RSA key for each user
- sending encrypted plain text messages and files
- sending any size of file
- sending session key before every message
- exchange of public RSA key
- holding private RSA key in encrypted form
- picking the encryption mode: EBC, CBC

# Setup
- go to main folder of application
- run: pip install -r requirements.txt
- run server by python server.py in one terminal
- run at least two instances of main.py application with different client names, like python main.py client_name
