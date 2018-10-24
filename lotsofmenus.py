from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///category_item_user.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Item for Action games
Category1 = Category(user_id=1, name="Action games")

session.add(Category1)
session.commit()

CategoryItem1 = CategoryItem(user_id=1, name="Def Jam: Fight for NY", description="This game features some of the best rap artists during the time of its release, like Snoop Dogg, T.I., and Busta Rhymes, and makes them duke it out with each other"
                     , games_category=Category1)

session.add(CategoryItem1)
session.commit()


CategoryItem2 = CategoryItem(user_id=1, name="BioShock", description="IS a first-person shooter video game developed by 2K Boston, and published by 2K Games. The game was released for Microsoft Windows and Xbox 360 platforms in August 2007"
                     , games_category=Category1)

session.add(CategoryItem2)
session.commit()


CategoryItem3 = CategoryItem(user_id=1, name="Assassin's Creed II", description="2009 historical fiction action-adventure open world stealth video game developed by Ubisoft Montreal and published by Ubisoft. It is the second major installment"
                     , games_category=Category1)

session.add(CategoryItem3)
session.commit()



CategoryItem5 = CategoryItem(user_id=1, name="The Last of Us ", description="is an action-adventure survival horror video game developed by Naughty Dog and published by Sony Computer Entertainment. It was released for the PlayStation 3 on June 14, 2013"
                     , games_category=Category1)

session.add(CategoryItem5)
session.commit()


# Item for Strategy games
Category2 = Category(user_id=1, name="Strategy games")

session.add(Category2)
session.commit()


CategoryItem1 = CategoryItem(user_id=1, name="Brigandine", description="Brigandine is a tactical role-playing game for the PlayStation video game console, created by developer Hearty Robin and released in 1998. An American port, called Brigandine: The Legend of Forsena, was released in the same year by Atlus"
                    , games_category=Category2)

session.add(CategoryItem1)
session.commit()

CategoryItem2 = CategoryItem(user_id=1, name="Front Mission 3",
                     description="Front Mission 3 is the third main entry and the fifth entry overall in the Front Mission series. Like other Front Mission titles, Front Mission 3 is part of a serialized storyline that follows the stories of various characters and their struggles involving mecha known as wanzers"
                     , games_category=Category2)

session.add(CategoryItem2)
session.commit()

CategoryItem3 = CategoryItem(user_id=1, name="Age of Empires", description="Developed by Ensemble Studios and published by Microsoft. Ensemble was still an independent company, later acquired by Microsoft. The game uses the Genie, a 2D sprite-based game engine"
                    , games_category=Category2)

session.add(CategoryItem3)
session.commit()

CategoryItem4 = CategoryItem(user_id=1, name="Civilization II", description="Sid Meier's Civilization II is a turn-based strategy video game developed and published by MicroProse. It was first released in 1996 for the PC and later ported to the Sony PlayStation. In 2002, Atari re-released the game for newer operating systems, such as Windows 2000 and Windows XP"
       , games_category=Category2)

session.add(CategoryItem4)
session.commit()



# Item for Sports games
Category3 = Category(user_id=1, name="Sports games")

session.add(Category3)
session.commit()


CategoryItem1 = CategoryItem(user_id=1, name="NBA Street", description="basketball video game developed by EA Canada and was released in 2001 for the PlayStation 2 and in 2002 for the GameCube. It combines the talent and big names of the National Basketball Association with the attitude and atmosphere of streetball"
                    , games_category=Category3)

session.add(CategoryItem1)
session.commit()

CategoryItem2 = CategoryItem(user_id=1, name="Wii Sports", description="The game was first released in North America along with the Wii on November 19, 2006, and was released in Japan, Australia, and Europe the following month. It was included as a pack-in game with the Wii console in all territories except Japan and South Korea, making it the first game included with the launch of a Nintendo system since Mario's Tennis for the Virtual Boy in 1995. Wii Sports is now available on its own as part of the Nintendo Selects collection of games and is no longer a pack-in game for the Wii"
                    , games_category=Category3)

session.add(CategoryItem2)
session.commit()

CategoryItem3 = CategoryItem(user_id=1, name="Mario Tennis", description="The game was released in North America and Japan in the summer of 2000, and released in Europe later in November. It is the first tennis-based game starring Mario since Mario's Tennis, and the second game developed by Camelot on a Nintendo system. The game is known for being the introduction of Waluigi, and the re-introduction of Princess Daisy and Birdo. Mario Tennis was re-released on the Wii Virtual Console in 2010. The game's success led to two sequels: Mario Power Tennis released for the Nintendo GameCube in 2004"
                    , games_category=Category3)

session.add(CategoryItem3)
session.commit()

# Item for Puzzle games
Category4 = Category(user_id=1, name="Puzzle games")

session.add(Category4)
session.commit()

CategoryItem1 = CategoryItem(user_id=1, name="The Room", description="Gimmicky little room escape puzzle games have been something of a plague on mobile, but out of this strange ether appeared something astonishingly slick, smart and well produced. The Room, taking this odd concept a lot less literally than many, features impossible clockwork mechanisms that you must meticulously explore, experimentally clicking here and there to learn their secrets, and gradually progress through its odd story"
                    , games_category=Category4)

session.add(CategoryItem1)
session.commit()

CategoryItem2 = CategoryItem(user_id=1, name="Bejeweled 3", description="Yes, without Bejeweled we wouldnot have Candy Crush Saga, and the world would therefore be 3.4% better than it currently is, but it also provided us with far more lovely pleasures like Puzzle Quest (see later), and indeed the best damned match-3 game of all time, ZooKeeper. Good with the bad"
                    , games_category=Category4)

session.add(CategoryItem2)
session.commit()

# Item for Idle games
Category5 = Category(user_id=1, name="Idle games")

session.add(Category5)
session.commit()

CategoryItem1 = CategoryItem(user_id=1, name="WarClicks", description="WarClicks is the first community-based clicking game! Your clicking helps all of your country mates in becoming the ultimate clicking force. Refer friends to not only help your country become stronger but to also make YOU stronger. Upgrades, fuel-based clicking, infinitely scaling game"
                                   , games_category=Category5)

session.add(CategoryItem1)
session.commit()

CategoryItem2 = CategoryItem(user_id=1, name="Idle Miner Tycoon", description="Automate and optimize your gold mine and become a tycoon! Have you always dreamed of managing your own mine? Well this is your chance"
                    , games_category=Category5)

session.add(CategoryItem2)
session.commit()

CategoryItem3 = CategoryItem(user_id=1, name="Corrupt Mayor Clicker", description="It's a clicker game in that you are a corrupt mayor. Your main objective it's amass a fortune in your swiss bank account. You can do this by recollecting bills like a mad person or make contracts not enough legal and taking a wide variety of decisions"                    , games_category=Category5)

session.add(CategoryItem5)
session.commit()
print "added games items!"
