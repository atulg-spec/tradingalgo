(self.webpackChunkpaper_admin=self.webpackChunkpaper_admin||[]).push([[32],{7982:()=>{!function(){var t,i,e,s,o=window.jQuery,c=o(window),n=o(document),a="http://www.w3.org/2000/svg",r="SVGAngle"in window&&((e=document.createElement("div")).innerHTML="<svg/>",i=(e.firstChild&&e.firstChild.namespaceURI)==a,e.innerHTML="",i),p="transition"in(s=document.createElement("div").style)||"WebkitTransition"in s||"MozTransition"in s||"msTransition"in s||"OTransition"in s,l="ontouchstart"in window,h="mousedown"+(l?" touchstart":""),u="mousemove.clockpicker"+(l?" touchmove.clockpicker":""),k="mouseup.clockpicker"+(l?" touchend.clockpicker":""),d=navigator.vibrate?"vibrate":navigator.webkitVibrate?"webkitVibrate":null;function f(t){return document.createElementNS(a,t)}function v(t){return(t<10?"0":"")+t}var m=0;var b=100,g=80,w=13,y=p?350:1,M=['<div class="popover clockpicker-popover">','<div class="arrow"></div>','<div class="popover-title">','<span class="clockpicker-span-hours text-primary"></span>'," : ",'<span class="clockpicker-span-minutes"></span>','<span class="clockpicker-span-am-pm"></span>',"</div>",'<div class="popover-content">','<div class="clockpicker-plate">','<div class="clockpicker-canvas"></div>','<div class="clockpicker-dial clockpicker-hours"></div>','<div class="clockpicker-dial clockpicker-minutes clockpicker-dial-out"></div>',"</div>",'<span class="clockpicker-am-pm-block">',"</span>","</div>","</div>"].join("");function A(i,e){var s,c,a=o(M),p=a.find(".clockpicker-plate"),l=a.find(".clockpicker-hours"),d=a.find(".clockpicker-minutes"),A=a.find(".clockpicker-am-pm-block"),T="INPUT"===i.prop("tagName"),C=T?i:i.find("input"),H=i.find(".input-group-addon"),P=this;if(this.id=(c=++m+"",(s="cp")?s+c:c),this.element=i,this.options=e,this.isAppended=!1,this.isShown=!1,this.currentView="hours",this.isInput=T,this.input=C,this.addon=H,this.popover=a,this.plate=p,this.hoursView=l,this.minutesView=d,this.amPmBlock=A,this.spanHours=a.find(".clockpicker-span-hours"),this.spanMinutes=a.find(".clockpicker-span-minutes"),this.spanAmPm=a.find(".clockpicker-span-am-pm"),this.amOrPm="PM",e.twelvehour){var x=['<div class="clockpicker-am-pm-block">','<button type="button" class="btn btn-sm btn-default clockpicker-button clockpicker-am-button">',"AM</button>",'<button type="button" class="btn btn-sm btn-default clockpicker-button clockpicker-pm-button">',"PM</button>","</div>"].join("");o(x);o('<button type="button" class="btn btn-sm btn-default clockpicker-button am-button">AM</button>').on("click",(function(){P.amOrPm="AM",o(".clockpicker-span-am-pm").empty().append("AM")})).appendTo(this.amPmBlock),o('<button type="button" class="btn btn-sm btn-default clockpicker-button pm-button">PM</button>').on("click",(function(){P.amOrPm="PM",o(".clockpicker-span-am-pm").empty().append("PM")})).appendTo(this.amPmBlock)}e.autoclose||o('<button type="button" class="btn btn-sm btn-default btn-block clockpicker-button">'+e.donetext+"</button>").click(o.proxy(this.done,this)).appendTo(a),"top"!==e.placement&&"bottom"!==e.placement||"top"!==e.align&&"bottom"!==e.align||(e.align="left"),"left"!==e.placement&&"right"!==e.placement||"left"!==e.align&&"right"!==e.align||(e.align="top"),a.addClass(e.placement),a.addClass("clockpicker-align-"+e.align),this.spanHours.click(o.proxy(this.toggleView,this,"hours")),this.spanMinutes.click(o.proxy(this.toggleView,this,"minutes")),C.on("focus.clockpicker click.clockpicker",o.proxy(this.show,this)),H.on("click.clockpicker",o.proxy(this.toggle,this));var S,E,D,I,B=o('<div class="clockpicker-tick"></div>');if(e.twelvehour)for(S=1;S<13;S+=1)E=B.clone(),D=S/6*Math.PI,I=g,E.css("font-size","120%"),E.css({left:b+Math.sin(D)*I-w,top:b-Math.cos(D)*I-w}),E.html(0===S?"00":S),l.append(E),E.on(h,O);else for(S=0;S<24;S+=1){E=B.clone(),D=S/6*Math.PI;var z=S>0&&S<13;I=z?54:g,E.css({left:b+Math.sin(D)*I-w,top:b-Math.cos(D)*I-w}),z&&E.css("font-size","120%"),E.html(0===S?"00":S),l.append(E),E.on(h,O)}for(S=0;S<60;S+=5)E=B.clone(),D=S/30*Math.PI,E.css({left:b+Math.sin(D)*g-w,top:b-Math.cos(D)*g-w}),E.css("font-size","120%"),E.html(v(S)),d.append(E),E.on(h,O);function O(i,s){var o=p.offset(),c=/^touch/.test(i.type),a=o.left+b,l=o.top+b,h=(c?i.originalEvent.touches[0]:i).pageX-a,d=(c?i.originalEvent.touches[0]:i).pageY-l,f=Math.sqrt(h*h+d*d),v=!1;if(!s||!(f<67||f>93)){i.preventDefault();var m=setTimeout((function(){t.addClass("clockpicker-moving")}),200);r&&p.append(P.canvas),P.setHand(h,d,!s,!0),n.off(u).on(u,(function(t){t.preventDefault();var i=/^touch/.test(t.type),e=(i?t.originalEvent.touches[0]:t).pageX-a,s=(i?t.originalEvent.touches[0]:t).pageY-l;(v||e!==h||s!==d)&&(v=!0,P.setHand(e,s,!1,!0))})),n.off(k).on(k,(function(i){n.off(k),i.preventDefault();var o=/^touch/.test(i.type),c=(o?i.originalEvent.changedTouches[0]:i).pageX-a,r=(o?i.originalEvent.changedTouches[0]:i).pageY-l;(s||v)&&c===h&&r===d&&P.setHand(c,r),"hours"===P.currentView?P.toggleView("minutes",y/2):e.autoclose&&(P.minutesView.addClass("clockpicker-dial-out"),setTimeout((function(){P.done()}),y/2)),p.prepend(j),clearTimeout(m),t.removeClass("clockpicker-moving"),n.off(u)}))}}if(p.on(h,(function(t){0===o(t.target).closest(".clockpicker-tick").length&&O(t,!0)})),r){var j=a.find(".clockpicker-canvas"),L=f("svg");L.setAttribute("class","clockpicker-svg"),L.setAttribute("width",200),L.setAttribute("height",200);var U=f("g");U.setAttribute("transform","translate(100,100)");var W=f("circle");W.setAttribute("class","clockpicker-canvas-bearing"),W.setAttribute("cx",0),W.setAttribute("cy",0),W.setAttribute("r",2);var N=f("line");N.setAttribute("x1",0),N.setAttribute("y1",0);var X=f("circle");X.setAttribute("class","clockpicker-canvas-bg"),X.setAttribute("r",w);var Y=f("circle");Y.setAttribute("class","clockpicker-canvas-fg"),Y.setAttribute("r",3.5),U.appendChild(N),U.appendChild(X),U.appendChild(Y),U.appendChild(W),L.appendChild(U),j.append(L),this.hand=N,this.bg=X,this.fg=Y,this.bearing=W,this.g=U,this.canvas=j}V(this.options.init)}function V(t){t&&"function"==typeof t&&t()}A.DEFAULTS={default:"",fromnow:0,placement:"bottom",align:"left",donetext:"完成",autoclose:!1,twelvehour:!1,vibrate:!0},A.prototype.toggle=function(){this[this.isShown?"hide":"show"]()},A.prototype.locate=function(){var t=this.element,i=this.popover,e=t.offset(),s=t.outerWidth(),o=t.outerHeight(),c=this.options.placement,n=this.options.align,a={};switch(i.show(),c){case"bottom":a.top=e.top+o;break;case"right":a.left=e.left+s;break;case"top":a.top=e.top-i.outerHeight();break;case"left":a.left=e.left-i.outerWidth()}switch(n){case"left":a.left=e.left;break;case"right":a.left=e.left+s-i.outerWidth();break;case"top":a.top=e.top;break;case"bottom":a.top=e.top+o-i.outerHeight()}i.css(a)},A.prototype.show=function(i){if(!this.isShown){V(this.options.beforeShow);var e=this;this.isAppended||(t=o(document.body).append(this.popover),c.on("resize.clockpicker"+this.id,(function(){e.isShown&&e.locate()})),this.isAppended=!0);var s=((this.input.prop("value")||this.options.default||"")+"").split(":");if("now"===s[0]){var a=new Date(+new Date+this.options.fromnow);s=[a.getHours(),a.getMinutes()]}this.hours=+s[0]||0,this.minutes=+s[1]||0,this.spanHours.html(v(this.hours)),this.spanMinutes.html(v(this.minutes)),this.toggleView("hours"),this.locate(),this.isShown=!0,n.on("click.clockpicker."+this.id+" focusin.clockpicker."+this.id,(function(t){var i=o(t.target);0===i.closest(e.popover).length&&0===i.closest(e.addon).length&&0===i.closest(e.input).length&&e.hide()})),n.on("keyup.clockpicker."+this.id,(function(t){27===t.keyCode&&e.hide()})),V(this.options.afterShow)}},A.prototype.hide=function(){V(this.options.beforeHide),this.isShown=!1,n.off("click.clockpicker."+this.id+" focusin.clockpicker."+this.id),n.off("keyup.clockpicker."+this.id),this.popover.hide(),V(this.options.afterHide)},A.prototype.toggleView=function(t,i){var e=!1;"minutes"===t&&"visible"===o(this.hoursView).css("visibility")&&(V(this.options.beforeHourSelect),e=!0);var s="hours"===t,c=s?this.hoursView:this.minutesView,n=s?this.minutesView:this.hoursView;this.currentView=t,this.spanHours.toggleClass("text-primary",s),this.spanMinutes.toggleClass("text-primary",!s),n.addClass("clockpicker-dial-out"),c.css("visibility","visible").removeClass("clockpicker-dial-out"),this.resetClock(i),clearTimeout(this.toggleViewTimer),this.toggleViewTimer=setTimeout((function(){n.css("visibility","hidden")}),y),e&&V(this.options.afterHourSelect)},A.prototype.resetClock=function(t){var i=this.currentView,e=this[i],s="hours"===i,o=e*(Math.PI/(s?6:30)),c=s&&e>0&&e<13?54:g,n=Math.sin(o)*c,a=-Math.cos(o)*c,p=this;r&&t?(p.canvas.addClass("clockpicker-canvas-out"),setTimeout((function(){p.canvas.removeClass("clockpicker-canvas-out"),p.setHand(n,a)}),t)):this.setHand(n,a)},A.prototype.setHand=function(t,i,e,s){var c,n=Math.atan2(t,-i),a="hours"===this.currentView,p=Math.PI/(a||e?6:30),l=Math.sqrt(t*t+i*i),h=this.options,u=a&&l<67,k=u?54:g;if(h.twelvehour&&(k=g),n<0&&(n=2*Math.PI+n),n=(c=Math.round(n/p))*p,h.twelvehour?a?0===c&&(c=12):(e&&(c*=5),60===c&&(c=0)):a?(12===c&&(c=0),c=u?0===c?12:c:0===c?0:c+12):(e&&(c*=5),60===c&&(c=0)),this[this.currentView]!==c&&d&&this.options.vibrate&&(this.vibrateTimer||(navigator[d](10),this.vibrateTimer=setTimeout(o.proxy((function(){this.vibrateTimer=null}),this),100))),this[this.currentView]=c,this[a?"spanHours":"spanMinutes"].html(v(c)),r){s||!a&&c%5?(this.g.insertBefore(this.hand,this.bearing),this.g.insertBefore(this.bg,this.fg),this.bg.setAttribute("class","clockpicker-canvas-bg clockpicker-canvas-bg-trans")):(this.g.insertBefore(this.hand,this.bg),this.g.insertBefore(this.fg,this.bg),this.bg.setAttribute("class","clockpicker-canvas-bg"));var f=Math.sin(n)*k,m=-Math.cos(n)*k;this.hand.setAttribute("x2",f),this.hand.setAttribute("y2",m),this.bg.setAttribute("cx",f),this.bg.setAttribute("cy",m),this.fg.setAttribute("cx",f),this.fg.setAttribute("cy",m)}else this[a?"hoursView":"minutesView"].find(".clockpicker-tick").each((function(){var t=o(this);t.toggleClass("active",c===+t.html())}))},A.prototype.done=function(){V(this.options.beforeDone),this.hide();var t=this.input.prop("value"),i=v(this.hours)+":"+v(this.minutes);this.options.twelvehour&&(i+=this.amOrPm),this.input.prop("value",i),i!==t&&(this.input.triggerHandler("change"),this.isInput||this.element.trigger("change")),this.options.autoclose&&this.input.trigger("blur"),V(this.options.afterDone)},A.prototype.remove=function(){this.element.removeData("clockpicker"),this.input.off("focus.clockpicker click.clockpicker"),this.addon.off("click.clockpicker"),this.isShown&&this.hide(),this.isAppended&&(c.off("resize.clockpicker"+this.id),this.popover.remove())},o.fn.clockpicker=function(t){var i=Array.prototype.slice.call(arguments,1);return this.each((function(){var e=o(this),s=e.data("clockpicker");if(s)"function"==typeof s[t]&&s[t].apply(s,i);else{var c=o.extend({},A.DEFAULTS,e.data(),"object"==typeof t&&t);e.data("clockpicker",new A(e,c))}}))}}()}}]);
//# sourceMappingURL=npm.clockpicker.e6384fd063d815c1972e.js.map