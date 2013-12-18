HTML_FILES := $(wildcard src/*.html)
IMAGES := $(wildcard src/*.png)
CSS_FILES := $(wildcard src/*.css)
JS_FILES := $(wildcard src/*.js)
JS_LIBS := $(wildcard src/lib/*.js)

wt-tools.zip: src/manifest.json $(HTML_FILES) $(IMAGES) $(CSS_FILES) $(JS_FILES) $(JS_LIBS)
	zip wt-tools.zip manifest.json $(HTML_FILES) $(IMAGES) $(CSS_FILES) $(JS_FILES) $(JS_LIBS)