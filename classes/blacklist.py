class Blacklist(object):
    # represents a blacklist
    # functions : add, remove, create, search
    
    def __init__(self, path):
        self.path = path
        f = open(self.path, 'r')
        self.blist = [line.rstrip('\n') for line in f.readlines()]
        f.close()

    def remove(self, account, invokee):
        update = False
        for line in self.blist:
            if account in line:
                self.blist.remove(account)
                update = True
        # if the account was in the list
        if update == True:
            f = open(self.path, 'w')
            for line in self.blist:
                f.write(line + '\n')
            f.close()
            # refresh blist after modification
            f = open(self.path, 'r')
            self.blist = [line.rstrip('\n') for line in f.readlines()]
            f.close()

    def add(self, account, invokee):
        update = True
        for line in self.blist:
            if account in line:
                update = False
        # if the account was not found
        if update == True:
            f = open(self.path, 'a')
            f.write(account + '\n')
            f.close()
            # refresh blist after modification
            f = open(self.path, 'r')
            self.blist = [line.rstrip('\n') for line in f.readlines()]
            f.close()
                    
    def output_list(self, invokee):
        # return all members in the blacklist
        return self.blist