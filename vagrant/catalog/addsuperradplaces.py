# Refactored from restaurant project built during fsf course

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Place, User


engine = create_engine('sqlite:///placesandusers.db')
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

# Since this is a setup script, clear tables of any data that may be in them
# from previous setups
session.query(User).delete()
session.query(Category).delete()
session.query(Place).delete()

# Create user for initial items
User1 = User(name="Test User", email="example@example.com",
             picture='https://pixabay.com/get/e837b00b2df7073ed1584d05fb0938c9bd22ffd41db6174593f9c671a2/robot-1214536_1280.png')
session.add(User1)
session.commit()

# Water Parks category
category1 = Category(user_id=1, name="Water Parks")

session.add(category1)
session.commit()

place1 = Place(user_id=1, name="Aquatica", description="One enormous wave pool obviously wasn't enough for the team behind Aquatica, so they built two, side by side. - CNN.com", city="Orlando, Florida", country="USA", category=category1)

session.add(place1)
session.commit()


place2 = Place(user_id=1, name="Aquaventure Waterpark", description="As of 2013, this Middle East water park is home to the world's widest water slide, the Middle East's longest river ride (2.3 kilometers in length) and the Middle East's longest zip line. - CNN.com", city="Dubai", country="UAE", category=category1)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name="Area 47", description="An Alpine lake is the location for this outdoor water park, which opens from April to the end of September. - CNN.com", city="Innsbruck", country="Austria", category=category1)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name="Beach Park", description="Beach Park's most famous ride is Insano, which ranks as the world's tallest (135 feet/41 meters) and fastest (65 mph/104 kph) water slide. - CNN.com", city="Fortaleza", country="Brazil", category=category1)

session.add(place4)
session.commit()

place5 = Place(user_id=1, name="Caribbean Bay", description="You'll find four looping water slides and an enormous wave pool at this South Korean water park, alongside more traditional attractions such as hot spring pools. - CNN.com", city="Gyeonggi-do", country="South Korea", category=category1)

session.add(place5)
session.commit()

place6 = Place(user_id=1, name="Siam Park", description="Siam Park is a Thai-themed water park on the island of Tenerife. - CNN.com", city="Tenerife", country="Spain", category=category1)

session.add(place6)
session.commit()


# National Parks category
category2 = Category(user_id=1, name="National Parks")

session.add(category2)
session.commit()


place1 = Place(user_id=1, name="Serengeti", description="During the migration (one of the largest annual wildlife movements on the planet), more than a million wildebeests and other four-legged friends chase the horizon from one end of the park to the other. -  USNEWS.com", city="Arusha", country="Tanzania", category=category2)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name="Yellowstone", description="With dramatic peaks and pristine lakes, Yellowstone is an outdoor enthusiast's paradise. - USNEWS.com", city="West Yellowstone", country="USA", category=category2)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name="Galapagos Islands", description="With its untamed terrain and notoriously fearless creatures - from sea lions to seagoing lizards - the isolated isles of the Galapagos lure those looking for exhilarating encounters in the wild. - USNEWS.com", city="Puerto Ayora", country="Ecuador", category=category2)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name="Yosemite", description="One of California's most formidable natural landscapes, Yosemite National Park features nearly 1,200 square miles of sheer awe: towering waterfalls, millennia-old Sequoia trees, daunting cliff faces and some of the most unique rock formations in the United States. - USNEWS.com", city="Midpines", country="USA", category=category2)

session.add(place4)
session.commit()


# Vintage Shops category
category3 = Category(user_id=1, name="Vintage Shops")

session.add(category3)
session.commit()


place1 = Place(user_id=1, name="BillyGoat Vintage", description="aPortland's fashionistas (that's not a complete oxymoron) head to this shop for serious vintage pieces. The space is more boutique than thrift shop with clean, organized racks and a good variety of choices from several eras. - TRAVELANDLEISURE.com", city="Portland", country="USA", category=category3)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name="Absolute Vintage", description="This London favorite in the East End's Spitalfields Market seems to have every century of style covered for both men and women. Time and patience are required to sift through the merchandise, which is organized by color instead of time period, but it's worth the effort. - TRAVELANDLEISURE.com", city="London", country="UK", category=category3)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name="Goldmine Vintage", description="Tucked away in the modern shopping district on Pearl Street in Boulder, this one-stop shop for Southern gear features men's Pendleton wool shirts (Made in the USA) and a large assortment of colorful cowboy boots. - TRAVELANDLEISURE.com", city="Boulder", country="USA", category=category3)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name="Beacon's Closet", description="Of the three locations of this consignment and vintage shop, the Park Slope, Brooklyn has a great collection of high-end labels, unique accessories, and jewelry created by local artistans. - TRAVELANDLEISURE.com", city="Brooklyn", country="USA", category=category3)

session.add(place4)
session.commit()

place5 = Place(user_id=1, name="GoldyMama", description="At this Paris shop, committed designers and casual shoppers will find vintage clothing imported from the United States, England, and Belgium. Fun finds include a Morgane wedding dress, colorful bathing caps, and floral skirts from the 1950s. - TRAVELANDLEISURE.com", city="Paris", country="France", category=category3)

session.add(place5)
session.commit()


# Craft Breweries category
category4 = Category(user_id=1, name="Craft Breweries")

session.add(category1)
session.commit()


place1 = Place(user_id=1, name="Yuengling ", description="It may be the oldest operating brewery in the U.S., founded in 1829, however, Yuengling didn't always brew beer. During Prohibition, the brewery turned its attention to dairy products. - THEDAILYMEAL.com", city="Pottsville", country="USA", category=category4)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name="101 North Brewing Company", description="101 North Brewing Company, opened in 2012, currently offers five different brews, including a rye beer, stout, blonde ale, and two IPAs. - THEDAILYMEAL.com",
                     city="Petaluma", country="USA", category=category4)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name="Alpine Beer Company", description="Alpine Beer began by contracting with Alesmith (a microbrewery in San Diego)in 1999. It doesn't just brew, but also sells growlers and bottles, and offers tastings. - THEDAILYMEAL.com", city="Alpine", country="USA", category=category4)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name="MadTree Brewing", description="MadTree Brewing is a repeat favorite from last year's list and it's easy to see why. MadTree offers limited seasonal brews along with its year-round menu. - THEDAILYMEAL.com", city="Cincinnati", country="USA", category=category4)

session.add(place4)
session.commit()

place5 = Place(user_id=1, name="Darkhorse Brewing Company", description="What began as a small Michigan restaurant became a serious brewing operation once Aaron Morse convinced his father to turn the family eatery into a brewpub. - THEDAILYMEAL.com", city="Marshall", country="USA", category=category4)

session.add(place5)
session.commit()

place6 = Place(user_id=1, name="Lagunitas Brewing Company", description="With influences from the beer-making communities in Chicago; St. Louis; Quincy, Massachusetts; Memphis; and Walker Creek, California, the crew of Lagunitas Brewing Company came to meet in Petaluma, California, to make hoppy magic. - THEDAILYMEAL.com", city="Chicago", country="USA", category=category4)

session.add(place6)
session.commit()

# End of DB building
print "added super rad places!"
