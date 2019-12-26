# Generated by Django 2.2.9 on 2019-12-26 18:53

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20191226_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('ContactBlock', wagtail.core.blocks.StructBlock([('text_id', wagtail.core.blocks.CharBlock(label='Identificador de Navegacion ')), ('text_title_main', wagtail.core.blocks.CharBlock(help_text='Ejemplo: Envíenos un mensaje', label='Titulo Principal:')), ('text_title_secondary', wagtail.core.blocks.CharBlock(help_text='Ejemplo: Otros canales..', label='Titulo Segundario:')), ('text_description', wagtail.core.blocks.RichTextBlock(help_text='Se recomienda un texto menor a 40 palabras', label='Ingrese una Descripcion de contacto: ')), ('text_address', wagtail.core.blocks.CharBlock(help_text='329 WASHINGTON ST BOSTON, MA 02108', label='Direccion de residencia:')), ('number_contact', wagtail.core.blocks.CharBlock(help_text='(617) 557-0089', label='Telefono de contacto:')), ('email', wagtail.core.blocks.EmailBlock(help_text='contact@example.com', label='Correo de Contacto:')), ('social_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.CharBlock(blank=True, help_text='Agregue el texto que referencia un icono. Ejemplo: ion-social-facebook Lista de iconos: <a target="_blank" href="https://ionicons.com/v2/cheatsheet.html">Íconos</a>', label='Ícono de redsocial: ', max_length=255, null=True, required=False)), ('url_social', wagtail.core.blocks.URLBlock(label='Ingrese url de red social'))]), label='Añadir Red Social', required=False))])), ('ExperienceBlock', wagtail.core.blocks.StructBlock([('num_work', wagtail.core.blocks.IntegerBlock(label='Ingrese el numero de trabajos completados')), ('num_years', wagtail.core.blocks.IntegerBlock(label='Ingrese años de experiencia')), ('num_clients', wagtail.core.blocks.IntegerBlock(label='Ingrese cantidad de clientes')), ('num_awards', wagtail.core.blocks.IntegerBlock(label='Ingrese Cantidad de premios obtenidos'))])), ('ServiceBlock', wagtail.core.blocks.StructBlock([('text_id', wagtail.core.blocks.CharBlock(label='Identificador de Navegacion ')), ('text_title', wagtail.core.blocks.CharBlock(label='Ingrese Titulo del bloque Servicios: ')), ('text_subtitle', wagtail.core.blocks.CharBlock(label='Ingrese subtitulo del bloque servicio.')), ('service_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.CharBlock(blank=True, help_text='Agregue el texto que referencia un icono. Ejemplo: ion-code-working Lista de iconos: <a target="_blank" href="https://ionicons.com/v2/cheatsheet.html">Íconos</a>', label='Ícono de servicio: ', max_length=255, null=True, required=False)), ('name_service', wagtail.core.blocks.CharBlock(label='Ingrese el nombre del servicio')), ('description_service', wagtail.core.blocks.TextBlock(label='Ingrese una breve descripcion del servicio.'))]), label='Añadir Servicio', required=False))])), ('aboutblock', wagtail.core.blocks.StructBlock([('text_id', wagtail.core.blocks.CharBlock(label='Identificador de Navegacion ')), ('image_profile', wagtail.images.blocks.ImageChooserBlock(help_text='Seleccione una de Perfil para tu seccion "Sobre mi". Se recomienda imagen de 150x150', label='Imagen de Perfil', required=True)), ('text_name', wagtail.core.blocks.CharBlock(label='Ingrese nombre: ')), ('text_profile', wagtail.core.blocks.CharBlock(label='Ingrese rol de tu perfil: ')), ('text_email', wagtail.core.blocks.EmailBlock(label='Ingrese tu correo electronico: ')), ('text_phone', wagtail.core.blocks.CharBlock(label='Ingrese tu numero de telefono: ')), ('text_about', wagtail.core.blocks.RichTextBlock(help_text='En este apartado se recomienda escribir un texto no mayor a tres parrafos', label='Ingrese una Descripcion de perfil: ')), ('Skill_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('name_technology', wagtail.core.blocks.CharBlock(label='Ingrese el nombre de tu habilidad.')), ('num_skill', wagtail.core.blocks.IntegerBlock(help_text='En una escala del 1 al 100 puedes ingresar la destresa de tu habilidad.', label='Ingrese numero de habilidad:', max_value=100, min_value=1, required=True))]), label='Añadir Habilidades', required=False))])), ('mainblock', wagtail.core.blocks.StructBlock([('bg_imagen', wagtail.images.blocks.ImageChooserBlock(help_text='Seleccione una imagen para el fondo de la seccion de bienvenida. Se recomienda imagen de 1910x1055', label='Imagen de fondo de seccion', required=True)), ('message_welcome', wagtail.core.blocks.CharBlock(label='Mensaje de Bienvenida: ')), ('sub_title', wagtail.core.blocks.CharBlock(help_text='Para efectos de la animacion se debe separar por comas. Ejemplo: CEO DevFolio,Web Developer,Web Designer,Frontend Developer,Graphic Designer', label='Subtitulo de Mensaje de Bienvenida: '))]))], blank=True, null=True),
        ),
    ]
