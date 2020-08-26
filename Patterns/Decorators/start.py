from hero import *
from deco import *
# создаем героя
hero = Hero()
hero.get_stats()

# # {'HP': 128, 'MP': 42, 'SP': 100, 'Strength': 15, 'Perception': 4, 'Endurance': 8, 'Charisma': 2, 'Intelligence': 3, 'Agility': 8, 'Luck': 1}
# hero.stats
# # {'HP': 128, 'MP': 42, 'SP': 100, 'Strength': 15, 'Perception': 4, 'Endurance': 8, 'Charisma': 2, 'Intelligence': 3, 'Agility': 8, 'Luck': 1}
# hero.get_negative_effects()
# # [ ]
# hero.get_positive_effects()
# # [ ]
# # накладываем эффект
#
# brs1 = Berserk(hero)
# brs1.get_stats()
# # {'HP': 178, 'MP': 42, 'SP': 100, 'Strength': 22, 'Perception': 1, 'Endurance': 15, 'Charisma': -1, 'Intelligence': 0, 'Agility': 15, 'Luck': 8}
# # brs1.get_negative_effects()
# #[ ]
# brs1.get_positive_effects()
# #['Berserk']
#
#  # накладываем эффекты
# brs2 = Berserk(brs1)
#
# cur1 = Curse(brs2)
#
# cur1.get_stats()
# {'HP': 228, 'MP': 42, 'SP': 100, 'Strength': 27, 'Perception': -4, 'Endurance': 20, 'Charisma': -6, 'Intelligence': -5, 'Agility': 20, 'Luck': 13}
#  cur1.get_positive_effects()
# ['Berserk', 'Berserk']
# >>> cur1.get_negative_effects()
# ['Curse']
# >>> # снимаем эффект Berserk
# >>> cur1.base = brs1
# >>> cur1.get_stats()
# {'HP': 178, 'MP': 42, 'SP': 100, 'Strength': 20, 'Perception': -1, 'Endurance': 13, 'Charisma': -3, 'Intelligence': -2, 'Agility': 13, 'Luck': 6}
# >>> cur1.get_positive_effects()
# ['Berserk']
# >>> cur1.get_negative_effects()
# ['Curse']
#
# >>>