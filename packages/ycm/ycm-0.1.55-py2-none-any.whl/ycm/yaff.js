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

    yaffobj.prototype.extend = Yaff.extend;
    yaffobj.extend = Yaff.extend;
    yaffobj.prototype.mixin = Yaff.mixin;
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
        var index = this.key_map[data['pk_value']];

        // if the key doesn't exist: log to console and return
        if (typeof index === 'undefined') {
            console.log('Could not update item with key: ' + data['pk_value'] + ' - key not found');
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
        var index = this.key_map[data['pk_value']];

        // if the key doesn't exist: log to console and return
        if (typeof index === 'undefined') {
            console.log('Could not delete item with key: ' + data['pk_value'] + ' - key not found');
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
                { pk_value: composite (string) format}
        */
        var action = 'obtain_lock';
        var index = this.key_map[data['pk_value']];

        // if the key doesn't exist: log to console and return
        if (typeof index === 'undefined') {
            console.log('Could not obtain lock on item with key: ' + data['pk_value'] + ' - key not found');
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
                { pk_value: composite (string) format}
         */

        var action = 'renumber_item';
        var index = this.key_map[data['pk_value']];

        // if the key doesn't exist: log to console and return
        if (typeof index === 'undefined') {
            console.log('Could not renumber item with key: ' + data['pk_value'] + ' - key not found');
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

        // make the request

        var rq = new XMLHttpRequest();
        rq.open('POST', this.endpoint, true);
        rq.setRequestHeader('Content-Type', 'application/json');

        rq.onload = function() {
            if (this.status >= 200 && this.status < 400 && this.response) {
                self.callbacks[action].apply(self, this.response);
            } else {
                window.alert('Oops... something went wrong. The server sent the following error message: '
                        + this.response['error_message']);
            }
        };

        rq.onerror = function() {
            window.alert('Could not reach the server. Please check your connection and try again.');
        };

        rq.send(data);

    },

    submit_as_form: function() {
        /*
          Submits as a form. Requires is_form === true and property_regex;

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
            this.list_data.push(response['data']);

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
            var key = response['data']['pk_value'];
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
                var index = this.key_map[data[i]['pk_value']];
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
                primary_key: data['pk_value'],
                property: null,
                action: 'delete_item'
            };
            this.check_listeners(event);

        },

        obtain_lock: function(response) {
            var data = response['data'];
            var index = this.key_map[data['pk_value']];

            // update item with lock info
            this.list_data[index]['locked_by'] = 'current_user';
            this.list_data[index]['lock_expires'] = data['lock_expires'];

            // check listeners
            var event = {
                primary_key: data['pk_value'],
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
            if (ls['action'] === event['action']
                && (ls['pk_value'] === null || event['pk_value'] === null || ls['pk_value'] === event['pk_value'])
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
            if (this._listeners[i] === listener) {
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
        this.el = element;
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
        this._event_handlers = {};
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
        var elements = event['selector'] ? this.el.querySelectorAll(event['selector']) : [this.el];

        for (var i = 0, l = elements.length; i < l; i++) {
            this._event_handlers[event['event']] = self[event['callback']].bind(self);
            elements[i].addEventListener(event['event'], this._event_handlers[event['event']]);
        }

        this._events.push(event);
    },

    parse_bind_data: function() {
        /*
            Parse data- attributes from the DOM element

            data-bind is strictly in JSON format
            all others can be either JSON or simple types
         */

        // get all data- variables from the element
        for (var i = 0, attrs = this.el.attributes, l = this.el.attributes.length, data = {}; i < l; i++) {
            if (attrs[i].nodeName.substr(0, 4) === 'data') {
                var key = attrs[i].nodeName.substr(5, attrs[i].nodeName.length - 5);
                data[key] = attrs[i].nodeValue;
            }
        }
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
        for (var j = 0; j < m; j++) {
            // if the event specifies a selector, find element[s] with that selector
            var event = this._events[j];
            var elements = event['selector'] ? this.el.querySelectorAll(event['selector']) : this.el;

            for (var x = 0, y = this.elements.length; x < y; x++) {
                elements[x].removeEventListener(event['event'], this._event_handlers[event['event']])
            }
        }

        // remove DOM element
        if (typeof this.el !== 'undefined' && this.el !== null) {
            this.el.remove();
            this.el = null;
        }

    },

    mapped_property_change: function(list_id, event) {
        /*
            Handle the change in a list property mapped to a css-property of the view item
         */

        var list = this.page.lists[list_id];
        var index = list.key_map[event['pk_value']];
        var v = list['list_data'][index][event['property']];

        // get the property map details
        var p = this.property_map[event['property']];

        // update the css value of the element
        this.el.style[p['css-property']] = p['map'][v];

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
            self.handle_pop.call(self, event.state);
        }
    },

    replace_url: function(page, action) {
        var state = {'page': page};
        var url = this.base_url + '/' + page;
        if (action === 'push') {
            window.history.pushState(state, "", url);
        } else if (action === 'replace') {
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

        this.el = element;
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

                var elements = self.el.querySelectorAll(k);

                Array.prototype.forEach.call(elements, function(el){
                    var cls = self.selector_class_map[k];
                    var view_obj = new Yaff[cls](el, self);
                    view_obj.view_type = cls;
                    self.views.push(view_obj);
                    self.element_view_map[el] = view_obj;
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

        // submit to server
        var rq = new XMLHttpRequest();
        rq.open('POST', request['endpoint'], true);
        rq.setRequestHeader('Content-Type', 'application/json');

        rq.onload = function() {
            if (this.status >= 200 && this.status < 400 && this.response) {
                self.callbacks[request['action']].call(self, request, this.response);
            } else {
                if (this.response['redirect']) {
                    window.location.assign(this.response['redirect']);
                } else {
                    var default_err_msg = 'An error occurred. Please refresh the page and try again.';
                        var error_message = this.response['error_message'] ? this.response['error_message'] : default_err_msg;
                        window.alert(error_message);
                }
            }
        };

        rq.onerror = function() {
            window.alert('Error - could not connect to server. Failed to load page');
        };

        rq.send(data);



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
            this.el.innerHTML = response['html'];

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
            document.getElementById('page_title').innerHTML = response['page_title'];

            // register views
            this.register_views();
            this.page = response['page'];

            // upgrade the dom
            Yaff.utilities.upgrade_DOM(this.el);

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

    restrict_tabbing: function(action, parent) {
        var elements = parent.querySelectorAll('select, input, textarea, button, a').filter(':visible');
        var first = elements[0];
        var last = elements[elements.length - 1];

        var first_keydown = function(e) {
            if ((e.which === 9 && e.shiftKey)) {
                e.preventDefault();
                last.focus();
            }
        };

        var last_keydown = function(e) {
            if ((e.which === 9 && !e.shiftKey)) {
                e.preventDefault();
                first.focus();
            }
        };

        if (action === 'on') {

            first.addEventListener('keydown', first_keydown.bind(this));
            last.addEventListener('keydown', last_keydown.bind(this));

            var to = setTimeout(function(){first.focus();}, 0);

            // find children and ensure first and last tab back to each other
        } else if (action === 'off') {
            // remove the listeners that on created.
            first.removeEventListener('keydown', first_keydown);
            last.removeEventListener('keydown', last_keydown);
        }

    },

    compare_objects: function (obj1, obj2) {
        var key_count = [0, 0];
        var key_matches = [0, 0];
        for (var key in obj1) {
            if (obj1.hasOwnProperty(key)) {
                key_count[0] += 1;
                if (typeof obj2[key] !== 'undefined' && obj1[key] === obj2[key]) {
                    key_matches[0] += 1;
                }
            }

        }
        for (key in obj2) {
            if (obj2.hasOwnProperty(key)) {
                key_count[1] += 1;
                if (typeof obj1[key] !== 'undefined' && obj2[key] === obj1[key]) {
                    key_matches[1] += 1;
                }
            }
        }

        return (key_count[0] === key_count[1] && key_matches[0] === key_matches[1]);

    },

    upgrade_DOM: function(target) {
        // make an element array for the MDL component handler
        // MDL upgrade
        componentHandler.upgradeElements(target);
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
    },

    matches: function(el, selector) {
        return (el.matches || el.matchesSelector || el.msMatchesSelector || el.mozMatchesSelector || el.webkitMatchesSelector || el.oMatchesSelector).call(el, selector);
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
            this.get_parent();
        },

        get_parent: function() {
            var current_node;
            var parent = null;
            current_node = this.el.parentElement;
            while (parent === null) {
                if (current_node.classList.contains(this.parent_class)) {
                    parent = current_node;
                }
                current_node = current_node.parentElement;
            }

            if (parent) {
                this.parent_element = parent;
            }

        },

        reset_draggable: function() {
            Yaff.drag_context = {
                clone: null,
                clone_details: {
                    view_item: null,
                    width: null,
                    height: null,
                    mouseX: null,
                    mouseY: null,
                    currentX: null,
                    currentY: null
                },
                origin: null,
                dragging: false,
                drag_name: null,
                drag_type: null,

                animate_move: function(timestamp) {
                    var drag_clone = Yaff.drag_context['clone'];

                    if (!drag_clone) return; // move event may be fired after drag up due to throttling
                    drag_clone.style.left = Yaff.drag_context['clone_details']['currentX'] + 'px';
                    drag_clone.style.top = Yaff.drag_context['clone_details']['currentY'] + 'px';

                    Yaff.drag_context['anim_frame_ref'] = requestAnimationFrame(Yaff.drag_context.animate_move);
                },

                mousemove: function(e) {
                    e.preventDefault();
                    this.drag_move.call(this, e);
                },

                mouseup: function(e) {
                    e.preventDefault();
                    this.drag_up.call(this, e);
                }
            }
        },

        down_start: function(e) {
            if (Yaff.utilities.matches(e.target, this['draggable_exc_selectors'])) return false;
            e.preventDefault();
            var self = this;
            self.reset_draggable();
            Yaff.drag_context['origin'] = e.type === 'mousedown' ? 'mouse' : 'touch';

            var mouseup_handler = function(ev) {
                ev.preventDefault();
                clearTimeout(down_promise);
                window.removeEventListener('mouseup', mouseup_handler);
                window.removeEventListener('touchend', mouseup_handler);
                window.removeEventListener('touchcancel', mouseup_handler);
            }.bind(this);

            window.addEventListener('mouseup', mouseup_handler);
            window.addEventListener('touchend', mouseup_handler);
            window.addEventListener('touchcancel', mouseup_handler);

            var down_promise = setTimeout(function() {
                window.removeEventListener('mouseup', mouseup_handler);
                window.removeEventListener('touchend', mouseup_handler);
                window.removeEventListener('touchcancel', mouseup_handler);
                self.start_dragging.call(self, e);
            }, 300);

        },

        start_dragging: function(e) {
            var self = this;
            var style = window.getComputedStyle(this.el);

            // store details about the dragged item (this)
            var rect = this.el.getBoundingClientRect();
            var clientX, clientY;
            if (Yaff.drag_context['origin'] === 'mouse') {
                clientX = e.clientX;
                clientY = e.clientY;
            } else {
                clientX = parseInt(e.changedTouches[0].clientX);
                clientY = parseInt(e.changedTouches[0].clientY);
            }

            // create the clone
            var drag_clone = this.el.cloneNode(true);
            document.body.appendChild(drag_clone);

            // save clone details
            Yaff.drag_context['clone_details'] = {
                view_item: this,
                width: rect.width,
                height: rect.height,
                mouseX: clientX - rect.left,
                mouseY: clientY - rect.top,
                background: style.backgroundColor
            };

            // hide the contents of the original element
            var content = this.el.querySelectorAll('*');
            for (var i = 0, l = content.length; i < l; i++) {
                content[i].style.visibility = 'hidden';
            }

            // get the container and see if it scrolls
            var container = this.el.parentElement;
            Yaff.drag_context['container'] = container;
            Yaff.drag_context['container_rect'] = container.getBoundingClientRect();
            Yaff.drag_context['container_scrolls'] = (container.scrollHeight - container.clientHeight > 0);

            // style the clone
            var clone_style = 'border-style: dotted; border-color: #9e9e9e; border-width: 2px; ' +
                'background-color: rgba(255,255,255,0.7); position: absolute; ' +
                'width: ' + rect.width + 'px; ' +
                'height: ' + rect.height + 'px; ' +
                'padding: ' + style.padding + '; ' +
                'top: ' + (rect.top - parseInt(style.marginTop)) + 'px; ' +
                'left: ' + (rect.left - parseInt(style.marginLeft)) + 'px; ' +
                'cursor: move;' +
                'pointer-events: none;';

            drag_clone.style.cssText = drag_clone.style.cssText ? drag_clone.style.cssText + ' ' + clone_style : clone_style;
            Yaff.drag_context['clone'] = drag_clone;
            Yaff.drag_context['dragging'] = true;
            Yaff.drag_context['drag_name'] = this.drag_name;
            Yaff.drag_context['drag_type'] = this.drag_type;

            // create the shadow list_order on the drop containers
            var drop_containers = Yaff.drop_containers[this.drag_name];
            for (i = 0, l = drop_containers.length; i < l; i++) {
                drop_containers[i]['shadow_order'] = parseInt(drop_containers[i]['view_item']['list_order']);
            }
            Yaff.drag_context['clone_details']['shadow_order'] = parseInt(this.list_order);

            // make the dragged item appear as a gray box
            this.el.style.backgroundColor = 'gray';

            // trap move / end events
            this.mousemove = Yaff.drag_context.mousemove.bind(this);
            this.mouseup = Yaff.drag_context.mouseup.bind(this);

            if (Yaff.drag_context['origin'] === 'mouse') {
                window.addEventListener('mousemove', this.mousemove);
                window.addEventListener('mouseup', this.mouseup);
            } else {
                window.addEventListener('touchmove', this.mousemove);
                window.addEventListener('touchend', this.mouseup);
                window.addEventListener('touchcancel', this.mouseup);
            }
            // redraw the clone at the browser's discretion
            Yaff.drag_context['anim_frame_ref'] = requestAnimationFrame(Yaff.drag_context.animate_move);
        },

        drag_move: function(e) {
            var origin = Yaff.drag_context['origin'];
            var cd = Yaff.drag_context['clone_details'];
            // get co-ordinates
            var clientX, clientY;
            if (origin === 'mouse') {
                clientX = e.clientX;
                clientY = e.clientY;
            } else if (origin === 'touch') {
                clientX = e.changedTouches[0].clientX;
                clientY = e.changedTouches[0].clientY;
            }

            var drag_type = Yaff.drag_context['drag_type'];
            var drag_name = Yaff.drag_context['drag_name'];

            // set new co-ordinates
            if (drag_type === 'vertical' || 'freeform') {
                cd['currentY'] = clientY - cd['mouseY'];
            } else if (drag_type === 'horizontal' || 'freeform') {
                cd['currentX'] = clientX - cd['mouseX'];
            }

            // see if we're over any drag containers
            var drop_containers = Yaff.drop_containers[drag_name];
            var clone_rect = {
                top: cd['currentY'],
                left: cd['currentX'],
                width: cd['width'],
                height: cd['height'],
                right: cd['currentX'] + cd['width'],
                bottom: cd['currentY'] + cd['height']
            };

            var orig_rect = cd['view_item']['el'].getBoundingClientRect();

            var over = false, l = drop_containers.length, diff, target_rect, direction, intersection;

            while (!over && l--) {
                // get drop container co-ordinates
                target_rect = drop_containers[l]['element'].getBoundingClientRect();
                if (drag_type === 'vertical') {
                    direction = clone_rect.top < orig_rect.top ? 'up' : 'down';

                    if (direction === 'up') {
                        diff = clone_rect.bottom - target_rect.top;
                    } else {
                        diff = target_rect.bottom - clone_rect.top;
                    }

                    over = diff > 0 && clone_rect.height > diff;

                } else if (drag_type === 'horizontal') {
                    direction = clone_rect.left < orig_rect.left ? 'left' : 'right';

                    if (direction === 'left') {
                        diff = clone_rect.right - target_rect.left;
                    } else {
                        diff = target_rect.right - clone_rect.left;
                    }

                    over = clone_rect.width > diff && diff > 0;
                } else if (drag_type === 'freeform') {
                    // if the coinciding area is >50% of target or clone, then we're over
                    intersection = {
                        left: Math.max(clone_rect.left, target_rect.left),
                        right: Math.max(clone_rect.right, target_rect.right),
                        bottom: Math.max(clone_rect.bottom, target_rect.bottom),
                        top: Math.max(clone_rect.top, target_rect.top)
                    };
                    intersection.area = (intersection.right - intersection.left) * (intersection.bottom - intersection.top);

                    var clone_area = clone_rect.width * clone_rect.height;
                    var target_area = target_rect.width * target_rect.height;

                    over = (intersection.area >= (clone_area * .5) || intersection.area >= (target_area * .5));

                }
            }

            if (over) {
                var elements = [];
                var old_order = Yaff.drag_context['clone_details']['shadow_order'];
                var new_order = drop_containers[l]['shadow_order'];
                var increase = new_order > old_order;

                for (var j = 0, k = drop_containers.length, ord; j < k; j++) {
                    ord = drop_containers[j]['shadow_order'];
                    if (increase && ord > old_order && ord <= new_order) {
                        drop_containers[j]['shadow_order'] -= 1;
                    } else if (!increase && ord < old_order && ord >= new_order) {
                        drop_containers[j]['shadow_order'] += 1;
                    } else if (ord == old_order) {
                        drop_containers[j]['shadow_order'] = new_order;
                        Yaff.drag_context['clone_details']['shadow_order'] = new_order;
                    }
                }

                drop_containers.sort(function(a, b) {
                    if (a.shadow_order < b.shadow_order) return -1;
                    if (a.shadow_order > b.shadow_order) return 1;
                    return 0;
                });

                for (j = 0; j < k; j++) {
                    Yaff.drag_context.container.appendChild(drop_containers[j]['element']);
                }

            }

            // if the container scrolls and we're near the bottom, scroll down
            if (Yaff.drag_context['container_scrolls']) {
                if (clone_rect.bottom >= Yaff.drag_context['container_rect'].bottom) {
                    Yaff.drag_context['container'].scrollTop += 5;
                } else if (clone_rect.top <= Yaff.drag_context['container_rect'].top) {
                    Yaff.drag_context['container'].scrollTop -= 5;
                }
            }

        },

        drag_up: function(e) {
            // destroy the clone
            cancelAnimationFrame(Yaff.drag_context['anim_frame_ref']);

            // stop trapping drag-related events
            window.removeEventListener('touchmove', this.mousemove);
            window.removeEventListener('touchend', this.mouseup);
            window.removeEventListener('touchcancel', this.mouseup);
            window.removeEventListener('mousemove', this.mousemove);
            window.removeEventListener('mouseup', this.mouseup);

            Yaff.drag_context['clone'].parentNode.removeChild(Yaff.drag_context['clone']);

            var content = this.el.querySelectorAll('*');

            for (var i = 0, l = content.length; i < l; i++) {
                content[i].style.visibility = 'visible';
            }

            this.el.style.backgroundColor = Yaff.drag_context['clone_details']['background'];
            Yaff.utilities.upgrade_DOM(this.el);

            // check if we have renumbered, and if so call the relevant action on the list
            var old_order = Yaff.drag_context['clone_details']['view_item']['list_order'];
            var new_order = Yaff.drag_context['clone_details']['shadow_order'];
            var list_id = Yaff.drag_context['clone_details']['view_item']['list_id'];
            if (old_order != new_order) {
                Yaff.lists[list_id].renumber_item({
                    pk_value: Yaff.drag_context['clone_details']['view_item']['pk_value'],
                    list_order: new_order
                }, 'user');
            }

            // reset the drag context
            this.reset_draggable();
        }


    },

    droppable: {
        init_droppable: function() {

            Yaff.drop_containers = Yaff.drop_containers || {};
            Yaff.drop_containers[this.drag_name] = Yaff.drop_containers[this.drag_name] || [];
            Yaff.drop_containers[this.drag_name].push({
                view_item: this,
                element: this.el
            })

        }
    }

};


