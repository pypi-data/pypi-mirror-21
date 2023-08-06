jQuery(function($) {


  if ($('#listing-search').length > 0) {
    // Listing search viewlet.

    if ($('#listing-search div.results').length > 0) {
      // Hide the form when search was performed and show the edit form options link.
      $('div.results > form').hide();
      $('div.results #show-form').show().click(function(event) {
        event.preventDefault();
        $('div.results > form').slideToggle();
      });
    }
  }

  if($('.listing-map').length > 0) {
    $('.listing-map > div').addClass('map__canvas');
    loadGoogleMaps(initializeMap);
  }

  if ($('#listing-images .thumbnails').length > 0) {
    // Build JS Gallery for listing detail view.

    // Load the theme ones more. This is necessary for mobile devices.
    Galleria.loadTheme('++resource++plone.mls.listing.javascript/classic/galleria.classic.min.js');
    $('#listing-images a.preview').replaceWith('<div id="galleria"></div>');

    // Hide the thumbnails
    $('#listing-images .thumbnails').hide();

    // Initialize Galleria.
    var galleria_obj = $('#galleria').galleria({
      dataSource: '.thumbnails',
      width: 410,
      height: 400,
      preload: 3,
      transition: 'fade',
      transitionSpeed: 1000,
      autoplay: 5000
    });
  }


  if ($('.portletQuickSearch').length > 0) {

    if ($('.portletQuickSearch #formfield-form-widgets-object_type input:checked').length > 0) {
      $('.portletQuickSearch #formfield-form-widgets-object_type > .collapser').click();
    }

    if ($('.portletQuickSearch #formfield-form-widgets-location_type input:checked').length > 0) {
      $('.portletQuickSearch #formfield-form-widgets-location_type > .collapser').click();
    }

    if ($('.portletQuickSearch #formfield-form-widgets-geographic_type input:checked').length > 0) {
      $('.portletQuickSearch #formfield-form-widgets-geographic_type > .collapser').click();
    }

    if ($('.portletQuickSearch #formfield-form-widgets-view_type input:checked').length > 0) {
      $('.portletQuickSearch #formfield-form-widgets-view_type > .collapser').click();
    }

    if ($('.portletQuickSearch #formfield-form-widgets-ownership_type input:checked').length > 0) {
      $('.portletQuickSearch #formfield-form-widgets-ownership_type > .collapser').click();
    }

    if ($('.portletQuickSearch #formfield-form-widgets-air_condition input:checked').val() != '--NOVALUE--') {
      $('.portletQuickSearch #formfield-form-widgets-air_condition > .collapser').click();
    }

    if ($('.portletQuickSearch #formfield-form-widgets-pool input:checked').val() != '--NOVALUE--') {
      $('.portletQuickSearch #formfield-form-widgets-pool > .collapser').click();
    }

    if ($('.portletQuickSearch #formfield-form-widgets-jacuzzi input:checked').val() != '--NOVALUE--') {
      $('.portletQuickSearch #formfield-form-widgets-jacuzzi > .collapser').click();
    }

  }

});
