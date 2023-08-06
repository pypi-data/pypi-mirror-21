/**
 * gettext for Dojo
 * (adopted from 'gettext for jQuery' by Green Tech)
 *
 * Copyright (c) 2008 Sabin Iacob (m0n5t3r) <iacobs@m0n5t3r.info>
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * @license http://www.gnu.org/licenses/gpl.html
 * @project jquery.gettext
 *
 * Usage:
 *
 * This plugin expects its input data to be a JSON object like
 * {"": header, "string": "translation", ...}
 *
 * After getting the server side set up (either as a static file - my choice - or
 * as a web service), the client side is simple:
 *  * add to the head section of the page something like
 *    <link href="path/to/translation.json" lang="ro" rel="gettext"/>
 *  * in your script, use $.gt.gettext(string) or _(string); for plural forms, use
 *    $.gt.ngettext(sg, pl1[, pl2, ...], count) or n_(sg, pl1[, pl2, ...], count)
 *  * to extract strings to a .po file, you can use standard gettext utilities like
 *    xgettext and msgfmt; to generate the JSON, one could use the following Python
 *    snippet, assuming a domain.mo file exists under path/lang/LC_MESSAGES:
 *
 *    import json
 *
 *    def gettext_json(domain, path, lang = [], indent = False):
 *        try:
 *            tr = gettext.translation(domain, path, lang)
 *            return json.dumps(tr._catalog, ensure_ascii = False, indent = indent)
 *        except IOError:
 *            return None
 *
 *    why go through the additional hassle of gettext? well, it's a matter of
 *    preference, the main advantags I see are:
 *     * well known editing tools like KBabel, poEdit, gtranslator, Emacs PO mode,
 *       etc.
 *     * translation memory, fuzzy matches and other features that get really
 *       helpful when your application is big and you have hundreds of strings
 */
define(['dojo/query',
        'dojo/_base/lang',
	'dojo/_base/xhr',
        'dojo/domReady!'
       ],
function(query, lang, xhr) {

    var _messages = {};
    var _lang = 'C';
    var _setLang = function(code) {
        _lang = typeof code == 'string' && code != ' ' ? code : 'C';
    };

    var _pl_re = /^Plural-Forms:\s*nplurals\s*=\s*(\d+);\s*plural\s*=\s*([^a-zA-Z0-9\$]*([a-zA-Z0-9\$]+).+)$/m;
    var _plural = function(n) {return n != 1;};
    var _load = function() {
        query('link[rel=gettext]').forEach(
            function(item) {
	        var lang = item.lang;
	        xhr.get(item.href, function(data) {
	            _messages[lang] = _messages[lang] || {};
		    var messages = data;

                    lang.mixin(_messages[lang], messages);

                    var pl = _pl_re.exec(_messages[lang]['']);
		    if (pl) {
                        var expr = pl[2];
		        var np = pl[1];
		        var v = pl[3];
		        try {
		            eval('var fn = (function(' + v + ') {return ' + expr + ';})');
		            _plural = fn;
			}
                        catch(e) {
		            return;
			}
		    }
                });
            });
        _setLang(query('html').attr('lang'));
    };

    var _gettext = function(msgstr) {

        if (_lang == 'C' || typeof _messages[_lang] == 'undefined') {
            return msgstr;
	}

        var trans = _messages[_lang][msgstr];

        if (typeof trans == 'string') { // regular action
            return trans;
	}
        else if (typeof trans == 'object' && trans.constructor == Array) {
            // the translation contains plural(s), yet gettext was called
            return trans[0];
	}
        return msgstr;
    };

    var _ngettext = function() {
        var argv = Array.apply(null, arguments);
        var cnt = argv[argv.length - 1];
        var sg = argv[0];
        var pls = argv.slice(0, -1);

        var trans = pls;

        if (_lang != 'C' && typeof _messages[_lang] != 'undefined') {
            trans = _messages[_lang][sg];
	}

        if (typeof trans == 'string') {
            // called ngettext, but no plural forms available :-?
            return trans;
	}
        else if (typeof trans == 'object' && trans.constructor == Array) {
            var pl = _plural(cnt);
	    if (typeof pl == 'boolean' && pls.length == 2) {
	        pl = pl ? 1 : 0;
	    }
	    if (typeof pl == 'number' && pl < trans.length) {
	        return trans[pl];
	    }
	}
        return sg;
    };
    if (typeof _ == 'undefined') {
	    window._ = _gettext;
    }
    if (typeof n_ == 'undefined') {
	    window.n_ = _ngettext;
    }

    return { gettext: _gettext,
             ngettext: _ngettext,
             _: _gettext,
             n_: _ngettext};
});

