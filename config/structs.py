from json import dumps
from re   import compile


class Message_Dissection:
    def __init__(self, message):
        try:
            self.user = message.author.display_name
        except Exception as e:
            self.user = ""

        if self.is_bot():
            try:
                self.contents = dumps(message.embeds[0].to_dict())
            except Exception as e:
                try:
                    self.contents = message.content
                except Exception as e:
                    self.contents = ''
        else:
            try:
                self.contents = message.content
            except Exception as e:
                self.contents = ''

    # Bot messages
    def is_bot(self):
        if self.user == "Mining Simulator":
            return True
        return False

    def repair_needed(self):
        if self.is_bot():
            if compile(r'pickaxe broke').search(self.contents):
                return True
        return False

    def repair_success(self):
        if self.is_bot():
            if compile(r'successfully repaired').search(self.contents):
                return True
        return False

    def monster_appeared(self):
        if self.is_bot():
            if compile(r'being attacked').search(self.contents):
                return True
        return False

    def monster_defeated(self):
        if self.is_bot():
            if compile(r'defeated the enemy').search(self.contents):
                return True
        return False
    
    # User messages
    def is_user(self):
        return not self.is_bot()

    def request_mine(self):
        if self.is_user():
            if compile(r'm!m').search(self.contents):
                return True
        return False

    def request_repair(self):
        if self.is_user():
            if compile(r'm!repair').search(self.contents):
                return True
        return False

    def request_fight(self):
        if self.is_user():
            if compile(r'm!fight').search(self.contents):
                return True
        return False
