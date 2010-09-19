registry = {
    "pybtex.database.output": {
        "class_name": "Writer", 
        "aliases": {
            "yaml": "bibyaml"
        }, 
        "default_plugin": "bibtex", 
        "filenames": {
            "*.yaml": "bibyaml", 
            "*.bib": "bibtex", 
            "*.bibyaml": "bibyaml", 
            "*.xml": "bibtexml", 
            "*.bibtexml": "bibtexml"
        }, 
        "plugins": [
            "bibtex", 
            "bibtexml", 
            "bibyaml"
        ]
    }, 
    "pybtex.style.formatting": {
        "class_name": "Style", 
        "aliases": {}, 
        "default_plugin": "unsrt", 
        "filenames": {}, 
        "plugins": [
            "unsrt"
        ]
    }, 
    "pybtex.style.labels": {
        "class_name": "LabelStyle", 
        "aliases": {}, 
        "default_plugin": "number", 
        "filenames": {}, 
        "plugins": [
            "number"
        ]
    }, 
    "pybtex.backends": {
        "class_name": "Backend", 
        "aliases": {
            "text": "plaintext"
        }, 
        "default_plugin": "latex", 
        "filenames": {
            "*.html": "html", 
            "*.txt": "plaintext", 
            "*.tex": "latex"
        }, 
        "plugins": [
            "html", 
            "latex", 
            "plaintext"
        ]
    }, 
    "pybtex.database.input": {
        "class_name": "Parser", 
        "aliases": {
            "yaml": "bibyaml"
        }, 
        "default_plugin": "bibtex", 
        "filenames": {
            "*.yaml": "bibyaml", 
            "*.bib": "bibtex", 
            "*.bibyaml": "bibyaml", 
            "*.xml": "bibtexml", 
            "*.bibtexml": "bibtexml"
        }, 
        "plugins": [
            "bibtex", 
            "bibtexml", 
            "bibyaml"
        ]
    }, 
    "pybtex.style.names": {
        "class_name": "NameStyle", 
        "aliases": {
            "last_first": "lastfirst"
        }, 
        "default_plugin": "plain", 
        "filenames": {}, 
        "plugins": [
            "lastfirst", 
            "plain"
        ]
    }
}
