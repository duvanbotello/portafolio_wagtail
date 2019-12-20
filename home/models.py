from django.db import models
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


LAYOUT_STREAMBLOCKS = [
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

    class Meta:
        verbose_name = 'Configuraciones Generales'

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('text_menu'),

            ],
            heading='Configuraciones página'
        ),
    ]