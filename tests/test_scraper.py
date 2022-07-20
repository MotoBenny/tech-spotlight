""""
pytest mock to handle any waits and calls to 3rd party packages

"""
import time
import pytest
from tech_spotlight import scraper


def test_monkeypatching_time_sleep(monkeypatch):
    def mocksleep(slept):
        pass

    monkeypatch.setattr(time, "sleep", mocksleep)
    time.sleep(3600)


@pytest.mark.skip("TODO")
def test_scraper_works():
    scraper.scraper("Python Programmer", "Seattle", 3, 5, "test_filename.csv")
