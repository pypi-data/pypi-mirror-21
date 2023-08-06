from icekit.content_collections.abstract_models import AbstractListingPage
from .abstract_models import  AbstractArticle


class Article(AbstractArticle):
    pass


class ArticleCategoryPage(AbstractListingPage):
    def get_items_to_list(self, request=None):
        unpublished_pk = self.get_draft().pk
        return Article.objects.published().filter(parent_id=unpublished_pk)

    def get_items_to_mount(self, request):
        unpublished_pk = self.get_draft().pk
        return Article.objects.visible().filter(parent_id=unpublished_pk)

    class Meta:
        db_table = "icekit_articlecategorypage"
