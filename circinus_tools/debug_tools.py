# note if you want to use list comprehensions with local variables in ipdb ( getting around the NameError issue),  execute first: 
# ipdb> globals().update( locals() )
#  got this from: https://github.com/inducer/pudb/issues/103

def debug_breakpt(option='ipdb'):
    if option == 'ipdb':
        print("YOU ARE IN debug_breakpt(). ENTER 's' TO GET TO DEBUG CALL")
        print("use > globals().update(locals()) to make list comps work")

        import ipdb
        ipdb.set_trace()
    else:
        raise NotImplementedError