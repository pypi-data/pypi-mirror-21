/*!
 * structjsonfield v1.0.0
 * https://github.com/tleguijt/structjsonfield
 *
 * Licensed under BSD License (https://github.com/tleguijt/structjsonfield/blob/master/LICENSE)
 */

(function ( $ ) {
    $.fn.structjson = function( options ) {
    	/**
    	 * Required settings to be able to use this jQuery widget:
    	 * @param {String} target The lookup string for the target where all the data-lines go
    	 * @param {String} template The lookup string for the template to be used for a data-line
    	 * @param {String} addButton The lookup string for the 'add'-button
    	 */
    	var settings = $.extend({
			target: null,
			template: null,
			addButton: null,
        }, options );

    	if (!settings.target || !settings.template || !settings.addButton) {
    		console.error("structjsonfield not configured correctly: make sure you specify the following: 'target', 'template' and 'addButton'");
    		return;
    	}

    	// provide a custom lookup function that checks if the required element exists and if not
    	// outputs an error message and set the _error-flag to true
    	var _error = false;
    	function _lookup(lookupStr) {
    		var elm = $(lookupStr);
    		if (elm.length ===
    		 0) {
    			console.error("structjsonfield could not find element with lookup '" + lookupStr + "'");
    			_error = true;
    		}
    		return elm;
    	}

    	// lookup necessary elements
    	var buttonAdd = _lookup(settings.addButton),
    		target = _lookup(settings.target),
    		template = _lookup(settings.template),
    		input = $(this);

    	// in case of an error; exit
    	if (_error)
    		return;

    	/**
    	 * Update the source input with the new values from the tables
    	 */
    	function updateInput() {
    		lines = []

    		target.children().each(function() {
    			var line = $(this);
    			var lineObj = {};
    			line.find('input, textarea, select').not('[data-storevalue="false"]').each(function() {
    				lineObj[$(this).attr('name')] = $(this).val();
    			});

    			lines.push(lineObj);
    		})

    		input.val(JSON.stringify(lines));
    		input.trigger("change");
    		toggleHeaders();
    	}

    	/**
    	 * Decide if table headers should be shown/hidden based on the content
    	 */
    	function toggleHeaders() {
    		if (target.children().length === 0) {
    			target.siblings('thead').hide();
    		} else {
    			target.siblings('thead').show();
    		}
    	}

    	/**
    	 * Adds a new line to the target-table
    	 * @param {Object} values The values that have to be filled in this line
    	 */
    	function newLine(values) {
    		var line = $(template.html());

    		if (values) {
	    		for (var key in values) {
	    			var value = values[key];
	    			line.find('[name="' + key + '"]').val(value);
	    		}
	    	}
    		return line;
    	}

    	/**
    	 * Commented-out unpack method.
    	 * This can be used to get the data from the source input and
    	 * fill the target-table with it line by line.
    	 * However; this is done in the Django template itself to speed things up.
    	 */
	    // 	function unpack() {
	    // 		lines = JSON.parse(input.val());
	    // 		$.each(lines, function() {
					// target.append(newLine(this));
	    // 		})
	    // 	}
	    //  unpack();

    	buttonAdd.click(function(e) {
	      e.preventDefault();
	      target.append(newLine());
	      toggleHeaders();
	    });

    	/**
    	 * Listen for change-events on the input fields in the target table
    	 * and update the source input accordingly
    	 */
	    target.on('change', 'input, textarea, select', function() {
	    	updateInput();
	    })

	    /**
	     * Handle delete actions
	     */
	    target.on('click', '[data-structjsonfield-action="delete"]', function() {
	    	$(this).parents(".structjsonfield_line").remove();
	    	updateInput();
	    })

    	return this;
    };
}( jQuery ));
