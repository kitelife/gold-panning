__author__ = 'xiayf'

import hashlib

import requests

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker


def fetch_page(url):
    r = requests.get(url)
    if r.status_code != 200:
        return False
    return r.text


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    name = Column(String(100, collation='utf8_general_ci'), nullable=False)
    title = Column(String(1024, collation='utf8_general_ci'), nullable=False)
    url = Column(String(512, collation='utf8_general_ci'), nullable=False)
    fingerprint = Column(String(40, collation='utf8_general_ci'), nullable=False)
    created_time = Column(DateTime, nullable=False)


engine = create_engine('mysql://root:06122553@127.0.0.1/scrape_website?charset=utf8')
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


def gen_fingerprint(raw_string):
    md5_it = hashlib.md5()
    md5_it.update(raw_string)
    return md5_it.hexdigest()