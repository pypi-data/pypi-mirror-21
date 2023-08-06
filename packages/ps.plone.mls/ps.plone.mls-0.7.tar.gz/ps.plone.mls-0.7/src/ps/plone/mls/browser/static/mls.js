jQuery(function(jq) {

  if (jq('.mls .development__gallery .thumbnails').length > 0) {
    // Build JS Gallery for development detail view.

    // Load the theme ones more. This is necessary for mobile devices.
    Galleria.loadTheme('++resource++plone.mls.listing.javascript/classic/galleria.classic.min.js');
    jq('.mls .development__gallery .thumbnails').before('<div id="galleria" class="development__galleria"></div>');

    // Hide the thumbnails
    jq('.mls .development__gallery .thumbnails').hide();

    // Initialize Galleria.
    var galleria_obj = jq('#galleria').galleria({
      dataSource: '.thumbnails',
      width: 'auto',
      height: 400,
      preload: 3,
      transition: 'fade',
      transitionSpeed: 1000,
      autoplay: 5000
    });
  }

});
