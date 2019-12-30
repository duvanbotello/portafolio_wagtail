from django.utils.safestring import mark_safe
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


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


class PortfolioBlockMain(blocks.StructBlock):
    text_id = blocks.CharBlock(label='Identificador de Navegacion ')
    text_title = blocks.CharBlock(label='Ingrese Titulo de bloque: ')
    subtitle = blocks.CharBlock(label='Ingrese subtitulo del bloque: ')

    project_list = blocks.ListBlock(blocks.StructBlock([
        ('project_image', ImageChooserBlock(required=True, label='Imagen de proyecto',
                                      help_text='Seleccione una de Perfil para tu seccion "Sobre mi". '
                                                'Se recomienda imagen de 150x150')),
        ('project_description', blocks.RichTextBlock(label='Ingrese una Descripcion del proyecto: ',
                                      help_text='En este apartado se recomienda escribir un '
                                                'texto no mayor a un parrafo')),
        ('project_url', blocks.URLBlock(label='Ingrese url de DEMO del proyecto.')),
    ]), label='Añadir Proyecto', required=False)

    class Meta:
        template = 'blocks/main/portfolioblock_main_block.html'
        label = 'Nuevo Portafolio'


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


class ContactBlock(blocks.StructBlock):
    text_id = blocks.CharBlock(label='Identificador de Navegacion ')
    text_title_main = blocks.CharBlock(label='Titulo Principal:', help_text='Ejemplo: Envíenos un mensaje')
    text_title_secondary = blocks.CharBlock(label='Titulo Segundario:', help_text='Ejemplo: Otros canales..')
    text_description = blocks.RichTextBlock(label='Ingrese una Descripcion de contacto: ',
                                      help_text='Se recomienda un texto menor a 40 palabras')
    text_address = blocks.CharBlock(label='Direccion de residencia:', help_text='329 WASHINGTON ST BOSTON, MA 02108')
    number_contact = blocks.CharBlock(label='Telefono de contacto:', help_text='(617) 557-0089')
    email = blocks.EmailBlock(label='Correo de Contacto:', help_text='contact@example.com')

    social_list = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(label='Ícono de redsocial: ', max_length=255, blank=True, null=True,
                                  required=False, help_text=mark_safe('Agregue el texto que referencia un icono.'
                                                                      ' Ejemplo: ion-social-facebook Lista de iconos: '
                                                                      '<a target="_blank" '
                                                                      'href="https://ionicons.com/v2/cheatsheet.html">'
                                                                      'Íconos</a>'))),
        ('url_social', blocks.URLBlock(label='Ingrese url de red social')),
    ]), label='Añadir Red Social', required=False)

    class Meta:
        template = 'blocks/main/contact_main_block.html'
        label = 'Bloque de contacto'


class ExperienceBlock(blocks.StructBlock):
    num_work = blocks.IntegerBlock(label='Ingrese el numero de trabajos completados')
    num_years = blocks.IntegerBlock(label='Ingrese años de experiencia')
    num_clients = blocks.IntegerBlock(label='Ingrese cantidad de clientes')
    num_awards = blocks.IntegerBlock(label='Ingrese Cantidad de premios obtenidos')

    class Meta:
        template = 'blocks/main/experience_main_block.html'
        label = 'Mi experiencia'


class TestimonialBlock(blocks.StructBlock):

    text_id = blocks.CharBlock(label='Identificador de Navegacion ')

    Testimonial_list = blocks.ListBlock(blocks.StructBlock([
        ('image_profile', ImageChooserBlock(required=True, label='Imagen perfil del cliente',
                                      help_text='Seleccione una de Perfil del autor'
                                                'Se recomienda imagen de 150x150')),
        ('text_name', blocks.CharBlock(label='Ingrese nombre completo del autor: ')),
        ('text_Testimonial', blocks.TextBlock(label='Ingrese Descripcion del Testimonio: ',
                                      help_text='En este apartado se recomienda escribir un '
                                                'texto no mayor a un parrafo')),
    ]), label='Añadir Testimonio', required=False)

    class Meta:
        template = 'blocks/main/testimonials_main_block.html'
        label = 'Bloque de Testimonios'


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