HTML_FILES := $(wildcard *.html)
IMAGES := $(wildcard *.png)
CSS_FILES := $(wildcard *.css)
JS_FILES := $(wildcard *.js)
JS_LIBS := $(wildcard lib/*.js)

wt-tools.zip: manifest.json $(HTML_FILES) $(IMAGES) $(CSS_FILES) $(JS_FILES) $(JS_LIBS)
	zip wt-tools.zip manifest.json $(HTML_FILES) $(IMAGES) $(CSS_FILES) $(JS_FILES) $(JS_LIBS)