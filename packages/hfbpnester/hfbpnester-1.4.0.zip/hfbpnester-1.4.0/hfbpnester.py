"""This is the "nester.py" module and it provides one function called print_lol()
   which prints lists that may or may not include nested lists."""
def print_lol (the_list, indent=False, level=0, fh=std.stdout):
    """This function takes one positional argument called "the list", which
       is any python list (of - possibly - nested lists). Each data item in the
       provided list is (recursively) printed to the screen on it's own line.
       The second argument called "indent" which provide judgement base of whether
       indent or not.
       The third argument called "level" which proivded indent level for recursively
       list.
       The fourth argument called "fh" which provide the output destination for print."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                """for tab_stop in range(level):
                    print("\t", end='')"""
                print("\t" * level, end = '', file=fh)
            print(each_item, file=fh)
