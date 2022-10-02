class ObjectMap:
    def __init__(this,map =None) -> None:
        this.map = dict()
        if map!= None:
            for k,v in map:
                this.set(k,v)

    def set(this,key,value):
        this.map[str(key)] = value
        return value

    def get(this,key,default = None):
        value = this.map.get(str(key),None)
        if value == None:
            return default
        return value

    def pop(this,key):
        return this.map.pop(str(key),None)

    def __repr__(this) -> str:
        map = ""
        for k,v in this.map.items():
            map+= k+' ==> '+str(v)
        return map