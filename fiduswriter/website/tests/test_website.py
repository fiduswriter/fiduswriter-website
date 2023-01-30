import time
import os
from tempfile import mkdtemp

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from testing.testcases import LiveTornadoTestCase
from testing.selenium_helper import SeleniumHelper

from django.core import mail

from website import models


class WebsiteTest(LiveTornadoTestCase, SeleniumHelper):
    fixtures = [
        "initial_documenttemplates.json",
        "initial_styles.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = cls.live_server_url
        cls.download_dir = mkdtemp()
        driver_data = cls.get_drivers(1, cls.download_dir)
        cls.driver = driver_data["drivers"][0]
        cls.client = driver_data["clients"][0]
        cls.driver.implicitly_wait(driver_data["wait_time"])
        cls.wait_time = driver_data["wait_time"]

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        os.rmdir(cls.download_dir)
        super().tearDownClass()

    def setUp(self):
        self.user = self.create_user(
            username="user",
            email="user@sciencenewsportal.com",
            passtext="otter1",
        )
        self.editor = self.create_user(
            username="editor",
            email="editor@sciencenewsportal.com",
            passtext="otter1",
        )
        models.Editor.objects.create(user=self.editor)

    def test_website(self):
        self.login_user(self.user, self.driver, self.client)
        self.driver.get(self.base_url + "/documents/")
        # Create news article 1
        WebDriverWait(self.driver, self.wait_time).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".new_document button")
            )
        ).click()
        WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "editor-toolbar"))
        )
        self.driver.find_element(By.CSS_SELECTOR, ".article-title").click()
        self.driver.find_element(By.CSS_SELECTOR, ".article-title").send_keys(
            "News article 1"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, "span.header-nav-item[title='Publish to website']"
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR,
            "span.fw-pulldown-item[title='Submit for publishing to website']",
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).click()
        submission_message = "This article is ready for publication."
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).send_keys(submission_message)
        emails_before_submission = len(mail.outbox)
        self.driver.find_element(By.CSS_SELECTOR, "button.fw-dark").click()
        time.sleep(1)
        # Check that email has been sent to editor
        emails_after_submission = len(mail.outbox)
        assert emails_after_submission == (emails_before_submission + 1)
        notify_editor_email = mail.outbox[-1]
        assert self.editor.email in notify_editor_email.to
        assert submission_message in notify_editor_email.body
        assert "submitted to be published" in notify_editor_email.body

        # Log in as editor and ask for changes.
        self.login_user(self.editor, self.driver, self.client)
        document_link = self.find_urls(notify_editor_email.body)[0]
        self.driver.get(document_link)
        self.driver.find_element(
            By.CSS_SELECTOR, "span.header-nav-item[title='Publish to website']"
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR,
            "span.fw-pulldown-item[title='Publish, reject or request changes']",
        ).click()
        review_message = self.driver.find_element(
            By.CSS_SELECTOR, "#submission-dialog"
        )
        assert submission_message in review_message.text
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).click()
        editor_message = "It's good, but not quite good enough."
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).send_keys(editor_message)
        emails_before_ask_for_changes = len(mail.outbox)
        self.driver.find_elements(By.CSS_SELECTOR, "button.fw-dark")[1].click()
        time.sleep(1)
        # Check that email has been sent to user
        emails_after_ask_for_changes = len(mail.outbox)
        assert emails_after_ask_for_changes == (
            emails_before_ask_for_changes + 1
        )
        notify_user_email = mail.outbox[-1]
        assert self.user.email in notify_user_email.to
        assert editor_message in notify_user_email.body
        assert "need to change some things" in notify_user_email.body

        # Log in as user, make changes and resubmit.
        self.login_user(self.user, self.driver, self.client)
        document_link = self.find_urls(notify_user_email.body)[0]
        self.driver.get(document_link)
        self.driver.find_element(By.CSS_SELECTOR, ".article-body").click()
        self.driver.find_element(By.CSS_SELECTOR, ".article-body").send_keys(
            "An updated body."
        )
        self.driver.find_element(
            By.CSS_SELECTOR, "span.header-nav-item[title='Publish to website']"
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR,
            "span.fw-pulldown-item[title='Submit for publishing to website']",
        ).click()
        review_message = self.driver.find_element(
            By.CSS_SELECTOR, "#submission-dialog"
        )
        assert submission_message in review_message.text
        assert editor_message in review_message.text
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).click()
        resubmission_message = "I've made substantial changes. Please review."
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).send_keys(resubmission_message)
        emails_before_resubmission = len(mail.outbox)
        self.driver.find_element(By.CSS_SELECTOR, "button.fw-dark").click()
        time.sleep(1)
        # Check that email has been sent to editor
        emails_after_resubmission = len(mail.outbox)
        assert emails_after_resubmission == (emails_before_resubmission + 1)
        notify_editor_again_email = mail.outbox[-1]
        assert self.editor.email in notify_editor_again_email.to
        assert resubmission_message in notify_editor_again_email.body
        assert "submitted to be published" in notify_editor_again_email.body

        # Log in as editor and reject.
        self.login_user(self.editor, self.driver, self.client)
        document_link = self.find_urls(notify_editor_email.body)[0]
        self.driver.get(document_link)
        self.driver.find_element(
            By.CSS_SELECTOR, "span.header-nav-item[title='Publish to website']"
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR,
            "span.fw-pulldown-item[title='Publish, reject or request changes']",
        ).click()
        review_message = self.driver.find_element(
            By.CSS_SELECTOR, "#submission-dialog"
        )
        assert submission_message in review_message.text
        assert editor_message in review_message.text
        assert resubmission_message in review_message.text
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).click()
        rejection_message = "I don't think you realize what a serious we are. This submission has been rejected."
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).send_keys(rejection_message)
        emails_before_rejection = len(mail.outbox)
        self.driver.find_elements(By.CSS_SELECTOR, "button.fw-dark")[2].click()
        time.sleep(1)
        # Check that email has been sent to editor
        emails_after_rejection = len(mail.outbox)
        assert emails_after_rejection == (emails_before_rejection + 1)
        notify_user_again_email = mail.outbox[-1]
        assert self.user.email in notify_user_again_email.to
        assert rejection_message in notify_user_again_email.body
        assert "reviewed and rejected" in notify_user_again_email.body

        # Check that article does not show on front page
        self.logout_user(self.driver, self.client)
        self.driver.get(self.base_url + "/")
        articles_shown = self.driver.find_elements(
            By.CSS_SELECTOR, "div.articles a.article"
        )
        assert len(articles_shown) == 0

        # Write a second article.
        self.login_user(self.user, self.driver, self.client)
        self.driver.get(self.base_url + "/documents/")
        # Create news article 1
        WebDriverWait(self.driver, self.wait_time).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".new_document button")
            )
        ).click()
        WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "editor-toolbar"))
        )
        self.driver.find_element(By.CSS_SELECTOR, ".article-title").click()
        self.driver.find_element(By.CSS_SELECTOR, ".article-title").send_keys(
            "News article 2"
        )
        self.driver.find_element(By.CSS_SELECTOR, ".article-body").click()
        self.driver.find_element(By.CSS_SELECTOR, ".article-body").send_keys(
            "This article has a real body."
        )
        self.driver.find_element(
            By.CSS_SELECTOR, "span.header-nav-item[title='Publish to website']"
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR,
            "span.fw-pulldown-item[title='Submit for publishing to website']",
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).click()
        submission_message = "This article is ready for publication and much better than the previous one."
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).send_keys(submission_message)
        emails_before_submission = len(mail.outbox)
        self.driver.find_element(By.CSS_SELECTOR, "button.fw-dark").click()
        time.sleep(1)
        # Check that email has been sent to editor
        emails_after_submission = len(mail.outbox)
        assert emails_after_submission == (emails_before_submission + 1)
        notify_editor_email = mail.outbox[-1]
        assert self.editor.email in notify_editor_email.to
        assert submission_message in notify_editor_email.body
        assert "submitted to be published" in notify_editor_email.body

        # Log in as editor and publish.
        self.login_user(self.editor, self.driver, self.client)
        document_link = self.find_urls(notify_editor_email.body)[0]
        self.driver.get(document_link)
        self.driver.find_element(
            By.CSS_SELECTOR, "span.header-nav-item[title='Publish to website']"
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR,
            "span.fw-pulldown-item[title='Publish, reject or request changes']",
        ).click()
        review_message = self.driver.find_element(
            By.CSS_SELECTOR, "#submission-dialog"
        )
        assert submission_message in review_message.text
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).click()
        editor_message = "It's good, really good. I'll publish it right away."
        self.driver.find_element(
            By.CSS_SELECTOR, "textarea#submission-message"
        ).send_keys(editor_message)
        emails_before_publishing = len(mail.outbox)
        self.driver.find_elements(By.CSS_SELECTOR, "button.fw-dark")[0].click()
        time.sleep(1)
        # Check that email has been sent to user
        emails_after_publishing = len(mail.outbox)
        assert emails_after_publishing == (emails_before_publishing + 1)
        notify_user_email = mail.outbox[-1]
        assert self.user.email in notify_user_email.to
        assert editor_message in notify_user_email.body

        # Check that article does show on front page
        self.logout_user(self.driver, self.client)
        self.driver.get(self.base_url + "/")
        articles_shown = self.driver.find_elements(
            By.CSS_SELECTOR, "div.articles a.article"
        )
        assert len(articles_shown) == 1

        # Log in as editor and publish directly.
        self.login_user(self.editor, self.driver, self.client)
        self.driver.get(self.base_url + "/documents/")
        # Create news article 1
        WebDriverWait(self.driver, self.wait_time).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".new_document button")
            )
        ).click()
        WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "editor-toolbar"))
        )
        self.driver.find_element(By.CSS_SELECTOR, ".article-title").click()
        self.driver.find_element(By.CSS_SELECTOR, ".article-title").send_keys(
            "News article 3"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, "span.header-nav-item[title='Publish to website']"
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR,
            "span.fw-pulldown-item[title='Publish, reject or request changes']",
        ).click()
        emails_before_publishing = len(mail.outbox)
        self.driver.find_elements(By.CSS_SELECTOR, "button.fw-dark")[0].click()
        time.sleep(1)
        # Check that no email has been sent to user
        emails_after_publishing = len(mail.outbox)
        assert emails_after_publishing == emails_before_publishing

        # Check that article does show on front page
        self.logout_user(self.driver, self.client)
        self.driver.get(self.base_url + "/")
        articles_shown = self.driver.find_elements(
            By.CSS_SELECTOR, "div.articles a.article"
        )
        assert len(articles_shown) == 2
