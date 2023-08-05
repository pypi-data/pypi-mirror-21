$(window).on('pytsite.widget.init:pytsite.odm_ui._browser.Browser', function (e, widget) {
    $(window).trigger('pytsite.widget.init:pytsite.widget._misc.BootstrapTable', [widget])
});
