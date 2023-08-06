/*
 * MyAMS
 * « My Application Management Skin »
 *
 * $Tag: 0.1.26 $
 * A bootstrap based application/administration skin
 *
 * Custom administration and application skin tools
 * Released under Zope Public License ZPL 1.1
 * ©2014-2016 Thierry Florac <tflorac@ulthar.net>
 */

(function($, globals) {

	"use strict";

	/**
	 * String prototype extensions
	 */
	String.prototype.startsWith = function(str) {
		var slen = this.length,
			dlen = str.length;
		if (slen < dlen) {
			return false;
		}
		return (this.substr(0,dlen) === str);
	};

	String.prototype.endsWith = function(str) {
		var slen = this.length,
			dlen = str.length;
		if (slen < dlen) {
			return false;
		}
		return (this.substr(slen-dlen) === str);
	};


	/**
	 * Array prototype extensions
	 */
	if (!Array.prototype.indexOf) {
		Array.prototype.indexOf = function(elt, from) {
			var len = this.length;

			from = Number(from) || 0;
			from = (from < 0) ? Math.ceil(from) : Math.floor(from);
			if (from < 0) {
				from += len;
			}

			for (; from < len; from++) {
				if (from in this && this[from] === elt) {
					return from;
				}
			}
			return -1;
		};
	}


	/**
	 * JQuery 'hasvalue' expression
	 * Filter inputs containing value
	 */
	$.expr[":"].hasvalue =  function(obj, index, meta /*, stack*/) {
		return $(obj).val() !== "";
	};


	/**
	 * JQuery 'econtains' expression
	 * Case insensitive contains expression
	 */
	$.expr[":"].econtains = function(obj, index, meta /*, stack*/) {
		return (obj.textContent || obj.innerText || $(obj).text() || "").toLowerCase() === meta[3].toLowerCase();
	};


	/**
	 * JQuery 'withtext' expression
	 * Case sensitive exact search expression
	 */
	$.expr[":"].withtext = function(obj, index, meta /*, stack*/) {
		return (obj.textContent || obj.innerText || $(obj).text() || "") === meta[3];
	};


	/**
	 * JQuery filter on parents class
	 */
	$.expr[':'].parents = function(obj, index, meta /*, stack*/) {
		return $(obj).parents(meta[3]).length > 0;
	};


	/**
	 * JQuery 'scrollbarWidth' function
	 * Get width of vertical scrollbar
	 */
	if ($.scrollbarWidth === undefined) {
		$.scrollbarWidth = function() {
			var parent = $('<div style="width:50px; height:50px; overflow:auto"><div/></div>').appendTo('body');
			var child = parent.children();
			var width = child.innerWidth() - child.height(99).innerWidth();
			parent.remove();
			return width;
		};
	}


	/**
	 * MyAMS JQuery extensions
	 */
	$.fn.extend({

		/*
		 * Check if current object is empty or not
		 */
		exists: function() {
			return $(this).length > 0;
		},

		/*
		 * Get object if it supports given CSS class,
		 * otherwise looks for parents
		 */
		objectOrParentWithClass: function(klass) {
			if (this.hasClass(klass)) {
				return this;
			} else {
				return this.parents('.' + klass);
			}
		},

		/*
		 * Build an array of attributes of the given selection
		 */
		listattr: function(attr) {
			var result = [];
			this.each(function() {
				result.push($(this).attr(attr));
			});
			return result;
		},

		/*
		 * CSS style function
		 * Code from Aram Kocharyan on stackoverflow.com
		 */
		style: function(styleName, value, priority) {
			// DOM node
			var node = this.get(0);
			// Ensure we have a DOM node
			if (typeof(node) === 'undefined') {
				return;
			}
			// CSSStyleDeclaration
			var style = this.get(0).style;
			// Getter/Setter
			if (typeof(styleName) !== 'undefined') {
				if (typeof(value) !== 'undefined') {
					// Set style property
					priority = typeof(priority) !== 'undefined' ? priority : '';
					style.setProperty(styleName, value, priority);
					return this;
				} else {
					// Get style property
					return style.getPropertyValue(styleName);
				}
			} else {
				// Get CSSStyleDeclaration
				return style;
			}
		},

		/*
		 * Remove CSS classes starting with a given prefix
		 */
		removeClassPrefix: function (prefix) {
			this.each(function (i, it) {
				var classes = it.className.split(" ").map(function(item) {
					return item.startsWith(prefix) ? "" : item;
				});
				it.className = $.trim(classes.join(" "));
			});
			return this;
		},

		/*
		 * Context menu handler
		 */
		contextMenu: function(settings) {

			function getMenuPosition(mouse, direction, scrollDir) {
				var win = $(window)[direction](),
					menu = $(settings.menuSelector)[direction](),
					position = mouse;
				// opening menu would pass the side of the page
				if (mouse + menu > win && menu < mouse) {
					position -= menu;
				}
				return position;
			}

			return this.each(function () {

				// Open context menu
				$('a', $(settings.menuSelector)).each(function() {
					$(this).data('ams-context-menu', true);
				});
				$(this).on("contextmenu", function (e) {
					// return native menu if pressing control
					if (e.ctrlKey) {
						return;
					}
					//open menu
					$(settings.menuSelector).data("invokedOn", $(e.target))
											.show()
											.css({
												position: 'fixed',
												left: getMenuPosition(e.clientX, 'width', 'scrollLeft') - 10,
												top: getMenuPosition(e.clientY, 'height', 'scrollTop') - 10
											})
											.off('click')
											.on('click', function (e) {
												$(this).hide();
												var invokedOn = $(this).data("invokedOn");
												var selectedMenu = $(e.target);
												settings.menuSelected.call(this, invokedOn, selectedMenu);
												ams.event.stop(e);
											});
					return false;
				});

				//make sure menu closes on any click
				$(document).click(function () {
					$(settings.menuSelector).hide();
				});
			});
		},

		/*
		 * Main menus manager
		 */
		myams_menu: function(options) {
			// Extend our default options with those provided
			var defaults = {
				accordion : true,
				speed : 200,
				closedSign : '<em class="fa fa-angle-down"></em>',
				openedSign : '<em class="fa fa-angle-up"></em>'
			};
			var settings = $.extend({}, defaults, options);

			// Assign current element to variable, in this case is UL element
			var menu = $(this);

			// Add a mark [+] to a multilevel menu
			menu.find("LI").each(function() {
				var menuItem = $(this);
				if (menuItem.find("UL").size() > 0) {

					// add the multilevel sign next to the link
					menuItem.find("A:first")
							 .append("<b class='collapse-sign'>" + settings.closedSign + "</b>");

					// avoid jumping to the top of the page when the href is an #
					var firstLink = menuItem.find("A:first");
					if (firstLink.attr('href') === "#") {
						firstLink.click(function() {
							return false;
						});
					}
				}
			});

			// Open active level
			menu.find("LI.active").each(function() {
				var activeParent = $(this).parents('UL');
				var activeItem = activeParent.parent('LI');
				activeParent.slideDown(settings.speed);
				activeItem.find("b:first").html(settings.openedSign);
				activeItem.addClass("open");
			});

			menu.find("LI A").on('click', function() {
				var link = $(this);
				if (link.hasClass('active')) {
					return;
				}
				var href = link.attr('href').replace(/^#/,'');
				var parentUL = link.parent().find("UL");
				if (settings.accordion) {
					var parents = link.parent().parents("UL");
					var visible = menu.find("UL:visible");
					visible.each(function(visibleIndex) {
						var close = true;
						parents.each(function(parentIndex) {
							if (parents[parentIndex] === visible[visibleIndex]) {
								close = false;
								return false;
							}
						});
						if (close) {
							if (parentUL !== visible[visibleIndex]) {
								var visibleItem = $(visible[visibleIndex]);
								if (href || !visibleItem.hasClass('active')) {
									visibleItem.slideUp(settings.speed, function () {
										$(this).parent("LI")
											   .removeClass('open')
											   .find("B:first")
											   .delay(settings.speed)
											   .html(settings.closedSign);
									});
								}
							}
						}
					});
				}
				var firstUL = link.parent().find("UL:first");
				if (!href && firstUL.is(":visible") && !firstUL.hasClass("active")) {
					firstUL.slideUp(settings.speed, function() {
						link.parent("LI")
							.removeClass("open")
							.find("B:first")
							.delay(settings.speed)
							.html(settings.closedSign);
					});
				} else /*if (link.attr('href') !== location.hash)*/ {
					firstUL.slideDown(settings.speed, function() {
						link.parent("LI")
							.addClass("open")
							.find("B:first")
							.delay(settings.speed)
							.html(settings.openedSign);
					});
				}
			});
		}
	});


	/**
	 * UTF-8 encoding class
	 * Mainly used by IE...
	 */
	$.UTF8 = {

		// public method for url encoding
		encode : function (string) {
			string = string.replace(/\r\n/g,"\n");
			var utftext = "";

			for (var n = 0; n < string.length; n++) {

				var c = string.charCodeAt(n);

				if (c < 128) {
					utftext += String.fromCharCode(c);
				}
				else if((c > 127) && (c < 2048)) {
					utftext += String.fromCharCode((c >> 6) | 192);
					utftext += String.fromCharCode((c & 63) | 128);
				}
				else {
					utftext += String.fromCharCode((c >> 12) | 224);
					utftext += String.fromCharCode(((c >> 6) & 63) | 128);
					utftext += String.fromCharCode((c & 63) | 128);
				}
			}
			return utftext;
		},

		// public method for url decoding
		decode : function (utftext) {
			var string = "";
			var i = 0,
				c = 0,
				c2 = 0,
				c3 = 0;

			while ( i < utftext.length ) {

				c = utftext.charCodeAt(i);

				if (c < 128) {
					string += String.fromCharCode(c);
					i++;
				}
				else if((c > 191) && (c < 224)) {
					c2 = utftext.charCodeAt(i+1);
					string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
					i += 2;
				}
				else {
					c2 = utftext.charCodeAt(i+1);
					c3 = utftext.charCodeAt(i+2);
					string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
					i += 3;
				}
			}
			return string;
		}
	}; /** $.UTF8 */


	/**
	 * MyAMS extensions to JQuery
	 */
	if (globals.MyAMS === undefined) {
		globals.MyAMS = {
			devmode: true,
			devext: '',
			lang: 'en',
			throttleDelay: 350,
			menuSpeed: 235,
			navbarHeight: 49,
			ajaxNav: true,
			enableWidgets: true,
			enableMobile: false,
			enableFastclick: false,
			warnOnFormChange: false,
			ismobile: (/iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()))
		};
	}
	var MyAMS = globals.MyAMS;
	var ams = MyAMS;

	/**
	 * Get MyAMS base URL
	 * Copyright Andrew Davy: https://forrst.com/posts/Get_the_URL_of_the_current_javascript_file-Dst
	 */
	MyAMS.baseURL = (function () {
		var script = $('script[src*="/myams.js"], script[src*="/myams.min.js"]');
		var src = script.attr("src");
		ams.devmode = src.indexOf('.min.js') < 0;
		ams.devext = ams.devmode ? '' : '.min';
		return src.substring(0, src.lastIndexOf('/') + 1);
	})();


	/**
	 * Basic logging function which log all arguments to console
	 */
	MyAMS.log = function() {
		if (globals.console) {
			globals.console.log(this, arguments);
		}
	};


	/**
	 * Extract parameter value from given query string
	 */
	MyAMS.getQueryVar = function(src, varName) {
		// Check src
		if (src.indexOf('?') < 0) {
			return false;
		}
		if (!src.endsWith('&')) {
			src += '&';
		}
		// Dynamic replacement RegExp
		var regex = new RegExp('.*?[&\\?]' + varName + '=(.*?)&.*');
		// Apply RegExp to the query string
		var val = src.replace(regex, "$1");
		// If the string is the same, we didn't find a match - return false
		return val === src ? false : val;
	};


	/**
	 * Color conversion function
	 */
	MyAMS.rgb2hex = function(color) {
		return "#" + $.map(color.match(/\b(\d+)\b/g), function(digit) {
			return ('0' + parseInt(digit).toString(16)).slice(-2);
		}).join('');
	};


	/**
	 * Generate a random ID
	 */
	MyAMS.generateId = function() {
		function s4() {
			return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
		}
		return s4() + s4() + s4() + s4();
	};


	/**
	 * Generate a random UUID
	 */
	MyAMS.generateUUID = function () {
		var d = new Date().getTime();
		var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
			var r = (d + Math.random() * 16) % 16 | 0;
			d = Math.floor(d / 16);
			return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
		});
		return uuid;
	};


	/**
	 * Get and execute a function given by name
	 * Small piece of code by Jason Bunting
	 */
	MyAMS.getFunctionByName = function(functionName, context) {
		if (functionName === undefined) {
			return undefined;
		} else if (typeof(functionName) === 'function') {
			return functionName;
		}
		var namespaces = functionName.split(".");
		var func = namespaces.pop();
		context = (context === undefined || context === null) ? window : context;
		for (var i=0; i < namespaces.length; i++) {
			try {
				context = context[namespaces[i]];
			} catch (e) {
				return undefined;
			}
		}
		try {
			return context[func];
		} catch (e) {
			return undefined;
		}
	};

	MyAMS.executeFunctionByName = function(functionName, context /*, args */) {
		var func = ams.getFunctionByName(functionName, window);
		if (typeof(func) === 'function') {
			var args = Array.prototype.slice.call(arguments, 2);
			return func.apply(context, args);
		}
	};

	/**
	 * Check to know if given element is still present in DOM
	 */
	MyAMS.isInDOM = function(element) {
		element = $(element);
		if (!element.exists()) {
			return false;
		}
		return globals.document.body.contains(element[0]);
	};

	/**
	 * Get script or CSS file using browser cache
	 * Script or CSS URLs can include variable names, given between braces, as in
	 * {MyAMS.baseURL}
	 */
	MyAMS.getSource = function(url) {
		return url.replace(/{[^{}]*}/g, function(match) {
			return ams.getFunctionByName(match.substr(1, match.length-2));
		});
	};

	MyAMS.getScript = function(url, callback, options) {
		if (typeof(callback) === 'object') {
			options = callback;
			callback = null;
		}
		if (options === undefined) {
			options = {};
		}
		var defaults = {
			dataType: 'script',
			url: ams.getSource(url),
			success: callback,
			error: ams.error.show,
			cache: !ams.devmode,
			async: options.async === undefined ? typeof(callback) === 'function' : options.async
		};
		var settings = $.extend({}, defaults, options);
		return $.ajax(settings);
	};

	MyAMS.getCSS = function(url, id) {
		var head = $('HEAD');
		var css = $('link[data-ams-id="' + id + '"]', head);
		if (css.length === 0) {
			var source = ams.getSource(url);
			if (ams.devmode) {
				source += '?_=' + new Date().getTime();
			}
			$('<link />').attr({rel: 'stylesheet',
								type: 'text/css',
								href: source,
								'data-ams-id': id})
						 .appendTo(head);
		}
	};


	/**
	 * Events management
	 */
	MyAMS.event = {

		stop: function(event) {
			if (!event) {
				event = window.event;
			}
			if (event) {
				if (event.stopPropagation) {
					event.stopPropagation();
					event.preventDefault();
				} else {
					event.cancelBubble = true;
					event.returnValue = false;
				}
			}
		}
	};


	/**
	 * Browser testing functions; mostly for IE...
	 */
	MyAMS.browser = {

		getInternetExplorerVersion: function() {
			var rv = -1;
			if (navigator.appName === "Microsoft Internet Explorer") {
				var ua = navigator.userAgent;
				var re = new RegExp("MSIE ([0-9]{1,}[.0-9]{0,})");
				if (re.exec(ua) !== null) {
					rv = parseFloat(RegExp.$1);
				}
			}
			return rv;
		},

		checkVersion: function() {
			var msg = "You're not using Windows Internet Explorer.";
			var ver = this.getInternetExplorerVersion();
			if (ver > -1) {
				if (ver >= 8) {
					msg = "You're using a recent copy of Windows Internet Explorer.";
				} else {
					msg = "You should upgrade your copy of Windows Internet Explorer.";
				}
			}
			if (globals.alert) {
				globals.alert(msg);
			}
		},

		isIE8orlower: function() {
			var msg = "0";
			var ver = this.getInternetExplorerVersion();
			if (ver > -1) {
				if (ver >= 9) {
					msg = 0;
				} else {
					msg = 1;
				}
			}
			return msg;
		},

		copyToClipboard: function() {
			return function() {
				var source = $(this);
				source.parents('.btn-group').removeClass('open');
				if (globals.prompt) {
					globals.prompt(MyAMS.i18n.CLIPBOARD_COPY, source.text());
				}
			};
		}
	};


	/**
	 * Errors management features
	 */
	MyAMS.error = {

		/**
		 * Default JQuery AJAX error handler
		 */
		ajax: function(event, response, request, error) {
			if (response.statusText === 'OK') {
				return;
			}
			var response = ams.ajax.getResponse(response);
			if (response.contentType === 'json') {
				ams.ajax.handleJSON(response.data);
			} else {
				var title = event.statusText || event.type;
				var message = response.responseText;
				ams.skin.messageBox('error', {
					title: ams.i18n.ERROR_OCCURED,
					content: '<h4>' + title + '</h4><p>' + message + '</p>',
					icon: 'fa fa-warning animated shake',
					timeout: 10000
				});
			}
			if (globals.console) {
				globals.console.error(event);
				globals.console.debug(response);
			}
		},

		/**
		 * Show AJAX error
		 */
		show: function(request, status, error) {
			if (!error) {
				return;
			}
			var response = ams.ajax.getResponse(request);
			if (response.contentType === 'json') {
				ams.ajax.handleJSON(response.data);
			} else {
				ams.skin.messageBox('error', {
					title: ams.i18n.ERRORS_OCCURED,
					content: '<h4>' + status + '</h4><p>' + error + '</p>',
					icon: "fa fa-warning animated shake",
					timeout: 10000
				});
			}
			if (globals.console) {
				globals.console.error(error);
				globals.console.debug(request);
			}
		}
	};


	/**
	 * AJAX helper functions
	 */
	MyAMS.ajax = {

		/**
		 * Check for given feature and download script if necessary
		 *
		 * @checker: pointer to a javascript object which will be downloaded in undefined
		 * @source: URL of a javascript file containing requested feature
		 * @callback: pointer to a function which will be called after the script is downloaded. The first
		 *   argument of this callback is a boolean value indicating if the script was just downloaded (true)
		 *   or if the requested object was already loaded (false)
		 * @options: callback options
		 */
		check: function(checker, source, callback, options) {
			if (typeof(callback) === 'object') {
				options = callback;
				callback = undefined;
			}
			var defaults = {
				async: typeof(callback) === 'function'
			};
			var settings = $.extend({}, defaults, options);
			if (checker instanceof Array) {
				var deferred = [];
				for (var index = 0; index < checker.length; index++) {
					if (checker[index] === undefined) {
						deferred.push(ams.getScript(source[index], {async: true}));
					}
				}
				if (deferred.length > 0) {
					$.when.apply($, deferred).then(function () {
						if (typeof(callback) === 'function') {
							callback(true, options);
						}
					});
				} else if (typeof(callback) === 'function') {
					callback(false, options);
				}
			} else if (checker === undefined) {
				if (typeof(source) === 'string') {
					ams.getScript(source, function () {
						if (typeof(callback) === 'function') {
							callback(true, options);
						}
					}, settings);
				}
			} else {
				if (typeof(callback) === 'function') {
					callback(false, options);
				}
			}
		},

		/**
		 * Get address relative to current page
		 */
		getAddr: function(addr) {
			var href = addr || $('HTML HEAD BASE').attr('href') || window.location.href;
			return href.substr(0, href.lastIndexOf("/") + 1);
		},

		/**
		 * AJAX start callback
		 */
		start: function() {
			$('#ajax-gear').show();
		},

		/**
		 * AJAX stop callback
		 */
		stop: function() {
			$('#ajax-gear').hide();
		},

		/**
		 * Handle AJAX upload and download progress
		 *
		 * @param event: the source event
		 */
		progress: function(event) {
			if (!event.lengthComputable) {
				return;
			}
			if (event.loaded >= event.total) {
				return;
			}
			if (globals.console) {
				globals.console.log(parseInt((event.loaded / event.total * 100), 10) + "%");
			}
		},

		/**
		 * Post data to given URL
		 */
		post: function(url, data, options, callback) {
			var addr;
			if (url.startsWith(window.location.protocol)) {
				addr = url;
			} else {
				addr = this.getAddr() + url;
			}
			if (typeof(options) === 'function') {
				callback = options;
				options = {};
			} else if (!options) {
				options = {};
			}
			if (typeof(callback) === 'undefined') {
				callback = options.callback;
			}
			if (typeof(callback) === 'string') {
				callback = ams.getFunctionByName(callback);
			}
			delete options.callback;

			var result;
			var defaults = {
				url: addr,
				type: 'post',
				cache: false,
				async: typeof(callback) === 'function',
				data: $.param(data),
				dataType: 'json',
				success: callback || function(data /*, status*/) {
					result = data.result;
				}
			};
			var settings = $.extend({}, defaults, options);
			$.ajax(settings);
			return result;
		},

		/**
		 * Extract data type and result from response
		 */
		getResponse: function(request) {
			var contentType = request.getResponseHeader('content-type'),
				dataType,
				result;
			if (contentType) {
				// Got server response
				if (contentType.startsWith('application/javascript')) {
					dataType = 'script';
					result = request.responseText;
				} else if (contentType.startsWith('text/html')) {
					dataType = 'html';
					result = request.responseText;
				} else if (contentType.startsWith('text/xml')) {
					dataType = 'xml';
					result = request.responseText;
				} else {
					result = request.responseJSON;
					if (result) {
						dataType = 'json';
					} else {
						try {
							result = JSON.parse(request.responseText);
							dataType = 'json';
						} catch (e) {
							result = request.responseText;
							dataType = 'text';
						}
					}
				}
			} else {
				// Probably no response from server...
				dataType = 'json';
				result = {
					status: 'alert',
					alert: {
						title: ams.i18n.ERROR_OCCURED,
						content: ams.i18n.NO_SERVER_RESPONSE
					}
				};
			}
			return {contentType: dataType,
					data: result};
		},

		/**
		 * Handle server response in JSON format
		 *
		 * Result is made of several JSON attributes:
		 *  - status: error, success, callback, callbacks, reload or redirect
		 *  - close_form: boolean indicating if current modal should be closed
		 *  - location: target URL for reload or redirect status
		 *  - target: target container's selector for loaded content ('#content' by default)
		 *  - content: available for any status producing output content:
		 *        {target: target container's selector (source form by default)
		 *         html: HTML result}
		 *  - message: available for any status producing output message:
		 *        {target: target message container's selector
		 *         status: message status
		 *         header: message header
		 *         subtitle: message subtitle,
		 *         body: message body}
		 *
		 * For errors data structure, please see MyAMS.form.showErrors function
		 */
		handleJSON: function(result, form, target) {
			var status = result.status;
			var url;
			switch (status) {
				case 'alert':
					if (globals.alert) {
						globals.alert(result.alert.title + '\n\n' + result.alert.content);
					}
					break;
				case 'error':
					ams.form.showErrors(form, result);
					break;
				case 'info':
				case 'success':
					ams.form.resetChanged(form);
					if (result.close_form !== false) {
						ams.dialog.close(form);
					}
					break;
				case 'message':
				case 'messagebox':
					break;
				case 'notify':
				case 'callback':
				case 'callbacks':
					ams.form.resetChanged(form);
					if (result.close_form !== false) {
						ams.dialog.close(form);
					}
					break;
				case 'modal':
					ams.dialog.open(result.location);
					break;
				case 'reload':
					ams.form.resetChanged(form);
					if (result.close_form !== false) {
						ams.dialog.close(form);
					}
					url = result.location || window.location.hash;
					if (url.startsWith('#')) {
						url = url.substr(1);
					}
					ams.skin.loadURL(url, result.target || target || '#content');
					break;
				case 'redirect':
					ams.form.resetChanged(form);
					if (result.close_form === true) {
						ams.dialog.close(form);
					}
					url = result.location || window.location.href;
					if (result.window) {
						window.open(url, result.window, result.options);
					} else {
						if (window.location.href === url) {
							window.location.reload(true);
						} else {
							window.location.href = url;
						}
					}
					break;
				default:
					if (globals.console) {
						globals.console.log("Unhandled status: " + status);
					}
			}

			var index;
			var content;
			var container;
			if (result.content) {
				content = result.content;
				container = $(content.target || target || form || '#content');
				if (content.raw === true) {
					container.text(content.text);
				} else {
					container.html(content.html);
					ams.initContent(container);
				}
				if (!content.keep_hidden) {
					container.removeClass('hidden');
				}
			}
			if (result.contents) {
				var contents = result.contents;
				for (index=0; index < contents.length; index++) {
					content = contents[index];
					container = $(content.target);
					if (content.raw === true) {
						container.text(content.text);
					} else {
						container.html(content.html);
						ams.initContent(container);
					}
					if (!content.keep_hidden) {
						container.removeClass('hidden');
					}
				}
			}

			var message;
			if (result.message) {
				message = result.message;
				if (typeof(message) === 'string') {
					if ((status === 'info') || (status === 'success')) {
						ams.skin.smallBox(status,
										  {
											  title: message,
											  icon: 'fa fa-fw fa-info-circle font-xs align-top margin-top-10',
											  timeout: 3000
										  });
					} else {
						ams.skin.alert($(form || '#content'), status, message);
					}
				} else {
					ams.skin.alert($(message.target || target || form || '#content'),
								   message.status || 'success',
								   message.header,
								   message.body,
								   message.subtitle);
				}
			}
			if (result.smallbox) {
				ams.skin.smallBox(result.smallbox_status || status,
								  {title: result.smallbox,
								   icon: 'fa fa-fw fa-info-circle font-xs align-top margin-top-10',
								   timeout: 3000});
			}
			if (result.messagebox) {
				message = result.messagebox;
				if (typeof(message) === 'string') {
					ams.skin.messageBox('info',
										{
											title: ams.i18n.ERROR_OCCURED,
											content: message,
											timeout: 10000
										});
				} else {
					var messageStatus = message.status || 'info';
					if (messageStatus === 'error' && form && target) {
						ams.executeFunctionByName(form.data('ams-form-submit-error') || 'MyAMS.form.finalizeSubmitOnError', form, target);
					}
					ams.skin.messageBox(messageStatus,
										{title: message.title || ams.i18n.ERROR_OCCURED,
										 content: message.content,
										 icon: message.icon,
										 number: message.number,
										 timeout: message.timeout === null ? undefined : (message.timeout || 10000)});
				}
			}
			if (result.event) {
				form.trigger(result.event, result.event_options);
			}
			if (result.callback) {
				ams.executeFunctionByName(result.callback, form, result.options);
			}
			if (result.callbacks) {
				var callback;
				for (index=0; index < result.callbacks.length; index++) {
					callback = result.callbacks[index];
					ams.executeFunctionByName(callback, form, callback.options);
				}
			}
		}
	};


	/**
	 * JSON-RPC helper functions
	 */
	MyAMS.jsonrpc = {

		/**
		 * Get address relative to current page
		 */
		getAddr: function(addr) {
			var href = addr || $('HTML HEAD BASE').attr('href') || window.location.href;
			var target = href.replace(/\+\+skin\+\+\w+\//, '');
			return target.substr(0, target.lastIndexOf("/") + 1);
		},

		/**
		 * Execute JSON-RPC request on given method
		 *
		 * Query can be given as a simple "query" string or as an object containing all query parameters.
		 * Parameters:
		 *  - @query: query string (posted as "query" parameter) or object containing all parameters
		 *  - @method: name of JSON-RPC procedure to call
		 *  - @options: additional JSON-RPC procedure parameters
		 *  - @callback: name of a callback which will be called on server response
		 */
		query: function(query, method, options, callback) {
			ams.ajax.check($.jsonRpc,
						   ams.baseURL + 'ext/jquery-jsonrpc' + ams.devext + '.js',
						   function() {
								if (typeof(options) === 'function') {
									callback = options;
									options = {};
								}
								else if (!options) {
									options = {};
								}
								if (callback === 'undefined') {
									callback = options.callback;
								}
								if (typeof(callback) === 'string') {
									callback = ams.getFunctionByName(callback);
								}
								delete options.callback;

								var params = {};
								if (typeof(query) === 'string') {
									params.query = query;
								} else if (typeof(query) === 'object') {
									$.extend(params, query);
								}
								$.extend(params, options);

								var result;
								var settings = {
									url: ams.jsonrpc.getAddr(options.url),
									type: 'post',
									cache: false,
									method: method,
									params: params,
									async: typeof(callback) === 'function',
									success: callback || function(data /*, status*/) {
										result = data.result;
									},
									error: ams.error.show
								};
								$.jsonRpc(settings);
								return result;
						   });
		},

		/**
		 * Execute given JSON-RPC post on given method
		 *
		 * Parameters:
		 *  - @method: name of JSON-RPC procedure to call
		 *  - @options: additional JSON-RPC method call parameters
		 *  - @callback: name of a callback which will be called on server response
		 */
		post: function(method, data, options, callback) {
			ams.ajax.check($.jsonRpc,
						   ams.baseURL + 'ext/jquery-jsonrpc' + ams.devext + '.js',
						   function() {
								if (typeof(options) === 'function') {
									callback = options;
									options = {};
								}
								else if (!options) {
									options = {};
								}
								if (typeof(callback) === 'undefined') {
									callback = options.callback;
								}
								if (typeof(callback) === 'string') {
									callback = ams.getFunctionByName(callback);
								}
								delete options.callback;

								var result;
								var defaults = {
									url: ams.jsonrpc.getAddr(options.url),
									type: 'post',
									cache: false,
									method: method,
									params: data,
									async: typeof(callback) === 'function',
									success: callback || function(data /*, status*/) {
										result = data.result;
									},
									error: ams.error.show
								};
								var settings = $.extend({}, defaults, options);
								$.jsonRpc(settings);
								return result;
						   });
		}
	};


	/**
	 * XML-RPC helper functions
	 */
	MyAMS.xmlrpc = {

		/**
		 * Get address relative to current page
		 */
		getAddr: function(addr) {
			var href = addr || $('HTML HEAD BASE').attr('href') || window.location.href;
			var target = href.replace(/\+\+skin\+\+\w+\//, '');
			return target.substr(0, target.lastIndexOf("/") + 1);
		},

		/**
		 * Execute given XML-RPC post on given method
		 *
		 * Parameters:
		 *  - @url: base method URL
		 *  - @method: name of JSON-RPC procedure to call
		 *  - @options: additional JSON-RPC procedure parameters
		 *  - @callback: name of a callback which will be called on server response
		 */
		post: function(url, method, data, options, callback) {
			ams.ajax.check($.xmlrpc,
						   ams.baseURL + 'ext/jquery-xmlrpc' + ams.devext + '.js',
						   function() {
								if (typeof(options) === 'function') {
									callback = options;
									options = {};
								}
								else if (!options) {
									options = {};
								}
								if (typeof(callback) === 'undefined') {
									callback = options.callback;
								}
								if (typeof(callback) === 'string') {
									callback = ams.getFunctionByName(callback);
								}
								delete options.callback;

								var result;
								var defaults = {
									url: ams.xmlrpc.getAddr(url),
									methodName: method,
									params: data,
									success: callback || function(response /*, status, xhr*/) {
										result = response;
									},
									error: ams.error.show
								};
								var settings = $.extend({}, defaults, options);
								$.xmlrpc(settings);
								return result;
						   });
		}
	};


	/**
	 * Forms helper functions
	 */
	MyAMS.form = {

		/**
		 * Init forms to activate form change listeners
		 *
		 * @param element: the parent element
		 */
		init: function(element) {
			// Activate form changes if required
			var forms;
			if (ams.warnOnFormChange) {
				forms = $('FORM[data-ams-warn-on-change!="false"]', element);
			} else {
				forms = $('FORM[data-ams-warn-on-change="true"]', element);
			}
			forms.each(function() {
				var form = $(this);
				$('INPUT[type="text"], ' +
				  'INPUT[type="checkbox"], ' +
				  'INPUT[type="radio"], ' +
				  'SELECT, ' +
				  'TEXTAREA, ' +
				  '[data-ams-changed-event]', form).each(function() {
						var source = $(this);
						if (source.data('ams-ignore-change') !== true) {
							var event = source.data('ams-changed-event') || 'change';
							source.on(event, function () {
								ams.form.setChanged($(this).parents('FORM'));
							});
						}
				});
				form.on('reset', function() {
					ams.form.resetChanged($(this));
				});
			});
		},

		/**
		 * Set focus to first container input
		 */
		setFocus: function(container) {
			var focused = $('[data-ams-focus-target]', container).first();
			if (!focused.exists()) {
				focused = $('input, select', container).first();
			}
			if (focused.exists()) {
				if (focused.hasClass('select2-input')) {
					focused = focused.parents('.select2');
				}
				if (focused.hasClass('select2')) {
					setTimeout(function() {
						focused.select2('focus');
						if (focused.data('ams-focus-open') === true) {
							focused.select2('open');
						}
					}, 100);
				} else {
					focused.focus();
				}
			}
		},

		/**
		 * Check for modified forms before exiting
		 */
		checkBeforeUnload: function() {
			var forms = $('FORM[data-ams-form-changed="true"]');
			if (forms.exists()) {
				return ams.i18n.FORM_CHANGED_WARNING;
			}
		},

		/**
		 * Check for modified forms before loading new inner content
		 */
		confirmChangedForm: function(element, callback, cancelCallback) {
			if (typeof(element) === 'function') {
				callback = element;
				element = undefined;
			}
			var forms = $('FORM[data-ams-form-changed="true"]', element);
			if (forms.exists()) {
				if (cancelCallback) {
					if (globals.confirm(ams.i18n.FORM_CHANGED_WARNING, ams.i18n.WARNING)) {
						callback.call(element);
					} else {
						cancelCallback.call(element);
					}
				} else {
					ams.skin.bigBox({
						title: ams.i18n.WARNING,
						content: '<i class="text-danger fa fa-2x fa-bell shake animated"></i>&nbsp; ' + ams.i18n.FORM_CHANGED_WARNING,
						buttons: ams.i18n.BTN_OK_CANCEL
					}, function(button) {
						if (button === ams.i18n.BTN_OK) {
							callback.call(element);
						}
					});
				}
			} else {
				callback.call(element);
			}
		},

		/**
		 * Update form "chenged" status flag
		 */
		setChanged: function(form) {
			form.attr('data-ams-form-changed', true);
		},

		/**
		 * Reset form changed flag
		 */
		resetChanged: function(form) {
			if (form !== undefined) {
				$(form).removeAttr('data-ams-form-changed');
			}
		},

		/**
		 * Submit given form
		 */
		submit: function(form, handler, submitOptions) {
			// Check params
			form = $(form);
			if (!form.exists()) {
				return false;
			}
			if (typeof(handler) === 'object') {
				submitOptions = handler;
				handler = undefined;
			}
			// Prevent multiple submits of the same form
			if (form.data('submitted')) {
				if (!form.data('ams-form-hide-submitted')) {
					ams.skin.messageBox('warning', {
						title: ams.i18n.WAIT,
						content: ams.i18n.FORM_SUBMITTED,
						icon: 'fa fa-save shake animated',
						timeout: form.data('ams-form-alert-timeout') || 5000
					});
				}
				return false;
			}
			// Check submit validators
			if (!ams.form._checkSubmitValidators(form)) {
				return false;
			}
			// Remove remaining status messages
			$('.alert-danger, SPAN.state-error', form).not('.persistent').remove();
			$('.state-error', form).removeClassPrefix('state-');
			// Check submit button
			var button = $(form.data('ams-submit-button'));
			if (button && !button.data('ams-form-hide-loading')) {
				button.data('ams-progress-content', button.html());
				button.button('loading');
			}
			ams.ajax.check($.fn.ajaxSubmit,
						   ams.baseURL + 'ext/jquery-form-3.49' + ams.devext + '.js',
						   function() {

								function _submitAjaxForm(form, options) {

									var button,
										buttonData,
										buttonTarget;
									var data = form.data();
									var formOptions = data.amsFormOptions;
									var formData;
									var formDataCallback;

									var progressHandler;
									var progressInterval;
									var progressCallback;
									var progressEndCallback;

									// Inner progress status handler
									function _getProgress(handler, progress_id) {

										var interval;

										function _clearProgressStatus() {
											clearInterval(interval);
											ams.form.resetAfterSubmit(form, button);
											button.html(button.data('ams-progress-content'));
											ams.executeFunctionByName(progressEndCallback, form, button);
											ams.form.resetChanged(form);
										}

										function _getProgressStatus() {
											ams.ajax.post(handler,
														  {progress_id: progress_id},
														  {error: _clearProgressStatus},
														  ams.getFunctionByName(progressCallback) || function(result, status) {
															if (status === 'success') {
																if (result.status === 'running') {
																	if (result.message) {
																		button.text(result.message);
																	} else {
																		var text = button.data('ams-progress-text') || ams.i18n.PROGRESS;
																		if (result.current) {
																			text += ': ' + result.current + '/ ' + (result.length || 100);
																		} else {
																			text += '...';
																		}
																		button.text(text);
																	}
																} else if (result.status === 'finished') {
																	_clearProgressStatus();
																}
															} else {
																_clearProgressStatus();
															}
														  });
										}

										button.button('loading');
										interval = setInterval(_getProgressStatus, progressInterval);
									}

									// Initialize form data
									if (submitOptions) {
										formDataCallback = submitOptions.formDataInitCallback;
									}
									if (formDataCallback) {
										delete submitOptions.formDataInitCallback;
									} else {
										formDataCallback = data.amsFormDataInitCallback;
									}
									if (formDataCallback) {
										var veto = {};
										if (typeof(formDataCallback) === 'function') {
											formData = formDataCallback.call(form, veto);
										} else {
											formData = ams.executeFunctionByName(formDataCallback, form, veto);
										}
										if (veto.veto) {
											button = form.data('ams-submit-button');
											if (button) {
												button.button('reset');
											}
											ams.form.finalizeSubmitFooter.call(form);
											return false;
										}
									} else {
										formData = data.amsFormData || {};
									}

									// Check submit button for custom action handler and target
									button = $(form.data('ams-submit-button'));
									if (button && button.exists()) {
										buttonData = button.data();
										buttonTarget = buttonData.amsFormSubmitTarget;
									} else {
										buttonData = {};
									}

									// Check action URL
									var url;
									var formHandler = handler || buttonData.amsFormHandler || data.amsFormHandler || '';
									if (formHandler.startsWith(window.location.protocol)) {
										url = formHandler;
									} else {
										var action = buttonData.amsFormAction || form.attr('action').replace(/#/, '');
										if (action.startsWith(window.location.protocol)) {
											url = action;
										} else {
											url = ams.ajax.getAddr() + action;
										}
										url += formHandler;
									}
									progressHandler = buttonData.amsProgressHandler || data.amsProgressHandler || '';
									progressInterval = buttonData.amsProgressInterval || data.amsProgressInterval || 1000;
									progressCallback = buttonData.amsProgressCallback || data.amsProgressCallback;
									progressEndCallback = buttonData.amsProgressEndCallback || data.amsProgressEndCallback;

									// Initialize submit target with AJAX indicator
									var target = null;
									if (submitOptions && submitOptions.initSubmitTarget) {
										ams.executeFunctionByName(submitOptions.initSubmitTarget, form);
									} else {
										if (data.amsFormInitSubmitTarget) {
											target = $(buttonTarget || data.amsFormSubmitTarget || '#content');
											ams.executeFunctionByName(data.amsFormInitSubmit || 'MyAMS.form.initSubmit', form, target);
										} else if (!data.amsFormHideSubmitFooter) {
											ams.executeFunctionByName(data.amsFormInitSubmit || 'MyAMS.form.initSubmitFooter', form);
										}
									}

									// Complete form data
									if (submitOptions) {
										formData = $.extend({}, formData, submitOptions.form_data);
									}

									// Check progress handler
									var hasUpload;
									if (progressHandler) {
										formData.progress_id = ams.generateUUID();
									} else {
										// Check progress meter via Apache progress module
										hasUpload = typeof(options.uuid) !== 'undefined';
										if (hasUpload) {
											if (url.indexOf('X-Progress-ID') < 0) {
												url += "?X-Progress-ID=" + options.uuid;
											}
											delete options.uuid;
										}
									}

									// Initialize default AJAX settings
									var defaults = {
										url: url,
										type: 'post',
										cache: false,
										data: formData,
										dataType: data.amsFormDatatype,
										beforeSerialize: function(/*form, options*/) {
											if (typeof(globals.tinyMCE) !== 'undefined') {
												globals.tinyMCE.triggerSave();
											}
										},
										beforeSubmit: function(data, form /*, options*/) {
											form.data('submitted', true);
										},
										error: function(request, status, error, form) {
											if (target) {
												ams.executeFunctionByName(data.amsFormSubmitError || 'MyAMS.form.finalizeSubmitOnError', form, target);
											}
											ams.form.resetAfterSubmit(form);
										},
										iframe: hasUpload
									};

									// Initialize IFrame for custom download target
									var downloadTarget = (submitOptions && submitOptions.downloadTarget) || data.amsFormDownloadTarget;
									if (downloadTarget) {
										var iframe = $('iframe[name="' + downloadTarget + '"]');
										if (!iframe.exists()) {
											iframe = $('<iframe></iframe>').hide()
																		   .attr('name', downloadTarget)
																		   .appendTo($('body'));
										}
										defaults = $.extend({}, defaults, {
											iframe: true,
											iframeTarget: iframe,
											success: function(result, status, request, form) {
												var modal = $(form).parents('.modal-dialog');
												if (modal.exists()) {
													ams.dialog.close(form);
												} else {
													var callback;
													var button = form.data('ams-submit-button');
													if (button) {
														callback = button.data('ams-form-submit-callback');
													}
													if (!callback) {
														callback = ams.getFunctionByName(data.amsFormSubmitCallback) || ams.form._submitCallback;
													}
													try {
														callback.call(form, result, status, request, form);
													} finally {
														ams.form.resetAfterSubmit(form);
														ams.form.resetChanged(form);
													}
												}
											}
										});
									} else {
										defaults = $.extend({}, defaults, {
											error: function(request, status, error, form) {
												if (target) {
													ams.executeFunctionByName(data.amsFormSubmitError || 'MyAMS.form.finalizeSubmitOnError', form, target);
												}
												ams.form.resetAfterSubmit(form);
											},
											success: function(result, status, request, form) {
												var callback;
												var button = form.data('ams-submit-button');
												if (button) {
													callback = button.data('ams-form-submit-callback');
												}
												if (!callback) {
													callback = ams.getFunctionByName(data.amsFormSubmitCallback) || ams.form._submitCallback;
												}
												try {
													callback.call(form, result, status, request, form);
												} finally {
													ams.form.resetAfterSubmit(form);
													ams.form.resetChanged(form);
												}
											},
											iframe: hasUpload
										});
									}
									var settings = $.extend({}, defaults, options, formOptions, submitOptions);

									// Initialize progress handler
									if (progressHandler) {
										_getProgress(progressHandler, formData.progress_id);
									}

									// Submit form
									$(form).ajaxSubmit(settings);

									// If external download target is specified, reset form submit button and footer
									if (downloadTarget) {
										var modal = $(form).parents('.modal-dialog');
										var keepModal = modal.exists() && button.exists() && button.data('ams-keep-modal');
										if (modal.exists() && (keepModal !== true)) {
											ams.dialog.close(form);
										} else {
											if (!progressHandler) {
												setTimeout(function () {
													ams.form.resetAfterSubmit(form, button);
													ams.form.resetChanged(form);
												}, button.data('ams-form-reset-timeout') || 2000);
											}
										}
									}
								}

								var hasUpload = (form.data('ams-form-ignore-uploads') !== true) &&
												($('INPUT[type="file"]', form).length > 0);
								if (hasUpload) {
									// JQuery-progressbar plug-in must be loaded synchronously!!
									// Otherwise, hidden input fields created by jquery-validate plug-in
									// and matching named buttons will be deleted (on first form submit)
									// before JQuery-form plug-in can get them when submitting the form...
									ams.ajax.check($.progressBar,
												   ams.baseURL + 'ext/jquery-progressbar' + ams.devext + '.js');
									var settings = $.extend({}, {
										uuid: $.progressBar.submit(form)
									});
									_submitAjaxForm(form, settings);
								} else {
									_submitAjaxForm(form, {});
								}
						   });
			return false;
		},

		/**
		 * Initialize AJAX submit call
		 *
		 * @param this: the submitted form
		 * @param target: the form submit container target
		 * @param message: the optional message
		 */
		initSubmit: function(target, message) {
			var form = $(this);
			var spin = '<i class="fa fa-3x fa-gear fa-spin"></i>';
			if (!message) {
				message = form.data('ams-form-submit-message');
			}
			if (message) {
				spin += '<strong>' + message + '</strong>';
			}
			$(target).html('<div class="row margin-20"><div class="text-center">' + spin + '</div></div>');
			$(target).parents('.hidden').removeClass('hidden');
		},

		/**
		 * Reset form status after submit
		 *
		 * @param form: the submitted form
		 */
		resetAfterSubmit: function(form) {
			if (form.is(':visible')) {
				var button = form.data('ams-submit-button');
				if (button) {
					button.button('reset');
				}
				ams.form.finalizeSubmitFooter.call(form);
			}
			form.data('submitted', false);
			form.removeData('ams-submit-button');
		},

		/**
		 * Finalize AJAX submit call
		 *
		 * @param target: the form submit container target
		 */
		finalizeSubmitOnError: function(target) {
			$('i', target).removeClass('fa-spin')
						  .removeClass('fa-gear')
						  .addClass('fa-ambulance');
		},

		/**
		 * Initialize AJAX submit call in form footer
		 *
		 * @param this: the submitted form
		 * @param message: the optional submit message
		 */
		initSubmitFooter: function(message) {
			var form = $(this);
			var spin = '<i class="fa fa-3x fa-gear fa-spin"></i>';
			if (!message) {
				message = $(this).data('ams-form-submit-message');
			}
			if (message) {
				spin += '<strong class="submit-message align-top padding-left-10 margin-top-10">' + message + '</strong>';
			}
			var footer = $('footer', form);
			$('button', footer).hide();
			footer.append('<div class="row"><div class="text-center">' + spin + '</div></div>');
		},

		/**
		 * Finalize AJAX submit call
		 *
		 * @param this: the submitted form
		 * @param target: the form submit container target
		 */
		finalizeSubmitFooter: function(/*target*/) {
			var form = $(this);
			var footer = $('footer', form);
			if (footer) {
				$('.row', footer).remove();
				$('button', footer).show();
			}
		},

		/**
		 * Handle AJAX submit results
		 *
		 * Submit results are auto-detected via response content type, except when this content type
		 * is specified into form's data attributes.
		 * Submit response can be of several content types:
		 * - html or text: the response is directly included into a "target" container (#content by default)
		 * - json: a "status" attribute indicates how the request was handled and how the response should be
		 *   treated:
		 *     - error: indicates that an error occured; other response attributes indicate error messages
		 *     - success: basic success, no other action is requested
		 *     - callback: only call given function to handle the result
		 *     - callbacks: only call given set of functions to handle the result
		 *     - reload: page's body should be reloaded from a given URL
		 *     - redirect: redirect browser to given URL
		 *   Each JSON response can also specify an HTML content, a message and a callback (
		 */
		_submitCallback: function(result, status, request, form) {

			var button;
			if (form.is(':visible')) {
				ams.form.finalizeSubmitFooter.call(form);
				button = form.data('ams-submit-button');
				if (button) {
					button.button('reset');
				}
			}

			var data = form.data();
			var dataType;
			if (data.amsFormDatatype) {
				dataType = data.amsFormDatatype;
			} else {
				var response = ams.ajax.getResponse(request);
				dataType = response.contentType;
				result = response.data;
			}

			var target;
			if (button) {
				target = $(button.data('ams-form-submit-target') || data.amsFormSubmitTarget || '#content');
			} else {
				target = $(data.amsFormSubmitTarget || '#content');
			}

			switch (dataType) {
				case 'json':
					ams.ajax.handleJSON(result, form, target);
					break;
				case 'script':
					break;
				case 'xml':
					break;
				case 'html':
					/* falls through */
				case 'text':
					/* falls through */
				default:
					ams.form.resetChanged(form);
					if (button && (button.data('ams-keep-modal') !== true)) {
						ams.dialog.close(form);
					}
					if (!target.exists()) {
						target = $('body');
					}
					target.parents('.hidden').removeClass('hidden');
					$('.alert', target.parents('.alerts-container')).remove();
					target.css({opacity: '0.0'})
						  .html(result)
						  .delay(50)
						  .animate({opacity: '1.0'}, 300);
					ams.initContent(target);
					ams.form.setFocus(target);
			}
			var callback = request.getResponseHeader('X-AMS-Callback');
			if (callback) {
				var options = request.getResponseHeader('X-AMS-Callback-Options');
				ams.executeFunctionByName(callback, form, options === undefined ? {} : JSON.parse(options), request);
			}
		},

		/**
		 * Get list of custom validators called before submit
		 */
		_getSubmitValidators: function(form) {
			var validators = [];
			var formValidator = form.data('ams-form-validator');
			if (formValidator) {
				validators.push([form, formValidator]);
			}
			$('[data-ams-form-validator]', form).each(function() {
				var source = $(this);
				validators.push([source, source.data('ams-form-validator')]);
			});
			return validators;
		},

		/**
		 * Call list of custom validators before submit
		 *
		 * Each validator can return:
		 *  - a boolean 'false' value to just specify that an error occured
		 *  - a string value containing an error message
		 *  - an array containing a list of string error messages
		 * Any other value (undefined, null, True...) will lead to a successful submit.
		 */
		_checkSubmitValidators: function(form) {
			var validators = ams.form._getSubmitValidators(form);
			if (!validators.length) {
				return true;
			}
			var output = [];
			var result = true;
			for (var index=0; index < validators.length; index++) {
				var validator = validators[index];
				var source = validator[0];
				var handler = validator[1];
				var validatorResult = ams.executeFunctionByName(handler, form, source);
				if (validatorResult === false) {
					result = false;
				} else if (typeof(validatorResult) === 'string') {
					output.push(validatorResult);
				} else if (result.length && (result.length > 0)) {
					output = output.concat(result);
				}
			}
			if (output.length > 0) {
				var header = output.length === 1 ? ams.i18n.ERROR_OCCURED : ams.i18n.ERRORS_OCCURED;
				ams.skin.alert(form, 'danger', header, output);
				return false;
			} else {
				return result;
			}
		},

		/**
		 * Display JSON errors
		 * JSON errors should be defined in an object as is:
		 * {status: 'error',
		 *  error_message: "Main error message",
		 *  messages: ["Message 1", "Message 2",...]
		 *  widgets: [{label: "First widget name",
		 *             name: "field-name-1",
		 *             message: "Error message"},
		 *            {label: "Second widget name",
		 *             name: "field-name-2",
		 *             message: "Second error message"},...]}
		 */
		showErrors: function(form, errors) {
			var header;
			if (typeof(errors) === 'string') {
				ams.skin.alert(form, 'error', ams.i18n.ERROR_OCCURED, errors);
			} else if (errors instanceof Array) {
				header = errors.length === 1 ? ams.i18n.ERROR_OCCURED : ams.i18n.ERRORS_OCCURED;
				ams.skin.alert(form, 'error', header, errors);
			} else {
				$('.state-error', form).removeClass('state-error');
				header = errors.error_header ||
						 (errors.widgets && (errors.widgets.length > 1) ? ams.i18n.ERRORS_OCCURED : ams.i18n.ERROR_OCCURED);
				var message = [];
				var index;
				if (errors.messages) {
					for (index = 0; index < errors.messages.length; index++) {
						var msg = errors.messages[index];
						if (msg.header) {
							message.push('<strong>' + msg.header + '</strong><br />' + msg.message);
						} else {
							message.push(msg.message || msg);
						}
					}
				}
				if (errors.widgets) {
					for (index = 0; index < errors.widgets.length; index++) {
						// set widget status message
						var widgetData = errors.widgets[index];
						var widget = $('[name="' + widgetData.name + '"]', form);
						widget.parents('label:first')
								.removeClassPrefix('state-')
								.addClass('state-error')
								.after('<span for="name" class="state-error">' + widgetData.message + '</span>');
						// complete form alert message
						if (widgetData.label) {
							message.push(widgetData.label + ' : ' + widgetData.message);
						}
						// mark parent tab (if any) with error status
						var tabIndex = widget.parents('.tab-pane').index() + 1;
						if (tabIndex > 0) {
							var navTabs = $('.nav-tabs', $(widget).parents('.tabforms'));
							$('li:nth-child(' + tabIndex + ')', navTabs).removeClassPrefix('state-')
																		.addClass('state-error');
							$('li.state-error:first a', form).click();
						}
					}
				}
				ams.skin.alert($('fieldset:first', form), errors.error_level || 'error', header, message, errors.error_message);
			}
		}
	};


	/**
	 * Modal dialogs helper functions
	 */
	MyAMS.dialog = {

		/**
		 * List of registered 'shown' callbacks
		 */
		_shown_callbacks: [],

		/**
		 * Register a callback which should be called when a dialog is shown
		 */
		registerShownCallback: function(callback, element) {
			var dialog;
			if (element) {
				dialog = element.objectOrParentWithClass('modal-dialog');
			}

			var callbacks;
			if (dialog && dialog.exists()) {
				callbacks = dialog.data('shown-callbacks');
				if (callbacks === undefined) {
					callbacks = [];
					dialog.data('shown-callbacks', callbacks);
				}
			} else {
				callbacks = ams.dialog._shown_callbacks;
			}
			if (callbacks.indexOf(callback) < 0) {
				callbacks.push(callback);
			}
		},

		/**
		 * List of registered 'hide' callbacks
		 */
		_hide_callbacks: [],

		/**
		 * Register a callback which should be called when a dialog is closed
		 */
		registerHideCallback: function(callback, element) {
			var dialog;
			if (element) {
				dialog = element.objectOrParentWithClass('modal-dialog');
			}

			var callbacks;
			if (dialog && dialog.exists()) {
				callbacks = dialog.data('hide-callbacks');
				if (callbacks === undefined) {
					callbacks = [];
					dialog.data('hide-callbacks', callbacks);
				}
			} else {
				callbacks = ams.dialog._hide_callbacks;
			}
			if (callbacks.indexOf(callback) < 0) {
				callbacks.push(callback);
			}
		},

		/**
		 * Modal dialog opener
		 */
		open: function(source, options) {
			ams.ajax.check($.fn.modalmanager,
						   ams.baseURL + 'ext/bootstrap-modalmanager' + ams.devext + '.js',
						   function() {
								ams.ajax.check($.fn.modal.defaults,
											   ams.baseURL + 'ext/bootstrap-modal' + ams.devext + '.js',
								function(first_load) {
									if (first_load) {
										$(document).off('click.modal');
										$.fn.modal.defaults.spinner = $.fn.modalmanager.defaults.spinner =
											'<div class="loading-spinner" style="width: 200px; margin-left: -100px;">' +
												'<div class="progress progress-striped active">' +
													'<div class="progress-bar" style="width: 100%;"></div>' +
												'</div>' +
											'</div>';
									}

									var sourceData;
									var url;
									if (typeof(source) === 'string') {
										sourceData = {};
										url = source;
									} else {
										sourceData = source.data();
										url = source.attr('href') || sourceData.amsUrl;
										var url_getter = ams.getFunctionByName(url);
										if (typeof(url_getter) === 'function') {
											url = url_getter.call(source);
										}
									}
									if (!url) {
										return;
									}
									$('body').modalmanager('loading');
									if (url.indexOf('#') === 0) {
										// Inner hidden modal dialog
										$(url).modal('show');
									} else {
										// Remote URL modal dialog
										$.ajax({
											url: url,
											type: 'get',
											cache: sourceData.amsAllowCache === undefined ? false : sourceData.amsAllowCache,
											data: options,
											success: function(data, status, request) {
												$('body').modalmanager('removeLoading');
												var response = ams.ajax.getResponse(request);
												var dataType = response.contentType;
												var result = response.data;
												switch (dataType) {
													case 'json':
														ams.ajax.handleJSON(result, $($(source).data('ams-json-target') || '#content'));
														break;
													case 'script':
														break;
													case 'xml':
														break;
													case 'html':
														/* falls through */
													case 'text':
														/* falls through */
													default:
														var content = $(result);
														var dialog = $('.modal-dialog', content.wrap('<div></div>').parent());
														var dialogData = dialog.data();
														var dataOptions = {
															backdrop: 'static',
															overflow: dialogData.amsModalOverflow || '.modal-viewport',
															maxHeight: dialogData.amsModalMaxHeight === undefined ?
																	function() {
																		return $(window).height() -
																					$('.modal-header', content).outerHeight(true) -
																					$('footer', content).outerHeight(true) - 85;
																	}
																	: ams.getFunctionByName(dialogData.amsModalMaxHeight)
														};
														var settings = $.extend({}, dataOptions, dialogData.amsModalOptions);
														settings = ams.executeFunctionByName(dialogData.amsModalInitCallback, dialog, settings) || settings;
														$('<div>').addClass('modal fade')
																  .append(content)
																  .modal(settings)
																  .on('shown', ams.dialog.shown)
																  .on('hidden', ams.dialog.hidden);
														ams.initContent(content);
														if (sourceData.amsLogEvent !== false) {
															ams.stats.logPageview(url);
														}
												}
											}
										});
									}
								});
						   });
		},

		/**
		 * Modals shown callback
		 * This callback is used to initialize modal's viewport size
		 */
		shown: function(e) {

			function resetViewport(ev) {
				var top = $('.scrollmarker.top', viewport);
				var topPosition = viewport.scrollTop();
				if (topPosition > 0) {
					top.show();
				} else {
					top.hide();
				}
				var bottom = $('.scrollmarker.bottom', viewport);
				if (maxHeight + topPosition >= viewport.get(0).scrollHeight) {
					bottom.hide();
				} else {
					bottom.show();
				}
			}

			var modal = e.target;
			var viewport = $('.modal-viewport', modal);
			if (viewport.exists()) {
				var maxHeight = parseInt(viewport.css('max-height'));
				var barWidth = $.scrollbarWidth();
				if ((viewport.css('overflow') !== 'hidden') &&
					(viewport.height() === maxHeight)) {
					$('<div></div>').addClass('scrollmarker')
						.addClass('top')
						.css('top', 0)
						.css('width', viewport.width() - barWidth)
						.hide()
						.appendTo(viewport);
					$('<div></div>').addClass('scrollmarker')
						.addClass('bottom')
						.css('top', maxHeight - 20)
						.css('width', viewport.width() - barWidth)
						.appendTo(viewport);
					viewport.scroll(resetViewport);
					viewport.off('resize')
						.on('resize', resetViewport);
				} else {
					$('.scrollmarker', viewport).remove();
				}
			}

			// Check for shown callbacks defined via data API
			$('[data-ams-shown-callback]', modal).each(function() {
				var callback = ams.getFunctionByName($(this).data('ams-shown-callback'));
				if (callback) {
					callback.call(modal, this);
				}
			});
			// Call shown callbacks registered for this dialog
			var index;
			var callbacks = $('.modal-dialog', modal).data('shown-callbacks');
			if (callbacks) {
				for (index=0; index < callbacks.length; index++) {
					callbacks[index].call(modal);
				}
			}
			// Call globally registered shown callbacks
			callbacks = ams.dialog._shown_callbacks;
			if (callbacks) {
				for (index=0; index < callbacks.length; index++) {
					callbacks[index].call(modal);
				}
			}

			ams.form.setFocus(modal);
		},

		/**
		 * Close modal dialog associated with given context
		 */
		close: function(context) {
			if (typeof(context) === 'string') {
				context = $(context);
			}
			var modal = context.parents('.modal').data('modal');
			if (modal) {
				var manager = $('body').data('modalmanager');
				if (manager && (manager.getOpenModals().indexOf(modal) >= 0)) {
					modal.hide();
				}
			}
		},

		/**
		 * Modals hidden callback
		 * This callback can be used to clean contents added by plug-ins
		 */
		hidden: function(e) {
			var modal = e.target;
			// Call registered cleaning callbacks
			ams.skin.cleanContainer(modal);
			// Check for hidden callbacks defined via data API
			$('[data-ams-hidden-callback]', modal).each(function() {
				var callback = ams.getFunctionByName($(this).data('ams-hidden-callback'));
				if (callback) {
					callback.call(modal, this);
				}
			});
			// Call hidden callbacks registered for this dialog
			var index;
			var callbacks = $('.modal-dialog', modal).data('hide-callbacks');
			if (callbacks) {
				for (index=0; index < callbacks.length; index++) {
					callbacks[index].call(modal);
				}
			}
			// Call globally registered hidden callbacks
			callbacks = ams.dialog._hide_callbacks;
			if (callbacks) {
				for (index=0; index < callbacks.length; index++) {
					callbacks[index].call(modal);
				}
			}
		}
	};


	/**
	 * Plug-ins helpers functions
	 *
	 * These helpers functions are used by several JQuery plug-in extensions.
	 * They have been extracted from these extensions management code to reuse them more easily into
	 * application specific callbacks.
	 */
	MyAMS.helpers = {

		/** Clear Select2 slection */
		select2ClearSelection: function() {
			var source = $(this);
			var label = source.parents('label');
			var target = source.data('ams-select2-target');
			$('[name="' + target + '"]', label).data('select2').val('');
		},

		/** Select2 selection formatter */
		select2FormatSelection: function(object, container) {
			if (object instanceof Array) {
				$(object).each(function() {
					if (typeof(this) === 'object') {
						container.append(this.text);
					} else {
						container.append(this);
					}
				});
			} else {
				if (typeof(object) === 'object') {
					container.append(object.text);
				} else {
					container.append(object);
				}
			}
		},

		/** Select2 query results callback */
		select2QueryUrlResultsCallback: function(data, page, context) {
			switch (data.status) {
				case 'error':
					ams.skin.messageBox('error', {
						title: ams.i18n.ERROR_OCCURED,
						content: '<h4>' + data.error_message + '</h4>',
						icon: "fa fa-warning animated shake",
						timeout: 10000
					});
					break;
				case 'modal':
					$(this).data('select2').dropdown.hide();
					ams.dialog.open(data.location);
					break;
				default:
					return {
						results: data.results || data,
						more: data.has_more || false,
						context: data.context
					};
			}
		},

		/** Select2 JSON-RPC success callback */
		select2QueryMethodSuccessCallback: function(data, status, options) {
			var result = data.result;
			if (typeof(result) === 'string') {
				try {
					result = JSON.parse(result);
				} catch (e) {}
			}
			switch (result.status) {
				case 'error':
					ams.skin.messageBox('error', {
						title: ams.i18n.ERROR_OCCURED,
						content: '<h4>' + result.error_message + '</h4>',
						icon: "fa fa-warning animated shake",
						timeout: 10000
					});
					break;
				case 'modal':
					$(this).data('select2').dropdown.hide();
					ams.dialog.open(result.location);
					break;
				default:
					options.callback({
						results: result.results || result,
						more: result.has_more || false,
						context: result.context
					});
			}
		},

		/** Context menu handler */
		contextMenuHandler: function(target, menu) {
			var menuData = menu.data();
			if (menuData.toggle === 'modal') {
				ams.dialog.open(menu);
			} else {
				var href = menu.attr('href') || menuData.amsUrl;
				if (!href || href.startsWith('javascript') || menu.attr('target')) {
					return;
				}
				ams.event.stop();
				var hrefGetter = ams.getFunctionByName(href);
				if (typeof(hrefGetter) === 'function') {
					href = hrefGetter.call(menu, target);
				}
				if (typeof(href) === 'function') {
					// Javascript function call
					href.call(menu, target);
				} else {
					// Standard AJAX or browser URL call
					// Convert %23 chars to #
					href = href.replace(/\%23/, '#');
					target = menu.data('ams-target');
					if (target) {
						ams.form.confirmChangedForm(target, function () {
							ams.skin.loadURL(href, target, menu.data('ams-link-options'), menu.data('ams-link-callback'));
						});
					} else {
						ams.form.confirmChangedForm(function () {
							if (href.startsWith('#')) {
								if (href !== location.hash) {
									if (ams.root.hasClass('mobile-view-activated')) {
										ams.root.removeClass('hidden-menu');
										window.setTimeout(function () {
											window.location.hash = href;
										}, 150);
									} else {
										window.location.hash = href;
									}
								}
							} else {
								window.location = href;
							}
						});
					}
				}
			}
		},

		/** Datetimepicker dialog cleaner callback */
		datetimepickerDialogHiddenCallback: function() {
			$('.datepicker, .timepicker, .datetimepicker', this).datetimepicker('destroy');
		}
	};


	/**
	 * Plug-ins management features
	 *
	 * Only basic JQuery, Bootstrap and MyAMS javascript extensions are typically loaded from main page.
	 * Other JQuery plug-ins may be loaded dynamically.
	 * Several JQuery extension plug-ins are already included and pre-configured by MyAMS. Other external
	 * plug-ins can be defined and loaded dynamically using simple "data" attributes.
	 *
	 * WARNING: any plug-in implicated into a form submit process (like JQuery-form or JQuery-progressbar)
	 * must be loaded in a synchronous way. Otherwise, if you use named buttons to submit your forms,
	 * dynamic hidden input fields created by JQuery-validate plug-in will be removed from the form
	 * before the form is submitted!
	 */
	MyAMS.plugins = {

		/**
		 * Initialize list of content plug-ins
		 */
		init: function(element) {

			// Initialize custom data attributes
			ams.plugins.initData(element);

			// Check for disabled plug-ins
			var disabled = [];
			$('[data-ams-plugins-disabled]', element).each(function() {
				var plugins = $(this).data('ams-plugins-disabled').split(/\s+/);
				for (var index=0; index < plugins.length; index++) {
					disabled.push(plugins[index]);
				}
			});

			// Scan new element for plug-ins
			var plugins = {};
			var name;

			// Inner plug-in register function
			function _registerPlugin(name, new_plugin) {
				if (plugins.hasOwnProperty(name)) {
					var plugin = plugins[name];
					plugin.css = plugin.css || new_plugin.css;
					plugin.callbacks.push({
						callback: new_plugin.callback,
						context: new_plugin.context
					});
					if (new_plugin.register) {
						plugin.register = true;
					}
					if (new_plugin.async === false) {
						plugin.async = false;
					}
				} else {
					plugins[name] = {
						src: new_plugin.src,
						css: new_plugin.css,
						callbacks: [{
							callback: new_plugin.callback,
							context: new_plugin.context
						}],
						register: new_plugin.register,
						async: new_plugin.async
					};
				}
				if (new_plugin.css) {
					ams.getCSS(new_plugin.css, name + '_css');
				}
			}

			$('[data-ams-plugins]', element).each(function() {

				var source = $(this);
				var amsPlugins = source.data('ams-plugins');
				if (typeof(amsPlugins) === 'string') {
					var names = source.data('ams-plugins').split(/\s+/);
					for (var index = 0; index < names.length; index++) {
						name = names[index];
						var newPlugin = {
							src: source.data('ams-plugin-' + name + '-src'),
							css: source.data('ams-plugin-' + name + '-css'),
							callback: source.data('ams-plugin-' + name + '-callback'),
							context: source,
							register: source.data('ams-plugin-' + name + '-register'),
							async: source.data('ams-plugin-' + name + '-async')
						};
						_registerPlugin(name, newPlugin);
					}
				} else {
					for (name in amsPlugins) {
						if (!amsPlugins.hasOwnProperty(name)) {
							continue;
						}
						_registerPlugin(name, amsPlugins[name]);
					}
				}
			});

			// Inner plug-in loader function
			var plugin;

			function _loadPlugin(reload) {
				var index;
				var callbacks = plugin.callbacks,
					callback;
				if (callbacks && callbacks.length) {
					for (index=0; index < callbacks.length; index++) {
						callback = callbacks[index];
						callback.callback = ams.getFunctionByName(callback.callback);
						if (plugin.register !== false) {
							var enabled = ams.plugins.enabled;
							if (enabled.hasOwnProperty(name)) {
								enabled[name].push(callback);
							} else {
								enabled[name] = [callback];
							}
						}
					}
				} else {
					if (plugin.register !== false) {
						ams.plugins.enabled[name] = null;
					}
				}
				// If running in async mode, newly registered plug-ins are run
				// before callback is called so we call plug-in manually
				if ((reload !== true) && callbacks && callbacks.length && (plugin.async !== false)) {
					for (index=0; index < callbacks.length; index++) {
						callback = callbacks[index];
						ams.executeFunctionByName(callback.callback, element, callback.context);
					}
				}
			}

			function _checkPluginContext() {
				// Update context for an already loaded plug-in
				var enabled = ams.plugins.enabled[name];
				// Clean all plug-in contexts
				for (index=0; index < enabled.length; index++) {
					var callback = enabled[index];
					if (callback && callback.context && !ams.isInDOM(callback.context)) {
						enabled[index] = null;
					}
				}
			}

			for (name in plugins) {
				if (!plugins.hasOwnProperty(name)) {
					continue;
				}
				plugin = plugins[name];
				if (ams.plugins.enabled[name] === undefined) {
					ams.getScript(plugin.src, _loadPlugin, {
						async: plugin.async === undefined ? true : plugin.async
					});
				} else {
					_checkPluginContext();
					_loadPlugin(true);
				}
			}

			// Run all enabled plug-ins
			for (var index in ams.plugins.enabled) {
				if (!ams.plugins.enabled.hasOwnProperty(index)) {
					continue;
				}
				if (disabled.indexOf(index) >= 0) {
					continue;
				}
				var callbacks = ams.plugins.enabled[index];
				if (callbacks) {
					switch (typeof(callbacks)) {
						case 'function':
							callbacks(element);
							break;
						default:
							for (var cbIndex = 0; cbIndex < callbacks.length; cbIndex++) {
								var callback = callbacks[cbIndex];
								switch (typeof(callback)) {
									case 'function':
										callback(element);
										break;
									default:
										if (callback && callback.callback) {
											callback.callback(callback.context);
										}
								}
							}
					}
				}
			}
		},

		/**
		 * Data initializer
		 * This plug-in converts a single JSON "data-ams-data" attribute into a set of several equivalent "data-" attributes.
		 * This way of defining data attributes can be used with HTML templates engines which don't allow you
		 * to create dynamic attributes easily.
		 */
		initData: function(element) {
			$('[data-ams-data]', element).each(function() {
				var dataElement = $(this);
				var data = dataElement.data('ams-data');
				if (data) {
					for (var name in data) {
						if (data.hasOwnProperty(name)) {
							var elementData = data[name];
							if (typeof(elementData) !== 'string') {
								elementData = JSON.stringify(elementData);
							}
							dataElement.attr('data-' + name, elementData);
						}
					}
				}
			});
		},

		/**
		 * Register a new plug-in through Javascript instead of HTML data attributes
		 *
		 * @plugin: plugin function caller or object containing plug-in properties
		 * @name: if @plugin is a function, defines plug-in name
		 * @callback: a callback function which can be called after plug-in registry
		 */
		register: function(plugin, name, callback) {
			if (typeof(name) === 'function') {
				callback = name;
				name = null;
			}
			name = name || plugin.name;
			if (ams.plugins.enabled.indexOf(name) >= 0) {
				if (globals.console) {
					globals.console.warn("Plugin " + name + " is already registered!");
				}
				return;
			}
			if (typeof(plugin) === 'object') {
				var src = plugin.src;
				if (src) {
					ams.ajax.check(plugin.callback, src, function(first_load) {
						if (first_load) {
							ams.plugins.enabled[name] = ams.getFunctionByName(plugin.callback);
							if (plugin.css) {
								ams.getCSS(plugin.css, name + '_css');
							}
							if (callback) {
								ams.executeFunctionByName(callback);
							}
						}
					});
				} else {
					ams.plugins.enabled[name] = ams.getFunctionByName(plugin.callback);
					if (plugin.css) {
						ams.getCSS(plugin.css, name + '_css');
					}
					if (callback) {
						ams.executeFunctionByName(callback);
					}
				}
			} else if (typeof(plugin) === 'function') {
				ams.plugins.enabled[name] = plugin;
				if (callback) {
					ams.executeFunctionByName(callback);
				}
			}
		},

		/**
		 * Map of enabled plug-ins
		 * This map can be extended by external plug-ins.
		 *
		 * Standard MyAMS plug-ins management method generally includes:
		 * - applying a class matching plug-in name on a set of HTML entities to apply the plug-in
		 * - defining a set of data-attributes on each of these entities to customize the plug-in
		 * For each standard plug-in, you can also provide an options object (to define plug-in options not handled
		 * by default MyAMS initialization engine) and an initialization callback (to define these options dynamically).
		 * Another callback can also be provided to be called after plug-in initialization.
		 *
		 * You can also register plug-ins using the 'register' function
		 */
		enabled: {

			/**
			 * Label hints
			 */
			hint: function(element) {
				var hints = $('.hint:not(:parents(.nohints))', element);
				if (hints.length > 0) {
					ams.ajax.check($.fn.tipsy,
								   ams.baseURL + 'ext/jquery-tipsy' + ams.devext + '.js',
								   function () {
									   ams.getCSS(ams.baseURL + '../css/ext/jquery-tipsy' + ams.devext + '.css',
												  'jquery-tipsy');
									   hints.each(function () {
										   var hint = $(this);
										   var data = hint.data();
										   var dataOptions = {
											   html: data.amsHintHtml,
											   title: ams.getFunctionByName(data.amsHintTitleGetter) || function () {
												   var hint = $(this);
												   return hint.attr('original-title') ||
														   hint.attr(data.amsHintTitleAttr || 'title') ||
														   (data.amsHintHtml ? hint.html() : hint.text());
											   },
											   opacity: data.amsHintOpacity || 0.95,
											   gravity: data.amsHintGravity || 'sw',
											   offset: data.amsHintOffset || 0
										   };
										   var settings = $.extend({}, dataOptions, data.amsHintOptions);
										   settings = ams.executeFunctionByName(data.amsHintInitCallback, hint, settings) || settings;
										   var plugin = hint.tipsy(settings);
										   ams.executeFunctionByName(data.amsHintAfterInitCallback, hint, plugin, settings);
									   });
								   });
				}
			},

			/**
			 * Context menu plug-in
			 */
			contextMenu: function(element) {
				var menus = $('.context-menu', element);
				if (menus.length > 0) {
					menus.each(function() {
						var menu = $(this);
						var data = menu.data();
						var dataOptions = {
							menuSelector: data.amsContextmenuSelector,
							menuSelected: ams.helpers.contextMenuHandler
						};
						var settings = $.extend({}, dataOptions, data.amsContextmenuOptions);
						settings = ams.executeFunctionByName(data.amsContextmenuInitCallback, menu, settings) || settings;
						var plugin = menu.contextMenu(settings);
						ams.executeFunctionByName(data.amsContextmenuAfterInitCallback, menu, plugin, settings);
					});
				}
			},

			/**
			 * Fieldset legend switcher
			 */
			switcher: function(element) {
				$('LEGEND.switcher', element).each(function() {
					var legend = $(this);
					var fieldset = legend.parent('fieldset');
					var data = legend.data();
					if (!data.amsSwitcher) {
						$('<i class="fa fa-fw"></i>')
							.prependTo($(this))
							.addClass(data.amsSwitcherState === 'open' ?
									  (data.amsSwitcherMinusClass || 'fa-minus') :
									  (data.amsSwitcherPlusClass || 'fa-plus'));
						legend.on('click', function(e) {
							e.preventDefault();
							var veto = {};
							legend.trigger('ams.switcher.before-switch', [legend, veto]);
							if (veto.veto) {
								return;
							}
							if (fieldset.hasClass('switched')) {
								fieldset.removeClass('switched');
								$('.fa', legend).removeClass(data.amsSwitcherPlusClass || 'fa-plus')
												.addClass(data.amsSwitcherMinusClass || 'fa-minus');
								legend.trigger('ams.switcher.opened', [legend]);
								var id = legend.attr('id');
								if (id) {
									$('legend.switcher[data-ams-switcher-sync="'+id+'"]', fieldset).each(function() {
										var switcher = $(this);
										if (switcher.parents('fieldset').hasClass('switched')) {
											switcher.click();
										}
									});
								}
							} else {
								fieldset.addClass('switched');
								$('.fa', legend).removeClass(data.amsSwitcherMinusClass || 'fa-minus')
												.addClass(data.amsSwitcherPlusClass || 'fa-plus');
								legend.trigger('ams.switcher.closed', [legend]);
							}
						});
						if (data.amsSwitcherState !== 'open') {
							fieldset.addClass('switched');
						}
						legend.data('ams-switcher', 'on');
					}
				});
			},

			/**
			 * Fieldset legend checker
			 */
			checker: function(element) {
				$('LEGEND.checker', element).each(function() {
					var legend = $(this);
					var fieldset = legend.parent('fieldset');
					var data = legend.data();
					if (!data.amsChecker) {
						var checker = $('<label class="checkbox"></label>');
						var fieldname = data.amsCheckerFieldname || ('checker_'+ams.generateId());
						var checkboxId = fieldname.replace(/\./, '_');
						var prefix = data.amsCheckerHiddenPrefix;
						var hidden = null;
						var checkedValue = data.amsCheckerHiddenValueOn || 'true';
						var uncheckedValue = data.amsCheckerHiddenValueOff || 'false';
						var marker = data.amsCheckerMarker || false;
						if (prefix) {
							hidden = $('<input type="hidden">').attr('name', prefix + fieldname)
															   .val(data.amsCheckerState === 'on' ? checkedValue : uncheckedValue)
															   .prependTo(legend);
						} else if (marker) {
							$('<input type="hidden">').attr('name', marker)
													  .attr('value', 1)
													  .prependTo(legend);
						}
						var input = $('<input type="checkbox">').attr('name', fieldname)
																.attr('id', checkboxId)
																.data('ams-checker-hidden-input', hidden)
																.data('ams-checker-init', true)
																.val(data.amsCheckerValue || true)
																.attr('checked', data.amsCheckerState === 'on' ? 'checked' : null);
						if (data.amsCheckerReadonly) {
							input.attr('disabled', 'disabled');
						} else {
							input.on('change', function(e) {
								e.preventDefault();
								var veto = {};
								var isChecked = $(this).is(':checked');
								legend.trigger('ams.checker.before-switch', [legend, veto]);
								if (veto.veto) {
									// reset checked status because event is fired after change...
									$(this).prop('checked', !isChecked);
									return;
								}
								ams.executeFunctionByName(data.amsCheckerChangeHandler, legend, isChecked);
								if (!data.amsCheckerCancelDefault) {
									var hidden = input.data('ams-checker-hidden-input');
									if (isChecked) {
										if (data.amsCheckerMode === 'disable') {
											fieldset.removeAttr('disabled');
										} else {
											fieldset.removeClass('switched');
										}
										if (hidden) {
											hidden.val(checkedValue);
										}
										$('[data-required]', fieldset).attr('required', 'required');
										legend.trigger('ams.checker.opened', [legend]);
									} else {
										if (data.amsCheckerMode === 'disable') {
											fieldset.prop('disabled', 'disabled');
										} else {
											fieldset.addClass('switched');
										}
										if (hidden) {
											hidden.val(uncheckedValue);
										}
										$('[data-required]', fieldset).removeAttr('required');
										legend.trigger('ams.checker.closed', [legend]);
									}
								}
							});
						}
						input.appendTo(checker);
						$('>label', legend).attr('for', input.attr('id'));
						checker.append('<i></i>')
							   .prependTo(legend);
						var required = $('[required]', fieldset);
						required.attr('data-required', true);
						if (data.amsCheckerState === 'on') {
							input.attr('checked', true);
						} else {
							if (data.amsCheckerMode === 'disable') {
								fieldset.attr('disabled', 'disabled');
							} else {
								fieldset.addClass('switched');
							}
							required.removeAttr('required');
						}
						legend.data('ams-checker', 'on');
					}
				});
			},

			/**
			 * Sliders
			 */
			slider: function(element) {
				var sliders = $('.slider', element);
				if (sliders.length > 0) {
					ams.ajax.check($.fn.slider,
								   ams.baseURL + 'ext/bootstrap-slider-2.0.0' + ams.devext + '.js',
								   function() {
										sliders.each(function() {
											var slider = $(this);
											var data = slider.data();
											var dataOptions = {};
											var settings = $.extend({}, dataOptions, slider.data.amsSliderOptions);
											settings = ams.executeFunctionByName(data.amsSliderInitCallback, slider, settings) || settings;
											var plugin = slider.slider(settings);
											ams.executeFunctionByName(data.amsSliderAfterInitCallback, slider, plugin, settings);
										});
								   });
				}
			},

			/**
			 * Draggable plug-in
			 */
			draggable: function(element) {
				var draggables = $('.draggable', element);
				if (draggables.length > 0) {
					draggables.each(function() {
						var draggable = $(this);
						var data = draggable.data();
						var dataOptions = {
							containment: data.amsDraggableContainment,
							helper: ams.getFunctionByName(data.amsDraggableHelper) || data.amsDraggableHelper,
							start: ams.getFunctionByName(data.amsDraggableStart),
							stop: ams.getFunctionByName(data.amsDraggableStop)
						};
						var settings = $.extend({}, dataOptions, data.amsDraggableOptions);
						settings = ams.executeFunctionByName(data.amsDraggableInitCallback, draggable, settings) || settings;
						var plugin = draggable.draggable(settings);
						draggable.disableSelection();
						ams.executeFunctionByName(data.amsDraggableAfterInitCallback, draggable, plugin, settings);
					});
				}
			},

			/**
			 * Sortable plug-in
			 */
			sortable: function(element) {
				var sortables = $('.sortable', element);
				if (sortables.length > 0) {
					sortables.each(function() {
						var sortable = $(this);
						var data = sortable.data();
						var dataOptions = {
							items: data.amsSortableItems,
							handle: data.amsSortableHandle,
							connectWith: data.amsSortableConnectwith,
							start: ams.getFunctionByName(data.amsSortableStart),
							over: ams.getFunctionByName(data.amsSortableOver),
							containment: data.amsSortableContainment,
							placeholder: data.amsSortablePlaceholder,
							stop: ams.getFunctionByName(data.amsSortableStop)
						};
						var settings = $.extend({}, dataOptions, data.amsSortableOptions);
						settings = ams.executeFunctionByName(data.amsSortableInitCallback, sortable, settings) || settings;
						var plugin = sortable.sortable(settings);
						sortable.disableSelection();
						ams.executeFunctionByName(data.amsSortableAfterInitCallback, sortable, plugin, settings);
					});
				}
			},

			/**
			 * Resizable plug-in
			 */
			resizable: function(element) {
				var resizables = $('.resizable', element);
				if (resizables.length > 0) {
					resizables.each(function() {
						var resizable = $(this);
						var data = resizable.data();
						var dataOptions = {
							autoHide: data.amsResizableAutohide === false ? true : data.amsResizableAutohide,
							containment: data.amsResizableContainment,
							grid: data.amsResizableGrid,
							handles: data.amsResizableHandles,
							start: ams.getFunctionByName(data.amsResizableStart),
							stop: ams.getFunctionByName(data.amsResizableStop)
						};
						var settings = $.extend({}, dataOptions, data.amsResizableOptions);
						settings = ams.executeFunctionByName(data.amsResizableInitCallback, resizable, settings) || settings;
						var plugin = resizable.resizable(settings);
						resizable.disableSelection();
						ams.executeFunctionByName(data.amsResizableAfterInitCallback, resizable, plugin, settings);
					});
				}
			},

			/**
			 * JQuery typeahead plug-in
			 */
			typeahead: function(element) {
				var typeaheads = $('.typeahead', element);
				if (typeaheads.length > 0) {
					ams.ajax.check($.fn.typeahead,
								   ams.baseURL + 'ext/jquery-typeahead' + ams.devext + '.js',
								   function() {
										typeaheads.each(function() {
											var input = $(this);
											var data = input.data();
											var dataOptions = {};
											var settings = $.extend({}, dataOptions, data.amsTypeaheadOptions);
											settings = ams.executeFunctionByName(data.amsTypeaheadInitCallback, input, settings) || settings;
											var plugin = input.typeahead(settings);
											ams.executeFunctionByName(data.amsTypeaheadAfterInitCallback, input, plugin, settings);
										});
								   });
				}
			},

			/**
			 * Select2 plug-in
			 */
			select2: function(element) {
				var selects = $('.select2', element);
				if (selects.length > 0) {
					ams.ajax.check($.fn.select2,
								   ams.baseURL + 'ext/jquery-select2-3.5.2' + ams.devext + '.js',
								   function() {
										selects.each(function() {
											var select = $(this);
											var data = select.data();
											var dataOptions = {
												placeholder: data.amsSelect2Placeholder,
												multiple: data.amsSelect2Multiple,
												minimumInputLength: data.amsSelect2MinimumInputLength || 0,
												maximumSelectionSize: data.amsSelect2MaximumSelectionSize,
												openOnEnter: data.amsSelect2EnterOpen === undefined ? true : data.amsSelect2EnterOpen,
												allowClear: data.amsSelect2AllowClear === undefined ? true : data.amsSelect2AllowClear,
												width: data.amsSelect2Width || '100%',
												initSelection: ams.getFunctionByName(data.amsSelect2InitSelection),
												formatSelection: data.amsSelect2FormatSelection === undefined ?
																	ams.helpers.select2FormatSelection
																	: ams.getFunctionByName(data.amsSelect2FormatSelection),
												formatResult: ams.getFunctionByName(data.amsSelect2FormatResult),
												formatMatches: data.amsSelect2FormatMatches === undefined ?
																	function(matches) {
																		if (matches === 1) {
																			return ams.i18n.SELECT2_MATCH;
																		} else {
																			return matches + ams.i18n.SELECT2_MATCHES;
																		}
																	}
																	: ams.getFunctionByName(data.amsSelect2FormatMatches),
												formatNoMatches: data.amsSelect2FormatResult === undefined ?
																	function(term) {
																		return ams.i18n.SELECT2_NOMATCHES;
																	}
																	: ams.getFunctionByName(data.amsSelect2FormatResult),
												formatInputTooShort: data.amsSelect2FormatInputTooShort === undefined ?
																	function(input, min) {
																		var n = min - input.length;
																		return ams.i18n.SELECT2_INPUT_TOOSHORT
																						.replace(/\{0\}/, n)
																						.replace(/\{1\}/, n === 1 ? "" : ams.i18n.SELECT2_PLURAL);
																	}
																	: ams.getFunctionByName(data.amsSelect2FormatInputTooShort),
												formatInputTooLong: data.amsSelect2FormatInputTooLong === undefined ?
																	function(input, max) {
																		var n = input.length - max;
																		return ams.i18n.SELECT2_INPUT_TOOLONG
																						.replace(/\{0\}/, n)
																						.replace(/\{1\}/, n === 1 ? "" : ams.i18n.SELECT2_PLURAL);
																	}
																	: ams.getFunctionByName(data.amsSelect2FormatInputTooLong),
												formatSelectionTooBig: data.amsSelect2FormatSelectionTooBig === undefined ?
																	function(limit) {
																		return ams.i18n.SELECT2_SELECTION_TOOBIG
																						.replace(/\{0\}/, limit)
																						.replace(/\{1\}/, limit === 1 ? "" : ams.i18n.SELECT2_PLURAL);
																	}
																	: ams.getFunctionByName(data.amsSelect2FormatSelectionTooBig),
												formatLoadMore: data.amsSelect2FormatLoadMore === undefined ?
																	function (pageNumber) {
																		return ams.i18n.SELECT2_LOADMORE;
																	}
																	: ams.getFunctionByName(data.amsSelect2FormatLoadMore),
												formatSearching: data.amsSelect2FormatSearching === undefined ?
																	function() {
																		return ams.i18n.SELECT2_SEARCHING;
																	}
																	: ams.getFunctionByName(data.amsSelect2FormatSearching),
												separator: data.amsSelect2Separator || ',',
												tokenSeparators: data.amsSelect2TokensSeparators || [','],
												tokenizer: ams.getFunctionByName(data.amsSelect2Tokenizer)
											};

											switch (select.context.type) {
												case 'text':
												case 'hidden':
													if (!dataOptions.initSelection) {
														var valuesData = select.data('ams-select2-values');
														if (valuesData) {
															dataOptions.initSelection = function(element, callback) {
																var data = [];
																$(element.val().split(dataOptions.separator)).each(function() {
																	data.push({id: this,
																			   text: valuesData[this] || this});
																});
																callback(data);
															};
														}
													}
													break;
												default:
													break;
											}

											if (select.attr('readonly')) {
												if (select.attr('type') === 'hidden') {
													dataOptions.query = function () {
														return [];
													};
												}
											} else if (data.amsSelect2Query) {
												// Custom query method
												dataOptions.query = ams.getFunctionByName(data.amsSelect2Query);
												dataOptions.minimumInputLength = data.amsSelect2MinimumInputLength || 1;
											} else if (data.amsSelect2QueryUrl) {
												// AJAX query
												dataOptions.ajax = {
													url: data.amsSelect2QueryUrl,
													quietMillis: data.amsSelect2QuietMillis || 200,
													type: data.amsSelect2QueryType || 'POST',
													dataType: data.amsSelect2QueryDatatype || 'json',
													data: function(term, page, context) {
														var options = {};
														options[data.amsSelect2QueryParamName || 'query'] = term;
														options[data.amsSelect2PageParamName || 'page'] = page;
														options[data.amsSelect2ContextParamName || 'context'] = context;
														return $.extend({}, options, data.amsSelect2QueryOptions);
													},
													results: ams.helpers.select2QueryUrlResultsCallback
												};
												dataOptions.minimumInputLength = data.amsSelect2MinimumInputLength || 1;
											} else if (data.amsSelect2QueryMethod) {
												// JSON-RPC query
												dataOptions.query = function(options) {
													var settings = {
														url: data.amsSelect2MethodTarget || ams.jsonrpc.getAddr(),
														type: data.amsSelect2MethodType || 'POST',
														cache: false,
														method: data.amsSelect2QueryMethod,
														params: data.amsSelect2QueryParams || {},
														success: function(data, status) {
															return ams.helpers.select2QueryMethodSuccessCallback.call(select, data, status, options);
														},
														error: ams.error.show
													};
													settings.params[data.amsSelect2QueryParamName || 'query'] = options.term;
													settings.params[data.amsSelect2PageParamName || 'page'] = options.page;
													settings.params[data.amsSelect2ContextParamName || 'context'] = options.context;
													settings = $.extend({}, settings, data.amsSelect2QueryOptions);
													settings = ams.executeFunctionByName(data.amsSelect2QueryInitCallback, select, settings) || settings;
													ams.ajax.check($.jsonRpc,
																   ams.baseURL + 'ext/jquery-jsonrpc' + ams.devext + '.js',
																   function() {
																		$.jsonRpc(settings);
																   });
												};
												dataOptions.minimumInputLength = data.amsSelect2MinimumInputLength || 1;
											} else if (data.amsSelect2Tags) {
												// Tags mode
												dataOptions.tags = data.amsSelect2Tags;
											} else if (data.amsSelect2Data) {
												// Provided data mode
												dataOptions.data = data.amsSelect2Data;
											}

											if (data.amsSelect2EnableFreeTags) {
												dataOptions.createSearchChoice = function(term) {
													return {id: term,
															text: (data.amsSelect2FreeTagsPrefix || ams.i18n.SELECT2_FREETAG_PREFIX) + term};
												};
											}

											var settings = $.extend({}, dataOptions, data.amsSelect2Options);
											settings = ams.executeFunctionByName(data.amsSelect2InitCallback, select, settings) || settings;
											var plugin = select.select2(settings);
											ams.executeFunctionByName(data.amsSelect2AfterInitCallback, select, plugin, settings);
											if (select.hasClass('ordered')) {
												ams.ajax.check($.fn.select2Sortable,
															   ams.baseURL + 'ext/jquery-select2-sortable' + ams.devext + '.js',
															   function() {
																	select.select2Sortable({
																		bindOrder: 'sortableStop'
																	});
															   });
											}

											select.on('change', function() {
												var validator = $(select.get(0).form).data('validator');
												if (validator !== undefined) {
													$(select).valid();
												}
											});
										});
								   });
				}
			},

			/**
			 * Edit mask plug-in
			 */
			maskedit: function(element) {
				var masks = $('[data-mask]', element);
				if (masks.length > 0) {
					ams.ajax.check($.fn.mask,
								   ams.baseURL + 'ext/jquery-maskedinput-1.4.1' + ams.devext + '.js',
								   function() {
										masks.each(function() {
											var mask = $(this);
											var data = mask.data();
											var dataOptions = {
												placeholder: data.amsMaskeditPlaceholder === undefined ? 'X' : data.amsMaskeditPlaceholder,
												complete: ams.getFunctionByName(data.amsMaskeditComplete)
											};
											var settings = $.extend({}, dataOptions, data.amsMaskeditOptions);
											settings = ams.executeFunctionByName(data.amsMaskeditInitCallback, mask, settings) || settings;
											var plugin = mask.mask(mask.attr('data-mask'), settings);
											ams.executeFunctionByName(data.amsMaskeditAfterInitCallback, mask, plugin, settings);
										});
								   });
				}
			},

			/**
			 * JQuery input-mask plug-in
			 *
			 * Mask value can be set in a "data-input-mask" attribute defined:
			 * - as a simple string containing mask
			 * - as a JSON object defining all mask attributes, for example:
			 *   data-input-mask='{"alias": "integer", "allowPlus": false, "allowMinus": false}'
			 */
			inputmask: function(element) {
				var masks = $('[data-input-mask]', element);
				if (masks.length > 0) {
					ams.ajax.check($.fn.inputmask,
								   ams.baseURL + 'ext/jquery-inputmask-bundle-3.2.8' + ams.devext + '.js',
								   function() {
										masks.each(function() {
											var input = $(this);
											var data = input.data();
											var dataOptions;
											if (typeof(data.inputMask) === 'object') {
												dataOptions = data.inputMask;
											} else {
												dataOptions = {
													mask: data.inputMask.toString()
												};
											}
											var settings = $.extend({}, dataOptions, data.amsInputmaskOptions);
											settings = ams.executeFunctionByName(data.amsInputmaskInitCallback, input, settings) || settings;
											var plugin = input.inputmask(settings);
											ams.executeFunctionByName(data.amsInputmaskAfterInitCallback, input, plugin, settings);
										});
								   });
				}
			},

			/**
			 * JQuery date picker
			 */
			datepicker: function(element) {
				var datepickers = $('.datepicker', element);
				if (datepickers.length > 0) {
					ams.ajax.check($.fn.datetimepicker,
								   ams.baseURL + 'ext/jquery-datetimepicker' + ams.devext + '.js',
								   function(first_load) {
										if (first_load) {
											ams.getCSS(ams.baseURL + '../css/ext/jquery-datetimepicker' + ams.devext + '.css', 'jquery-datetimepicker');
											ams.dialog.registerHideCallback(ams.helpers.datetimepickerDialogHiddenCallback);
										}
										datepickers.each(function() {
											var input = $(this);
											var data = input.data();
											var dataOptions = {
												lang: data.amsDatetimepickerLang || ams.lang,
												format: data.amsDatetimepickerFormat || 'd/m/y',
												datepicker: true,
												dayOfWeekStart: 1,
												timepicker: false
											};
											var settings = $.extend({}, dataOptions, data.amsDatetimepickerOptions);
											settings = ams.executeFunctionByName(data.amsDatetimepickerInitCallback, input, settings) || settings;
											var plugin = input.datetimepicker(settings);
											ams.executeFunctionByName(data.amsDatetimepickerAfterInitCallback, input, plugin, settings);
										});
								   });
				}
			},

			/**
			 * JQuery datetime picker
			 */
			datetimepicker: function(element) {
				var datetimepickers = $('.datetimepicker', element);
				if (datetimepickers.length > 0) {
					ams.ajax.check($.fn.datetimepicker,
								   ams.baseURL + 'ext/jquery-datetimepicker' + ams.devext + '.js',
								   function(first_load) {
										if (first_load) {
											ams.getCSS(ams.baseURL + '../css/ext/jquery-datetimepicker' + ams.devext + '.css', 'jquery-datetimepicker');
											ams.dialog.registerHideCallback(ams.helpers.datetimepickerDialogHiddenCallback);
										}
										datetimepickers.each(function() {
											var input = $(this);
											var data = input.data();
											var dataOptions = {
												lang: data.amsDatetimepickerLang || ams.lang,
												format: data.amsDatetimepickerFormat || 'd/m/y H:i',
												datepicker: true,
												dayOfWeekStart: 1,
												timepicker: true
											};
											var settings = $.extend({}, dataOptions, data.amsDatetimepickerOptions);
											settings = ams.executeFunctionByName(data.amsDatetimepickerInitCallback, input, settings) || settings;
											var plugin = input.datetimepicker(settings);
											ams.executeFunctionByName(data.amsDatetimepickerAfterInitCallback, input, plugin, settings);
										});
								   });
				}
			},

			/**
			 * JQuery time picker
			 */
			timepicker: function(element) {
				var timepickers = $('.timepicker', element);
				if (timepickers.length > 0) {
					ams.ajax.check($.fn.datetimepicker,
								   ams.baseURL + 'ext/jquery-datetimepicker' + ams.devext + '.js',
								   function(first_load) {
										if (first_load) {
											ams.getCSS(ams.baseURL + '../css/ext/jquery-datetimepicker' + ams.devext + '.css', 'jquery-datetimepicker');
											ams.dialog.registerHideCallback(ams.helpers.datetimepickerDialogHiddenCallback);
										}
										timepickers.each(function() {
											var input = $(this);
											var data = input.data();
											var dataOptions = {
												lang: data.amsDatetimepickerLang || ams.lang,
												format: data.amsDatetimepickerFormat || 'H:i',
												datepicker: false,
												timepicker: true
											};
											var settings = $.extend({}, dataOptions, data.amsDatetimepickerOptions);
											settings = ams.executeFunctionByName(data.amsDatetimepickerInitCallback, input, settings) || settings;
											var plugin = input.datetimepicker(settings);
											ams.executeFunctionByName(data.amsDatetimepickerAfterInitCallback, input, plugin, settings);
										});
								   });
				}
			},

			/**
			 * JQuery color picker
			 */
			colorpicker: function(element) {
				var colorpickers = $('.colorpicker', element);
				if (colorpickers.length > 0) {
					ams.ajax.check($.fn.minicolors,
								   ams.baseURL + 'ext/jquery-minicolors' + ams.devext + '.js',
								   function(first_load) {
										if (first_load) {
											ams.getCSS(ams.baseURL + '../css/ext/jquery-minicolors' + ams.devext + '.css', 'jquery-minicolors');
										}
										colorpickers.each(function() {
											var input = $(this);
											var data = input.data();
											var dataOptions = {
												position: data.amsColorpickerPosition || input.closest('label.input').data('ams-colorpicker-position') || 'bottom left'
											};
											var settings = $.extend({}, dataOptions, data.amsColorpickerOptions);
											settings = ams.executeFunctionByName(data.amsColorpickerInitCallback, input, settings) || settings;
											var plugin = input.minicolors(settings);
											ams.executeFunctionByName(data.amsDatetimepickerAfterInitCallback, input, plugin, settings);
										});
								   });
				}
			},

			/**
			 * JQuery validation plug-in
			 */
			validate: function(element) {
				var forms = $('FORM:not([novalidate])', element);
				if (forms.length > 0) {
					ams.ajax.check($.fn.validate,
								   ams.baseURL + 'ext/jquery-validate-1.11.1' + ams.devext + '.js',
								   function(first_load) {
										if (first_load) {
											$.validator.setDefaults({
												highlight: function(element) {
													$(element).closest('.form-group, label:not(:parents(.form-group))').addClass('state-error');
												},
												unhighlight: function(element) {
													$(element).closest('.form-group, label:not(:parents(.form-group))').removeClass('state-error');
												},
												errorElement: 'span',
												errorClass: 'state-error',
												errorPlacement: function(error, element) {
													var label = element.parents('label:first');
													if (label.length) {
														error.insertAfter(label);
													} else {
														error.insertAfter(element);
													}
												}
											});
											if (ams.plugins.i18n) {
												for (var key in ams.plugins.i18n.validate) {
													if (!ams.plugins.i18n.validate.hasOwnProperty(key)) {
														continue;
													}
													var message = ams.plugins.i18n.validate[key];
													if ((typeof(message) === 'string') &&
														(message.indexOf('{0}') > -1)) {
														ams.plugins.i18n.validate[key] = $.validator.format(message);
													}
												}
												$.extend($.validator.messages, ams.plugins.i18n.validate);
											}
										}
										forms.each(function() {
											var form = $(this);
											var data = form.data();
											var dataOptions = {
												ignore: null,
												submitHandler: form.attr('data-async') !== undefined ?
															   data.amsFormSubmitHandler === undefined ?
																	function() {
																		// JQuery-form plug-in must be loaded synchronously!!
																		// Otherwise, hidden input fields created by jquery-validate plug-in
																		// and matching named buttons will be deleted (on first form submit)
																		// before JQuery-form plug-in can get them when submitting the form...
																		$('.state-error', form).removeClass('state-error');
																		ams.ajax.check($.fn.ajaxSubmit,
																					   ams.baseURL + 'ext/jquery-form-3.49' + ams.devext + '.js');
																		return ams.form.submit(form);
																	}
																	: ams.getFunctionByName(data.amsFormSubmitHandler)
															   : undefined,
												invalidHandler: form.attr('data-async') !== undefined ?
																data.amsFormInvalidHandler === undefined ?
																	function(event, validator) {
																		$('.state-error', form).removeClass('state-error');
																		for (var index=0; index < validator.errorList.length; index++) {
																			var error = validator.errorList[index];
																			var tabIndex = $(error.element).parents('.tab-pane').index() + 1;
																			if (tabIndex > 0) {
																				var navTabs = $('.nav-tabs', $(error.element).parents('.tabforms'));
																				$('li:nth-child(' + tabIndex + ')', navTabs)
																						.removeClassPrefix('state-')
																						.addClass('state-error');
																				$('li.state-error:first a', navTabs).click();
																			}
																		}
																	}
																	: ams.getFunctionByName(data.amsFormInvalidHandler)
																: undefined
											};
											$('[data-ams-validate-rules]', form).each(function(index) {
												if (index === 0) {
													dataOptions.rules = {};
												}
												dataOptions.rules[$(this).attr('name')] = $(this).data('ams-validate-rules');
											});
											var settings = $.extend({}, dataOptions, data.amsValidateOptions);
											settings = ams.executeFunctionByName(data.amsValidateInitCallback, form, settings) || settings;
											var plugin = form.validate(settings);
											ams.executeFunctionByName(data.amsValidateAfterInitCallback, form, plugin, settings);
										});
								   });
				}
			},

			/**
			 * JQuery dataTables
			 */
			datatable: function(element) {
				var tables = $('.datatable', element);
				if (tables.length > 0) {
					ams.ajax.check($.fn.dataTable,
								   ams.baseURL + 'ext/jquery-dataTables-1.9.4' + ams.devext + '.js',
								   function(first_load) {
										$(tables).each(function() {
											ams.ajax.check($.fn.dataTableExt.oPagination.bootstrap_full,
														   ams.baseURL + 'myams-dataTables' + ams.devext + '.js');
											var table = $(this);
											var data = table.data();
											var extensions = (data.amsDatatableExtensions || '').split(/\s+/);
											// Check DOM elements
											var sDom = data.amsDatatableSdom ||
												"W" +
												((extensions.indexOf('colreorder') >= 0 ||
												  extensions.indexOf('colreorderwithresize') >= 0) ? 'R' : '') +
												"<'dt-top-row'" +
												(extensions.indexOf('colvis') >= 0 ? 'C' : '') +
												((data.amsDatatablePagination === false ||
												  data.amsDatatablePaginationSize === false) ? '' : 'L') +
												(data.amsDatatableGlobalFilter === false ? '' : 'F') +
												">r<'dt-wrapper't" +
												(extensions.indexOf('scroller') >= 0 ? 'S' : '') +
												"><'dt-row dt-bottom-row'<'row'<'col-sm-6'" +
												(data.amsDatatableInformation === false ? '': 'i') +
												"><'col-sm-6 text-right'p>>";

											var index;
											// Check initial sorting
											var sorting = data.amsDatatableSorting;
											if (typeof(sorting) === 'string') {
												var sortings = sorting.split(';');
												sorting = [];
												for (index=0; index < sortings.length; index++) {
													var colSorting = sortings[index].split(',');
													colSorting[0] = parseInt(colSorting[0]);
													sorting.push(colSorting);
												}
											}
											// Check columns sortings
											var columns = [];
											var column;
											var sortables = $('th', table).listattr('data-ams-datatable-sortable');
											for (index=0; index < sortables.length; index++) {
												var sortable = sortables[index];
												if (sortable !== undefined) {
													column = columns[index] || {};
													column.bSortable = sortable;
													columns[index] = column;
												}
											}
											// Check columns types
											var sortTypes = $('th', table).listattr('data-ams-datatable-stype');
											for (index=0; index < sortTypes.length; index++) {
												var sortType = sortTypes[index];
												if (sortType) {
													column = columns[index] || {};
													column.sType = sortType;
													columns[index] = column;
												}
											}
											// Set options
											var dataOptions = {
												bJQueryUI: false,
												bFilter: data.amsDatatableGlobalFilter !== false || extensions.indexOf('columnfilter') >= 0,
												bPaginate: data.amsDatatablePagination !== false,
												bInfo: data.amsDatatableInfo !== false,
												bSort: data.amsDatatableSort !== false,
												aaSorting: sorting,
												aoColumns: columns.length > 0 ? columns : undefined,
												bDeferRender: true,
												bAutoWidth: false,
												iDisplayLength: data.amsDatatableDisplayLength || 25,
												sPaginationType: data.amsDatatablePaginationType || 'bootstrap_full',
												sDom: sDom,
												oLanguage: ams.plugins.i18n.datatables,
												fnInitComplete: function(oSettings, json) {
													$('.ColVis_Button').addClass('btn btn-default btn-sm')
																	   .html((ams.plugins.i18n.datatables.sColumns || "Columns") +
																			 ' <i class="fa fa-fw fa-caret-down"></i>');
												}
											};
											var settings = $.extend({}, dataOptions, data.amsDatatableOptions);
											if (extensions.length > 0) {
												for (index=0; index < extensions.length; index++) {
													switch (extensions[index]) {
														case 'autofill':
															ams.ajax.check($.fn.dataTable.AutoFill,
																		   ams.baseURL + 'ext/jquery-dataTables-autoFill' + ams.devext + '.js');
															break;
														case 'columnfilter':
															ams.ajax.check($.fn.columnFilter,
																		   ams.baseURL + 'ext/jquery-dataTables-columnFilter' + ams.devext + '.js');
															break;
														case 'colreorder':
															ams.ajax.check($.fn.dataTable.ColReorder,
																		   ams.baseURL + 'ext/jquery-dataTables-colReorder' + ams.devext + '.js');
															break;
														case 'colreorderwithresize':
															ams.ajax.check($.fn.dataTable.ColReorder,
																		   ams.baseURL + 'ext/jquery-dataTables-colReorderWithResize' + ams.devext + '.js');
															break;
														case 'colvis':
															ams.ajax.check($.fn.dataTable.ColVis,
																		   ams.baseURL + 'ext/jquery-dataTables-colVis' + ams.devext + '.js');
															var cvDefault = {
																activate: 'click',
																sAlign: 'right'
															};
															settings.oColVis = $.extend({}, cvDefault, data.amsDatatableColvisOptions);
															break;
														case 'editable':
															ams.ajax.check($.fn.editable,
																		   ams.baseURL + 'ext/jquery-jeditable' + ams.devext + '.js');
															ams.ajax.check($.fn.makeEditable,
																		   ams.baseURL + 'ext/jquery-dataTables-editable' + ams.devext + '.js');
															break;
														case 'fixedcolumns':
															ams.ajax.check($.fn.dataTable.FixedColumns,
																		   ams.baseURL + 'ext/jquery-dataTables-fixedColumns' + ams.devext + '.js');
															break;
														case 'fixedheader':
															ams.ajax.check($.fn.dataTable.FixedHeader,
																		   ams.baseURL + 'ext/jquery-dataTables-fixedHeader' + ams.devext + '.js');
															break;
														case 'keytable':
															ams.ajax.check(window.KeyTable,
																		   ams.baseURL + 'ext/jquery-dataTables-keyTable' + ams.devext + '.js');
															break;
														case 'rowgrouping':
															ams.ajax.check($.fn.rowGrouping,
																		   ams.baseURL + 'ext/jquery-dataTables-rowGrouping' + ams.devext + '.js');
															break;
														case 'rowreordering':
															ams.ajax.check($.fn.rowReordering,
																		   ams.baseURL + 'ext/jquery-dataTables-rowReordering' + ams.devext + '.js');
															break;
														case 'scroller':
															ams.ajax.check($.fn.dataTable.Scroller,
																		   ams.baseURL + 'ext/jquery-dataTables-scroller' + ams.devext + '.js');
															break;
														default:
															break;
													}
												}
											}
											settings = ams.executeFunctionByName(data.amsDatatableInitCallback, table, settings) || settings;
											try {  // Some settings can easily generate DataTables exceptions...
												var plugin = table.dataTable(settings);
												ams.executeFunctionByName(data.amsDatatableAfterInitCallback, table, plugin, settings);
												if (extensions.length > 0) {
													for (index=0; index < extensions.length; index++) {
														switch (extensions[index]) {
															case 'autofill':
																var afSettings = $.extend({}, data.amsDatatableAutofillOptions, settings.autofill);
																afSettings = ams.executeFunctionByName(data.amsDatatableAutofillInitCallback, table, afSettings) || afSettings;
																table.data('ams-autofill', data.amsDatatableAutofillConstructor === undefined ?
																							new $.fn.dataTable.AutoFill(table, afSettings)
																							: ams.executeFunctionByName(data.amsDatatableAutofillConstructor, table, plugin, afSettings));
																break;
															case 'columnfilter':
																var cfDefault = {
																	sPlaceHolder: 'head:after'
																};
																var cfSettings = $.extend({}, cfDefault, data.amsDatatableColumnfilterOptions, settings.columnfilter);
																cfSettings = ams.executeFunctionByName(data.amsDatatableColumnfilterInitCallback, table, cfSettings) || cfSettings;
																table.data('ams-columnfilter', data.amsDatatableColumnfilterConstructor === undefined ?
																							plugin.columnFilter(cfSettings)
																							: ams.executeFunctionByName(data.amsDatatableColumnfilterConstructor, table, plugin, cfSettings));
																break;
															case 'editable':
																var edSettings = $.extend({}, data.amsDatatableEditableOptions, settings.editable);
																edSettings = ams.executeFunctionByName(data.amsDatatableEditableInitCallback, table, edSettings) || edSettings;
																table.data('ams-editable', data.amsDatatableEditableConstructor === undefined ?
																							table.makeEditable(edSettings)
																							: ams.executeFunctionByName(data.amsDatatableEditableConstructor, table, plugin, edSettings));
																break;
															case 'fixedcolumns':
																var fcSettings = $.extend({}, data.amsDatatableFixedcolumnsOptions, settings.fixedcolumns);
																fcSettings = ams.executeFunctionByName(data.amsDatatableFixedcolumnsInitCallback, table, fcSettings) || fcSettings;
																table.data('ams-fixedcolumns', data.amsDatatableFixedcolumnsConstructor === undefined ?
																							new $.fn.dataTable.FixedColumns(table, fcSettings)
																							: ams.executeFunctionByName(data.amsDatatableFixedcolumnsConstructor, table, plugin, fcSettings));
																break;
															case 'fixedheader':
																var fhSettings = $.extend({}, data.amsDatatableFixedheaderOptions, settings.fixedheader);
																fhSettings = ams.executeFunctionByName(data.amsDatatableFixedheadeInitCallback, table, fhSettings) || fhSettings;
																table.data('ams-fixedheader', data.amsDatatableFixedheaderConstructor === undefined ?
																							new $.fn.dataTable.FixedHeader(table, fhSettings)
																							: ams.executeFunctionByName(data.amsDatatableFixedheaderConstructor, table, plugin, fhSettings));
																break;
															case 'keytable':
																var ktDefault = {
																	table: table.get(0),
																	datatable: plugin
																};
																var ktSettings = $.extend({}, ktDefault, data.amsDatatableKeytableOptions, settings.keytable);
																ktSettings = ams.executeFunctionByName(data.amsDatatableKeytableInitCallback, table, ktSettings) || ktSettings;
																table.data('ams-keytable', data.amsDatatableKeytableConstructor === undefined ?
																							new KeyTable(ktSettings)
																							: ams.executeFunctionByName(data.amsDatatableKeytableConstructor, table, plugin, ktSettings));
																break;
															case 'rowgrouping':
																var rgSettings = $.extend({}, data.amsDatatableRowgroupingOptions, settings.rowgrouping);
																rgSettings = ams.executeFunctionByName(data.amsDatatableRowgroupingInitCallback, table, rgSettings) || rgSettings;
																table.data('ams-rowgrouping', data.amsDatatableRowgroupingConstructor === undefined ?
																							table.rowGrouping(rgSettings)
																							: ams.executeFunctionByName(data.amsDatatableRowgroupingConstructor, table, plugin, rgSettings));
																break;
															case 'rowreordering':
																var rrSettings = $.extend({}, data.amsDatatableRowreorderingOptions, settings.rowreordering);
																rrSettings = ams.executeFunctionByName(data.amsDatatableRowreorderingInitCallback, table, rrSettings) || rrSettings;
																table.data('ams-rowreordering', data.amsDatatableRowreorderingConstructor === undefined ?
																							table.rowReordering(rrSettings)
																							: ams.executeFunctionByName(data.amsDatatableRowreorderingConstructor, table, plugin, rrSettings));
																break;
															default:
																break;
														}
													}
												}
												var finalizers = (data.amsDatatableFinalizeCallback || '').split(/\s+/);
												if (finalizers.length > 0) {
													for (index=0; index < finalizers.length; index++) {
														ams.executeFunctionByName(finalizers[index], table, plugin, settings);
													}
												}
											}
											catch (e) {}
										});
								   });
				}
			},

			/**
			 * TableDND plug-in
			 */
			tablednd: function(element) {
				var tables = $('.table-dnd', element);
				if (tables.length > 0) {
					ams.ajax.check($.fn.tableDnD,
								   ams.baseURL + 'ext/jquery-tablednd' + ams.devext + '.js',
								   function(first_load) {
										tables.each(function() {
											var table = $(this);
											var data = table.data();
											if (data.amsTabledndDragHandle) {
												$('tr', table).addClass('no-drag-handle');
											} else {
												$(table).on('mouseover', 'tr', function () {
													$(this.cells[0]).addClass('drag-handle');
												}).on('mouseout', 'tr', function () {
													$(this.cells[0]).removeClass('drag-handle');
												});
											}
											var dataOptions = {
												onDragClass: data.amsTabledndDragClass || 'dragging-row',
												onDragStart: ams.getFunctionByName(data.amsTabledndDragStart),
												dragHandle: data.amsTabledndDragHandle,
												scrollAmount: data.amsTabledndScrollAmount,
												onAllowDrop: data.amsTabledndAllowDrop,
												onDrop: ams.getFunctionByName(data.amsTabledndDrop) || function(dnd_table, row) {
													var target = data.amsTabledndDropTarget;
													if (target) {
														// Disable row click handler
														$(row).data('ams-disabled-handlers', 'click');
														var rows = [];
														$(dnd_table.rows).each(function() {
															var rowId = $(this).data('ams-element-name');
															if (rowId) {
																rows.push(rowId);
															}
														});
														var localTarget = ams.getFunctionByName(target);
														if (typeof(localTarget) === 'function') {
															localTarget.call(table, dnd_table, rows);
														} else {
															ams.ajax.post(target, {names: JSON.stringify(rows)});
														}
														// Restore row click handler
														setTimeout(function() {
															$(row).removeData('ams-disabled-handlers');
														}, 50);
													}
													return false;
												}
											};
											var settings = $.extend({}, dataOptions, data.amsTabledndOptions);
											settings = ams.executeFunctionByName(data.amsTabledndInitCallback, table, settings) || settings;
											var plugin = table.tableDnD(settings);
											ams.executeFunctionByName(data.amsTabledndAfterInitCallback, table, plugin, settings);
										});
								   });
				}
			},

			/**
			 * Image area select plug-in
			 */
			imgareaselect: function(element) {
				var images = $('.imgareaselect', element);
				if (images.length > 0) {
					ams.ajax.check($.fn.imgAreaSelect,
								   ams.baseURL + 'ext/jquery-imgareaselect-0.9.11-rc1' + ams.devext + '.js',
								   function(first_load) {
									   if (first_load) {
										   ams.getCSS(ams.baseURL + '../css/ext/jquery-imgareaselect' + ams.devext + '.css');
									   }
									   images.each(function() {
										   var image = $(this);
										   var data = image.data();
										   var parent = data.amsImgareaselectParent ? image.parents(data.amsImgareaselectParent) : 'body';
										   var dataOptions = {
											   instance: true,
											   handles: true,
											   parent: parent,
											   x1: data.amsImgareaselectX1 || 0,
											   y1: data.amsImgareaselectY1 || 0,
											   x2: data.amsImgareaselectX2 || data.amsImgareaselectImageWidth,
											   y2: data.amsImgareaselectY2 || data.amsImgareaselectImageHeight,
											   imageWidth: data.amsImgareaselectImageWidth,
											   imageHeight: data.amsImgareaselectImageHeight,
											   minWidth: 128,
											   minHeight: 128,
											   aspectRatio: data.amsImgareaselectRatio,
											   onSelectEnd: ams.getFunctionByName(data.amsImgareaselectSelectEnd) || function(img, selection) {
												   var target = data.amsImgareaselectTargetField || 'image_';
												   $('input[name="' + target + 'x1"]', parent).val(selection.x1);
												   $('input[name="' + target + 'y1"]', parent).val(selection.y1);
												   $('input[name="' + target + 'x2"]', parent).val(selection.x2);
												   $('input[name="' + target + 'y2"]', parent).val(selection.y2);
											   }
										   };
										   var settings = $.extend({}, dataOptions, data.amsImgareaselectOptions);
										   settings = ams.executeFunctionByName(data.amsImgareaselectInitCallback, image, settings) || settings;
										   var plugin = image.imgAreaSelect(settings);
										   ams.executeFunctionByName(data.amsImgareaselectAfterInitCallback, image, plugin, settings);
										   // Add update timeout when plug-in is displayed into a modal dialog
										   setTimeout(function() {
											   plugin.update();
										   }, 250);
									   });
								   });
				}
			},

			/**
			 * FancyBox plug-in
			 */
			fancybox: function(element) {
				var fancyboxes = $('.fancybox', element);
				if (fancyboxes.length > 0) {
					ams.ajax.check($.fn.fancybox,
								   ams.baseURL + 'ext/jquery-fancybox-2.1.5' + ams.devext + '.js',
								   function(first_load) {
										if (first_load) {
											ams.getCSS(ams.baseURL + '../css/ext/jquery-fancybox-2.1.5' + ams.devext + '.css');
										}
										fancyboxes.each(function() {
											var fancybox = $(this);
											var data = fancybox.data();
											var helpers = (data.amsFancyboxHelpers || '').split(/\s+/);
											if (helpers.length > 0) {
												for (var index=0; index < helpers.length; index++) {
													var helper = helpers[index];
													switch (helper) {
														case 'buttons':
															ams.ajax.check($.fancybox.helpers.buttons,
																		   ams.baseURL + 'ext/fancybox-helpers/fancybox-buttons' + ams.devext + '.js');
															break;
														case 'thumbs':
															ams.ajax.check($.fancybox.helpers.thumbs,
																		   ams.baseURL + 'ext/fancybox-helpers/fancybox-thumbs' + ams.devext + '.js');
															break;
														case 'media':
															ams.ajax.check($.fancybox.helpers.media,
																		   ams.baseURL + 'ext/fancybox-helpers/fancybox-media' + ams.devext + '.js');
															break;
														default:
															break;
													}
												}
											}
											var dataOptions = {
												type: data.amsFancyboxType,
												padding: data.amsFancyboxPadding || 10,
												margin: data.amsFancyboxMargin || 10,
												beforeLoad: ams.getFunctionByName(data.amsFancyboxBeforeLoad) || function() {
													this.title = ams.executeFunctionByName(data.amsFancyboxTitleGetter, this) || $(this.element).attr('original-title') || $(this.element).attr('title');
												},
												helpers: {
													title: {
														type: 'inside'
													}
												}
											};
											var settings = $.extend({}, dataOptions, data.amsFancyboxOptions);
											settings = ams.executeFunctionByName(data.amsFancyboxInitCallback, fancybox, settings) || settings;
											var plugin = fancybox.fancybox(settings);
											ams.executeFunctionByName(data.amsFancyboxAfterInitCallback, fancybox, plugin, settings);
										});
								   });
				}
			},

			/**
			 * Sparkline graphs
			 */
			graphs: function(element) {
				var graphs = $('.sparkline', element);
				if (graphs.length > 0) {
					ams.ajax.check(ams.graphs,
								   ams.baseURL + 'myams-graphs' + ams.devext + '.js',
								   function() {
										ams.graphs.init(graphs);
								   });
				}
			},

			/**
			 * Custom scrollbars
			 */
			scrollbars: function(element) {
				var scrollbars = $('.scrollbar', element);
				if (scrollbars.length > 0) {
					ams.ajax.check($.event.special.mousewheel,
								   ams.baseURL + 'ext/jquery-mousewheel.min.js',
								   function() {
										ams.ajax.check($.fn.mCustomScrollbar,
													   ams.baseURL + 'ext/jquery-mCustomScrollbar' + ams.devext + '.js',
													   function(first_load) {
															if (first_load) {
																ams.getCSS(ams.baseURL + '../css/ext/jquery-mCustomScrollbar.css',
																		   'jquery-mCustomScrollbar');
															}
															scrollbars.each(function() {
																var scrollbar = $(this);
																var data = scrollbar.data();
																var dataOptions = {
																	theme: data.amsScrollbarTheme || 'light'
																};
																var settings = $.extend({}, dataOptions, data.amsScrollbarOptions);
																settings = ams.executeFunctionByName(data.amsScrollbarInitCallback, scrollbar, settings) || settings;
																var plugin = scrollbar.mCustomScrollbar(settings);
																ams.executeFunctionByName(data.amsScrollbarAfterInitCallback, scrollbar, plugin, settings);
															});
													   });
									});
				}
			}
		}
	};


	/**
	 * Callbacks management features
	 */
	MyAMS.callbacks = {

		/**
		 * Initialize list of callbacks
		 *
		 * Callbacks are initialized each time a page content is loaded and integrated into page's DOM.
		 * Unlike plug-ins, callbacks are called once in current's content context but are not kept into
		 * browser's memory for future use.
		 * Callbacks are defined via several data attributes:
		 * - data-ams-callback: name of function callback
		 * - data-ams-callback-source: source URL of file containing callback's function; can contain variables names
		 *   if enclosed between braces
		 * - data-ams-callback-options: JSON object containing callback options
		 */
		init: function(element) {
			$('[data-ams-callback]', element).each(function() {
				var self = this;
				var data = $(self).data();
				var callback = ams.getFunctionByName(data.amsCallback);
				if (callback === undefined) {
					if (data.amsCallbackSource) {
						ams.getScript(data.amsCallbackSource,
									  function() {
										ams.executeFunctionByName(data.amsCallback, self, data.amsCallbackOptions);
									  });
					} else if (globals.console) {
						globals.console.warn("Undefined callback: " + data.amsCallback);
					}
				} else {
					callback.call(self, data.amsCallbackOptions);
				}
			});
		},

		/**
		 * Standard alert message callback
		 *
		 * An alert is an HTML div included on top of a "parent's" body
		 * Alert options include:
		 * - a status: 'info', 'warning', 'error' or 'success'
		 * - a parent: jQuery selector of parent's element
		 * - a header: alert's title
		 * - a subtitle
		 * - a message body
		 * - a boolean margin marker; if true, a 10 pixels margin will be added to alert's body
		 */
		alert: function(options) {
			var data = $(this).data();
			var settings = $.extend({}, options, data.amsAlertOptions);
			var parent = $(data.amsAlertParent || settings.parent || this);
			var status = data.amsAlertStatus || settings.status || 'info';
			var header = data.amsAlertHeader || settings.header;
			var message = data.amsAlertMessage || settings.message;
			var subtitle = data.amsAlertSubtitle || settings.subtitle;
			var margin = data.amsAlertMargin === undefined ? (settings.margin === undefined ? false : settings.margin) : data.amsAlertMargin;
			ams.skin.alert(parent, status, header, message, subtitle, margin);
		},

		/**
		 * Standard message box callback
		 *
		 * Message boxes are small informations messages displayed on bottom right page's corner
		 * Message box options include:
		 * - data-ams-messagebox-status: determines message box color; given as 'info', 'warning', 'error' or 'success'
		 * - data-ams-messagebox-title: message's title
		 * - data-ams-messagebox-content: message's HTML content
		 * - data-ams-messagebox-icon: if given, CSS class of message's icon
		 * - data-ams-messagebox-number: if given, a small error/message number displayed below message
		 * - data-ams-messagebox-timeout: if given, the message box will be automatically hidden passed this number
		 *   of milliseconds
		 * - data-ams-messagebox-callback: a callback's name, which will be called when message box is closed
		 */
		messageBox: function(options) {
			var data = $(this).data();
			var dataOptions = $.extend({}, options, data.amsMessageboxOptions);
			var settings = $.extend({}, dataOptions, {
				title: data.amsMessageboxTitle || dataOptions.title || '',
				content: data.amsMessageboxContent || dataOptions.content || '',
				icon: data.amsMessageboxIcon || dataOptions.icon,
				number: data.amsMessageboxNumber || dataOptions.number,
				timeout: data.amsMessageboxTimeout || dataOptions.timeout
			});
			var status = data.amsMessageboxStatus || dataOptions.status || 'info';
			var callback = ams.getFunctionByName(data.amsMessageboxCallback || dataOptions.callback);
			ams.skin.messageBox(status, settings, callback);
		},

		/**
		 * Standard small box callback
		 *
		 * Small boxes are notification messages displayed on top right page's corner.
		 * Small box options include:
		 * - data-ams-smallbox-status: determines message box color; given as 'info', 'warning', 'error' or 'success'
		 * - data-ams-smallbox-title: message's title
		 * - data-ams-smallbox-content: message's HTML content
		 * - data-ams-smallbox-icon: if given, CSS class of message's icon
		 * - data-ams-smallbox-icon-small: if given, CSS class of small message's icon
		 * - data-ams-smallbox-timeout: if given, the message box will be automatically hidden passed this number
		 *   of milliseconds
		 * - data-ams-smallbox-callback: a callback's name, which will be called when message box is closed
		 */
		smallBox: function(options) {
			var data = $(this).data();
			var dataOptions = $.extend({}, options, data.amsSmallboxOptions);
			var settings = $.extend({}, dataOptions, {
				title: data.amsSmallboxTitle || dataOptions.title || '',
				content: data.amsSmallboxContent || dataOptions.content || '',
				icon: data.amsSmallboxIcon || dataOptions.icon,
				iconSmall: data.amsSmallboxIconSmall || dataOptions.iconSmall,
				timeout: data.amsSmallboxTimeout || dataOptions.timeout
			});
			var status = data.amsSmallboxStatus || dataOptions.status || 'info';
			var callback = ams.getFunctionByName(data.amsSmallboxCallback || dataOptions.callback);
			ams.skin.smallBox(status, settings, callback);
		}
	};


	/**
	 * Events management
	 */
	MyAMS.events = {

		/**
		 * Initialize events listeners
		 *
		 * "data-ams-events-handlers" is a data attribute containing a JSON object where:
		 *  - each key is an event name
		 *  - value is a callback name.
		 * For example: data-ams-events-handlers='{"change": "MyAPP.events.changeListener"}'
		 */
		init: function(element) {
			$('[data-ams-events-handlers]', element).each(function() {
				var element = $(this);
				var handlers = element.data('ams-events-handlers');
				if (handlers) {
					for (var event in handlers) {
						if (handlers.hasOwnProperty(event)) {
							element.on(event, ams.getFunctionByName(handlers[event]));
						}
					}
				}
			});
		}
	};


	/**
	 * Container management
	 */
	MyAMS.container = {

		/**
		 * Change container elements order
		 *
		 * This is a callback which may be used with TableDnD plug-in which allows you to
		 * change order of table rows.
		 * Rows order is stored in an hidden input which is defined in table's data attribute
		 * called 'data-ams-input-name'
		 */
		changeOrder: function(table, names) {
			var input = $('input[name="' + $(this).data('ams-input-name') + '"]', $(this));
			input.val(names.join(';'));
		},

		/**
		 * Delete an element from a container table
		 *
		 * @param element
		 * @returns {Function}
		 */
		deleteElement: function(element) {
			return function() {
				var link = $(this);
				MyAMS.skin.bigBox({
					title: ams.i18n.WARNING,
					content: '<i class="text-danger fa fa-2x fa-bell shake animated"></i>&nbsp; ' + ams.i18n.DELETE_WARNING,
					buttons: ams.i18n.BTN_OK_CANCEL
				}, function(button) {
					if (button === ams.i18n.BTN_OK) {
						var table = link.parents('table');
						var location = table.data('ams-location') || '';
						var tr = link.parents('tr');
						var deleteTarget = tr.data('ams-delete-target') || table.data('ams-delete-target') || 'delete-element.json';
						var objectName = tr.data('ams-element-name');
						MyAMS.ajax.post(location + '/' + deleteTarget, {'object_name': objectName}, function(result, status) {
							if (result.status === 'success') {
								if (table.hasClass('datatable')) {
									table.dataTable().fnDeleteRow(tr[0]);
								} else {
									tr.remove();
								}
							} else {
								MyAMS.ajax.handleJSON(result);
							}
						});
					}
				});
			};
		}
	};


	/**
	 * Generic skin features
	 */
	MyAMS.skin = {

		/**
		 * Compute navigation page height
		 */
		_setPageHeight: function() {
			var mainHeight = $('#main').height();
			var menuHeight = ams.leftPanel.height();
			var windowHeight = $(window).height() - ams.navbarHeight;
			if (mainHeight > windowHeight) {
				ams.root.css('min-height', mainHeight + ams.navbarHeight);
			} else {
				ams.root.css('min-height', windowHeight);
			}
			ams.leftPanel.css('min-height', windowHeight);
			ams.leftPanel.css('max-height', windowHeight);
		},

		/**
		 * Check width for mobile devices
		 */
		_checkMobileWidth: function() {
			if ($(window).width() < 979) {
				ams.root.addClass('mobile-view-activated');
			} else if (ams.root.hasClass('mobile-view-activated')) {
				ams.root.removeClass('mobile-view-activated');
			}
		},

		/**
		 * Show/hide shortcut buttons
		 */
		_showShortcutButtons: function() {
			ams.shortcuts.animate({
				height: 'show'
			}, 200, 'easeOutCirc');
			ams.root.addClass('shortcut-on');
		},

		_hideShortcutButtons: function() {
			ams.shortcuts.animate({
				height: 'hide'
			}, 300, 'easeOutCirc');
			ams.root.removeClass('shortcut-on');
		},

		/**
		 * Check notification badge
		 */
		checkNotification: function() {
			var badge = $('#activity > .badge');
			if (parseInt(badge.text()) > 0) {
				badge.removeClass("hidden")
					 .addClass("bg-color-red bounceIn animated");
			} else {
				badge.addClass("hidden")
					 .removeClass("bg-color-red bounceIn animated");
			}
		},

		refreshNotificationsPanel: function(e) {
			var button = $(this);
			button.addClass('disabled');
			$('i', button).addClass('fa-spin');
			$('input[name="activity"]:checked', '#user-activity').change();
			$('i', button).removeClass('fa-spin');
			button.removeClass('disabled');
		},

		/**
		 * Initialize desktop and mobile widgets
		 */
		_initDesktopWidgets: function(element) {
			if (ams.enableWidgets) {
				var widgets = $('.ams-widget', element);
				if (widgets.length > 0) {
					ams.ajax.check($.fn.MyAMSWidget,
								   ams.baseURL + 'myams-widgets' + ams.devext + '.js',
								   function () {
									   widgets.each(function () {
										   var widget = $(this);
										   var data = widget.data();
										   var dataOptions = {
											   deleteSettingsKey: '#deletesettingskey-options',
											   deletePositionKey: '#deletepositionkey-options'
										   };
										   var settings = $.extend({}, dataOptions, data.amsWidgetOptions);
										   settings = ams.executeFunctionByName(data.amsWidgetInitcallback, widget, settings) || settings;
										   widget.MyAMSWidget(settings);
									   });
									   globals.MyAMSWidget.initWidgetsGrid($('.ams-widget-grid', element));
								   });
				}
			}
		},

		_initMobileWidgets: function(element) {
			if (ams.enableMobile && ams.enableWidgets) {
				ams.skin._initDesktopWidgets(element);
			}
		},

		/**
		 * Add an alert on top of a container
		 *
		 * @parent: parent container where the alert will be displayed
		 * @status: info, success, warning or danger
		 * @header: alert header
		 * @message: main alert message
		 * @subtitle: optional subtitle
		 * @margin: if true, a margin will be displayed around alert
		 */
		alert: function(parent, status, header, message, subtitle, margin) {
			if (status === 'error') {
				status = 'danger';
			}
			$('.alert-' + status, parent).remove();
			var content = '<div class="' + (margin ? 'margin-10' : '') + ' alert alert-block alert-' + status + ' padding-5 fade in">' +
				'<a class="close" data-dismiss="alert"><i class="fa fa-check"></i></a>' +
				'<h4 class="alert-heading">' +
				'<i class="fa fa-fw fa-warning"></i> ' + header +
				'</h4>' +
				(subtitle ? ('<p>' + subtitle + '</p>') : '');
			if (typeof(message) === 'string') {
				content += '<ul><li>' + message + '</li></ul>';
			} else if (message) {
				content += '<ul>';
				for (var index in message) {
					if (!$.isNumeric(index)) {  // IE check
						continue;
					}
					content += '<li>' + message[index] + '</li>';
				}
				content += '</ul>';
			}
			content += '</div>';
			var alert = $(content).prependTo(parent);
			if (parent.exists) {
				ams.ajax.check($.scrollTo,
							   ams.baseURL + 'ext/jquery-scrollTo.min.js',
							   function() {
								   $.scrollTo(parent, {offset: {top: -50}});
							   });
			}
		},

		/**
		 * Big message box
		 */
		bigBox: function(options, callback) {
			ams.ajax.check(ams.notify,
						   ams.baseURL + 'myams-notify' + ams.devext + '.js',
						   function() {
								ams.notify.messageBox(options, callback);
						   });
		},

		/**
		 * Medium notification message box, displayed on page's bottom right
		 */
		messageBox: function(status, options, callback) {
			if (typeof(status) === 'object') {
				callback = options;
				options = status || {};
				status = 'info';
			}
			ams.ajax.check(ams.notify,
						   ams.baseURL + 'myams-notify' + ams.devext + '.js',
						   function() {
							   switch (status) {
								   case 'error':
								   case 'danger':
									   options.color = '#C46A69';
									   break;
								   case 'warning':
									   options.color = '#C79121';
									   break;
								   case 'success':
									   options.color = '#739E73';
									   break;
								   default:
									   options.color = options.color || '#3276B1';
							   }
							   options.sound = false;
							   ams.notify.bigBox(options, callback);
						   });
		},

		/**
		 * Small notification message box, displayed on page's top right
		 */
		smallBox: function(status, options, callback) {
			if (typeof(status) === 'object') {
				callback = options;
				options = status || {};
				status = 'info';
			}
			ams.ajax.check(ams.notify,
						   ams.baseURL + 'myams-notify' + ams.devext + '.js',
						   function () {
							   switch (status) {
								   case 'error':
								   case 'danger':
									   options.color = '#C46A69';
									   break;
								   case 'warning':
									   options.color = '#C79121';
									   break;
								   case 'success':
									   options.color = '#739E73';
									   break;
								   default:
									   options.color = options.color || '#3276B1';
							   }
							   options.sound = false;
							   ams.notify.smallBox(options, callback);
						   });
		},

		/**
		 * Initialize breadcrumbs based on active menu position
		 */
		_drawBreadCrumb: function() {
			var crumb = $('OL.breadcrumb', '#ribbon');
			$('li', crumb).not('.parent').remove();
			if (!$('li', crumb).exists()) {
				crumb.append($('<li></li>').append($('<a></a>').text(ams.i18n.HOME)
															   .addClass('padding-right-5')
															   .attr('href', $('nav a[href!="#"]:first').attr('href'))));
			}
			$('LI.active >A', 'nav').each(function() {
				var menu = $(this);
				var body = $.trim(menu.clone()
									  .children(".badge")
									  .remove()
									  .end()
									  .text());
				var item = $("<li></li>").append(menu.attr('href').replace(/^#/, '') ?
												 $("<a></a>").html(body).attr('href', menu.attr('href'))
												 : body);
				crumb.append(item);
			});
		},

		/**
		 * Check URL matching current location hash
		 */
		checkURL: function() {

			function updateActiveMenus(menu) {
				$('.active', nav).removeClass('active');
				menu.addClass('open')
					.addClass('active');
				menu.parents('li').addClass('open active')
					.children('ul').addClass('active')
					.show();
				menu.parents('li:first').removeClass('open');
				menu.parents('ul').addClass(menu.attr('href').replace(/^#/, '') ? 'active' : '')
					.show();
			}

			var menu;
			var nav = $('nav');
			var hash = location.hash;
			var url = hash.replace(/^#/, '');
			if (url) {
				var container = $('#content');
				if (!container.exists()) {
					container = $('body');
				}
				menu = $('A[href="' + hash + '"]', nav);
				if (menu.exists()) {
					updateActiveMenus(menu);
				}
				ams.skin.loadURL(url, container, {afterLoadCallback: function() {
					var prefix = $('html head title').data('ams-title-prefix');
					document.title = (prefix ? prefix + ' > ' : '') +
						($('[data-ams-page-title]:first', container).data('ams-page-title') ||
						menu.attr('title') ||
						document.title);
				}});
			} else {
				var activeUrl = $('[data-ams-active-menu]').data('ams-active-menu');
				if (activeUrl) {
					menu = $('A[href="' + activeUrl + '"]', nav);
				} else {
					menu = $('>UL >LI >A[href!="#"]', nav).first();
				}
				if (menu.exists()) {
					updateActiveMenus(menu);
					if (activeUrl) {
						ams.skin._drawBreadCrumb();
					} else {
						window.location.hash = menu.attr('href');
					}
				}
			}
		},

		/**
		 * List of registered 'cleaning' callbacks
		 * These callbacks are called before loading a new URL into a given container
		 * to clean required elements from memory before the DOM elements are removed
		 */
		_clean_callbacks: [],

		/**
		 * Register a callback which should be called before a container is replaced
		 */
		registerCleanCallback: function(callback) {
			var callbacks = ams.skin._clean_callbacks;
			if (callbacks.indexOf(callback) < 0) {
				callbacks.push(callback);
			}
		},

		/**
		 * Remove given callback from registry
		 */
		unregisterCleanCallback: function(callback) {
			var callbacks = ams.skin._clean_callbacks;
			var index = callbacks.indexOf(callback);
			if (index >= 0) {
				callbacks.splice(index, 1);
			}
		},

		/**
		 * Call registered cleaning callbacks on given container
		 */
		cleanContainer: function(container) {
			var callbacks = ams.skin._clean_callbacks;
			for (var index=0; index < callbacks.length; index++) {
				callbacks[index].call(container);
			}
		},

		/**
		 * Load given URL into container
		 */
		loadURL: function(url, container, options, callback) {
			if (url.startsWith('#')) {
				url = url.substr(1);
			}
			if (typeof(options) === 'function') {
				callback = options;
				options = {};
			} else if (options === undefined) {
				options = {};
			}
			container = $(container);
			var defaults = {
				type: 'GET',
				url: url,
				dataType: 'html',
				cache: false,
				beforeSend: function() {
					ams.skin.cleanContainer(container);
					container.html('<h1 class="loading"><i class="fa fa-cog fa-spin"></i> ' + ams.i18n.LOADING + ' </h1>');
					if (container[0] === $('#content')[0]) {
						ams.skin._drawBreadCrumb();
						var prefix = $('html head title').data('ams-title-prefix');
						document.title = (prefix ? prefix + ' > ' : '') + $('.breadcrumb LI:last-child').text();
						$('html, body').animate({scrollTop: 0}, 'fast');
					} else {
						container.animate({scrollTop: 0}, 'fast');
					}
				},
				success: function(data, status, request) {
					if (callback) {
						ams.executeFunctionByName(callback, this, data, status, request, options);
					} else {
						var response = ams.ajax.getResponse(request);
						var dataType = response.contentType;
						var result = response.data;
						$('.loading', container).remove();
						switch (dataType) {
							case 'json':
								ams.ajax.handleJSON(result, container);
								break;
							case 'script':
								break;
							case 'xml':
								break;
							case 'html':
								/* falls through */
							case 'text':
								/* falls through */
							default:
								// Show and init container
								container.parents('.hidden').removeClass('hidden');
								$('.alert', container.parents('.alerts-container')).remove();
								container.css({opacity: '0.0'})
										 .html(data)
										 .removeClass('hidden')
										 .delay(50)
										 .animate({opacity: '1.0'}, 300);
								ams.initContent(container);
								ams.form.setFocus(container);
						}
						if (options && options.afterLoadCallback) {
							ams.executeFunctionByName(options.afterLoadCallback, this);
						}
						ams.stats.logPageview();
					}
				},
				error: function(request, options, error) {
					container.html('<h3 class="error"><i class="fa fa-warning txt-color-orangeDark"></i> ' +
								   ams.i18n.ERROR + error + '</h3>' +
								   request.responseText);
				},
				async: options.async === undefined ? true : options.async
			};
			var settings = $.extend({}, defaults, options);
			$.ajax(settings);
		},

		/**
		 * Change user language
		 */
		setLanguage: function(options) {
			var lang = options.lang;
			var handlerType = options.handler_type || 'json';
			switch (handlerType) {
				case 'json':
					var method = options.method || 'setUserLanguage';
					ams.jsonrpc.post(method, {lang: lang}, function() {
						window.location.reload(true);
					});
					break;
				case 'ajax':
					var href = options.href || 'setUserLanguage';
					ams.ajax.post(href, {lang: lang}, function() {
						window.location.reload(true);
					});
					break;
			}
		},

		/**
		 * Go to logout page
		 */
		logout: function() {
			window.location = ams.loginURL;
		}
	};


	/**
	 * Statistics management
	 */
	MyAMS.stats = {

		/**
		 * Log current or specified page load
		 */
		logPageview: function(url) {
			if (typeof(globals._gaq) === 'undefined') {
				return;
			}
			var location = globals.window.location;
			globals._gaq.push(['_trackPageview', url || location.pathname + location.hash]);
		},

		/**
		 * Send event to Google Analytics platform
		 *
		 * @param category
		 * @param action
		 * @param label
		 */
		logEvent: function(category, action, label) {
			if (typeof(globals._gaq) === 'undefined') {
				return;
			}
			if (typeof(category) === 'object') {
				action = category.action;
				label = category.label;
				category = category.category;
			}
			globals._gaq.push(['_trackEvent', category, action, label]);
		}
	};


	/**
	 * Main page initialization
	 * This code is called only once to register global events and callbacks
	 */
	MyAMS.initPage = function() {

		var body = $('body');

		/* Init main components */
		ams.root = body;
		ams.leftPanel = $('#left-panel');
		ams.shortcuts = $('#shortcut');
		ams.plugins.initData(body);

		// Init main AJAX events
		var xhr = $.ajaxSettings.xhr;
		$.ajaxSetup({
			progress: ams.ajax.progress,
			progressUpload: ams.ajax.progress,
			xhr: function() {
				var request = xhr();
				if (request && (typeof(request.addEventListener) === "function")) {
					var that = this;
					request.addEventListener("progress", function(evt) {
						that.progress(evt);
					}, false);
				}
				return request;
			}
		});
		$(document).ajaxStart(ams.ajax.start);
		$(document).ajaxStop(ams.ajax.stop);
		$(document).ajaxError(ams.error.ajax);

		// Check mobile/desktop
		if (!ams.isMobile) {
			ams.root.addClass('desktop-detected');
			ams.device = 'desktop';
		} else {
			ams.root.addClass('mobile-detected');
			ams.device = 'mobile';
			if (ams.enableFastclick) {
				ams.ajax.check($.fn.noClickDelay,
							   ams.baseURL + '/ext/jquery-smartclick' + ams.devext + '.js',
							   function() {
								   $('NAV UL A').noClickDelay();
								   $('A', '#hide-menu').noClickDelay();
							   });
			}
		}

		// Hide menu button
		$('#hide-menu >:first-child > A').click(function(e) {
			body.toggleClass("hidden-menu");
			e.preventDefault();
		});

		// Switch shortcuts
		$('#show-shortcut').click(function(e) {
			if (ams.shortcuts.is(":visible")) {
				ams.skin._hideShortcutButtons();
			} else {
				ams.skin._showShortcutButtons();
			}
			e.preventDefault();
		});
		ams.shortcuts.click(function(e) {
			ams.skin._hideShortcutButtons();
		});

		$(document).mouseup(function(e) {
			if (!ams.shortcuts.is(e.target) &&
				ams.shortcuts.has(e.target).length === 0) {
				ams.skin._hideShortcutButtons();
			}
		});

		// Show & hide mobile search field
		$('#search-mobile').click(function() {
			ams.root.addClass('search-mobile');
		});

		$('#cancel-search-js').click(function() {
			ams.root.removeClass('search-mobile');
		});

		// Activity badge
		$('#activity').click(function(e) {
			var activity = $(this);
			var dropdown = activity.next('.ajax-dropdown');
			if (!dropdown.is(':visible')) {
				dropdown.css('left', activity.position().left - dropdown.innerWidth() / 2 + activity.innerWidth() / 2)
						.fadeIn(150);
				activity.addClass('active');
			} else {
				dropdown.fadeOut(150);
				activity.removeClass('active');
			}
			e.preventDefault();
		});
		ams.skin.checkNotification();

		$(document).mouseup(function(e) {
			var dropdown = $('.ajax-dropdown');
			if (!dropdown.is(e.target) &&
				dropdown.has(e.target).length === 0) {
				dropdown.fadeOut(150)
						.prev().removeClass("active");
			}
		});

		$('input[name="activity"]').change(function(e) {
			var href = $(this).data('ams-url');
			if (href) {
				e.preventDefault();
				e.stopPropagation();
				var hrefGetter = ams.getFunctionByName(href);
				if (typeof(hrefGetter) === 'function') {
					href = hrefGetter.call(this);
				}
				if (typeof(href) === 'function') {
					// Javascript function call
					href.call(this);
				} else {
					var container = $('.ajax-notifications');
					ams.skin.loadURL(href, container);
				}
			}
		});

		// Logout button
		$('a', '#logout').click(function(e) {
			e.preventDefault();
			e.stopPropagation();
			//get the link
			ams.loginURL = $(this).attr('href');
			// ask verification
			ams.skin.bigBox({
				title : "<i class='fa fa-sign-out txt-color-orangeDark'></i> " + ams.i18n.LOGOUT +
						" <span class='txt-color-orangeDark'><strong>" + $('#show-shortcut').text() + "</strong></span> ?",
				content : ams.i18n.LOGOUT_COMMENT,
				buttons : '['+ams.i18n.BTN_NO+']['+ams.i18n.BTN_YES+']'
			}, function(ButtonPressed) {
				if (ButtonPressed === ams.i18n.BTN_YES) {
					ams.root.addClass('animated fadeOutUp');
					setTimeout(ams.skin.logout, 1000);
				}
			});
		});

		// Initialize left nav
		var nav = $('nav');
		$('UL', nav).myams_menu({
			accordion : nav.data('ams-menu-accordion') !== false,
			speed : ams.menuSpeed
		});

		// Left navigation collapser
		$('.minifyme').click(function(e) {
			$('BODY').toggleClass("minified");
			$(this).effect("highlight", {}, 500);
			e.preventDefault();
		});

		// Reset widgets
		$('#refresh').click(function(e) {
			ams.skin.bigBox({
				title: "<i class='fa fa-refresh' style='color: green'></i> " + ams.i18n.CLEAR_STORAGE_TITLE,
				content: ams.i18n.CLEAR_STORAGE_CONTENT,
				buttons: '['+ams.i18n.BTN_CANCEL+']['+ams.i18n.BTN_OK+']'
			}, function(buttonPressed) {
				if (buttonPressed === ams.i18n.BTN_OK && localStorage) {
					localStorage.clear();
					location.reload();
				}
			});
			e.preventDefault();
		});

		// Check active pop-overs
		body.on('click', function(e) {
			var element = $(this);
			if (!element.is(e.target) &&
				element.has(e.target).length === 0 &&
				$('.popover').has(e.target).length === 0) {
				element.popover('hide');
			}
		});

		// Resize events
		ams.ajax.check($.resize,
					   ams.baseURL + 'ext/jquery-resize' + ams.devext + '.js',
					   function() {
						   $('#main').resize(function() {
							   ams.skin._setPageHeight();
							   ams.skin._checkMobileWidth();
						   });
						   nav.resize(function() {
							   ams.skin._setPageHeight();
						   });
					   });

		// Init AJAX navigation
		if (ams.ajaxNav) {
			$(document).on('click', 'a[href="#"]', function(e) {
				e.preventDefault();
			});
			$(document).on('click', 'a[href!="#"]:not([data-toggle]), [data-ams-url]:not([data-toggle])', function(e) {
				var link = $(e.currentTarget);
				var handlers = link.data('ams-disabled-handlers');
				if ((handlers === true) || (handlers === 'click') || (handlers === 'all')) {
					return;
				}
				var href = link.attr('href') || link.data('ams-url');
				if (!href || href.startsWith('javascript') || link.attr('target') || (link.data('ams-context-menu') === true)) {
					return;
				}
				e.preventDefault();
				e.stopPropagation();
				var hrefGetter = ams.getFunctionByName(href);
				if (typeof(hrefGetter) === 'function') {
					href = hrefGetter.call(link);
				}
				if (typeof(href) === 'function') {
					// Javascript function call
					href.call(link);
				} else {
					// Standard AJAX or browser URL call
					// Convert %23 chars to #
					href = href.replace(/\%23/, '#');
					var target = link.data('ams-target');
					if (target) {
						ams.form.confirmChangedForm(target, function () {
							ams.skin.loadURL(href, target, link.data('ams-link-options'), link.data('ams-link-callback'));
						});
					} else {
						ams.form.confirmChangedForm(function () {
							if (href.startsWith('#')) {
								if (href !== location.hash) {
									if (ams.root.hasClass('mobile-view-activated')) {
										ams.root.removeClass('hidden-menu');
										window.setTimeout(function () {
											window.location.hash = href;
										}, 50);
									} else {
										window.location.hash = href;
									}
								}
							} else {
								window.location = href;
							}
						});
					}
				}
			});
			$(document).on('click', 'a[target="_blank"]', function(e) {
				e.preventDefault();
				var target = $(e.currentTarget);
				window.open(target.attr('href'));
				ams.stats.logEvent(target.data('ams-stats-category') || 'Navigation',
								   target.data('ams-stats-action') || 'External',
								   target.data('ams-stats-label') || target.attr('href'));
			});
			$(document).on('click', 'a[target="_top"]', function(e) {
				e.preventDefault();
				ams.form.confirmChangedForm(function() {
					window.location = $(e.currentTarget).attr('href');
				});
			});

			// Check URL when hash changed
			$(window).on('hashchange', ams.skin.checkURL);
		}

		// Initialize modal dialogs links
		$(document).off('click.modal')
				   .on('click', '[data-toggle="modal"]', function(e) {
			var source = $(this);
			var handlers = source.data('ams-disabled-handlers');
			if ((handlers === true) || (handlers === 'click') || (handlers === 'all')) {
				return;
			}
			if (source.data('ams-context-menu') === true) {
				return;
			}
			if (source.data('ams-stop-propagation') === true) {
				e.stopPropagation();
			}
			e.preventDefault();
			ams.dialog.open(source);
			if (source.parents('#shortcut').exists()) {
				setTimeout(ams.skin._hideShortcutButtons, 300);
			}
		});

		// Initialize form buttons
		$(document).on('click', 'button[type="submit"], button.submit', function() {
			var button = $(this);
			$(button.get(0).form).data('ams-submit-button', button);
		});

		// Cancel clicks on readonly checkbox
		$(document).on('click', 'input[type="checkbox"][readonly]', function() {
			return false;
		});

		// Initialize custom click handlers
		$(document).on('click', '[data-ams-click-handler]', function(e) {
			var source = $(this);
			var handlers = source.data('ams-disabled-handlers');
			if ((handlers === true) || (handlers === 'click') || (handlers === 'all')) {
				return;
			}
			var data = source.data();
			if (data.amsClickHandler) {
				if ((data.amsStopPropagation === true) || (data.amsClickStopPropagation === true)) {
					e.stopPropagation();
				}
				if (data.amsClickKeepDefault !== true) {
					e.preventDefault();
				}
				var callback = ams.getFunctionByName(data.amsClickHandler);
				if (callback !== undefined) {
					callback.call(source, data.amsClickHandlerOptions);
				}
			}
		});

		// Initialize custom change handlers
		$(document).on('change', '[data-ams-change-handler]', function(e) {
			var source = $(this);
			// Disable change handlers for readonly inputs
			// These change handlers are activated by IE!!!
			if (source.prop('readonly')) {
				return;
			}
			var handlers = source.data('ams-disabled-handlers');
			if ((handlers === true) || (handlers === 'change') || (handlers === 'all')) {
				return;
			}
			var data = source.data();
			if (data.amsChangeHandler) {
				if (data.amsChangeKeepDefault !== true) {
					e.preventDefault();
				}
				var callback = ams.getFunctionByName(data.amsChangeHandler);
				if (callback !== undefined) {
					callback.call(source, data.amsChangeHandlerOptions);
				}
			}
		});

		// Notify reset to update Select2 widgets
		$(document).on('reset', 'form', function(e) {
			var form = $(this);
			setTimeout(function() {
				form.find('.select2').trigger('change');
			}, 10);
			ams.form.setFocus(form);
		});

		// Initialize custom reset handlers
		$(document).on('reset', '[data-ams-reset-handler]', function(e) {
			var form = $(this);
			var data = form.data();
			if (data.amsResetHandler) {
				if (data.amsResetKeepDefault !== true) {
					e.preventDefault();
				}
				var callback = ams.getFunctionByName(data.amsResetHandler);
				if (callback !== undefined) {
					callback.call(form, data.amsResetHandlerOptions);
				}
			}
		});

		// Handle update on file upload placeholder
		$(document).on('change', 'input[type="file"]', function(e) {
			e.preventDefault();
			var input = $(this);
			var button = input.parent('.button');
			if (button.exists() && button.parent().hasClass('input-file')) {
				button.next('input[type="text"]').val(input.val());
			}
		});

		// Prevent bootstrap dialog from blocking TinyMCE focus
		$(document).on('focusin', function(e) {
			if ($(e.target).closest('.mce-window').length) {
				e.stopImmediatePropagation();
			}
		});

		// Disable clicks on disabled tabs
		$("a[data-toggle=tab]", ".nav-tabs").on("click", function(e) {
			if ($(this).parent('li').hasClass("disabled")) {
				e.preventDefault();
				return false;
			}
		});

		// Enable tabs dynamic loading
		$(document).on('show.bs.tab', function(e) {
			var link = $(e.target);
			var data = link.data();
			if (data.amsUrl) {
				if (data.amsTabLoaded) {
					return;
				}
				try {
					link.append('<i class="fa fa-spin fa-cog margin-left-5"></i>');
					ams.skin.loadURL(data.amsUrl, link.attr('href'), {afterLoadCallback: function() {
						if (data.amsTabLoadOnce) {
							link.data('ams-tab-loaded', true);
						}
					}});
				}
				finally {
					$('i', link).remove();
				}
			}
		});

		// Check modal form dialogs on close
		$(document).on('hide.bs.modal', function(e) {
			var modal = $(e.target);
			ams.form.confirmChangedForm(modal, function() {
				// Confirm closing if OK
				modal.data('modal').isShown = true;
				return true;
			}, function() {
				// Prevent closing if cancelled
				e.preventDefault();
				return false;
			});
		});

		// Init page content
		ams.initContent(document);
		if (ams.ajaxNav && nav.exists()) {
			ams.skin.checkURL();
		}
		ams.form.setFocus(document);

		// Add unload event listener to check for modified forms
		$(window).on('beforeunload', ams.form.checkBeforeUnload);

	};


	/**
	 * Main content plug-ins initializer
	 * This code is called to initialize plugins, callbacks and events listeners each time an HTML content
	 * is loaded dynamically from remote server.
	 */
	MyAMS.initContent = function(element) {

		// Remove left tips
		$('.tipsy').remove();

		// Activate tooltips and popovers
		$("[rel=tooltip]", element).tooltip();
		$("[rel=popover]", element).popover();

		// Activate popovers with hover states
		$("[rel=popover-hover]", element).popover({
			trigger : "hover"
		});

		// Init registered plug-ins and callbacks
		ams.plugins.init(element);
		ams.callbacks.init(element);
		ams.events.init(element);
		ams.form.init(element);

		// Initialize widgets
		if (ams.device === 'desktop') {
			ams.skin._initDesktopWidgets(element);
		} else {
			ams.skin._initMobileWidgets(element);
		}
		ams.skin._setPageHeight();

	};


	/**
	 * MyAMS locale strings
	 */
	MyAMS.i18n = {

		INFO: "Information",
		WARNING: "!! WARNING !!",
		ERROR: "ERROR: ",

		LOADING: "Loading...",
		PROGRESS: "Processing",

		WAIT: "Please wait!",
		FORM_SUBMITTED: "This form was already submitted...",
		NO_SERVER_RESPONSE: "No response from server!",
		ERROR_OCCURED: "An error occured!",
		ERRORS_OCCURED: "Some errors occured!",

		BAD_LOGIN_TITLE: "Bad login!",
		BAD_LOGIN_MESSAGE: "Your anthentication credentials didn't allow you to open a session; " +
						   "please check your credentials or contact administrator.",

		CONFIRM: "Confirm",
		CONFIRM_REMOVE: "Removing this content can't be undone. Do you confirm?",

		CLEAR_STORAGE_TITLE: "Clear Local Storage",
		CLEAR_STORAGE_CONTENT: "Would you like to RESET all your saved widgets and clear LocalStorage?",

		BTN_OK: "OK",
		BTN_CANCEL: "Cancel",
		BTN_OK_CANCEL: "[OK][Cancel]",
		BTN_YES: "Yes",
		BTN_NO: "No",
		BTN_YES_NO: "[Yes][No]",

		CLIPBOARD_COPY: "Copy to clipboard with Ctrl+C, and Enter",

		FORM_CHANGED_WARNING: "Some changes were not saved. These updates will be lost if you leave this page.",
		DELETE_WARNING: "This change can't be undone. Are you sure that you want to delete this element?",
		NO_UPDATE: "No changes were applied.",
		DATA_UPDATED: "Data successfully updated.",

		HOME: "Home",
		LOGOUT: "Logout?",
		LOGOUT_COMMENT: "You can improve your security further after logging out by closing this opened browser",

		SELECT2_PLURAL: 's',
		SELECT2_MATCH: "One result is available, press enter to select it.",
		SELECT2_MATCHES: " results are available, use up and down arrow keys to navigate.",
		SELECT2_NOMATCHES: "No matches found",
		SELECT2_SEARCHING: "Searching...",
		SELECT2_LOADMORE: "Loading more results...",
		SELECT2_INPUT_TOOSHORT: "Please enter {0} more character{1}",
		SELECT2_INPUT_TOOLONG: "Please delete {0} character{1}",
		SELECT2_SELECTION_TOOBIG: "You can only select {0} item{1}",
		SELECT2_FREETAG_PREFIX: "Free text: ",

		DT_COLUMNS: "Columns"

	};


	$(document).ready(function() {
		$ = jQuery.noConflict();
		var html = $('HTML');
		var lang = html.attr('lang') || html.attr('xml:lang');
		if (lang && !lang.startsWith('en')) {
			MyAMS.lang = lang;
			MyAMS.getScript(MyAMS.baseURL + 'i18n/myams_' + lang.substr(0, 2) + '.js', function () {
				MyAMS.initPage();
			});
		} else {
			MyAMS.initPage();
		}
	});

})(jQuery, this);
