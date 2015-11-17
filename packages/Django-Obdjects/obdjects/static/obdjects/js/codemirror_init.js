/*
 * var editor = CodeMirror.fromTextArea('id_%(name)s', {
    path: "%(media_prefix)sjs/",
    parserfile: "parsedjango.js",
    stylesheet: "%(media_prefix)scss/django.css",
    continuousScanning: 500,
    height: "40.2em",
    tabMode: "shift",
    indentUnit: 4,
    lineNumbers: true
});
*/

django.jQuery (document).ready(function() {
    django.jQuery ('.codemirroreditor').each (function(i,e) {
        console.log (e);
        console.log (django.jQuery (e));
        //var editor1 =
        new CodeMirror.fromTextArea (e, {
            width: "70%",
            height: "200px",
            parserfile: ["parsexml.js", "parsecss.js", "tokenizejavascript.js",
                       "parsejavascript.js", "parsehtmlmixed.js"],
            stylesheet: ["/static/codemirror/codemirror.css"],
                        //"/static/codemirror/xmlcolors.css",
                        //"/static/codemirror/jscolors.css",
                        //"/static/codemirror/csscolors.css"],
            path: "/static/codemirror/",
            content: e.value  // html() // document.getElementById("id_content").value
        })
    });

    django.jQuery ("textarea.codemirroreditor + iframe").css("border", "2px solid rgb(204, 204, 204)");
});