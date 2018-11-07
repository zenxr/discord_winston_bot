class Playlists(object):
    # represents a list of playlists with IDs
    # functions : add, remove, create, search
    def __init__(self, path):
        self.path = path
        f = open(self.path, 'r')
        self.plists = [line.rstrip('\n') for line in f.readlines()]
        f.close()
    
    def remove(self, user):
        update = False
        for line in self.plists:
            if user in line:
                self.plists.remove(line)
                update = True
        # if the account was in the list, update the file
        if update:
            f = open(self.path, 'w')
            for line in self.plists:
                f.write(line + '\n')
            f.close()
            # refresh plists after modification
            f = open(self.path, 'r')
            self.plists = [line.rstrip('\n') for line in f.readlines()]
            f.close()
    def add(self, user, url):
        update = True
        for line in self.plists:
            if user in line:
                update = False
        # if the user was not found
        if update:
            f = open(self.path, 'a')
            f.write(user + ' ' + url + '\n')
            f.close()
            # refresh plists after modification
            f = open(self.path, 'r')
            self.plists = [line.rstrip('\n') for line in f.readlines()]
            f.close()
    def search(self, user):
        found = "Not found"
        for line in self.plists:
            if user in line:
                chunkedLine = splitmessage(line)
                found = chunkedLine[1]
        return found

    def output_list(self):
        # return the playlists
        return self.plists