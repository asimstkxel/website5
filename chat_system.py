from datetime import datetime


class User:
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return self.username


class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content}"


class ChatRoom:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.messages = []

    def join(self, user):
        if user not in self.users:
            self.users.append(user)
            print(f"{user} has joined the chat room '{self.name}'.")
        else:
            print(f"{user} is already in the chat room.")

    def leave(self, user):
        if user in self.users:
            self.users.remove(user)
            print(f"{user} has left the chat room '{self.name}'.")
        else:
            print(f"{user} is not in the chat room.")

    def send_message(self, user, content):
        if user in self.users:
            message = Message(user, content)
            self.messages.append(message)
            print(f"Message sent: {message}")
        else:
            print(f"{user} must join the chat room before sending messages.")

    def view_history(self):
        print(f"\n--- Chat History for '{self.name}' ---")
        if not self.messages:
            print("No messages yet.")
        else:
            for message in self.messages:
                print(message)
        print("--- End of History ---\n")


if __name__ == "__main__":
    alice = User("Alice")
    bob = User("Bob")
    charlie = User("Charlie")

    room = ChatRoom("Python Learners")

    room.join(alice)
    room.join(bob)
    room.join(charlie)

    room.send_message(alice, "Hello everyone!")
    room.send_message(bob, "Hi Alice, how are you?")
    room.send_message(charlie, "Hey folks, excited to learn Python!")

    room.leave(bob)

    room.send_message(bob, "Can I still chat?")
    room.send_message(alice, "Bob just left the room.")

    room.view_history()
