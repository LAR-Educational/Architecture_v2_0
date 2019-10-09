






def reverse(summing, piece):

    if len(piece) == 0:
        return summing 

    else:
        print "piece", piece[len(piece)-1] 
        
        
        summing+= piece[len(piece)-1]
        print "Sum", (summing)
        print 

        piece = piece[:len(piece)-1]
        return reverse(summing,piece)


def check_number_(mystr):

    mylist = list(mystr)

    for c in mystr:
    # for c in mylist:
        try:
            int (c)
        except:
            return False
    
    return True
        # print c, type(c)


#print check_number_("2234")



h = hash("oi")

mylist =  { "":""}


mylist[h]= True


def insert(obj):
    mylist[hash(obj)] =True

def verify(obj):
    try:
        return mylist[hash(obj)]
    except:
        return False


# print verify("s")

# insert("s")

# print verify("s")

def in_string(string):
    for s in string:
        insert(s)

def ver_string(string):
    for s in string:
        if not verify(s):
            return False

    return True


in_string("My name is bond")

print ver_string("name is nt")


