from json import dumps


mine_sim = "Mining Simulator"

pattern_mine             = compile(r'During the session you found')
pattern_repair_needed    = compile(r'pickaxe broke')
pattern_repair_success   = compile(r'successfully repaired')
pattern_monster_appeared = compile(r'being attacked')
pattern_monster_defeated = compile(r'defeated the enemy')


class Message_Dissection:
  def __init__(self, message):
    self.is_mine_sim      = False
    self.mine             = False
    self.repair_needed    = False
    self.repair_success   = False
    self.monster_appeared = False
    self.monster_defeated = False

    if message.author.display_name == mine_sim:
        self.is_mine_sim = True

        if hasattr(message, "embeds") and message.embeds:
            try:
                contents_text = dumps(message.embeds[0].to_dict())
                if not contents_text: contents_text = False
            except Exception as e:
                print("Message is empty")

            if   pattern_mine            .search(contents_text): self.mine             = True
            if   pattern_repair_needed   .search(contents_text): self.repair_needed    = True
            elif pattern_repair_success  .search(contents_text): self.repair_success   = True
            if   pattern_monster_appeared.search(contents_text): self.monster_appeared = True
            elif pattern_monster_defeated.search(contents_text): self.monster_defeated = True
