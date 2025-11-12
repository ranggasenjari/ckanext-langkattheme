ckan.module("langkattheme-check-dataset-rule", function ($, _) {
  "use strict";
  return {
    options: {
      debug: false,
    },

    initialize: function () {
      // console.log('langkattheme-check-dataset-rule js initialization');
      // console.log(this.options);

      $(function () {
        $("#check_dataset_rule").on("change", function () {
          toggleButtonSubmit(this.checked);
        });

        toggleButtonSubmit(false);
      });

      function toggleButtonSubmit(isActive) {
        var btn = $('.form-actions button[type="submit"]');
        btn.prop("disabled", !isActive);
      }
    },
  };
});
