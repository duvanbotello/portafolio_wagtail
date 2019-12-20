from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from django.utils.translation import gettext as _

from home.blocks.navbar_block import NavPageLinkWithSubLinkBlock, NavDocumentLinkWithSubLinkBlock, \
    NavExternalLinkWithSubLinkBlock

NAVIGATION_BLOCKS = [
    ('page_link', NavPageLinkWithSubLinkBlock()),
    ('external_link', NavExternalLinkWithSubLinkBlock()),
    ('document_link', NavDocumentLinkWithSubLinkBlock()),
]


@register_snippet
class MenuPage(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Título'),
    )

    navigation = StreamField(NAVIGATION_BLOCKS, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('navigation')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Menú de Navegación')
        verbose_name_plural = _('Menús de Navegación')
