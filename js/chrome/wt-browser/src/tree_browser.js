// Copyright Roland Arsenault

var treeDisplay;


function TreeDisplay(anchorProfile,treeDiv){
	this.treeDiv = treeDiv;
	this.zoom = 1.0;
	
	this.theta = Math.PI*200/180;
	this.thetaOffset = -Math.PI/2;
	this.radius = 1.25;
	this.geometricRatio = .75;
	
	var self = this;
	this.treeDiv.bind('mousewheel',function(e){
		if(e.originalEvent.wheelDelta > 0){
			self.zoom *= 1.1;
		} else {
			self.zoom /= 1.1;
		}
		self.layout();
		
	});
	this.center = new wt.Ahnentafel();
	this.showCount = 3;
	this.prefetchCount = 3;
	
	var ctrlDiv = $(document.createElement( "div" ));
	ctrlDiv.css("position","fixed");
	ctrlDiv.css("top","5%");
	ctrlDiv.css("left","5%");

	var label = $(document.createElement( "span" ));
	label.html("radius");
	ctrlDiv.append(label);
	
	var rad = $(document.createElement( "input" ));
	rad.attr("type","text");
	rad.attr("size","4");
	rad.val(this.radius);
	rad.change(function(){
		self.radius = parseFloat(rad.val());
		self.layout();
	});
	ctrlDiv.append(rad);

	label = $(document.createElement( "span" ));
	label.html("geometric factor");
	ctrlDiv.append(label);
	
	var geo = $(document.createElement( "input" ));
	geo.attr("type","text");
	geo.attr("size","4");
	geo.val(this.geometricRatio);
	geo.change(function(){
		self.geometricRatio = parseFloat(geo.val());
		self.layout();
	});
	ctrlDiv.append(geo);

	label = $(document.createElement( "span" ));
	label.html("angle");
	ctrlDiv.append(label);
	
	var angle = $(document.createElement( "input" ));
	angle.attr("type","text");
	angle.attr("size","4");
	angle.val(this.theta*180/Math.PI);
	angle.change(function(){
		self.theta = parseFloat(angle.val())*Math.PI/180.0;
		self.layout();
	});
	ctrlDiv.append(angle);
	
	$("body").append(ctrlDiv);
	
	this.addProfileDisplayNode(anchorProfile,this.center);
	this.reCenter(this.center);
}

TreeDisplay.prototype.getDiv =  function(aNum){
	var ret = undefined;
	this.treeDiv.find("div.profile").each(function(index){
		$this = $(this);
		thisANum = $this.data("ahnentafel");
		if(thisANum != undefined && thisANum.equals(aNum)){
			ret = $this;
		}
	});
	return ret;
};

TreeDisplay.prototype.getProfile = function(aNum){
	var div = this.getDiv(aNum);
	if(div != undefined)
		return div.data("profile");
};

TreeDisplay.prototype.reCenter = function(center){
	
	var gen1 = this.center.getGen();
	var zoomFactor1 = 1;
	if(gen1>0)
		zoomFactor1 = (1-this.geometricRatio)/(1-Math.pow(this.geometricRatio,gen1));
	
	var gen2 = center.getGen();
	var zoomFactor2 = 1;
	if(gen2>0)
		zoomFactor2 = (1-this.geometricRatio)/(1-Math.pow(this.geometricRatio,gen2));
	
	this.zoom *= zoomFactor1/zoomFactor2;
	
	this.center = center;
	var ancestors = this.center.getAncestors(this.showCount);
	for(var i = 0; i < ancestors.length; i++){
		if(this.getDiv(ancestors[i]) == undefined){
			this.addDiv(ancestors[i]);
		}
	}
	this.load(center);
	this.layout();
};

TreeDisplay.prototype.load = function(aNum,callback){
	var p = this.getProfile(aNum);
	if(p===undefined){
		var a = aNum.getChild();
		if(a.valid()){
			var cp = this.getProfile(a);
			var self = this;
			if(cp != undefined){
				cp.load(function(){
					if(a.getFather().equals(aNum)){
						self.addProfileDisplayNode(cp.Father,aNum);
					} else {
						self.addProfileDisplayNode(cp.Mother,aNum);
					}
					self.load(aNum,callback);
				});
			} else {
				this.load(a,function(){
					self.load(aNum,callback);
				});
			}
		}
	} else {
		if(callback != undefined)
			callback();
		var cgen = this.center.getGen();
		var gen = aNum.getGen();
		if(gen-cgen >= 0 && gen-cgen < this.prefetchCount){
			this.load(aNum.getFather());
			this.load(aNum.getMother());
		}
	}
};

TreeDisplay.prototype.layout = function(){


	var baseOffset = this.treeDiv.offset();
	var baseWidth = this.treeDiv.innerWidth();
	var baseHeight = this.treeDiv.innerHeight();
	
	var centerGen =  this.center.getGen();
	var centerGenSize = this.center.genSize();
	var centerGenPos = this.center.genPosition();

	var cthetaN = this.thetaOffset+ this.theta/2.0-(this.theta*(1-(centerGenPos+0.5)/centerGenSize));
	
	var centerGeoFactor = (1-Math.pow(this.geometricRatio,centerGen))/(1-this.geometricRatio);
	
	var cr = $this.outerWidth()*this.radius*centerGeoFactor*this.zoom;
	
	var centerXOffset = cr*Math.cos(cthetaN);
	var centerYOffset = cr*Math.sin(cthetaN);

	
	var center = {
		left: baseOffset.left+baseWidth/2,
		top: baseOffset.top+baseHeight*.65
	};
	
	var self=this;
	
	$(".profile",this.treeDiv).each(function(index){
		//console.log(index,this);
		var $this = $(this);
		var anum = $this.data("ahnentafel");
		gen = anum.getGen();
		genSize = anum.genSize();
		genPos = anum.genPosition();
		
		var geoFactor = (1-Math.pow(self.geometricRatio,gen))/(1-self.geometricRatio);
		var zoomFactor = 1;
		if (geoFactor>0)
			zoomFactor /= geoFactor;

/*		var zoomFactor = 1;// /(1+Math.abs(gen-centerGen));
		if(gen > 1)
			zoomFactor -= (1-1/gen);
*/		//if(gen == centerGen)
			//zoomFactor /= 1+Math.abs(genPos-centerGenPos);
		
		var thetaN = self.thetaOffset+ self.theta/2.0-(self.theta*(1-(genPos+0.5)/genSize));
		var r = $this.outerWidth()*self.radius*geoFactor*self.zoom;
		
		var xOffset = r*Math.cos(thetaN)-centerXOffset;
		var yOffset = r*Math.sin(thetaN)-centerYOffset;
		
		//var xOffset = self.zoom * $this.outerWidth() * (-.5+1.15*(gen-centerGen));
		//var yOffset = self.zoom * $this.outerHeight() * ((genPos-genSize/2)-(centerGenPos-centerGenSize/2))*1.15;
		//if(gen < centerGen){
		//	xOffset = self.zoom * $this.outerWidth() * (-.5+1.15*(gen-centerGen)*Math.sqrt(zoomFactor));
		//	yOffset = self.zoom * $this.outerHeight()*Math.sqrt(zoomFactor) * ((genPos-genSize/2)-(centerGenPos-centerGenSize/2))*1.15;
		//}
		var startOffset = $this.offsetParent().offset();
		$this.css("transform","scale("+self.zoom*zoomFactor+")");
		$this.stop(true,true);
		$this.animate({
			left: xOffset+(center.left-startOffset.left),
			top: yOffset+(center.top-startOffset.top),
		},{
			complete: function(){
				$(this).fadeIn();
			},
		});
	});
};

TreeDisplay.prototype.addDiv = function(aNum){
	retDiv = $(document.createElement( "div" ));
	this.treeDiv.append(retDiv);
	retDiv.hide();
	retDiv.data("ahnentafel", aNum);
	  
	retDiv.prop("class","profile");
	
	var self = this;
	
	retDiv.click(function(){
		self.reCenter(aNum);
  	});
	return retDiv;
};

TreeDisplay.prototype.addProfileDisplayNode = function (profile,aNum){
	var retDiv = this.getDiv(aNum);
	if (retDiv == undefined){
		retDiv = this.addDiv(aNum);
	} else {
		retDiv.empty();
	}
	if(profile === undefined)
		profile = null;
	retDiv.data("profile",profile);
	  
	var header = $(document.createElement( "div" ));
	header.prop("class","unknown");
	retDiv.append(header);
	
	var nameDisplay = $(document.createElement( "span" ));
	nameDisplay.css("width","90%");
	header.append(nameDisplay);
	  

	if(profile != null){
		profile.load(function(){
			nameDisplay.html(profile.FirstName+" "+profile.LastNameCurrent);
			header.prop("class",profile.Gender);
			retDiv.append('<a href="/wiki/'+profile.Name+'" target="_blank"+>View Profile</a>');
		});
	} else {
		nameDisplay.html("Unknown");
	}
};


function init(){
  wt.init($('#status'));
  wt.onLogin(function(){
    wt.getRootPerson().load(function(){
    	treeDisplay = new TreeDisplay(this,$("#tree-content"));
    });
  });
}
      
$( document ).ready(init);
