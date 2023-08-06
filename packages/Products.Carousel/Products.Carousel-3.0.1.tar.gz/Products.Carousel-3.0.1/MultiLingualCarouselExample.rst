This is an example how to create a multilingual compatible Products.Carousel viewlet.


* Check if native language has a carousel

* If not fetch carousel from the canonical language

* LinguaPlone / Archetypes

viewlets.py::

    from Acquisition import aq_base
    from Products.Carousel.config import CAROUSEL_ID
    from Products.Carousel.interfaces import ICarousel
    from Products.LinguaPlone.interfaces import ITranslatable


    class MultiLingualCarousel(grok.Viewlet):
        """
        Make carousel to fetch images from the canonical language.
        """

        #grok.name("Products.Carousel.viewlet")
        grok.name("multilingualcarousel")
        grok.template("multilingualcarousel")
        grok.viewletmanager(IAboveContent)

        def _template_for_carousel(self, name, carousel):
            """
            Returns a template for rendering the banners or pager.
            """

            template = queryMultiAdapter(
                (carousel, self.request),
                Interface,
                default=None,
                name=name.replace('@@', '')
            )

            if template:
                return template.__of__(carousel)
            return None

        def getCarousel(self, folder):
            """
            """
            if hasattr(aq_base(folder), CAROUSEL_ID):
                carousel = ICarousel(folder[CAROUSEL_ID], None)
                if not carousel:
                    return None
            else:
                return None

            settings = carousel.getSettings()

            if not settings.enabled:
                return None

            return carousel

        def update(self):
            """
            Set the variables needed by the template.
            """

            self.available = False

            context_state = self.context.restrictedTraverse('@@plone_context_state')
            if context_state.is_structural_folder() and not context_state.is_default_page():
                folder = self.context
            else:
                folder = context_state.parent()

            # Try first carousel in the current language
            carousel = self.getCarousel(folder)

            # Then try the carousel in the parent language
            if not carousel:
                if ITranslatable.providedBy(folder):
                    translatable = ITranslatable(folder)
                    folder = translatable.getCanonical()
                    carousel = self.getCarousel(folder)

            if not carousel:
                # Could not find native or canonical language carousel
                return

            settings = carousel.getSettings()

            if settings.default_page_only and not context_state.is_default_page():
                return

            banners = carousel.getBanners()
            if not banners:
                return

            # Shuffle carousel images if needde
            if settings.random_order:
                shuffle(banners)

            self.banners = self._template_for_carousel(
                settings.banner_template or u'@@banner-default',
                carousel
            )

            self.pager = self._template_for_carousel(
                settings.pager_template or u'@@pager-numbers',
                carousel
            )

            width, height = banners[0].getSize()
            self.height = settings.height or height or 0
            self.width = settings.width or width or 0
            self.transition = settings.transition_type
            self.speed = int(settings.transition_speed * 1000)
            self.delay = int(settings.transition_delay * 1000)
            self.element_id = settings.element_id
            self.available = True


    # Monkey-patch carousel to handle multi-lingual banner look-up correctly
    from Products.CMFCore.interfaces import IFolderish
    from Products.ATContentTypes.interface.topic import IATTopic
    from Products.Carousel.interfaces import ICarousel, ICarouselSettings, \
        ICarouselFolder, ICarouselSettingsView, ICarouselBanner


    def getBanners(self):
        """
        Returns a list of objects that provide ICarouselBanner.
        """

        banner_brains = []
        if IFolderish.providedBy(self.context):
            catalog = getToolByName(self.context, 'portal_catalog')
            banner_brains = catalog.searchResults({
                'path': '/'.join(self.context.getPhysicalPath()),
                'object_provides': ICarouselBanner.__identifier__,
                'sort_on': 'getObjPositionInParent',
                'Language': 'all'
            })
        elif IATTopic.providedBy(self.context):
            banner_brains = self.context.queryCatalog()

        banner_objects = [b.getObject() for b in banner_brains]
        banner_objects = [b for b in banner_objects if ICarouselBanner.providedBy(b)]

        # Shuffle carousel images if needde
        if self.getSettings().random_order:
            shuffle(banner_objects)

        return banner_objects


    from Products.Carousel.browser import folder
    folder.Carousel.getBanners = getBanners
