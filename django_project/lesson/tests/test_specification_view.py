# coding=utf-8
"""Test for lesson views."""
import logging

from django.core.urlresolvers import reverse

from django.test import TestCase, override_settings, Client

from base.tests.model_factories import ProjectF
from core.model_factories import UserF
from lesson.tests.model_factories import SectionF, WorksheetF, SpecificationF


class TestViews(TestCase):
    """Tests that Lesson Specification views work."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """
        Setup before each test
        We force the locale to en otherwise it will use
        the locale of the host running the tests and we
        will get unpredictable results / 404s
        """

        self.client = Client()
        self.client.post(
                '/set_language/', data={'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.user = UserF.create(**{'username': 'timlinux', 'is_staff': True})
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

        # Create project
        self.test_project = ProjectF.create()

        # Create section
        self.test_section = SectionF.create()

        # Create worksheet
        self.test_worksheet = WorksheetF.create()

        # Create specification
        self.test_specification = SpecificationF.create()

        self.kwargs_project = {
            'project_slug': self.test_worksheet.section.project.slug
        }
        self.kwargs_section = {
            'section_slug': self.test_worksheet.section.slug
        }
        self.kwargs_worksheet = {
            'worksheet_slug': self.test_worksheet.slug
        }
        self.kwargs_specification = {
            'specification_slug': self.test_specification.slug
        }
        self.kwargs_parent = {
            'worksheet_slug': self.test_worksheet.slug,
            'section_slug': self.test_worksheet.section.slug,
            'project_slug': self.test_worksheet.section.project.slug,
        }
        self.kwargs_full = {
            'slug': self.test_specification.slug,
            'worksheet_slug': self.test_specification.worksheet.slug,
            'section_slug': self.test_specification.worksheet.section.slug,
            'project_slug': (
                self.test_specification.worksheet.section.project.slug),
        }

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SpecificationListView(self):
        """Test List View of Worksheet."""
        client = Client()
        response = client.get(
            reverse('specification-list', kwargs=self.kwargs_parent))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'specification/list.html', 'lesson/specification_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
