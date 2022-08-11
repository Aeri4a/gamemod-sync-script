import json, os, ftplib, time


class DataObtainer:
    data_local = None
    data_server = None
    names_changes = []
    version_changes = []

    host = ""
    port = 21
    user = ""
    paswrd = ""

    def load_files(self):

        ftp = ftplib.FTP(timeout=30)

        ftp.connect(self.host, self.port)
        ftp.login(self.user, self.paswrd)

        ftp.cwd("profile/mods")
        target = "version.json"
        temp_version = "version_temp.json"

        with open(temp_version, "wb") as file_server:
            retCode = ftp.retrbinary(f"RETR {target}", file_server.write)

        ftp.quit()

        with open("version_temp.json", "r") as file_server:
            self.data_server = json.load(file_server)

        #os.remove("version_temp.json")

        if os.path.exists("version.json"):
            with open("version.json", "r") as file_local:
                self.data_local = json.load(file_local)
            return True
        else:
            return False

    def version_check(self):
        if self.data_server[0]["ver"] == self.data_local[0]["ver"]:
            return True
        else:
            return False


    def comparison(self):
        status = 0
        pin1, pin2 = 0, 0
        dl = self.data_local
        ds = self.data_server

        #finding versions and names
        for origin in ds[1:]:
            got_it = False
            for copy in dl[1:]:
                if copy["name"] == origin["name"]:
                    got_it = True
                    if copy["ver"] != origin["ver"]:
                        self.version_changes.append(origin["name"])
                        pin1 = 1

            if not got_it:
                self.names_changes.append(origin["name"])
                pin2 = 2

        status = pin1 + pin2
        return status


    def removing_old(self):
        for todel in self.version_changes:
            os.remove(todel)


    def update_download(self, which):
        ftp = ftplib.FTP(timeout=30)

        ftp.connect(self.host, self.port)
        ftp.login(self.user, self.paswrd)

        ftp.cwd("profile/mods")
        for w in which:
            getfile = w
            savefile = getfile

            with open(savefile, "wb") as file_server:
                retCode = ftp.retrbinary(f"RETR {getfile}", file_server.write)

        ftp.quit()


    def update_version_file(self):
        os.remove("version.json")
        os.rename("version_temp.json", "version.json")


    def initate(self):
        ftp = ftplib.FTP(timeout=30)

        ftp.connect(self.host, self.port)
        ftp.login(self.user, self.paswrd)

        ftp.cwd("profile/mods")

        all = self.data_server[1:]

        for a in all:
            getfile = a["name"]
            savefile = getfile

            with open(savefile, "wb") as file_server:
                retCode = ftp.retrbinary(f"RETR {getfile}", file_server.write)

        ftp.quit()

        os.rename("version_temp.json", "version.json")


mod = DataObtainer()
print("Loading files...")
if mod.load_files():
    print("Success")

    print("Checking version...")
    if mod.version_check():
        print("Version current\n")
        time.sleep(2)
        exit()
    else:
        print("Version outdated")
        print("Checking mods...")
        status = mod.comparison()

        if status == 1:
            print("\nNew versions of mods: ")
            for ver in mod.version_changes:
                print(ver)

            print("\nDeleting old mods...")
            mod.removing_old()

            print("Downloading new mods...")
            mod.update_download(mod.version_changes)

            mod.update_version_file()
            print("Done")
            time.sleep(2)
            exit()

        elif status == 2:
            print("\nNew mods are available")
            for new in mod.names_changes:
                print(new)

            print("\nDownloading new mods...")
            mod.update_download(mod.names_changes)

            mod.update_version_file()
            print("Done")
            time.sleep(2)
            exit()

        elif status == 3:
            print("\nNew versions of mods: ")
            for ver in mod.version_changes:
                print(ver)

            print("\nDeleting old mods...")
            mod.removing_old()

            print("Downloading new mods...")
            mod.update_download(mod.version_changes)

            print("\nNew mods are available")
            for new in mod.names_changes:
                print(new)

            print("\nDownloading new mods...")
            mod.update_download(mod.names_changes)

            mod.update_version_file()
            print("Done")
            time.sleep(2)
            exit()

else:
    print("Can't find version.json")
    print("Downloading all mods...")
    mod.initate()
    print("Done")
    time.sleep(2)
    exit()
