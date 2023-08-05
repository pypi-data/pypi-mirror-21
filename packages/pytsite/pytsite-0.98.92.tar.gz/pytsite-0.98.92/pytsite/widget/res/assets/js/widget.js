pytsite.widget = {
    init: function () {
        // Initialize all widgets found on a page
        $('.pytsite-widget').not('.initialized').each(function () {
            new pytsite.widget.Widget(this);
        });
    },

    Widget: function (em) {
        var self = this;
        self.em = em = $(em);
        self.cid = em.data('cid');
        self.uid = em.data('uid');
        self.replaces = em.data('replaces');
        self.formArea = em.data('formArea');
        self.parentUid = em.data('parentUid');
        self.alwaysHidden = em.data('hidden') == 'True';
        self.weight = em.data('weight');
        self.assets = em.data('assets') ? self.em.data('assets') : [];
        self.messagesEm = em.find('.widget-messages').first();
        self.children = {};

        // Clear state fo the widget
        self.clearState = function () {
            self.em.removeClass('has-success');
            self.em.removeClass('has-warning');
            self.em.removeClass('has-error');

            return self;
        };

        // Set state of the widget
        self.setState = function (type) {
            self.clearState();
            self.em.addClass('has-' + type);

            return self;
        };

        // Clear messages of the widget
        self.clearMessages = function () {
            if (self.messagesEm.length)
                self.messagesEm.html('');

            return self;
        };

        // Add message to the widget
        self.addMessage = function (msg) {
            if (self.messagesEm.length)
                self.messagesEm.append('<span class="help-block">{0}</span>'.format(msg));

            return self;
        };

        // Hide the widget
        self.hide = function () {
            self.em.addClass('hidden');

            return self;
        };

        // Show the widget
        self.show = function () {
            if (!self.alwaysHidden)
                self.em.removeClass('hidden');

            return self;
        };

        /*
         * Add a child widget
         */
        self.addChild = function (child) {
            if (self.children.hasOwnProperty(child.uid))
                throw 'Widget ' + self.uid + ' already has child widget ' + child.uid;

            self.children[child.uid] = child;
        };

        // Load widget's assets
        pytsite.browser.loadAssets(self.assets).done(function () {
            // Initialize the widget
            $(window).trigger('pytsite.widget.init:' + self.cid, [self]);
            $(self).trigger('ready', [self]);
            self.em.addClass('initialized');

            // Initialize children widgets
            self.em.find(".pytsite-widget[data-parent-uid='" + self.uid + "']:not(.initialized)").each(function () {
                self.addChild(new pytsite.widget.Widget(this));
            });
        }).fail(function () {
            $(self).trigger('initError', [self]);
        });
    }
};

$(function () {
    pytsite.widget.init();
});
