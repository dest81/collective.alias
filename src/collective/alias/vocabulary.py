from five import grok
from plone import api
from zope.component.hooks import getSite


from zope.schema.interfaces import IVocabularyFactory, IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.app.vocabularies.catalog import  CatalogSource

from Products.CMFCore.utils import getToolByName


class PortalTypesVocabulary(object):
    """Portal types vocabulary that doesn't require the 'context' object to
    be acquisition wrapped.
    """

    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        if site is None:
            return SimpleVocabulary.fromValues([])

        ttool = getToolByName(site, 'portal_types', None)
        if ttool is None:
            return SimpleVocabulary.fromValues([])

        items = [(ttool[t].Title(), t) for t in ttool.listContentTypes()]
        items.sort()
        return SimpleVocabulary([SimpleTerm(i[1], i[1], i[0]) for i in items])

grok.global_utility(PortalTypesVocabulary,
                    name=u"collective.alias.PortalTypes")


@grok.provider(IContextSourceBinder)
def languageRootActivity(context):
    lg_root = api.portal.get_navigation_root(context)
    path = '/'.join(lg_root.getPhysicalPath())
    return CatalogSource(portal_type=['Activity'], path=path)