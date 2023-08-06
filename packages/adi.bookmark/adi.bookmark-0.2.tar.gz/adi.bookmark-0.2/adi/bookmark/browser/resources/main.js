// Bind dollar-sign to jQuery and wait until DOM loaded:
(function($) {$(document).ready(function() {
  // If we are in edit-mode and autosave was passed as URL-param:
  if( $('.template-atct_edit').length > 0 &&
    window.location.search.indexOf('autosave') > -1 ) {
    // Click the save-button:
    $('input.context').click()
  }
}); })(jQuery);
