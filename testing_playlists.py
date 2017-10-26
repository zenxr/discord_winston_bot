class Playlists(object):
    # represents a blacklist
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
                chunkedline = splitmessage(line)
                found = chunkedline[1]
        return found
    
    def output_list(self):
        # return the playlists
        return self.plists

def splitmessage(s):
    words = []
    inword = 0
    for c in s:
        if c in " \r\n\t": #whitespace
            inword = 0
        elif not inword:
            words = words + [c]
            inword = 1
        else:
            words[-1] = words[-1] + c
    return words

print("\r\nCurrent file: \r\n")
playlist = Playlists('playlists.txt')
for line in playlist.output_list():
    print(line)
print("\r\nNow adding something.\r\n")
playlist.add("FkaNgaCosine", "http://youtube.com/1")
for line in playlist.output_list():
    print(line)

print("\r\nNow removing something.\r\n")
playlist.remove("FkaNgaCosine")
for line in playlist.output_list():
    print(line)

searchRes = playlist.search("Zeus")
print("Searching for Zeus : " + searchRes)
