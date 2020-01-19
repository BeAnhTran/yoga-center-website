$('select#language').change(function () {
    $(this).parent('form#form-translations').submit();
});