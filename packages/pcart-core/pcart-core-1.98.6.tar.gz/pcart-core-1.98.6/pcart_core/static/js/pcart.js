window.PCART = {
    'get_cookie': function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    'get_src': function(element) {
        var src = $(element).data('src');
        var src_eval = $(element).data('src-eval');
        if(src_eval) {
            return eval(src_eval);
        } else {
            return src;
        }
    },
    'ajax_load': function(element) {
        $(element).load(window.PCART.get_src(element));
    },
    'init_actions': function() {
        $('.__action--ajax-load').each(function() {
            window.PCART.ajax_load(this);
        });

        $('body').on('click', '.__action--ajax-link', function(event) {
            var src = window.PCART.get_src(this);
            var target = $(this).data('target');
            $(target).load(src);
        });

        $('body').on('click', '.__action--link', function(event) {
            var src = window.PCART.get_src(this);
            window.location = src;
        });

        $('body').on('click', 'form.__action--ajax-submit [type="submit"][data-allow-ajax="true"]', function(event) {
            $('form.__action--ajax-submit [type="submit"][data-allow-ajax="true"]').removeData('append-to-ajax-request');
            $(this).attr('data-append-to-ajax-request', 'true');
        });

        $('body').on('click', 'form.__action--ajax-submit [type="submit"][data-disable-ajax="true"]', function(event) {
            $(this).closest('form.__action--ajax-submit').removeClass('__action--ajax-submit');
        });

        $('body').on('submit', 'form.__action--ajax-submit', function(event) {
            window.PCART.ajax_submit($(this));
            event.preventDefault();
        });

        $('.__action--ajax-load-for-event').each(function() {
            var event = $(this).data('event');
            var target = $(this).data('target');
            $('body').on(event, target, function(_this) {
                return function(event) {
                    window.PCART.ajax_load($(_this));
                }
            }(this));
        });

        $('.__action--subform-onchange-ajax-reload').each(function() {
            $(this).on('change', 'input,select,checkbox', function(_this) {
                return function(event) {
                    var post_data = Array();
                    $(_this).find('input,select,checkbox').each(function() {
                        post_data.push({name: this.name, value: this.value});
                    });

                    var src = window.PCART.get_src(_this);
                    var method = $(_this).data('subform-method');
                    var csrf_token = window.PCART.get_cookie('csrftoken');
                    if(csrf_token) {
                        post_data.push({name: 'csrfmiddlewaretoken', value: csrf_token});
                    }
                    var post_signal = $(_this).data("subform-post-signal");
                    var remove_element_sel = $(_this).data("subform-post-remove-element");

                    window.PCART.ajax_post_data(src, method, post_data, post_signal, remove_element_sel, _this);
                }
            }(this));
        });
    },
    'send_signal': function(signal) {
        // Reload ajax blocks
        $('.__action--ajax-load-for-signal[data-signal="'+signal+'"]').each(function() {
            window.PCART.ajax_load(this);
        });
    },
    'ajax_post_data': function(src, method, post_data, post_signal, remove_element_sel, result_container) {
        $.ajax(
            {
                url: src,
                type: method,
                data: post_data,
                success:function(data, textStatus, jqXHR) {
                    if(remove_element_sel) {
                        $(remove_element_sel).remove();
                    }
                    if(post_signal) {
                        window.PCART.send_signal(post_signal);
                    }

                    if(result_container) {
                        $(result_container).html(data);
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    //if fails
                }
        });
    },
    'ajax_submit': function(form) {
        var post_data = $(form).serializeArray();
        var append_to_ajax = $(form).find('[data-append-to-ajax-request]');
        append_to_ajax.each(function() {
            post_data.push({name: this.name, value: this.value});  // add a button data
        });
        var form_url = $(form).attr("action");
        var method = $(form).attr("method");
        var post_signal = $(form).data("post-signal");
        var remove_element_sel = $(form).data("post-remove-element");
        var result_container = $(form).data("target");
        window.PCART.ajax_post_data(form_url, method, post_data, post_signal, remove_element_sel, result_container);
    },
}

$(document).ready(function() {
    window.PCART.init_actions();
});