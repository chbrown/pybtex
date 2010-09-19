registry = {
    "pybtex.database.output": {
        "class_name": "Writer", 
        "aliases": {
            "bibyaml": "yaml"
        }, 
        "default_plugin": "bibtex", 
        "filenames": {
            "*.yaml": "yaml", 
            "*.bib": "bibtex", 
            "*.bibyaml": "yaml", 
            "*.xml": "bibtexml", 
            "*.bibtexml": "bibtexml"
        }, 
        "plugins": [
            "bibtex", 
            "bibtexml", 
            "yaml"
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
            "bibyaml": "yaml"
        }, 
        "default_plugin": "bibtex", 
        "filenames": {
            "*.yaml": "yaml", 
            "*.bib": "bibtex", 
            "*.bibyaml": "yaml", 
            "*.xml": "bibtexml", 
            "*.bibtexml": "bibtexml"
        }, 
        "plugins": [
            "bibtex", 
            "bibtexml", 
            "yaml"
        ]
    }, 
    "pybtex.style.names": {
        "class_name": "NameStyle", 
        "aliases": {
            "lastfirst": "last_first"
        }, 
        "default_plugin": "plain", 
        "filenames": {}, 
        "plugins": [
            "last_first", 
            "plain"
        ]
    }
}
