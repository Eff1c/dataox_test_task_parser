import socket
from time import sleep

from migration import create_dbs, migration
from scraper import parse

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect(('db', 5432))
        s.close()
        break
    except socket.error as ex:
        print(ex)
        sleep(2)

create_dbs()
migration()

parse("pd zuo pins zm docu cldr run")
