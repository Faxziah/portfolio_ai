(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        var colorPicker = document.getElementById('id_theme_custom');
        var valueField = document.getElementById('id_value');

        if (colorPicker && valueField) {
            // Update value field when color picker changes
            colorPicker.addEventListener('input', function() {
                valueField.value = this.value;
            });

            // Also on change (for browsers that don't support input event well)
            colorPicker.addEventListener('change', function() {
                valueField.value = this.value;
            });
        }
    });
})();
