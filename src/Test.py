__author__ = 'Franklyn'

from random import normalvariate, randint, randrange, sample
from datetime import date, timedelta
from House import House

NUM_LISTINGS = 10000

def generate_datum():
    """Returns a synthetic Listing in the Phoenix area"""
    num_bedrooms = randint(1, 4)
    num_bathrooms = randint(1, 4)
    living_area = randint(1e3, 5e3)
    list_date = random_date(date(1999, 1, 1), date(2015, 6, 1))
    list_price = randint(100e3, 500e3)
    lat = randint(33086, 33939) / float(1e3)
    lon = randint(-112649, -111437) / float(1e3)
    exterior_stories = randint(1, 3)
    pool = sample(House.POOL_TYPES, 1)[0]
    dwelling_type = sample(House.DWELLING_TYPES, 1)[0]
    is_closed = randrange(8) < 10  # 80% of listings close

    if is_closed:
        dom = randint(7, 180)
        list_to_close = normalvariate(0.03, 0.06)
        close_date = list_date + timedelta(days=dom)
        close_price = list_price * (1 - list_to_close)
    else:
        close_date = None
        close_price = None

    return House(House.Listing(num_bedrooms, num_bathrooms, living_area, lat, lon,exterior_stories, pool, dwelling_type,
                               list_date, list_price, close_date, close_price))

def random_date(start_date, end_date):
    """Returns a random date between start_date and end_date"""
    delta = end_date - start_date
    return start_date + timedelta(days=randrange(delta.days))

def generate_test_set():
    """Tries to read the test set from disk and generates and stores it if no test set is available
    """
    try:
        House.read_serialized_object("../static/data/house_listings")
    except Exception as e:
        print "No test data available, Generating dataset: {0}".format(e.message)
        for k in range(0, NUM_LISTINGS):
            house = generate_datum()
            house.save()
        House.write_serialized_object("../static/data/house_listings")


if __name__ == "__main__":
    """Generate a random listing and benchmark how long the query takes
    """
    import timeit
    generate_test_set()
    house = generate_datum()
    print timeit.timeit(lambda : house.get_similar(10),number=50)/50
