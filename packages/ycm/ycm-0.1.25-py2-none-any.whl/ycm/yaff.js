/*
*
*  YAFF is Yet Another Front-end Framework
*
*  (C) Copyright Jack Cantrell-Warren 2016. All rights reserved.
*  This software may not be copied, altered, distributed, or otherwise used without the express written consent of
*  the copyright owner.
* */

// base model
var Yaff = function() {};

// the extend function, to propogate everywhere
Yaff.extend = function(extension) {

    var parent = this;
    var yaffobj;

    if(extension && (extension.hasOwnProperty('constructor')) && (typeof extension.constructor === 'function') ) {
        yaffobj = extension.constructor;
    } else {
        yaffobj = function(){ return parent.apply(this, arguments); };
    }

    yaffobj.prototype = Object.create(parent.prototype);
    yaffobj.prototype.constructor = yaffobj;

    for (var i in extension) {
        if (extension.hasOwnProperty(i) && (i != 'constructor')) {
            yaffobj.prototype[i] = extension[i];
        }
    }

    yaffobj.extend = Yaff.extend;
    yaffobj.mixin = Yaff.mixin;

    return yaffobj;
};

// the mixin function, to mix in an extension to a class definition
// usage: this.mixin(extension) - added at run time
Yaff.mixin = function(name) {

    var extension = Yaff.mixins[name];

    for (var k in extension) {
        if (extension.hasOwnProperty(k)) {
            this[k] = extension[k]
        }
    }

    // if there's an init function, run it
    var initfn = 'init_' + name;
    if (this.hasOwnProperty(initfn)) {
        this[initfn].apply(this);
    }

};

Yaff.List = Yaff.extend({

    /*  Basic list object for Yaff.

        Constructor accepts a list_obj dictionary of the following format:

        {
          list_id: the internal name of the list,
          list_data: a list of dictionaries representing the list data,
          primary_key: [list of key fields]
          action_parameters: {dictionary of actions}
          save_to_server: 0 | 1
          endpoint: <string> the endpoint to submit requests to
          is_form: boolean
          property_regex: { dictionary of regexes for each property }
        }

        action_parameters:
        {
            action: [list of parameters to be sent to the server]
        }

     */

    constructor: function(list_obj) {
        this.set_initial_values.apply(this, arguments);  // empty by default
        this.list_id = list_obj['list_id'];  // the name of the list
        this.list_data = list_obj['list_data']; // the list data
        this.action_parameters = list_obj['action_parameters']; // dictionary of actions, listing req'd params for each
        this.primary_key = list_obj['primary_key']; // list of primary key fields
        this.save_to_server = list_obj['save_to_server'];
        this.endpoint = list_obj['endpoint'];
        this.is_form = list_obj['is_form'];
        this.property_regex = list_obj['property_regex'];
        this._listeners = [];
        this.build_key_map.apply(this, arguments);
        this.initialize.apply(this, arguments);
    },

    set_initial_values: function() {},

    initialize: function() {},

    build_key_map: function() {
        // build a map of keys to indices
        this.key_map = {};
        var l = this.list_data.length;
        for (var i=0; i<l; i++) {
            var key = this.composite_key(i);
            this.key_map[key] = i;
        }
    },

    composite_key: function(index) {
        // return a composite of the primary key in the format 'field1~field2~field3...~fieldn'
        var l = this.primary_key.length;
        var key = this.list_data[index][this.primary_key[0]];
        for (var i=1; i<l; i++) {
            key[i] = key[i] + '~' + this.list_data[index][this.primary_key[i]];
        }
    },

    /*
        CRUD operations
     */

    update_item: function(data, source) {

        /*
            Update a row of the list

            Params:
                data: an object containing primary key and other fields to update
                source: 'user' | 'model' | 'app'

            data:
                { primary_key: composite (string) format}
         */

        var action = 'update_item';
        var index = this.key_map[data['primary_key']];

        // if the key doesn't exist: log to console and return
        if (typeof index === 'undefined') {
            console.log('Could not update item with key: ' + data['primary_key'] + ' - key not found');
            return
        }

        // update the internal representation of the list item
        for (var k in data) {
            if (data.hasOwnProperty(k)) {
                this.list_data[index][k] = data[k];
            }
        }

        // build a dictionary for submission to the server
        var cp = this.action_parameters[action];
        var l = cp.length;
        var item = {};
        for (var i=0; i<l; i++) {
            item[cp[i]] = this.list_data[index][cp[i]];
        }

        // see if needs to be updated to server
        if (this.save_to_server && (source in ['user', 'model'])) {
            // submit
            this.submit_to_server({
                action: action,
                data: item
            });
        } else {
            // if no requirement to submit, fake the callback so the item gets added
            var fake_response = {
                success: true,
                data: item
            };
            this.callbacks[action](fake_response);
        }

    },

    add_item: function(data, source) {
        /*
            Add an item to the list

            Params:
                data: an object containing any required fields
                source: 'user' | 'model' | 'app'

            data:
                { field: value }
         */
        var action = 'add_item';
        // create an object with the required parameters to add a new item
        var cp = this.action_parameters[action];
        var l = cp.length;
        var item = {};
        for (var i=0; i<l; i++) {
            item[cp[i]] = data[cp[i]];
        }

        // see if needs to be updated to server
        if (this.save_to_server && (source in ['user', 'model'])) {

            this.submit_to_server({
                action: action,
                data: item
            });

        } else {
            // if no requirement to submit, fake the callback so the item gets added
            var fake_response = {
                success: true,
                data: item
            };
            this.callbacks[action](fake_response);
        }
    },

    delete_item: function(data, source) {
        /*
            Removes an item from the list

            Params:
                data: an object containing primary key and other fields to update
                source: 'user' | 'model' | 'app'

            data:
                { primary_key: composite (string) format}
         */

        var action = 'delete_item';
        var index = this.key_map[data['primary_key']];

        // if the key doesn't exist: log to console and return
        if (typeof index === 'undefined') {
            console.log('Could not delete item with key: ' + data['primary_key'] + ' - key not found');
            return
        }

        // build a dictionary for submission to the server
        var cp = this.action_parameters[action];
        // create an object with the required parameters to add a new item
        var l = cp.length;
        var item = {};
        for (var i=0; i<l; i++) {
            item[cp[i]] = this.list_data[index][cp[i]];
        }

        // see if needs to be updated to server
        if (this.save_to_server && (source in ['user', 'model'])) {

            this.submit_to_server({
                action: action,
                data: item
            });

        } else {
            // if no requirement to submit, fake the callback so the item gets added
            var fake_response = {
                success: true,
                data: item
            };
            this.callbacks[action](fake_response);
        }

    },

    obtain_lock: function(data, source) {
        /*
            Obtains a lock on an item from the list

            Params:
                data: an object containing primary key
                source: 'user' | 'model' | 'app'

            data:
                { primary_key: composite (string) format}
        */
        var action = 'obtain_lock';
        var index = this.key_map[data['primary_key']];

        // if the key doesn't exist: log to console and return
        if (typeof index === 'undefined') {
            console.log('Could not obtain lock on item with key: ' + data['primary_key'] + ' - key not found');
            return
        }

        // build a dictionary for submission to the server
        var cp = this.action_parameters[action];
        // create an object with the required parameters to add a new item
        var l = cp.length;
        var item = {};
        for (var i=0; i<l; i++) {
            item[cp[i]] = this.list_data[index][cp[i]];
        }

        // see if needs to be updated to server
        if (this.save_to_server && (source in ['user', 'model'])) {

            this.submit_to_server({
                action: action,
                data: item
            });

        } else {
            // if no requirement to submit, fake the callback so the item gets updated
            var fake_response = {
                success: true,
                data: item
            };
            this.callbacks[action](fake_response);
        }
    },

    renumber_item: function(data, source) {
        /*
            Renumber an item (and the corresponding items in the list)

            Params:
                data: an object containing primary key and list_order
                source: 'user' | 'model' | 'app'

            data:
                { primary_key: composite (string) format}
         */

        var action = 'renumber_item';
        var index = this.key_map[data['primary_key']];

        // if the key doesn't exist: log to console and return
        if (typeof index === 'undefined') {
            console.log('Could not renumber item with key: ' + data['primary_key'] + ' - key not found');
            return
        }

        // build a dictionary for submission to the server
        var cp = this.action_parameters[action];
        // create an object with the required parameters to add a new item
        var l = cp.length;
        var item = {};
        for (var i=0; i<l; i++) {
            item[cp[i]] = data[cp[i]];
        }

        // see if needs to be updated to server
        if (this.save_to_server && (source in ['user', 'model'])) {

            // submit
            this.submit_to_server({
                action: action,
                data: item
            })
        } else {
            // if no requirement to submit, fake the callback so the item gets added
            var fake_response = {
                success: true,
                data: item
            };
            this.callbacks[action](fake_response);
        }
    },

    submit_to_server: function(request) {
        /*
          Submits a request to the server and directs the response to the appropriate callback.

          request: {
            action: the action to perform
            data: dictionary containing the required values. Must be the data itself, not a primary key ref (at this time).
        */

        // assemble required parameters
        var self = this;
        var action = request['action'];
        var data = JSON.stringify(request);
        // assemble the request parameters
        var request_parameters = { 'data': data, 'type': "POST", 'dataType': "json", 'contentType': "application/json" };

        $.ajax(this.endpoint, request_parameters)
            .done(function(response) {
                if (response.success) {
                    self.callbacks[action].apply(self, response);
                } else {
                    window.alert('Oops... something went wrong. The server sent the following error message: '
                        + response['error_message']);
                }
            })
            .fail(function () {
                window.alert('Could not reach the server. Please check your connection and try again.');
            });

    },

    submit_as_form: function() {
        /*
          Submits as a form. Requires is_form == true and property_regex;

          property_regex: {
            property: {
                regex: "regex",
                warning: "Warning if fails regex test"
            }
          }
           */

        // confirm all items match their regex
        var values = this.list_data[0];
        for (var p in this.property_regex) {
            if (this.property_regex.hasOwnProperty(p)) {
                var re = new RegExp(this.property_regex[p]['regex']);
                var valid = re.test(values[p]);
                if (!valid) {
                    window.alert('Submission failed for the following reason: \n\n' + this.property_regex[p]['warning']);
                }
            }
        }

        // submit to server
        var request = {
            action: 'submit_form',
            data: values
        };
        this.submit_to_server(request);

    },

    /*
        Callback functions
     */

    callbacks: {
        /*
            callbacks for server responses to the various actions

            response: {
                success: boolean
                html: html to add to the view
                data: dictionary representing the item affected
         */
        add_item: function(response) {
            // append to the list
            var l = this.list_data.length;
            this.list_data.append(response['data']);

            // add to key map
            var key = this.composite_key(l);
            this.key_map[key] = l;

            // check listeners
            var event = {
                primary_key: key,
                property: null,
                action: 'add_item'
            };
            this.check_listeners(event)
        },

        delete_item: function(response) {
            // remove item from the list
            var key = response['data']['primary_key'];
            var index = this.key_map[key];

            if (index !== null) {
                this.list_data.splice(index, 1);
            } else {
                console.log('Item submitted to server. Could not delete item with key: ' + key + ' - key not found');
            }

            // check listeners
            var event = {
                primary_key: key,
                property: null,
                action: 'delete_item'
            };
            this.check_listeners(event)
        },

        renumber_item: function(response) {
            // renumber the list using data from the response
            // in this instance, data is a list of dictionaries
            var data = response['data'];
            var l = data.length;

            for (var i=0; i<l; i++) {
                var index = this.key_map[data[i]['primary_key']];
                this.list_data[index]['list_order'] = data[i]['list_order'];
                if (typeof data[i]['section'] !== 'undefined') {
                    this.list_data[index]['section'] = data[i]['section'];
                }
            }

            // sort the list
            this.list_data.sort(function(a, b) { return a['list_order'] - b['list_order']});

            // check listeners
            var event = {
                primary_key: null,
                property: null,
                action: 'renumber_item'
            };
            this.check_listeners(event);

        },

        update_item: function(response) {
            var data = response['data'];

            // check listeners
            var event = {
                primary_key: data['primary_key'],
                property: null,
                action: 'delete_item'
            };
            this.check_listeners(event);

        },

        obtain_lock: function(response) {
            var data = response['data'];
            var index = this.key_map[data['primary_key']];

            // update item with lock info
            this.list_data[index]['locked_by'] = 'current_user';
            this.list_data[index]['lock_expires'] = data['lock_expires'];

            // check listeners
            var event = {
                primary_key: data['primary_key'],
                property: null,
                action: 'obtain_lock'
            };
            this.check_listeners(event);
        },

        submit_form: function(response) {
            // call listeners
            var event = {
                primary_key: null,
                property: null,
                action: 'submit_form'
            };
            this.check_listeners(event);
        }
    },

    /*
        Listener functions
     */

    add_listener: function(listener) {
        this._listeners.push(listener);
    },

    check_listeners: function(event) {

        /*
            Checks registered listeners to see if the event needs to be emitted

            event: {
                primary_key: string
                property: string
                action: string
            }
         */

        var l = this._listeners.length;
        var listeners_to_call = [];

        // get a list of listeners to call first, in case one of the earlier callbacks destroys the later ones
        for (var i=0; i<l; i++) {
            var ls = this._listeners[i];
            if (ls['action'] == event['action']
                && (ls['primary_key'] === null || event['primary_key'] === null || ls['primary_key'] === event['primary_key'])
                && (ls['property'] === null || event['property'] === null || ls['property'] === event['property'])) {

                listeners_to_call.push(ls);
            }
        }

        // call the listeners in turn
        var m = listeners_to_call.length;
        for (var j=0; j<m; j++) {

            var caller = listeners_to_call[i]['caller'];
            var callback = listeners_to_call[i]['callback'];
            caller[callback].call(caller, this.list_id, event);

        }

    },

    remove_listener: function(listener) {
        // find the listener
        var l = this._listeners.length;
        for (var i=0; i<l; i++) {
            if (this._listeners[i]==listener) {
                this._listeners.splice(i, 1);
                return;
            }
        }
    }

});

/*
*   View - represents an element or container of elements
*/

Yaff.View = Yaff.extend({
    /*  Basic view object for Yaff.

        Constructor accepts a the following parameters:
            element: the containing DOM element
            page: the page containing the view

     */

    constructor: function(element, page) {
        this.page = page;
        this.$el = element instanceof $ ? element : $(element);
        this.events = [];
        this.listeners = [];
        this.property_map = {};
        this.set_initial_values.apply(this, arguments);
        this.parse_bind_data();
        this.register_events();
        this.register_listeners();
        this.initialize.apply(this, arguments);
    },

    set_initial_values: function () {},

    initialize: function () {},

    register_events: function() {
        this._events = [];
        if (typeof this.events === 'undefined') return;
        var l = this.events.length;
        for (var i=0; i<l; i++) {
            this.register_event(this.events[i]);
        }
    },

    register_event: function(event) {
        /*
            Register an event object.

            event: {
                selector: the css selector (optional)
                event: the javascript event to bind to
                callback: the name of the function to run
            }
         */
        var self = this;

        // if the event specifies a selector, find element[s] with that selector
        var elements = event['selector'] ? this.$el.find(event['selector']) : this.$el;

        elements.each(function() {
            $(this).on(event['event'], function(e){
                self[event['callback']].apply(self, arguments);
            });
        });

        this._events.push(event);
    },

    parse_bind_data: function() {
        /*
            Parse data- attributes from the DOM element

            data-bind is strictly in JSON format
            all others can be either JSON or simple types
         */

        // get all data- variables from the element
        var data = this.$el.data();

        // parse the data-bind attribute
        if (data['bind']) {
            // parse bound data
            for (var k in data['bind']) {
                if (data['bind'].hasOwnProperty(k)) {
                    this[k] = data['bind'][k];
                }
            }
        }

        // go through the other data- attributes and parse
        for (var d in data) {
            if (data.hasOwnProperty(d) && d !== 'bind') {
                this[d] = data[d];
            }
        }

        // if there's a property map - use it to create listeners
        var p_map = this['property_map'] ? this['property_map'] : {};

        for (var p in p_map) {
            if (p_map.hasOwnProperty(p)) {
                // create a listener
                var ls = {
                    list_id: this.list_id,
                    primary_key: this.primary_key,
                    property: p_map[p],
                    action: 'update_item',
                    caller: this,
                    callback: this.mapped_property_change
                };
                this.register_listener(ls);
            }
        }
    },

    register_listeners: function() {
        this._listeners = [];
        var l = this.listeners.length;
        for (var i=0; i<l; i++) {
            this.register_listener(this.listeners[i]);
        }
    },

    register_listener: function(listener) {
        /*
            Register a listener with the relevant list and copy to the _listeners array

            listener: {
                list_id: name of list
                primary_key: string
                property: property
                action: action name
                caller: this
                callback: function name
         */

        this.page.lists[listener.list_id].add_listener(listener);
        this._listeners.push(listener);
    },

    remove: function() {

        // deregister listeners
        if (typeof this._listeners !== 'undefined' && this._listeners !== null) {
            var l = this._listeners ? this._listeners.length: -1;
            for (var i=0; i<l; i++) {
                this.page.lists[this._listeners['list_id']].remove_listener(this._listeners[i]);
            }
        }

        // delete events
        var m = this._events.length;
        for (var j=0; j<m; j++) {
            // if the event specifies a selector, find element[s] with that selector
            var event = this._events[j];
            var elements = event['selector'] ? this.$el.find(event['selector']) : this.$el;

            elements.each(function() {
                $(this).off();
            });
        }

        // remove DOM element
        if (typeof this.$el !== 'undefined' && this.$el !== null) {
            this.$el.remove();
            this.$el = null;
        }

    },

    mapped_property_change: function(list_id, event) {
        /*
            Handle the change in a list property mapped to a css-property of the view item
         */

        var list = this.page.lists[list_id];
        var index = list.key_map[event['primary_key']];
        var v = list['list_data'][index][event['property']];

        // get the property map details
        var p = this.property_map[event['property']];
        var css_value = p['map'][v];

        // update the css value of the element
        this.$el.css(p['css-property'], css_value);

    }

});

/*
*   Router - routes the browser
 */

Yaff.Router = Yaff.extend({
    constructor: function() {
        this.initialize.apply(this, arguments);
    },

    initialize: function() {
        this.base_url = window.location.origin;
        var self = this;
        window.onpopstate = function(event) {
            self.handle_pop.apply(self, event.state);
        }
    },

    replace_url: function(page, action) {
        var state = {'page': page};
        var url = this.base_url + '/' + page;
        if (action=='push') {
            window.history.pushState(state, "", url);
        } else if (action=='replace') {
            window.history.replaceState(state, "", url);
        }
    },

    handle_pop: function(state) {
        if (state) {
            var page = state['page'];
            if (page) {
                this.load_page(page, 'none');
            }
        }
    },

    // page loading function to be defined in implementation
    load_page: function(page) {}

});

/*
*   Page - holds list and view items together
 */

Yaff.Page = Yaff.extend({
    /*
        Basic Page object for Yaff - hold together views and lists

        Constructor takes the following arguments:
            element: the DOM element for the page container
            selector_class_map: a list of dicts of the form {selector: selector, class: class}
            endpoint: the endpoint for page requests
     */


    constructor: function(element, selector_class_map, endpoint) {

        this.$el = element instanceof $ ? element : $(element);
        this.selector_class_map = selector_class_map;
        this.endpoint = endpoint;
        this.views = [];
        this.lists = {};
        this.set_initial_values.apply(this, arguments);
        this.register_views();
        this.create_page_context();
        this.initialize.apply(this, arguments);

    },

    create_page_context: function() {
        /*
            Creates a page_context list.

            list_data: [ { list_id: list_id, selected: ['primary_key', 'primary_key'...] } ]
         */

        var list_obj = {
            list_id: 'page_context',
            list_data: [],
            primary_key: ['list_id'],
            action_parameters: {},
            save_to_server: 0,
            endpoint: ''
        };

        this.context = new Yaff.List(list_obj);
    },

    set_initial_values: function() {},

    initialize: function () {},

    register_views: function() {
        // register components within the page element and create views accordingly.
        var self = this;
        self.views = [];
        self.element_view_map = {};

        // go through the selector_class_map
        for (var k in self.selector_class_map) {
            if (self.selector_class_map.hasOwnProperty(k)) {
                self.$el.find(k).each(function(){
                    var cls = self.selector_class_map[k];
                    var view_obj = new Yaff[cls](this, self);
                    view_obj.view_type = cls;
                    self.views.push(view_obj);
                    self.element_view_map[this] = view_obj;
                });
            }
        }
    },

    drag_context: function() {},

    submit_to_server: function(request) {
        /*
            Submit a request to the server.

            request: {
                action: the action being performed
                endpoint: the endpoint to address
                data: the data to send
                router_action: for the router
            }
         */
        var self = this;
        var data = JSON.stringify(request['data']);
        var request_parameters = { 'data': data, 'type': "POST", 'dataType': "json", 'contentType': "application/json" };

        $.ajax(request['endpoint'], request_parameters)
            .done(function(response){
                if (response['success']) {
                    self.callbacks[request['action']].call(self, request, response);
                } else {
                    if (response['redirect']) {
                        window.location.assign(response['redirect']);
                    } else {
                        var default_err_msg = 'An error occurred. Please refresh the page and try again.';
                        var error_message = response['error_message'] ? response['error_message'] : default_err_msg;
                        window.alert(error_message);
                    }
                }
            })
            .fail(function() {
                window.alert('Error - could not connect to server. Failed to load page');
            });
    },

    callbacks: {

        load_page: function(request, response) {
            /*
                request: the request submitted to the 'submit_to_server' call
                response: {
                    success: boolean,
                    page: name of the page,
                    page_title: the title to display
                    html: html for the page
                    lists: { list_id: { list_obj } }
                }
             */


            var router_action = request['router_action'] ? request['router_action'] : "push";
            var lists = response['lists'] ? response['lists'] : {};

            // delete existing lists
            this.lists = {};

            // remove existing views
            var l = this.views.length;
            for (var i=0; i<l; i++) {
                this.views[0].remove();
                this.views.splice(0, 1);
            }

            // update html
            this.$el.html(response['html']);

            // update lists
            for (var k in lists) {
                if (lists.hasOwnProperty(k)) {
                    this.lists[k] = new Yaff.List(lists[k]);
                    // add a context list entry
                    this.context.add_item({
                        list_id: k,
                        selection: []
                    }, 'app');
                }
            }

            // update url and document/page titles
            Yaff.router.replace_url(page, router_action);
            document.title = "D5 Research - " + response['page_title'];
            $('#page_title').html(response['page_title']);

            // register views
            this.register_views();
            this.page = page;

            // upgrade the dom
            Yaff.utilities.upgrade_DOM(this.$el);

        },

        load_list: function(request, response) {
            /*
                Load a list, or group of lists, into the current page
             */

            var lists = response['lists'] ? response['lists'] : {};
            this._new_html = response['html'] ? response['html'] : '';

            // update lists
            for (var k in lists) {
                if (lists.hasOwnProperty(k)) {
                    this.lists[k] = new Yaff.List(lists[k]);
                }
            }
        }

    }

});

Yaff.Utilities = Yaff.extend({
    to_title_case: function(str) {
        return str.replace(/\b\w+/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    },

    restrict_tabbing: function(action, parent, nspace) {
        var $parent = parent instanceof $ ? parent : $(parent);
        var $elements = $parent.find('select, input, textarea, button, a').filter(':visible');
        var $first = $elements.first();
        var $last = $elements.last();
        var namespace = nspace ? nspace : 'restrict_tabbing';
        if (action=='on') {

            $first.on('keydown.restrict_tabbing', function(e) {
                if ((e.which === 9 && e.shiftKey)) {
                    e.preventDefault();
                    $last.focus();
                }
            });

            $last.on('keydown.restrict_tabbing', function(e) {
                if ((e.which === 9 && !e.shiftKey)) {
                    e.preventDefault();
                    $first.focus();
                }
            });

            var to = setTimeout(function(){$first.focus();}, 0);

            // find children and ensure first and last tab back to each other
        } else if (action=='off') {
            // remove the listeners that on created.
            $first.off('.restrict_tabbing');
            $last.off('.restrict_tabbing');
        }

    },

    compare_objects: function (obj1, obj2) {
        var key_count = [0, 0];
        var key_matches = [0, 0];
        for (var key in obj1) {
            if (obj1.hasOwnProperty(key)) {
                key_count[0] += 1;
                if (typeof obj2[key] !== 'undefined' && obj1[key]==obj2[key]) {
                    key_matches[0] += 1;
                }
            }

        }
        for (key in obj2) {
            if (obj2.hasOwnProperty(key)) {
                key_count[1] += 1;
                if (typeof obj1[key] !== 'undefined' && obj2[key] == obj1[key]) {
                    key_matches[1] += 1;
                }
            }
        }

        return (key_count[0]==key_count[1] && key_matches[0]==key_matches[1]);

    },

    upgrade_DOM: function($target) {
        // make a regular element array for the MDL component handler
        var target_array = $target.find('*').get();
        target_array.push($target.get());
        // MDL upgrade
        componentHandler.upgradeElements(target_array);
    },

    do_logout: function(redirect) {
        window.location.assign(redirect);
    },

    throttle: function(func, wait) {
        var context, args, result;
        var timeout = null;
        var previous = 0;

        var later = function() {
            previous = Date.now();
            timeout = null;
            result = func.apply(context, args);
            if (!timeout) context = args = null;
        };
        return function() {
            var now = Date.now();
            var remaining = wait - (now - previous);
            context = this;
            args = arguments;
            if (remaining <= 0 || remaining > wait) {
                if (timeout) {
                    clearTimeout(timeout);
                    timeout = null;
                }
                previous = now;
                result = func.apply(context, args);
                if (!timeout) context = args = null;
            } else if (!timeout) {
                timeout = setTimeout(later, remaining);
            }
            return result;
        };
    }

});

Yaff.mixins = {
    /*
        Sets of functions to add certain functionality

        Each mixin has an init function to set events, etc.

     */
    draggable: {
        init_draggable: function() {
            this.register_event({event: 'mousedown', callback: 'down_start'});
            this.register_event({event: 'touchstart', callback: 'down_start'});
            this.draggable_exc_selectors = 'textarea, button, input';
            this.reset_draggable.apply(this);
        },

        reset_draggable: function() {
            this.drag_context = {
                $clone: null,
                clone_details: {
                    view_item: null,
                    width: null,
                    height: null,
                    mouseX: null,
                    mouseY: null
                },
                origin: null,
                dragging: false
            }
        },

        down_start: function(e) {
            if ($(e.target).is(this['draggable_exc_selectors'])) return false;
            e.preventDefault();
            var self = this;
            self.reset_draggable();
            self.drag_context['origin'] = e.originalEvent.type === 'mousedown' ? 'mouse' : 'touch';

            var down_promise = setTimeout(function() {
                self.start_dragging.call(self, e);
            }, 300);

            var up_events = {'mouse': 'mouseup.draggable', 'touch': 'touchend.draggable touchcancel.draggable'};

            $(window).on(up_events[this.drag_context['origin']], function(ev) {
                ev.preventDefault();
                clearTimeout(down_promise);
                $(window).off('.draggable');
            });
        },

        start_dragging: function(e) {
            var self = this;

            // store details about the dragged item (this)
            var rect = this.$el[0].getBoundingClientRect();
            var clientX, clientY;
            if (this.drag_context['origin'] === 'mouse') {
                clientX = e.clientX;
                clientY = e.clientY;
            } else {
                clientX = parseInt(e.originalEvent.changedTouches[0].clientX);
                clientY = parseInt(e.originalEvent.changedTouches[0].clientY);
            }

            // create the clone
            // create clone element
            var $drag_clone = this.$el.clone();
            $('body').append($drag_clone);

            // save clone details
            this.drag_context['clone_details'] = {
                view_item: this,
                width: this.$el.innerWidth(),
                height: this.$el.innerHeight(),
                mouseX: clientX - rect.left,
                mouseY: clientY - rect.top,
                stored_contents: this.$el.children().detach(),   // store contents so we can make the dragged item a gray box
                background: this.$el.css('background-color')
            };

            // style the clone
            var clone_style = { 'border-style': 'dotted', 'border-color': '#9e9e9e', 'border-width': '2px',
                            'background-color': 'rgba(255,255,255,0.7)', 'position': 'absolute',
                           'width':  this.drag_context['clone_details'].width + 2 + 'px',  //-parseInt($element.css('padding-left'))-parseInt($element.css('padding-right'))
                           'height':  this.drag_context['clone_details'].height + 2 + 'px', //-parseInt($element.css('padding-top'))-parseInt($element.css('padding-bottom'))
                           'padding-top': this.$el.css('padding-top'), 'padding-left': this.$el.css('padding-left'),
                           'padding-bottom': this.$el.css('padding-bottom'), 'padding-right': this.$el.css('padding-right'),
                            'top': rect.top + 'px', 'left': rect.left + 'px', 'cursor': 'move', 'pointer-events' : 'none'};

            //var html = this.$el.html();
            //$drag_clone.html(html);
            //$drag_clone.attr('class', this.$el.attr('class'));
            $drag_clone.css(clone_style);
            this.drag_context['$clone'] = $drag_clone;
            this.drag_context['dragging'] = true;
            //Yaff.utilities.upgrade_DOM($drag_clone);

            // make the dragged item appear as a gray box
            var target_style = {'background-color': 'gray', 'height': this.drag_context['clone_details']['height'] + 2 + 'px'};
            this.$el.css(target_style);

            // trap move / end events
            if (this.drag_context['origin'] === 'mouse') {
                $(window).on('mousemove.draggable', Yaff.utilities.throttle(function(e) {
                    e.preventDefault();
                    self.drag_move.call(self, e);
                }, 50));

                $(window).on('mouseup.draggable', function(e){
                    e.preventDefault();
                    self.drag_up.call(self, e);
                });
            } else {
                $(e.target).on('touchmove.draggable', Yaff.utilities.throttle(function(e) {
                    e.preventDefault();
                    self.drag_move.call(self, e);
                }, 50));

                $(e.target).on('touchend.draggable touchcancel.draggable', function(e) {
                    e.preventDefault();
                    self.drag_up.call(self, e);
                });
            }
        },

        drag_move: function(e) {
            var origin = this.drag_context['origin'];
            var $drag_clone = this.drag_context['$clone'];

            if (!$drag_clone) return; // move event may be fired after drag up due to throttling

            // get co-ordinates
            var clientX, clientY;
            if (origin=='mouse') {
                clientX = e.clientX;
                clientY = e.clientY;
            } else if (origin=='touch') {
                clientX = e.originalEvent.changedTouches[0].clientX;
                clientY = e.originalEvent.changedTouches[0].clientY;
            }

            // set new co-ordinates
            var newX = clientX - this.drag_context['clone_details']['mouseX'];
            var newY = clientY - this.drag_context['clone_details']['mouseY'];
            //console.log(newX + ', ' + newY);
            $drag_clone.css('left', newX);
            $drag_clone.css('top', newY);
        },

        drag_up: function(e) {
            // destroy the clone
            this.drag_context['$clone'].remove();

            // stop trapping drag-related events
            $(window).off('.draggable');
            $(e.target).off('.draggable');

            // put the original html back
            this.drag_context['clone_details']['stored_contents'].appendTo(this.$el);
            this.$el.css('background-color', this.drag_context['clone_details']['background']);
            Yaff.utilities.upgrade_DOM(this.$el);

            // reset the drag context
            this.reset_draggable();
        }
    }

};

