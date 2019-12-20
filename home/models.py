from django.db import models
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel, FieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from home.snippet_models import MenuPage


class MainBlock(blocks.StructBlock):

    bg_imagen = ImageChooserBlock(required=True, label='Imagen de fondo de seccion', help_text='Seleccione una imagen para el fondo de la seccion de bienvenida. Se recomienda imagen de 1910x1055')
    message_welcome = blocks.CharBlock(label='Mensaje de Bienvenida: ')
    sub_title = blocks.CharBlock(label='Subtitulo de Mensaje de Bienvenida: ', help_text='Para efectos de la animacion se debe separar por comas. Ejemplo: CEO DevFolio,Web Developer,Web Designer,Frontend Developer,Graphic Designer')

    class Meta:
        template = 'blocks/main/mainblock_main_block.html'
        label = 'Seccion de Bienvenida'


class AboutBlock(blocks.StructBlock):
    text_id = blocks.CharBlock(label='Identificador de Navegacion ')
    image_profile = ImageChooserBlock(required=True, label='Imagen de Perfil', help_text='Seleccione una de Perfil para tu seccion "Sobre mi". Se recomienda imagen de 150x150')
    text_name = blocks.CharBlock(label='Ingrese nombre: ')
    text_profile = blocks.CharBlock(label='Ingrese rol de tu perfil: ')
    text_email = blocks.EmailBlock(label='Ingrese tu correo electronico: ')
    text_phone = blocks.CharBlock(label='Ingrese tu numero de telefono: ')
    text_about = blocks.RichTextBlock(label='Ingrese una Descripcion de perfil: ', help_text='En este apartado se recomienda escribir un texto no mayor a tres parrafos')

    Skill_list = blocks.ListBlock(blocks.StructBlock([
        ('name_technology', blocks.CharBlock(label='Ingrese el nombre de tu habilidad.')),
        ('num_skill', blocks.IntegerBlock(required=True, min_value=1, max_value=100, label='Ingrese numero de habilidad:', help_text='En una escala del 1 al 100 puedes ingresar la destresa de tu habilidad.')),
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