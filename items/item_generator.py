import json
from items.item import Item

MODULE_NAME = 'item_generator.py'
from console_module import Console

class ItemGenerator():
    '''
    Handles reading JSON item data and initialising objects for store/player inventories.
    '''
    def __init__(self, data):
        self.data = data

    async def returnItemWithID(self, id):
        '''
        Initialises and returns an Item object;
        an instantiated object with the data of a given item from item_data.json
        \nWill generate a placeholder item (itemID = 0) if given an invalid id.
        '''
        #data = self.__readJsonData() # not used
        #print(data["items"])
        itemList = self.data["items"]
        itemCount = len(self.data["items"])

        if not (id >= 1 and id <= itemCount-1):
            await Console.Log('record', 'info_dump', "ID used ({id}) - Generating a placeholder item instead", MODULE_NAME)
            print(f"Given id does not exist - generating a placeholder item instead.")
            id = 0
        
        #print(f"id used is : {id}")
        
        for entry in itemList:
            #print(f"item : {item}\n")
            #print(data["items"][item])
            item = self.data["items"][entry]
            baseAttributes = [item][0]["base"]
            #print(f"item : {item}\nbase attributes : {baseAttributes}\n")
            if (baseAttributes["id"] == id):
                itemObj = await json.loads(json.dumps(item), object_hook=Item)
                await Console.Log('record', 'info_dump', "itemObj : {itemObj}", MODULE_NAME)
                return itemObj

async def loadJsonData():
    file = open("/home/container/items/item_data.json")
    data = json.load(file)
    file.close()
    return data

# test code
'''
itemGenerator = ItemGenerator()
itemCount = len(itemGenerator.data["items"])

# should generate items 1 to 3 successfully
item1 = itemGenerator.returnItemWithID(1)
item1.printValues()
item2 = itemGenerator.returnItemWithID(2)
item2.printValues()
item3 = itemGenerator.returnItemWithID(3)
item3.printValues()

# should all generate placeholder items due to invalid ids
item4 = itemGenerator.returnItemWithID(0)
item4.printValues()
item5 = itemGenerator.returnItemWithID(-1)
item5.printValues()
item6 = itemGenerator.returnItemWithID(5)
item6.printValues()

#for id in range(1, itemCount):
#    item = itemGenerator.returnItemWithID(id)
#    item.printValues()
    #for attribute in attributes:
    #    print(f"{item.__dir__(attribute)}")
    #for attribute in dir(item):
    #    print(item.getattr(attribute))
    #print(dir(item), "\n")
    #print(item, type(item), item.base.id, item.base.name, "\n")
'''