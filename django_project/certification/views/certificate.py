# coding=utf-8
import urllib2
from django.http import Http404, HttpResponse
from django.views.generic import CreateView, DetailView
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Image
from core.settings.base import MEDIA_ROOT
from ..models import Certificate, Course, Attendee
from ..forms import CertificateForm
from base.models.project import Project
from PIL import Image as Im


class CertificateMixin(object):
    """Mixin class to provide standard settings for Certificate."""

    model = Certificate
    form_class = CertificateForm


class CertificateCreateView(
        LoginRequiredMixin, CertificateMixin, CreateView):
    """Create view for Certificate."""

    context_object_name = 'certificate'
    template_name = 'certificate/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the Course detail page.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('course-detail', kwargs={
            'project_slug': self.project_slug,
            'organisation_slug': self.organisation_slug,
            'slug': self.course_slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CertificateCreateView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.course_slug)
        context['attendee'] = Attendee.objects.get(pk=self.pk)
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CertificateCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.course_slug = self.kwargs.get('course_slug', None)
        self.pk = self.kwargs.get('pk', None)
        self.course = Course.objects.get(slug=self.course_slug)
        self.attendee = Attendee.objects.get(pk=self.pk)
        kwargs.update({
            'user': self.request.user,
            'course': self.course,
            'attendee': self.attendee,
        })
        return kwargs


class CertificateDetailView(DetailView):
    """Detail view for Certificate."""

    model = Certificate
    context_object_name = 'certificate'
    template_name = 'certificate/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        self.certificateID = self.kwargs.get('id', None)
        context = super(
            CertificateDetailView, self).get_context_data(**kwargs)
        context['certificate'] = \
            Certificate.objects.get(certificateID=self.certificateID)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is all certificate in the
            corresponding organisation.
        :rtype: QuerySet
        """

        qs = Certificate.objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a certificate
            depends on the input certificate ID.
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            certificateID = self.kwargs.get('id', None)
            if certificateID:
                obj = queryset.get(
                    certificateID=certificateID)
                return obj
            else:
                raise Http404('Sorry! Certificate by this ID is not exist.')


def certificate_pdf_view(request, **kwargs):

    project_slug = kwargs.pop('project_slug')
    course_slug = kwargs.pop('course_slug')
    pk = kwargs.pop('pk')
    project = Project.objects.get(slug=project_slug)
    course = Course.objects.get(slug=course_slug)
    attendee = Attendee.objects.get(pk=pk)
    certificate = Certificate.objects.get(course=course, attendee=attendee)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="certificate.pdf"'

    # Create the PDF object, using the response object as its "file."
    page = canvas.Canvas(response, pagesize=landscape(A4))
    width, height = A4
    center = height * 0.5

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    file_image = project.image_file.file
    page.setFillColorRGB(0.1, 0.1, 0.1)
    page.setFont('Times-Roman', 18)
    page.drawString(70, 520, project.name)
    #page.drawString(70, 550, str(file_image))
    #image = Im.open(str(file_image))
    #page.drawInlineImage(Image(image), 20, 520, 50, 50)
    page.drawString(550, 520, 'Certificate ID: %s' % certificate.certificateID)
    page.setFont('Times-Bold', 26)
    page.drawCentredString(center, 450, 'Certificate of Completion')
    page.drawCentredString(
        center, 370, '%s %s' % (attendee.firstname, attendee.surname))
    page.setFont('Times-Roman', 16)
    page.drawCentredString(
        center, 330, 'Has attended and completed the course:')
    page.setFont('Times-Bold', 20)
    page.drawCentredString(center, 290, course.course_type.name)
    page.setFont('Times-Roman', 16)
    page.drawString(
        290, 250, 'Course Date: %s - %s'
                  % (course.start_date, course.end_date))
    page.drawString(290, 220, 'Convener: %s' % course.course_convener.user)
    page.setFillColorRGB(0.1, 0.1, 0.1)
    page.drawCentredString(
        center, 170, 'Presented by %s at %s' % (
            course.certifying_organisation, course.training_center))
    page.setFont('Times-Roman', 8)
    page.drawString(
        70,30, 'You can verify this certificate by visiting this page.')

    # Close the PDF object cleanly.
    page.showPage()
    page.save()
    return response
