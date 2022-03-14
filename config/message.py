# Imported libraries
from json import dumps
from re   import compile

# Local libraries
from config.dicts import regex_patterns


class Message_Dissection:
    def __init__(self, message):
        try:
            self.user = message.author.display_name
        except Exception as e:
            self.user = ""

        if self.is_bot():
            try:
                # Hard-coded message structure of bot message
                self.contents = dumps(message.embeds[0].to_dict())
            except Exception as e:
                try:
                    self.contents = message.content
                except Exception as e:
                    self.contents = ''
        else:
            try:
                # Regular discord message
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
            if regex_patterns['repair_needed'].search(self.contents):
                return True
        return False

    def repair_success(self):
        if self.is_bot():
            if regex_patterns['repair_success'].search(self.contents):
                return True
        return False

    def monster_appeared(self):
        if self.is_bot():
            if regex_patterns['monster_appeared'].search(self.contents):
                return True
        return False

    def monster_defeated(self):
        if self.is_bot():
            if regex_patterns['monster_defeated'].search(self.contents):
                return True
        return False
    
    # User messages
    def is_user(self):
        return not self.is_bot()

    def request_mine(self):
        if self.is_user():
            if regex_patterns['request_mine'].search(self.contents):
                return True
        return False

    def request_repair(self):
        if self.is_user():
            if regex_patterns['request_repair'].search(self.contents):
                return True
        return False

    def request_fight(self):
        if self.is_user():
            if regex_patterns['request_fight'].search(self.contents):
                return True
        return False
