import pytest
from base_case import BaseCase
import logging

logger = logging.getLogger(__name__)


class TestCampaigns(BaseCase):
    CAMPAIGN_NAME_1 = 'test_campaign_alpha_fixed'
    CAMPAIGN_NAME_2 = 'test_campaign_beta_fixed'
    CAMPAIGN_URL = 'https://vk.com'
    CAMPAIGN_BUDGET_1 = '1000'
    CAMPAIGN_BUDGET_2 = '10000'

    GROUP_NAME = 'test_group_fixed'
    AD_NAME_1 = 'test_advertisement_one_fixed'
    AD_NAME_2 = 'объявление_два_fixed'
    AD_HEADER_1 = 'header_one_fixed'
    AD_DESCRIPTION_1 = 'description_one_fixed'
    AD_HEADER_2 = 'заголовок_два_fixed'
    AD_DESCRIPTION_2 = 'описание_два_fixed'

    FOLDER_NAME_1 = 'test_folder_one_fixed'
    FOLDER_NAME_2 = 'test_folder_two_fixed'

    @pytest.fixture
    def campaign(self, campaigns_page):
        name = self.CAMPAIGN_NAME_1
        campaigns_page.ensure_on_page()

        campaigns_page.create_campaign_site(
            name=name,
            url=self.CAMPAIGN_URL,
            budget=self.CAMPAIGN_BUDGET_1,
            group_name=self.GROUP_NAME,
            ad_name=self.AD_NAME_1,
            header=self.AD_HEADER_1,
            description=self.AD_DESCRIPTION_1,
        )
        campaigns_page.assert_campaign_visible(name)
        yield name
        try:
            campaigns_page.ensure_on_page()
            campaigns_page.delete_campaign(name=name)
            campaigns_page.assert_campaign_not_visible(name, timeout=5)
        except Exception as e:
            logger.error(f"Error during campaign teardown for '{name}': {e}")

    @pytest.fixture
    def folder(self, campaigns_page):
        name = self.FOLDER_NAME_1
        campaigns_page.ensure_on_page()

        campaigns_page.create_folder(name=name)
        campaigns_page.assert_folder_visible(name)
        yield name
        try:
            campaigns_page.ensure_on_page()
            campaigns_page.delete_folder(name=name)
        except Exception as e:
            logger.error(f"Error during folder teardown for '{name}': {e}")

    def test_create_campaign(self, campaigns_page, campaign):
        campaign_name = campaign
        campaigns_page.assert_campaign_visible(name=campaign_name)

    def test_delete_campaign(self, campaigns_page, campaign):
        campaign_name = campaign
        campaigns_page.delete_campaign(name=campaign_name)
        campaigns_page.assert_campaign_not_visible(name=campaign_name)

    def test_search_campaign(self, campaigns_page, campaign):
        campaign_name = campaign
        campaigns_page.search_for_campaign(name=campaign_name)
        campaigns_page.assert_campaign_visible(name=campaign_name)

        campaigns_page.clear_search()
        campaigns_page.assert_campaign_visible(name=campaign_name)

    def test_search_non_existent_campaign(self, campaigns_page):
        non_existent_name = "non_existent_campaign_xyz123_ совершенно_уникальное_имя"
        campaigns_page.search_for_campaign(name=non_existent_name)
        campaigns_page.assert_campaign_not_visible(name=non_existent_name)
        campaigns_page.clear_search()
        campaigns_page.assert_campaign_not_visible(name=non_existent_name)

    def test_create_folder(self, campaigns_page, folder):
        folder_name = folder
        campaigns_page.assert_folder_visible(name=folder_name)

    def test_delete_folder(self, campaigns_page, folder):
        folder_name = folder
        campaigns_page.delete_folder(name=folder_name)

    def test_add_campaign_to_folder_and_verify(self, campaigns_page, campaign, folder):
        campaign_name = campaign
        folder_name = folder
        campaigns_page.add_campaign_to_folder(folder_name=folder_name, campaign_name=campaign_name)

        campaigns_page.select_folder(name=folder_name)
        campaigns_page.assert_folder_selected(name=folder_name)
        campaigns_page.assert_campaign_visible(name=campaign_name)

    def test_edit_campaign_name_and_budget(self, campaigns_page, campaign):
        original_name = campaign
        new_name = self.CAMPAIGN_NAME_2
        new_budget = self.CAMPAIGN_BUDGET_2

        campaigns_page.edit_campaign(
            original_name=original_name,
            new_name=new_name,
            budget=new_budget
        )

        campaigns_page.assert_campaign_visible(name=new_name)
        campaigns_page.assert_campaign_not_visible(name=original_name)

        try:
            logger.info(f"Teardown for test_edit_campaign: deleting campaign '{new_name}'")
            campaigns_page.delete_campaign(name=new_name)
            campaigns_page.assert_campaign_not_visible(name=new_name, timeout=5)
        except Exception as e:
            logger.error(f"Could not clean up edited campaign '{new_name}' in test_edit_campaign_name_and_budget: {e}")

    def test_edit_ad_details(self, campaigns_page, campaign):
        campaigns_page.ensure_on_page()

        campaigns_page.edit_ad(
            original_ad_name=self.AD_NAME_1,
            new_name=self.AD_NAME_2,
            header=self.AD_HEADER_2,
            description=self.AD_DESCRIPTION_2
        )

        campaigns_page.assert_ad_visible(name=self.AD_NAME_2)
        campaigns_page.assert_ad_not_visible(name=self.AD_NAME_1)