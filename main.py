# this script it's for Fivem server, to update server artifacts using Python language.

# this script has written by DevX Gaming#1255
from sqlite3 import adapt
import requests
from bs4 import BeautifulSoup
from DevSqlite3.core import Database, Table
import os
import time
from datetime import datetime
from discord import Webhook, RequestsWebhookAdapter


class Config:
    def __init__(self):
        self.url = 'https://runtime.fivem.net/artifacts/fivem/build_proot_linux/master/' # url to check for linux
        self.path = '/root/gta/fx-server/'  # your alpine folder path
        self.backup = 'alpine'  # don't change here.
        self.discord = '*******webhook********',
    
    def send(self, message):
        webhook = Webhook.from_url(str(self.discord), adapter=RequestsWebhookAdapter())
        webhook.send(message)
        # requests.post(config.discord, data=data)

config = Config()


@Database('version')
class Version(Table):
    id = Table.integerField(primary=True, null=False)
    version = Table.stringField()

    def GetFirstOne(self):
        return self.execute('select * from Version').first()


class Download:
    def __init__(self, url):
        self.url = url

    def download(self):
        print(f'dev-artifacts: Start downloading latest Fivem-artifacts from url {self.url}')
        req = requests.get(self.url)
        filename = self.url.split('/')[-1]
        if os.path.exists(filename):
            os.remove(filename)

        with open(filename, 'wb') as arch:
            arch.write(req.content)
        print('dev-artifacts: Download Successfully.')
        return filename


class UpdateChecker:
    def __init__(self):
        self.url = config.url
        self.path = config.path
        self.backup = config.backup

    def check(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, 'html.parser')
        search = soup.find_all('a')
        latest = None
        for a in search:
            latest = a.get('class')
            if 'is-active' in latest:
                latest = a
                break  # the first one is latest version
        if latest:
            print('Checking databases ...')
            url = str(latest.get('href'))
            db = Version()
            result = db.GetFirstOne()
            download = f'{self.url}{url[2:]}'
            if result:
                if result.version == download:
                    print('Up to date.')
                else:
                    file = Download(download).download()
                    LinuxTarExtract(file)
                    result.version = download
                    result.save()
            else:
                file = Download(download).download()
                LinuxTarExtract(file)
                db.version = download
                db.save()
                print('Done. successfully updated.')
                config.send(f'New update has successfully installed, you should restart server later. :upside_down:```download url: {download}```')
        else:
            print('Latest version not found.')


class LinuxTarExtract:
    def __init__(self, path):
        folder = f'{config.path}{config.backup}'
        newName = f'{config.path}{config.backup}-backup'
        if os.path.exists(folder):
            if os.path.exists(newName):
                os.system(f'rm -rf {newName}')
                time.sleep(5)
            os.rename(folder, newName)
            time.sleep(5)
        os.popen(f'tar -xf {path} -C {config.path}')


# loop for ever
try:
    config.send(f'Auto update has successfully started.')
    while True:
        UpdateChecker().check()
        time.sleep(60 * 60)  # every 1 hour
except Exception as why:
    config.send(f'Auto update stoped. Reason: {why}')


