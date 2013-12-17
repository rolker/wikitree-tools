var people = {};

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    var cmd = request.command;
    if (cmd == 'add'){
      people[request.person.id] = request.person;
    } else if (cmd == 'get') {
      sendResponse({id:request.id,person:people[request.id]});
      return;
    } else if (cmd == "showPopup"){
      chrome.pageAction.show(sender.tab.id);
    } else if (cmd == "hidePopup") {
      chrome.pageAction.hide(sender.tab.id);
    } else if (cmd == "showOptions") {
      chrome.tabs.create({url:'options.html'});
    }
    sendResponse();
  });
