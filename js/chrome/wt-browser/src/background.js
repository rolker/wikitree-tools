chrome.app.runtime.onLaunched.addListener(function() {
  chrome.app.window.create('tree_browser.html', {
    'bounds': {
      'width': 400,
      'height': 500
    }
  });
});
