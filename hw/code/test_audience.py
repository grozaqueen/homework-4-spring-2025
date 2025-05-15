import pytest
from base_case import BaseCase

class TestAudience(BaseCase):
    _valid_name="audience_one"
    _valid_name2="test_name_two"
    _valid_list_name="user_list_one"
    _valid_list_name2="список_пользователей_два"

    def test_create_audience_from_user_list(self, audience_page):
        audience_page.create_audience_from_user_list(name=self._valid_name, list_name=self._valid_list_name)
        audience_page.assert_audience_visible(name=self._valid_name)
        audience_page.delete_audience(name=self._valid_name)
        audience_page.assert_audience_not_visible(name=self._valid_name)
        audience_page.delete_user_list(name=self._valid_list_name)
        audience_page.assert_user_list_not_visible(name=self._valid_list_name)

    def test_search_audience(self, audience_page):
        audience_page.create_audience_from_user_list(name=self._valid_name, list_name=self._valid_list_name)
        audience_page.assert_audience_visible(name=self._valid_name)
        audience_page.create_audience_from_user_list(name=self._valid_name2, list_name=self._valid_list_name2)
        audience_page.assert_audience_visible(name=self._valid_name2)

        audience_page.search_for_audience(name=self._valid_name)
        audience_page.assert_audience_visible(name=self._valid_name)
        audience_page.assert_audience_not_visible(name=self._valid_name2)

        audience_page.clear_search()
        audience_page.delete_audience(name=self._valid_name2)
        audience_page.assert_audience_not_visible(name=self._valid_name2)
        audience_page.delete_audience(name=self._valid_name)
        audience_page.assert_audience_not_visible(name=self._valid_name)
        audience_page.delete_user_list(name=self._valid_list_name2)
        audience_page.assert_user_list_not_visible(name=self._valid_list_name2)
        audience_page.delete_user_list(name=self._valid_list_name)
        audience_page.assert_user_list_not_visible(name=self._valid_list_name)

    def test_create_user_list(self, audience_page):
        audience_page.create_user_list(name=self._valid_list_name)
        audience_page.assert_user_list_visible(name=self._valid_list_name)

    def test_share_audience(self, audience_page):
        audience_page.create_audience_from_user_list(name=self._valid_name, list_name=self._valid_list_name)
        audience_page.share_audience(name=self._valid_name)

        audience_page.assert_access_granted_visible()

        audience_page.close_modal_and_unselect_all()
        audience_page.delete_audience(name=self._valid_name)
        audience_page.assert_audience_not_visible(name=self._valid_name)
        audience_page.delete_user_list(name=self._valid_list_name)
        audience_page.assert_user_list_not_visible(name=self._valid_list_name)
