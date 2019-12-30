from django.db import models
from django.template.loader import render_to_string

from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel, FieldPanel, InlinePanel, FieldRowPanel
from wagtail.admin.mail import send_mail

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting


from wagtail.core import blocks
from wagtail.core.blocks import ListBlock
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from home.blocks.wagtail_blocks import TestimonialBlock, ContactBlock, ExperienceBlock, ServiceBlock, AboutBlock, \
    MainBlock
from home.snippet_models import MenuPage





LAYOUT_STREAMBLOCKS2 = [
    ('TestimonialBlock', TestimonialBlock()),
    ('ContactBlock', ContactBlock()),
    ('ExperienceBlock', ExperienceBlock()),
    ('ServiceBlock', ServiceBlock()),
    ('aboutblock', AboutBlock()),
    ('mainblock', MainBlock()),
]


@register_snippet
class Book(models.Model):
    title = models.CharField(max_length=255)

    body = StreamField(LAYOUT_STREAMBLOCKS2, null=True, blank=True)

    panels = [
        FieldPanel('title'),
        StreamFieldPanel('body'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Portafolio'
        verbose_name_plural = 'Portafolios'


class portfolioBlock(blocks.StructBlock):
    protfolio = ListBlock(SnippetChooserBlock(Book))

    class Meta:
        template = 'blocks/main/portfolio_main_block.html'
        label = 'Bloque Portafolio'


LAYOUT_STREAMBLOCKS = [
    ('TestimonialBlock', TestimonialBlock()),
    ('ContactBlock', ContactBlock()),
    ('ExperienceBlock', ExperienceBlock()),
    ('ServiceBlock', ServiceBlock()),
    ('aboutblock', AboutBlock()),
    ('mainblock', MainBlock()),
    ('portfolioBlock', portfolioBlock()),
]


class HomePage(Page):
    menu = models.ForeignKey(
        MenuPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(LAYOUT_STREAMBLOCKS, null=True, blank=True)

    content_panels = [
        SnippetChooserPanel('menu'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Página principal'


@register_setting
class CongGeneralSettings(BaseSetting):
    text_menu = models.CharField(verbose_name='Ingrese Texto de menu', null=False, max_length=15)
    text_copyright = models.CharField(verbose_name='Ingrese Texto pie de pagina: Copyright', null=True, max_length=255)

    class Meta:
        verbose_name = 'Configuraciones Generales'

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('text_menu'),
                FieldPanel('text_copyright'),
            ],
            heading='Configuraciones página'
        ),
    ]


class Email(models.Model):
    parent = ParentalKey('EmailSettings', related_name='email_setting')
    # parent = models.ForeignKey('EmailSettings', related_name='email_setting', on_delete=models.CASCADE)
    email = models.EmailField(
        blank=False,
        verbose_name=('Email'),
        default='',
        help_text='Ingrese email a donde llegarán los datos de contacto enviados por el formulario',
    )
    panels = [
        FieldPanel('email'),
    ]


@register_setting(icon='mail')
class EmailSettings(BaseSetting, ClusterableModel):
    class Meta:
        verbose_name = 'Email'

    panels = [
        MultiFieldPanel(
            [
                InlinePanel('email_setting', label='Emails de envío de datos')

            ],
            heading='Emails'
        ),
    ]


FORM_FIELD_CHOICES = (
    ('singleline', 'Single line text'),
    ('multiline', 'Multi-line text'),
    ('email', 'Email'),
    ('number', 'Number'),
    ('url', 'URL'),
    ('dropdown', 'Drop down'),
    ('multiselect', 'Multiple select'),
    ('date', 'Date'),
    ('datetime', 'Date/time'),
    ('hidden', 'Hidden field'),
)


class FormField(AbstractFormField):
    field_type = models.CharField(verbose_name='field type', max_length=16, choices=FORM_FIELD_CHOICES)
    icon = models.CharField(verbose_name='Ícono', max_length=255, blank=False, null=False, default="",
                            help_text=mark_safe('Agregue el texto que referencia un icono.'
                                                ' Ejemplo: <b>ti-location-pin</b>. Lista de iconos: '
                                                '<a target="_blank" '
                                                'href="https://themify.me/themify-icons">'
                                                'Íconos themify</a> o '
                                                '<a target="_blank" '
                                                'href="https://fontawesome.com/icons?d=gallery">'
                                                'Íconos FontAwesome</a>'
                                                ))
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

    panels = AbstractFormField.panels + [
        FieldPanel('icon')
    ]


class FormPage(AbstractEmailForm):

    intro = RichTextField(blank=True, verbose_name="Texto de introducción",
                          help_text="Ingrese el texto que se mostrará encima del formulario")
    thank_you_text = RichTextField(blank=True, verbose_name="Texto después de envío",
                                   help_text="Ingrese texto para indicar que el formulario ha sido enviado")

    parent_page_types = ['home.HomePage']

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Campos del formulario"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    class Meta:
        verbose_name = 'Formulario'
        verbose_name_plural = 'Formularios'

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(',')]
        context = {
            'subject': self.subject,
            'title': self.title,
            'render_data': [

            ]

        }
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            context['render_data'].append({
                'title': field.label,
                'data': value
            })

        html_message = render_to_string('form_email.html', context)
        plain_message = strip_tags(html_message)
        send_mail(self.subject, plain_message, addresses, self.from_address, html_message=html_message,
                  fail_silently=False)



