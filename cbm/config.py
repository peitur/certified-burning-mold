#!/usr/bin/env python3

import re

from pprint import pprint

def generic_validate( vm, data ):
    
    missing_rlist = [ k for k, v in vm.items() if 'required' in v and k not in data ]
    if len( missing_rlist ) > 0:
        raise IndexError(",".join( missing_rlist ) )
    
    for k, v in data.items():
        
        if k not in vm: 
            raise AttributeError( k )        

        if 'type' in vm[k]:
            if isinstance( vm[k]['type'], str ):
                if type( v ).__name__ != vm[k]["type"]:
                    raise AttributeError( "Bad type '%s':'%s'" % ( type( v ).__name__, vm[k]["type"]  ) )
            elif isinstance( vm[k]['type'], list ):
                if type( v ).__name__ not in vm[k]["type"]:
                    raise AttributeError( "Bad type '%s':'%s'" % ( type( v ).__name__, ",".join( vm[k]["type"] ) ) )

        if 'pattern' in vm[k]:
            if isinstance( v, str ):
                if not re.search( vm[k]['pattern'], v ):
                    raise AttributeError("Bad pattern '%s':'%s'" %  ( v, vm[k]['pattern'] ) )
            
        if 'match' in vm[k]:
            if isinstance( v, str ):
                if not re.match( vm[k]['match'], v ):
                    raise AttributeError("Bad match '%s':'%s'" %  ( v, vm[k]['match'] ) )

        
                
class AbstractConfig( object ):
    
    def __init__( self, fileame, **opt ):
        pass

if __name__ == "__main__":
    vmap = {
        "aaaa": { "required": True, "type":"str" },
        "bbbb": {"type":["dict", "list"]},
        "cccc": { "required": True },
        "dddd": {"match": "^[a-z]+$"}
    }
    
    data = {
        "aaaa": "1111",
        "bbbb": {},
        "cccc": 123,
        "dddd": "abcd"
    }
    
    pprint( generic_validate( vmap, data) )