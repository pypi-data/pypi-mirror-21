from functools import partial
import hashlib

defaultDatabase = {
    'name':'DefaultDatabase',
    'items': {}
}

# add an item to a specified database
def add_to_specified_database(item, database):
    database['items'][(database['name'],item['code'])] = item
    
# partial function to add the item to the default database
add_to_database = partial(add_to_specified_database, database = defaultDatabase)

# get an item from the database in the exchange format
def get_exchange_from_database(name, database):
    for key in database['items'].keys():
        item = database['items'][key]
        if item['name'] == name:
            return (database.get('name'), item.get('code'))
    return False

# partial function to get the item from the default database
#get_exchange = partial(get_exchange_from_database, database=defaultDatabase)

# check if something already exists
def exists_in_specific_database(code, database):
    for key in database['items'].keys():
        item = database['items'][key]
        if item['code'] == code:
            return True
    return False

# partial function to find an item in the default database
#exists_in_database = partial(exists_in_specific_database, database = defaultDatabase)

# get an item from the database in the exchange format
def get_exchange_name_from_database(code, database):
    #print(database['name'])
    for key in database['items'].keys():
        item = database['items'][key]
        if item['code'] == code:
            return item.get('name')
    return None

# partial function to get the item from the default database
#get_name = partial(get_exchange_name_from_database, database=defaultDatabase)

# get an item from the database in the exchange format
def get_exchange_unit_from_database(code, database):
    for key in database['items'].keys():
        item = database['items'][key]
        if item['code'] == code:
            return item.get('unit')
    return None

# partial function to get the item from the default database
#get_unit = partial(get_exchange_unit_from_database, database=defaultDatabase)

# Create an exchange data structure

def exchange_factory(input, type, amount, uncertainty, comment):
    data_structure = {
        'input': input,
        'type': type,
        'amount': amount,
        'uncertainty type': uncertainty,
        'comment': comment,
    }
    return data_structure

# Create an item data structure

def item_factory(name, type, unit='kg', exchanges=None, location='GLO', categories=None, **kwargs):

    if exchanges is None:
        exchanges = []

    if categories is None:
       categories = []
        
        

    to_hash = name + type+ unit + location
    code = hashlib.md5(to_hash.encode('utf-8')).hexdigest()
    data_structure = {
        'name': name,
        'code': code,
        'type': type,
        'categories': categories,
        'location': location,
        'unit': unit,
        'exchanges': exchanges
    }

    for kw in kwargs:
        data_structure[kw] = kwargs[kw]

    return data_structure
'''
def create_product (name, location ='GLO', unit='kg', **kwargs):
    new_product = item_factory(name=name, location=location, unit=unit, type='product', **kwargs)
    
    if not exists_in_database(new_product['code']):
        add_to_database(new_product)
        print ('{} added to database'.format(name))
        return get_exchange(name)
    else:
        print('{} already exists in this database'.format(name))
        return False

def create_process(name, exchanges, location ='GLO', unit='kg'):
    found_exchanges = []
    for e in exchanges:

        exc_name = e.pop('name', None)

        this_exchange = get_exchange(exc_name)
        
        if this_exchange == None:
            my_unit = e.pop('unit', unit)
                
            this_exchange = create_product(exc_name, location=location, unit=my_unit, **e)
        
        found_exchanges.append(exchange_factory(this_exchange, e[1], 1, 1, '{} exchange of {}'.format(e[1], e[0])))
        
    new_process = item_factory(name=name, location=location, unit=unit, type='process', exchanges=found_exchanges)
    
    add_to_database(new_process)

    return True

'''