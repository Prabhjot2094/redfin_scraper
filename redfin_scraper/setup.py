import os

polipo_config = ['socksParentProxy = localhost:9050', 'diskCacheRoot=""', 'disableLocalInterface=true']
scrapy_dependencies = "sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev"

def install_linux():
    os.system('sudo apt-get update')
    os.system('sudo apt-get install tor')
    os.system('sudo apt-get install polipo')
    os.system(scrapy_dependencies)

    f = open ("/etc/polipo/config","w")
    for setting in polipo_config:
        f.write(setting)
    os.system('sudo /etc/init.d/tor start')
    os.system('sudo /etc/init.d/polipo restart')

install_linux()

