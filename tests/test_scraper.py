""""
pytest mock to handle any waits and calls to 3rd party packages

"""
import time

# from types import NoneType
# import pytest
from tech_spotlight import scraper


def test_monkeypatching_time_sleep(monkeypatch):
    def mocksleep(slept):
        pass

    monkeypatch.setattr(time, "sleep", mocksleep)
    time.sleep(3600)


#  @pytest.mark.skip("TODO")
def test_scraper_works():
    scraper.scraper("Python Programmer", "Seattle", 3, 10, "test_filename")


#  @pytest.mark.skip("TODO")
# @pytest.mark.skip("TODO")
# def test_scraper_nonetype():
#     with pytest.raises(AttributeError):
#       scraper.scraper(" ", "", 0, 0, "attribute_test")
