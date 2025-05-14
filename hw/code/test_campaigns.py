import pytest
from base_case import BaseCase


class TestCampaigns(BaseCase):
    _valid_name = 'test'
    _valid_name2 = 'name2'
    _valid_url = 'https://vk.com'
    _valid_budget = '1000'
    _valid_budget2 = '10000'
    _valid_group_name = 'group'
    _valid_ad_name = 'advertisement'
    _valid_ad_name2 = 'объявление'
    _valid_header = 'header'
    _valid_description = 'description'
    _valid_header2 = 'заголовок'
    _valid_description2 = 'описание'
    _valid_group_tag = 'VK'
    _valid_folder_name = 'folder1'

    def test_create_campaign_group(self, campaigns_page):
        campaigns_page.create_campaign_group(
            name=self._valid_name,
            group_name=self._valid_group_name,
            ad_name=self._valid_ad_name,
            group_tag=self._valid_group_tag,
            description=self._valid_description,
        )
        campaigns_page.assert_campaign_visible(self._valid_name)
        campaigns_page.delete_campaign(name=self._valid_name)

    def test_create_campaign_site(self, campaigns_page):
        campaigns_page.create_campaign_site(
            name=self._valid_name,
            url=self._valid_url,
            group_name=self._valid_group_name,
            ad_name=self._valid_ad_name,
            budget=self._valid_budget,
            header=self._valid_header,
            description=self._valid_description,
        )
        campaigns_page.assert_campaign_visible(self._valid_name)
        campaigns_page.delete_campaign(name=self._valid_name)



    def test_search(self, campaigns_page):
        campaigns_page.create_campaign_site(
            name=self._valid_name,
            url=self._valid_url,
            budget=self._valid_budget,
            group_name=self._valid_group_name,
            ad_name=self._valid_ad_name,
            header=self._valid_header,
            description=self._valid_description,
        )
        campaigns_page.create_campaign_site(
            name=self._valid_name2,
            url=self._valid_url,
            budget=self._valid_budget,
            group_name=self._valid_group_name,
            ad_name=self._valid_ad_name,
            header=self._valid_header,
            description=self._valid_description,
        )

        campaigns_page.assert_campaign_visible(self._valid_name)
        campaigns_page.assert_campaign_visible(self._valid_name2)

        campaigns_page.search_for_campaign(name=self._valid_name)

        campaigns_page.assert_campaign_visible(name=self._valid_name)
        campaigns_page.assert_campaign_not_visible(name=self._valid_name2)

        campaigns_page.clear_search()
        campaigns_page.delete_campaign(name=self._valid_name)
        campaigns_page.delete_campaign(name=self._valid_name2)

    def test_create_folder(self, campaigns_page):
        campaigns_page.create_folder(name=self._valid_folder_name)
        campaigns_page.assert_folder_visible(name=self._valid_folder_name)
        campaigns_page.delete_folder(name=self._valid_folder_name)

    def test_edit_folder(self, campaigns_page):
        campaigns_page.create_campaign_site(
            name=self._valid_name,
            url=self._valid_url,
            group_name=self._valid_group_name,
            ad_name=self._valid_ad_name,
            budget=self._valid_budget,
            header=self._valid_header,
            description=self._valid_description,
        )
        campaigns_page.create_folder(name=self._valid_folder_name)
        campaigns_page.add_campaign_to_folder(folder_name=self._valid_folder_name, campaign_name=self._valid_name)
        campaigns_page.select_folder(name=self._valid_folder_name)

        campaigns_page.assert_folder_selected(name=self._valid_folder_name)
        campaigns_page.assert_campaign_visible(name=self._valid_name)

        campaigns_page.delete_folder(name=self._valid_folder_name)
        campaigns_page.delete_campaign(name=self._valid_name)

    def test_edit_campaign(self, campaigns_page):
        campaigns_page.create_campaign_site(
            name=self._valid_name,
            url=self._valid_url,
            group_name=self._valid_group_name,
            ad_name=self._valid_ad_name,
            budget=self._valid_budget,
            header=self._valid_header,
            description=self._valid_description,
        )
        campaigns_page.edit_campaign(name=self._valid_name2, budget=self._valid_budget2)

        campaigns_page.assert_campaign_visible(name=self._valid_name2)

        campaigns_page.delete_campaign(name=self._valid_name2)

    def test_edit_ad(self, campaigns_page):
        campaigns_page.create_campaign_site(
            name=self._valid_name,
            url=self._valid_url,
            group_name=self._valid_group_name,
            ad_name=self._valid_ad_name,
            budget=self._valid_budget,
            header=self._valid_header,
            description=self._valid_description,
        )

        campaigns_page.edit_ad(
            name=self._valid_ad_name,
            new_name=self._valid_ad_name2,
            header=self._valid_header2,
            description=self._valid_description2
        )

        campaigns_page.assert_ad_visible(name=self._valid_ad_name2)
        campaigns_page.delete_campaign(name=self._valid_name)