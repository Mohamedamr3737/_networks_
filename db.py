from pymongo import MongoClient

class DB:
    # Constructor method
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['p2p-chat']

    # checks if an account with the username exists
    def is_account_exist(self, username):
        user_exists = self.db.accounts.find_one({'username': username})
        if user_exists is not None:
            return True
        else:
            return False

    def is_chatroom_exist(self, chatroomName):
        chatroom_exists = self.db.chatrooms.find_one({'chatroomName': chatroomName})
        if chatroom_exists is not None:
            return True
        else:
            return False

        # chatroom = self.db.chatrooms.find_one({'chatroomName': chatroomName})
        # return chatroom is not None and chatroom['chatroomName'] == chatroomName

    # registers a user
    # def is_chatroom_exist(self, chatroomName):
    #     chatroom_exists = self.db.chatrooms.find_one({'chatroomName': chatroomName})
    #     return chatroom_exists is not None

    # adds a chatroom to the database
    def addChatroom(self, chatroomName, RoomCreator):
        if not self.is_chatroom_exist(chatroomName):
            chatroom = {
                "chatroomName": chatroomName,
                "RoomCreator": RoomCreator,
                "peers": [RoomCreator]  # list of peers where beginning of list is hostname
            }
            self.db.accounts.update_one(
                {"username": RoomCreator}, {"$push": {"ChatRooms": chatroomName}}
            )
            self.db.chatrooms.insert_one(chatroom)



    def JoinChatRoom(self, chatroomName, username):  # add members to chatroom and update if new peer joined
        if not self.FindUserinChatroom(chatroomName,username):
            self.db.chatrooms.update_one(
                {"chatroomName": chatroomName}, {"$push": {"peers": username}}
            )
            self.db.accounts.update_one(
                {"username": username}, {"$push": {"ChatRooms": chatroomName}}
            )

    #add members to chatroom and update query if new peer is joined
    #
    # def addRoomMember(self, chatroomName, username, userPort,userip):
    #     query = {'chatroomName': chatroomName}
    #     newPeer = {"$push": {"usernames": username, "userPorts": userPort,"userIPs": userip}}
    #        self.db.chatrooms.update_one(query, newPeer)


    def FindUserinChatroom(self,chatroomName, username):
        return self.db.chatrooms.count_documents({'chatroomName': chatroomName, 'peers': username}) > 0

    def get_users(self, chatroomName):
        ChatRoom = self.db.chatrooms.find_one({"chatroomName": chatroomName})
        if ChatRoom and 'peers' in ChatRoom:
            # Return the list of users
            return ChatRoom['peers']





    #  def getRoomMembers(self, chatroomName):
  #      return self.db.chatrooms.find_one({"chatroomName": chatroomName})

    def register(self, username, password):
        account = {
            "username": username,
            "password": password
        }
        self.db.accounts.insert_one(account)

    # retrieves the password for a given username
    def get_password(self, username):
        return self.db.accounts.find_one({"username": username})["password"]

    # checks if an account with the username online
    def is_account_online(self, username):
        if self.db.online_peers.count_documents({"username": username}) > 0:
            return True
        else:
            return False

    # logs in the user
    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.db.online_peers.insert_one(online_peer)

    # logs out the user
    def user_logout(self, username):
        self.db.online_peers.delete_one({"username": username})

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return res["ip"], res["port"]

    def leave_Chatroom(self,chatroom, username):
        # chatroom_exists = self.db.chatrooms.find_one({'chatroom': chatroom})
        # if username in chatroom['username']:
        #     index = chatroom_exists['username'].index(username)
        #     chatroom_exists['username'].pop(index)
        #     self.db.chatrooms.update_one({'chatroom': chatroom}, {'$set': chatroom_exists})
        self.db.chatrooms.update_one(
            {"chatroomName": chatroom},
            {'$pull': {'peers': {'username': username}}}
        )


# def Register_room(self, room_name, password, Admin):
#     Chat_room = {
#         "room_name": room_name,
#         "Admin": Admin,
#         "users": [Admin],  # Initialize an list for users with admin as first user
#         "password": password
#     }
#     self.db.accounts.update_one(
#         {"username": Admin},
#         {"$push": {"ChatRooms": room_name}}
#     )
#     self.db.Chatrooms.insert_one(Chat_room)
#
#
# def does_room_exist(self, room_name):
#     return self.db.Chatrooms.count_documents({'room_name': room_name}) > 0
#
#
# def get_chat_rooms(self, username=None):
#     if username:
#         # Return specific user's room names
#         user_account = self.db.accounts.find_one({"username": username})
#         if user_account:
#             chat_rooms = user_account.get("ChatRooms", [])
#             if not chat_rooms:
#                 return None
#             else:
#                 return chat_rooms
#         else:
#             return None
#     else:
#         # Return all room names
#         chatrooms = self.db.Chatrooms.find()
#         room_names = [chat_room["room_name"] for chat_room in chatrooms]
#         return room_names
#
#
# def get_room_details(self, room_name):
#     room = self.db.Chatrooms.find_one({"room_name": room_name})
#     if room and "users" in room and "Admin" in room:
#         return room["Admin"], room["users"]
#     else:
#         print(f"Error: Required fields not found for {room_name}")
#         return None
#
#
# def Join_room(self, room_name, username):
#     # Update the users list in the chat room to add the new username
#     self.db.Chatrooms.update_one(
#         {"room_name": room_name},
#         {"$push": {"users": username}}
#     )
#     self.db.accounts.update_one(
#         {"username": username},
#         {"$push": {"ChatRooms": room_name}}
#     )
#
#
# def get_room_pass(self, room_name):
#     room_data = self.db.Chatrooms.find_one({"room_name": room_name})
#     return room_data["password"] if room_data else None
#
#
# def is_user_in_chat_room(self, username, room_name):
#     return self.db.Chatrooms.count_documents({'room_name': room_name, 'users': username}) > 0
#
#
# def remove_user_from_room(self, room_name, user_to_remove):
#     # Find the chat room with the specified name
#     chat_room = self.db.Chatrooms.find_one({"room_name": room_name})
#     # Remove the user from the room's user list
#     chat_room["users"].remove(user_to_remove)
#     # Update the database with the modified chat room
#     self.db.Chatrooms.update_one(
#         {"room_name": room_name},
#         {"$set": {"users": chat_room["users"]}}
#     )
#
#     # Update the user's account to remove the room from ChatRooms
#     self.db.accounts.update_one(
#         {"username": user_to_remove},
#         {"$pull": {"ChatRooms": room_name}}
#     )
#
#     return True, f"User '{user_to_remove}' removed from the room '{room_name}'."












