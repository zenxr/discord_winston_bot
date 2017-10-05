class Blacklist(object):
    # represents a blacklist
    # functions : add, remove, create, search
    
    def __init__(self, path):
        self.path = path
        
    def remove(self, account, invokee):
        f = open(self.path, 'r')
        flist = [line.rstrip('\n') for line in f.readlines()]
        f.close()

        update = False
        for line in flist:
            if account in line:
                flist.remove(account)
                update = True
        # if the account was in the list
        if update == True:
            f = open(self.path, 'w')
            for line in flist:
                f.write(line + '\n')
            f.close()

    def add(self, account, invokee):
        f = open(self.path, 'r')
        flist = [line.rstrip('\n') for line in f.readlines()]
        f.close()
        update = True
        for line in flist:
            if account in line:
                update = False
        # if the account was not found
        if update == True:
            f = open(self.path, 'a')
            f.write(account)
            f.close()
                    
    def output_list(self, invokee):
        # return all members in the blacklist
        f = open(self.path, 'r')
        flist = [line.rstrip('\n') for line in f.readlines()]
        f.close()
        return flist

blacklist = Blacklist('blacklist.txt')
outputlist = blacklist.output_list('Nah')
for line in outputlist:
    print(line)
blacklist.add("Poseidon", 'Nah')
print("==========")
for line in blacklist.output_list('Nah'):
    print(line)
print("===========")
blacklist.remove("Poseidon", "Nah")
for line in blacklist.output_list("Nah"):
    print(line)
