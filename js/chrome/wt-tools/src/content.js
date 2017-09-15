
tablify = function(value){
  var ret = $('<table>');
  
  for(var i in value){
    var row, data;
    if(typeof value[i] == 'string'){
      row = $("<tr>");
      data = $('<td style="background-color: #E0E0E0">');
      data.html(i);
      row.append(data);
      data = $("<td>");
      data.html(value[i]);
      row.append(data);
      ret.append(row);
    }else{
      for(var j = 0; j < value[i].length; j++){
        row = $("<tr>");
        data = $('<td style="background-color: #E0E0E0">');
        data.html(i);
        row.append(data);
        data = $("<td>");
        if(typeof value[i][j] == "string"){
          data.html(value[i][j]);
        } else {
          data.append(tablify(value[i][j]));
        }
        row.append(data);
        ret.append(row);
      }
    }
  }
  return ret;
};


parseItem = function(element){
  var ret = {};
  var items = element.find("[itemscope]");
  var subitems = items.find("[itemprop]");

  element.find("[itemprop]").not(subitems).each(function(index){
    var $this = $(this);
    var name = $this.attr("itemprop");
    if(ret[name] === undefined)
      ret[name] = [];
    if($this.attr("itemscope") !== undefined){
      ret[name].push(parseItem($this));
    } else {
      if(this.nodeName == "META"){
        ret[name].push($this.attr("content"));
      } else if (this.nodeName == "TIME"){
        ret[name].push($this.attr("datetime"));
      } else if (this.nodeName == "A" || this.nodeName == "LINK"){
        ret[name].push($this.attr("href"));
      } else{
        ret[name].push($this.html());
      }
    }
  });
  return ret;
};


scan = function(){
  var $person = $("html[itemscope][itemtype='http://schema.org/Person']");
  if($person.length){
    var data = parseItem($person);
    if(data.url == undefined){
    	data.id = urlToId(document.baseURI);
    } else {
        data.id = urlToId(data.url[0]);
    }
    return {person:data};
  }
};

urlToId = function(url){
  var parts = url.split('/');
  return parts[parts.length-1];
};

lint = function(data){
  var ret = $('<span>');
  var ok = true;

  var age;
  var status = 'error';
  var birth;
  var death;
  if(data.person.birthDate !== undefined){
    birth = new Date(data.person.birthDate[0]);
    death = new Date();
    if(data.person.deathDate !== undefined){
      death = new Date(data.person.deathDate[0]);
    }
    age = death - birth;
    age /= 3600000;
    age /= 24;
    age = Math.floor(age/365.25);
    if(age >= 0){
      if(age < 100){
        status = 'ok';
      } else if (age < 115) {
        status = 'warning';
      }
    }
  }
  if(status != 'ok')
    ok = false;
  ret.append($('<span class="wt-tools-'+status+'">age: '+age+'</span>'));

  var i;
  if(data.person.marriage !== undefined){
    for(i = 0; i < data.person.marriage.length; i++){
      status = "warning";
      var marriageAge;
      var marriageDate;
      if(data.person.marriage[i].startDate !== undefined){
        marriageDate = new Date(data.person.marriage[i].startDate[0]);
        if(birth !== undefined){
          marriageAge = marriageDate - birth;
          marriageAge /= 3600000;
          marriageAge /= 24;
          marriageAge = Math.floor(marriageAge/365.25);
          if(marriageAge < 0)
            status = "error";
          if(marriageAge >= 14)
            status = "ok";
        }
        if(death !== undefined && marriageDate > death)
          status = "error";
      }
      var md = marriageDate;
      if(md !== undefined){
        md = new Date(md.getTimezoneOffset()*60000+md.getTime());
        md = md.toDateString();
      }
      if(status != 'ok')
        ok = false;
      ret.append($('<span class="wt-tools-'+status+'">marriage date: '+md+' age: '+marriageAge+'</span>'));
    }
  }

  if(data.person.gender=="unknown"){
    ret.append($('<span class="wt-tools-warning">gender unknown</span>'));
    ok = false;
  }

  if((birth || death) && data.person.parent !== undefined){
    for(i = 0; i < data.person.parent.length; i++){
      chrome.runtime.sendMessage({command:'get', id:urlToId(data.person.parent[i].url[0])}, function(response) {
        var person = response.person;
        if(person){
          var parent = 'parent';
          if (person.gender[0] == 'male')
            parent = 'father';
          else if (person.gender[0] == 'female')
            parent = 'mother';
          var parentAge;
          var parentBirthDate;
          if(person.birthDate[0] !== undefined){
            parentBirthDate = new Date(person.birthDate[0]);
            if(parentBirthDate !== undefined){
              var status = "ok";
              parentAge = birth - parentBirthDate;
              parentAge /= 3600000;
              parentAge /= 24;
              parentAge = Math.floor(parentAge/365.25);
              if(parentAge < 12)
                status = "error";
              else if(parentAge <= 14 || parentAge > 60)
                status = "warning";
              ret.append($('<span class="wt-tools-'+status+'">'+parent+"'"+'s age at birth: '+parentAge+'</span>'));
            }
          }
        } else {
          ret.append($('<span class="wt-tools-warning">parent '+response.id+' not loaded</span>'));
        }
      });
    }
  }
  return {ok:ok, span:ret};
};

upgradePopups = function(){
	console.log($('a[href][title]'));
};

main = function(){
	upgradePopups();
	
  var data = scan();
  if(data !== undefined){
    chrome.runtime.sendMessage({command:'add', person:data.person}, function(response) {});

    var results = lint(data);
    var $status = $("<div>");
    $status.addClass("wt-tools");
    $status.append("WikiTree Tools:");
    $status.append(results.span);

    var dataDiv = $('<div style="display: none">');
    dataDiv.append(tablify(data.person));

    var $button = $('<button type="button" style="float: right; font-size: .85em; padding: 2px 6px;">Hide</button>');
    $button.click(function(){
      $status.hide(500);
      chrome.runtime.sendMessage({command:"showPopup"}, function(response) {});
    });

    $status.append($button);

    var $optionsButton = $('<button type="button" style="float: right; font-size: .85em; padding: 2px 6px;">Options</button>');
    $optionsButton.click(function(){
      chrome.runtime.sendMessage({command:"showOptions"}, function(response) {});
    });

    $status.append($optionsButton);

    var $showDataButton = $('<button type="button" style="float: right; font-size: .85em; padding: 2px 6px;">Show Data</button>');
    $showDataButton.click(function(){
      if($showDataButton.html() == 'Show Data'){
        dataDiv.show(500);
        $showDataButton.html('Hide Data');
      } else {
        dataDiv.hide(500);
        $showDataButton.html('Show Data');
      }
    });

    $status.append($showDataButton);
    $status.append(dataDiv);

    $("body").prepend($status);

    if(!results.ok){
      $status.show(500);
    } else {
      chrome.runtime.sendMessage({command:"showPopup"}, function(response) {});
    }

    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
      if (request == "showStatus"){
        $status.show(500);
        chrome.runtime.sendMessage({command:"hidePopup"}, function(response) {});
      }
      sendResponse();
    });
  }
};

main();
