__author__ = 'xiayf'

import hashlib

import requests

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    name = Column(String(100, collation='utf8_general_ci'), nullable=False)
    title = Column(String(1024, collation='utf8_general_ci'), nullable=False)
    url = Column(String(512, collation='utf8_general_ci'), nullable=False)
    fingerprint = Column(String(40, collation='utf8_general_ci'), nullable=False)
    created_time = Column(DateTime, nullable=False)


engine = create_engine('mysql://root:06122553@127.0.0.1/gold_panning?charset=utf8')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()


class Storage(object):
    @classmethod
    def add(cls, records):
        all_to_store = []
        for one_record in records:
            all_to_store.append(Record(**one_record))
        db_session.add_all(all_to_store)
        db_session.commit()

    @classmethod
    def close(cls):
        db_session.close()

    @classmethod
    def query_all_fingerprint(cls, condition):
        all_fingerprint = {}
        for one_record in db_session.query(Record, Record.fingerprint).filter(Record.name == condition):
            all_fingerprint[one_record.fingerprint] = all_fingerprint.get(one_record.fingerprint, 0) + 1
        return all_fingerprint


class ParserBase(object):

    def __init__(self, config):
        self.config = config
        self.all_fingerprint = Storage.query_all_fingerprint(self.config['name'])
        self.has_duplicate = False
        self.url_list = [self.config['url'], ]

    def __parse(self):
        pass

    def run(self):
        pass


def gen_fingerprint(raw_string):
    md5_it = hashlib.md5()
    md5_it.update(raw_string)
    return md5_it.hexdigest()


def fetch_page(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/38.0.2125.111 Chrome/38.0.2125.111 Safari/537.36'})
    if r.status_code != 200:
        return False
    return r.text
