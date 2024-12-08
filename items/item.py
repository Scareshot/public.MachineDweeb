import json
from console_module import Console

MODULE_NAME = 'item.py'

class Item(object):
    '''
    Item is an object defined according to attributes stored in item_data.\n
    Specified by item_generator, wherein json info is dumped in dictionary form,
    all items have a 'base' set of attributes, with some having additional data,
    such as 'consumable' data:
    \n  item.base.(...):
        int 'id',
        str 'name' (simple name; to be used for end user, 
                        the name used as a key for each individual item is the code name),
        str 'type' (generic or consumable; latter will mean item has additional information),
        int 'price' (default store price),
        int 'stock' (default amount in store; -1 means unlimited),    

      item.consumable.(...):
        str 'buff_class'  (used to differentiate effect of consumable item),
        int 'max_consume' (integer amount defining the items maximum number of uses),   
    '''
    # Initialising a new Item uses this, rather than directly using __init__, as to allow asynchronous usage
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls) # this *might* need an await, idk
        await instance.__init__(*a, **kw)
        return instance
        '''
        try:
            instance = await super().__new__(cls) # this *might* need an await, idk
            await instance.__init__(*a, **kw)
            return instance
        except Exception:
            await Console.Log(f'error', 'info_dump', "Item.__new__ encountered an error", MODULE_NAME)
        '''

    async def __init__(self, dict1):
        self.__dict__.update(dict1)
    
    #async def __init__(self, dict1):
    #    self.__dict__.update(dict1)
    
    # TODO: update this when needed / make it future-proof
    async def attributesToString(self) -> str:
        await Console.Log('record', 'info_dump', "attributesToString called", MODULE_NAME)
        try:
            returnString = str(
                f"Item\n",
                f" base:\n",
                f"   name: {self.base.name}\n",
                f"   id: {self.base.id}\n",
                f"   type: {self.base.type}\n",
                f"   price: {self.base.price}\n",
                f"   stock: {self.base.stock}"
                )
            
            if (self.base.type == "consumable"):
                returnString += (
                    f" consumable:\n",
                    f"   buff_class: {self.consumable.buff_class}\n",
                    f"   max_consume: {self.consumable.max_consume}\n"
                    )
            else:
                returnString += "\n"

            return returnString
        except Exception:
            return "ERROR"