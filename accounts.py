"""
Th class Accounts manages user's data
The file accounts.csv contains:
- username
- password hash
- status (active/pending)
of all users. Pending users are waiting to be approved.
"""
import csv


PATH = 'assets\\accounts.csv'
ACTIVE_STATUS = 'active'
PENDING_STATUS = 'pending'


class Accounts:

    def __init__(self):
        self.active_users = dict()
        self.pending_users = dict()
        self.load_users()

    def load_users(self):
        """load active users, pending accounts are not loaded"""
        print('> Loading users...')
        with open(PATH, 'r') as file:
            data = csv.reader(file)
            for user, pas_hash, status in data:
                if status == ACTIVE_STATUS:
                    self.active_users[user] = pas_hash
                elif status == PENDING_STATUS:
                    self.pending_users[user] = pas_hash
                    print(f'> New user "{user}" waiting for approval')

    def save_users(self):
        """save all user info to file in PATH"""
        with open(PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            for user in self.active_users:
                writer.writerow([user, self.active_users[user], ACTIVE_STATUS])
            for user in self.pending_users:
                writer.writerow([user, self.pending_users[user], PENDING_STATUS])

    def new_user(self, username, pas_hash):
        """add new user to pending users"""
        if username in self.active_users or username in self.pending_users:
            raise ValueError('User already registered')
        else:
            self.pending_users[username] = pas_hash

    def activate_user(self, username):
        """move user from pending to active"""
        self.active_users[username] = self.pending_users[username]
        self.pending_users.pop(username)

    def verify_password(self, username, pas_hash):
        """returns True if active user patches the pas_hash in the database"""
        if username in self:
            return self.active_users[username] == pas_hash
        else:
            return False


if __name__ == '__main__':
    a = Accounts()
    a.new_user('omar', 'a1a1')
    print(a.active_users)
    print(a.pending_users)
    a.save_users()
