from __future__ import absolute_import

from sentry.models import Rule
from sentry.testutils import AcceptanceTestCase


class ProjectAlertSettingsTest(AcceptanceTestCase):
    def setUp(self):
        super(ProjectAlertSettingsTest, self).setUp()
        self.user = self.create_user('foo@example.com')
        self.org = self.create_organization(
            name='Rowdy Tiger',
            owner=None,
        )
        self.team = self.create_team(
            organization=self.org,
            name='Mariachi Band'
        )
        self.project = self.create_project(
            organization=self.org,
            team=self.team,
            name='Bengal',
        )
        self.create_member(
            user=self.user,
            organization=self.org,
            role='owner',
            teams=[self.team],
        )

        action_data = {
            'id': 'sentry.rules.actions.notify_event.NotifyEventAction',
        }
        condition_data = {
            'id': 'sentry.rules.conditions.every_event.EveryEventCondition',
        }

        Rule.objects.filter(project=self.project).delete()

        Rule.objects.create(
            project=self.project,
            data={
                'conditions': [condition_data],
                'actions': [action_data],
            }
        )

        self.login_as(self.user)
        self.path1 = '/{}/{}/settings/plugins/webhooks/'.format(self.org.slug, self.project.slug)

    def test_settings_load(self):
        self.browser.get(self.path1)
        self.browser.wait_until('.ref-plugin-config-webhooks')
        self.browser.wait_until_not('.loading-indicator')
        self.browser.snapshot('project alert settings webhooks enabled')
