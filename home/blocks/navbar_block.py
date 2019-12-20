from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from django.utils.translation import gettext as _


class NavBaseLinkBlock(blocks.StructBlock):
    display_text = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Texto item menú'),
    )


class NavPageLinkBlock(NavBaseLinkBlock):
    """
    Page link.
    """
    page = blocks.PageChooserBlock(
        label=_('Página'),
    )

    class Meta:
        template = 'blocks/menu/page_link_block.html'
        label = _('URL página')


class NavDocumentLinkBlock(NavBaseLinkBlock):
    """
    Document link.
    """
    document = DocumentChooserBlock(
        label=_('Documento'),
    )

    class Meta:
        template = 'blocks/menu/document_link_block.html'
        label = _('URL documento')


class NavExternalLinkBlock(NavBaseLinkBlock):
    """
    External link.
    """
    link = blocks.CharBlock(
        required=False,
        label=_('URL'),
    )

    class Meta:
        template = 'blocks/menu/external_link_block.html'
        label = _('URL externa')


class NavSubLinkBlock(blocks.StructBlock):
    sub_links = blocks.StreamBlock(
        [
            ('page_link', NavPageLinkBlock()),
            ('external_link', NavExternalLinkBlock()),
            ('document_link', NavDocumentLinkBlock()),
        ],
        required=False,
        label=_('Sub menú'),
    )


class NavPageLinkWithSubLinkBlock(NavSubLinkBlock, NavPageLinkBlock):
    """
    Page link with option for sub-links or showing child pages.
    """
    open_page_new_window = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_('Abrir en una nueva página'),
        help_text=_('Seleccione si desea abrir en una nueva pestaña cuando el usuario de clic'),
    )

    class Meta:
        label = _('URL página con sub menú')


class NavDocumentLinkWithSubLinkBlock(NavSubLinkBlock, NavDocumentLinkBlock):
    """
    Document link with option for sub-links.
    """

    class Meta:
        label = _('URL Documento con sub menú')


class NavExternalLinkWithSubLinkBlock(NavSubLinkBlock, NavExternalLinkBlock):
    """
    External link with option for sub-links.
    """

    class Meta:
        label = _('URL externa con sub menú')

