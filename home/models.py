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
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField, RichTextField
from home.snippet_models import MenuPage


class MainBlock(blocks.StructBlock):
    bg_imagen = ImageChooserBlock(required=True, label='Imagen de fondo de seccion',
                                  help_text='Seleccione una imagen para el fondo de la seccion de bienvenida. '
                                            'Se recomienda imagen de 1910x1055')
    message_welcome = blocks.CharBlock(label='Mensaje de Bienvenida: ')
    sub_title = blocks.CharBlock(label='Subtitulo de Mensaje de Bienvenida: ',
                                 help_text='Para efectos de la animacion se debe separar por comas. Ejemplo: '
                                           'CEO DevFolio,Web Developer,Web Designer,Frontend Developer,Graphic Designer')

    class Meta:
        template = 'blocks/main/mainblock_main_block.html'
        label = 'Seccion de Bienvenida'


class AboutBlock(blocks.StructBlock):
    text_id = blocks.CharBlock(label='Identificador de Navegacion ')
    image_profile = ImageChooserBlock(required=True, label='Imagen de Perfil',
                                      help_text='Seleccione una de Perfil para tu seccion "Sobre mi". '
                                                'Se recomienda imagen de 150x150')
    text_name = blocks.CharBlock(label='Ingrese nombre: ')
    text_profile = blocks.CharBlock(label='Ingrese rol de tu perfil: ')
    text_email = blocks.EmailBlock(label='Ingrese tu correo electronico: ')
    text_phone = blocks.CharBlock(label='Ingrese tu numero de telefono: ')
    text_about = blocks.RichTextBlock(label='Ingrese una Descripcion de perfil: ',
                                      help_text='En este apartado se recomienda escribir un '
                                                'texto no mayor a tres parrafos')

    Skill_list = blocks.ListBlock(blocks.StructBlock([
        ('name_technology', blocks.CharBlock(label='Ingrese el nombre de tu habilidad.')),
        ('num_skill',
         blocks.IntegerBlock(required=True, min_value=1, max_value=100, label='Ingrese numero de habilidad:',
                             help_text='En una escala del 1 al 100 puedes ingresar la destresa de tu habilidad.')),
    ]), label='Añadir Habilidades', required=False)

    class Meta:
        template = 'blocks/main/presentation_main_block.html'
        label = 'Seccion Sobre Mi'


class ServiceBlock(blocks.StructBlock):
    text_id = blocks.CharBlock(label='Identificador de Navegacion ')
    text_title = blocks.CharBlock(label='Ingrese Titulo del bloque Servicios: ')
    text_subtitle = blocks.CharBlock(label='Ingrese subtitulo del bloque servicio.')
    service_list = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(label='Ícono de servicio: ', max_length=255, blank=True, null=True,
                                  required=False, help_text=mark_safe('Agregue el texto que referencia un icono.'
                                                                      ' Ejemplo: ion-code-working Lista de iconos: '
                                                                      '<a target="_blank" '
                                                                      'href="https://ionicons.com/v2/cheatsheet.html">'
                                                                      'Íconos</a>'))),
        ('name_service', blocks.CharBlock(label='Ingrese el nombre del servicio')),
        ('description_service', blocks.TextBlock(label='Ingrese una breve descripcion del servicio.')),
    ]), label='Añadir Servicio', required=False)

    class Meta:
        template = 'blocks/main/service_main_block.html'
        label = 'Mis servicios'


class ExperienceBlock(blocks.StructBlock):
    num_work = blocks.IntegerBlock(label='Ingrese el numero de trabajos completados')
    num_years = blocks.IntegerBlock(label='Ingrese años de experiencia')
    num_clients = blocks.IntegerBlock(label='Ingrese cantidad de clientes')
    num_awards = blocks.IntegerBlock(label='Ingrese Cantidad de premios obtenidos')

    class Meta:
        template = 'blocks/main/experience_main_block.html'
        label = 'Mi experiencia'


LAYOUT_STREAMBLOCKS = [
    ('ExperienceBlock', ExperienceBlock()),
    ('ServiceBlock', ServiceBlock()),
    ('aboutblock', AboutBlock()),
    ('mainblock', MainBlock()),
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
        help_text=('Ingrese email a donde llegarán los datos de contacto enviados por el formulario'),
    )
    panels = [
        FieldPanel('email'),
    ]


@register_setting(icon='mail')
class EmailSettings(BaseSetting, ClusterableModel):
    class Meta:
        verbose_name = ('Email')

    panels = [
        MultiFieldPanel(
            [
                InlinePanel('email_setting', label='Emails de envío de datos')

            ],
            heading=('Emails')
        ),
    ]


FORM_FIELD_CHOICES = (
    ('singleline', ('Single line text')),
    ('multiline', ('Multi-line text')),
    ('email', ('Email')),
    ('number', ('Number')),
    ('url', ('URL')),
    ('dropdown', ('Drop down')),
    ('multiselect', ('Multiple select')),
    ('date', ('Date')),
    ('datetime', ('Date/time')),
    ('hidden', ('Hidden field')),
)


class FormField(AbstractFormField):
    field_type = models.CharField(verbose_name=('field type'), max_length=16, choices=FORM_FIELD_CHOICES)
    icon = models.CharField(verbose_name=('Ícono'), max_length=255, blank=False, null=False, default="",
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

    intro = RichTextField(blank=True, verbose_name=("Texto de introducción"),
                          help_text=("Ingrese el texto que se mostrará encima del formulario"))
    thank_you_text = RichTextField(blank=True, verbose_name=("Texto después de envío"),
                                   help_text=("Ingrese texto para indicar que el formulario ha sido enviado"))

    parent_page_types = ['home.HomePage']

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label=("Campos del formulario")),
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
        verbose_name = ('Formulario')
        verbose_name_plural = ('Formularios')

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