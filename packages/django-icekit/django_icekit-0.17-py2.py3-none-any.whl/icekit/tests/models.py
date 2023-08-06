"""
Test models for ``icekit`` app.
"""
from urlparse import urljoin

from django.db import models
from django.http import HttpResponse

from fluent_pages.extensions import page_type_pool
from icekit.publishing.models import PublishableFluentContents

from icekit import abstract_models
from icekit.content_collections.abstract_models import AbstractListingPage, \
    AbstractCollectedContent, TitleSlugMixin
from icekit.content_collections.page_type_plugins import ListingPagePlugin

from icekit.page_types.layout_page.abstract_models import \
    AbstractLayoutPage, AbstractUnpublishableLayoutPage
from icekit.publishing.models import PublishingModel
from icekit.plugins import ICEkitFluentContentsPagePlugin
from icekit import mixins

class BaseModel(abstract_models.AbstractBaseModel):
    """
    Concrete base model.
    """
    pass


class FooWithLayout(mixins.LayoutFieldMixin):
    pass


class BarWithLayout(mixins.LayoutFieldMixin):
    pass


class BazWithLayout(mixins.LayoutFieldMixin):
    pass


class ImageTest(models.Model):
    image = models.ImageField(upload_to='testing/')


class ArticleListing(AbstractListingPage):
    """A page that lists articles that link to it as parent"""

    def get_items_to_list(self, request=None):
        unpublished_pk = self.get_draft().pk
        return Article.objects.published().filter(parent_id=unpublished_pk)

    def get_items_to_mount(self, request):
        unpublished_pk = self.get_draft().pk
        return Article.objects.visible().filter(parent_id=unpublished_pk)

    class Meta:
        db_table = 'test_articlelisting'


class Article(AbstractCollectedContent, PublishableFluentContents, TitleSlugMixin):
    """Articles that belong to a particular listing"""
    parent = models.ForeignKey(
        ArticleListing,
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'test_article'

    def get_response(self, request, parent=None, *args, **kwargs):
        return HttpResponse(
            u"%s: %s" % (self.parent.get_published().title, self.title)
        )


class LayoutPageWithRelatedPages(AbstractLayoutPage):
    related_pages = models.ManyToManyField('fluent_pages.Page')

    class Meta:
        db_table = 'test_layoutpage_with_related'


@page_type_pool.register
class LayoutPageWithRelatedPagesPlugin(ICEkitFluentContentsPagePlugin):
    """
    LayoutPage implementation as a plugin for use with pages.
    """
    model = LayoutPageWithRelatedPages
    render_template = 'icekit/page_types/article/default.html'


class UnpublishableLayoutPage(AbstractUnpublishableLayoutPage):
    pass


@page_type_pool.register
class UnpublishableLayoutPagePlugin(ICEkitFluentContentsPagePlugin):
    model = UnpublishableLayoutPage
    render_template = 'icekit/layouts/default.html'


@page_type_pool.register
class ArticleListingPlugin(ListingPagePlugin):
    model = ArticleListing


class PublishingM2MModelA(PublishingModel):
    pass


class PublishingM2MModelB(PublishingModel):
    related_a_models = models.ManyToManyField(
        PublishingM2MModelA,
        related_name='related_b_models',
    )
    through_related_a_models = models.ManyToManyField(
        PublishingM2MModelA,
        related_name='through_related_b_models',
        through='PublishingM2MThroughTable',
    )


class PublishingM2MThroughTable(models.Model):
    a_model = models.ForeignKey(PublishingM2MModelA)
    b_model = models.ForeignKey(PublishingM2MModelB)
