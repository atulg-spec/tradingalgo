"use strict";(self.webpackChunkpaper_admin=self.webpackChunkpaper_admin||[]).push([[1],{5526:(t,e,r)=>{r.d(e,{A:()=>W});var n=r(4486);function i(){i=function(){return e};var t,e={},r=Object.prototype,n=r.hasOwnProperty,o=Object.defineProperty||function(t,e,r){t[e]=r.value},a="function"==typeof Symbol?Symbol:{},u=a.iterator||"@@iterator",c=a.asyncIterator||"@@asyncIterator",s=a.toStringTag||"@@toStringTag";function l(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{l({},"")}catch(t){l=function(t,e,r){return t[e]=r}}function f(t,e,r,n){var i=e&&e.prototype instanceof m?e:m,a=Object.create(i.prototype),u=new T(n||[]);return o(a,"_invoke",{value:k(t,r,u)}),a}function d(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(t){return{type:"throw",arg:t}}}e.wrap=f;var h="suspendedStart",p="suspendedYield",v="executing",y="completed",g={};function m(){}function b(){}function w(){}var A={};l(A,u,(function(){return this}));var x=Object.getPrototypeOf,_=x&&x(x(S([])));_&&_!==r&&n.call(_,u)&&(A=_);var E=w.prototype=m.prototype=Object.create(A);function L(t){["next","throw","return"].forEach((function(e){l(t,e,(function(t){return this._invoke(e,t)}))}))}function W(t,e){function r(i,o,a,u){var c=d(t[i],t,o);if("throw"!==c.type){var s=c.arg,l=s.value;return l&&"object"==typeof l&&n.call(l,"__await")?e.resolve(l.__await).then((function(t){r("next",t,a,u)}),(function(t){r("throw",t,a,u)})):e.resolve(l).then((function(t){s.value=t,a(s)}),(function(t){return r("throw",t,a,u)}))}u(c.arg)}var i;o(this,"_invoke",{value:function(t,n){function o(){return new e((function(e,i){r(t,n,e,i)}))}return i=i?i.then(o,o):o()}})}function k(e,r,n){var i=h;return function(o,a){if(i===v)throw new Error("Generator is already running");if(i===y){if("throw"===o)throw a;return{value:t,done:!0}}for(n.method=o,n.arg=a;;){var u=n.delegate;if(u){var c=O(u,n);if(c){if(c===g)continue;return c}}if("next"===n.method)n.sent=n._sent=n.arg;else if("throw"===n.method){if(i===h)throw i=y,n.arg;n.dispatchException(n.arg)}else"return"===n.method&&n.abrupt("return",n.arg);i=v;var s=d(e,r,n);if("normal"===s.type){if(i=n.done?y:p,s.arg===g)continue;return{value:s.arg,done:n.done}}"throw"===s.type&&(i=y,n.method="throw",n.arg=s.arg)}}}function O(e,r){var n=r.method,i=e.iterator[n];if(i===t)return r.delegate=null,"throw"===n&&e.iterator.return&&(r.method="return",r.arg=t,O(e,r),"throw"===r.method)||"return"!==n&&(r.method="throw",r.arg=new TypeError("The iterator does not provide a '"+n+"' method")),g;var o=d(i,e.iterator,r.arg);if("throw"===o.type)return r.method="throw",r.arg=o.arg,r.delegate=null,g;var a=o.arg;return a?a.done?(r[e.resultName]=a.value,r.next=e.nextLoc,"return"!==r.method&&(r.method="next",r.arg=t),r.delegate=null,g):a:(r.method="throw",r.arg=new TypeError("iterator result is not an object"),r.delegate=null,g)}function N(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function j(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function T(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(N,this),this.reset(!0)}function S(e){if(e||""===e){var r=e[u];if(r)return r.call(e);if("function"==typeof e.next)return e;if(!isNaN(e.length)){var i=-1,o=function r(){for(;++i<e.length;)if(n.call(e,i))return r.value=e[i],r.done=!1,r;return r.value=t,r.done=!0,r};return o.next=o}}throw new TypeError(typeof e+" is not iterable")}return b.prototype=w,o(E,"constructor",{value:w,configurable:!0}),o(w,"constructor",{value:b,configurable:!0}),b.displayName=l(w,s,"GeneratorFunction"),e.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===b||"GeneratorFunction"===(e.displayName||e.name))},e.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,w):(t.__proto__=w,l(t,s,"GeneratorFunction")),t.prototype=Object.create(E),t},e.awrap=function(t){return{__await:t}},L(W.prototype),l(W.prototype,c,(function(){return this})),e.AsyncIterator=W,e.async=function(t,r,n,i,o){void 0===o&&(o=Promise);var a=new W(f(t,r,n,i),o);return e.isGeneratorFunction(r)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},L(E),l(E,s,"Generator"),l(E,u,(function(){return this})),l(E,"toString",(function(){return"[object Generator]"})),e.keys=function(t){var e=Object(t),r=[];for(var n in e)r.push(n);return r.reverse(),function t(){for(;r.length;){var n=r.pop();if(n in e)return t.value=n,t.done=!1,t}return t.done=!0,t}},e.values=S,T.prototype={constructor:T,reset:function(e){if(this.prev=0,this.next=0,this.sent=this._sent=t,this.done=!1,this.delegate=null,this.method="next",this.arg=t,this.tryEntries.forEach(j),!e)for(var r in this)"t"===r.charAt(0)&&n.call(this,r)&&!isNaN(+r.slice(1))&&(this[r]=t)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(e){if(this.done)throw e;var r=this;function i(n,i){return u.type="throw",u.arg=e,r.next=n,i&&(r.method="next",r.arg=t),!!i}for(var o=this.tryEntries.length-1;o>=0;--o){var a=this.tryEntries[o],u=a.completion;if("root"===a.tryLoc)return i("end");if(a.tryLoc<=this.prev){var c=n.call(a,"catchLoc"),s=n.call(a,"finallyLoc");if(c&&s){if(this.prev<a.catchLoc)return i(a.catchLoc,!0);if(this.prev<a.finallyLoc)return i(a.finallyLoc)}else if(c){if(this.prev<a.catchLoc)return i(a.catchLoc,!0)}else{if(!s)throw new Error("try statement without catch or finally");if(this.prev<a.finallyLoc)return i(a.finallyLoc)}}}},abrupt:function(t,e){for(var r=this.tryEntries.length-1;r>=0;--r){var i=this.tryEntries[r];if(i.tryLoc<=this.prev&&n.call(i,"finallyLoc")&&this.prev<i.finallyLoc){var o=i;break}}o&&("break"===t||"continue"===t)&&o.tryLoc<=e&&e<=o.finallyLoc&&(o=null);var a=o?o.completion:{};return a.type=t,a.arg=e,o?(this.method="next",this.next=o.finallyLoc,g):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),g},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),j(r),g}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var n=r.completion;if("throw"===n.type){var i=n.arg;j(r)}return i}}throw new Error("illegal catch attempt")},delegateYield:function(e,r,n){return this.delegate={iterator:S(e),resultName:r,nextLoc:n},"next"===this.method&&(this.arg=t),g}},e}function o(t,e,r,n,i,o,a){try{var u=t[o](a),c=u.value}catch(t){return void r(t)}u.done?e(c):Promise.resolve(c).then(n,i)}function a(t){return function(){var e=this,r=arguments;return new Promise((function(n,i){var a=t.apply(e,r);function u(t){o(a,n,i,u,c,"next",t)}function c(t){o(a,n,i,u,c,"throw",t)}u(void 0)}))}}function u(t,e){(null==e||e>t.length)&&(e=t.length);for(var r=0,n=new Array(e);r<e;r++)n[r]=t[r];return n}function c(t,e){var r="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(r)return(r=r.call(t)).next.bind(r);if(Array.isArray(t)||(r=function(t,e){if(t){if("string"==typeof t)return u(t,e);var r=Object.prototype.toString.call(t).slice(8,-1);return"Object"===r&&t.constructor&&(r=t.constructor.name),"Map"===r||"Set"===r?Array.from(t):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?u(t,e):void 0}}(t))||e&&t&&"number"==typeof t.length){r&&(t=r);var n=0;return function(){return n>=t.length?{done:!0}:{done:!1,value:t[n++]}}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var s=new MutationObserver(p),l=new n.A,f=[],d=!1,h=!1;function p(t){for(var e,r=c(t);!(e=r()).done;){var n=e.value;if("childList"===n.type&&(n.removedNodes.forEach((function(t){1===t.nodeType&&l.emit("removeNode",t)})),n.addedNodes.forEach((function(t){1===t.nodeType&&l.emit("addNode",t)}))),"attributes"===n.type){var i=n.target,o=n.attributeName,a=n.oldValue;if(i.hasAttribute(o))if(null===a)l.emit("addAttribute",i,o,i.getAttribute(o));else{var u=i.getAttribute(o);a!==u&&l.emit("changeAttribute",i,o,a,u)}else l.emit("removeAttribute",i,o,a)}}}function v(){d||(s.observe(document,{subtree:!0,childList:!0,attributes:!0,attributeOldValue:!0}),d=!0)}function y(){d&&((f=f.concat(s.takeRecords())).length&&!h&&(h=!0,queueMicrotask((function(){p(f),f.length=0,h=!1}))),s.disconnect(),d=!1)}function g(t){d?(y(),t(),v()):t()}function m(t){var e=t.trim();return e?e.split(/\s+/).filter((function(t,e,r){return r.indexOf(t)===e})):[]}function b(t,e){return t.filter((function(t){return!e.includes(t)}))}function w(t,e){for(var r=t.length-1;r>=0;r--)t[r]===e&&t.splice(r,1)}function A(t,e,r){void 0===r&&(r={}),t.dispatchEvent(new CustomEvent(e,{detail:r,bubbles:!0,composed:!0,cancelable:!0}))}var x="data-xclass",_="["+x+"]",E="_xclass_applied",L=!0,W={_registered:new Map,mutateDOM:g,start:function(){var t=this;document.body||console.warn("XClass Warning: Unable to initialize. Trying to load XClass before `<body>` is available. Did you forget to add `defer` in XClass's `<script>` tag?"),v(),L&&(L=!1,l.on("addNode",function(){var e=a(i().mark((function e(r){return i().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,t.initTree(r);case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()).on("removeNode",function(){var e=a(i().mark((function e(r){return i().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,t.destroyTree(r);case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()).on("addAttribute",function(){var e=a(i().mark((function e(r,n,o){var a;return i().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(n!==x){e.next=4;break}return a=m(o),e.next=4,t._initWidget.apply(t,[r].concat(a));case 4:case"end":return e.stop()}}),e)})));return function(t,r,n){return e.apply(this,arguments)}}()).on("changeAttribute",function(){var e=a(i().mark((function e(r,n,o,a){var u,c,s,l;return i().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(n!==x){e.next=9;break}return u=m(o),c=m(a),s=b(c,u),l=b(u,c),e.next=7,t._destroyWidget.apply(t,[r].concat(l));case 7:return e.next=9,t._initWidget.apply(t,[r].concat(s));case 9:case"end":return e.stop()}}),e)})));return function(t,r,n,i){return e.apply(this,arguments)}}()).on("removeAttribute",function(){var e=a(i().mark((function e(r,n,o){var a;return i().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(n!==x){e.next=4;break}return a=m(o),e.next=4,t._destroyWidget.apply(t,[r].concat(a));case 4:case"end":return e.stop()}}),e)})));return function(t,r,n){return e.apply(this,arguments)}}()),this.initTree().then((function(){A(document,"xclass:initialized")})))},stop:function(){y()},register:function(t,e){if(this._registered.has(t))throw new Error('Widget "'+t+'" is already registered.');this._registered.set(t,e);var r=e.onRegister;r&&r.call(e,e),A(document,"xclass:registered",{name:t,widgetObject:e})},isWidgetApplied:function(t,e){var r=t[E];return Array.isArray(r)&&r.includes(e)},addWidget:function(t){for(var e=this,r=m(t.getAttribute(x)||""),n=arguments.length,i=new Array(n>1?n-1:0),o=1;o<n;o++)i[o-1]=arguments[o];var a=i.map((function(n){return e.isWidgetApplied(t,n)?(console.warn('Widget "'+n+'" has already been applied to this element.'),Promise.resolve()):(r.push(n),e._initWidget(t,n))}));Promise.allSettled(a).then((function(){g((function(){r.length?t.setAttribute(x,r.join(" ")):t.removeAttribute(x)}))}))},deleteWidget:function(t){for(var e=this,r=m(t.getAttribute(x)||""),n=arguments.length,i=new Array(n>1?n-1:0),o=1;o<n;o++)i[o-1]=arguments[o];var a=i.map((function(n){return e.isWidgetApplied(t,n)?(w(r,n),e._destroyWidget(t,n)):(console.warn('Widget "'+n+'" was not applied to this element.'),Promise.resolve())}));Promise.allSettled(a).then((function(){g((function(){r.length?t.setAttribute(x,r.join(" ")):t.removeAttribute(x)}))}))},deleteAllWidgets:function(t){this._destroyAllFromAttribute(t).then((function(){g((function(){t.removeAttribute(x)}))}))},findClosest:function(t,e){for(var r=t;;){if(this.isWidgetApplied(r,e))return r;if(!(r=r.parentElement))return null}},find:function(t,e){for(var r,n=document.createTreeWalker(t,NodeFilter.SHOW_ELEMENT,null,!1);r=n.nextNode();)if(this.isWidgetApplied(r,e))return r;return null},findAll:function(t,e){for(var r,n=[],i=document.createTreeWalker(t,NodeFilter.SHOW_ELEMENT,null,!1);r=i.nextNode();)this.isWidgetApplied(r,e)&&n.push(r);return n},initTree:function(t){var e=this;return a(i().mark((function r(){var n;return i().wrap((function(r){for(;;)switch(r.prev=r.next){case 0:if(void 0===t&&(t=document.documentElement),t.nodeType!==document.ELEMENT_NODE||!t.matches(_)){r.next=4;break}return r.next=4,e._applyAllFromAttribute(t);case 4:return n=Array.from(t.querySelectorAll(_)).map((function(t){return e._applyAllFromAttribute(t)})),r.next=7,Promise.allSettled(n);case 7:case"end":return r.stop()}}),r)})))()},destroyTree:function(t){var e=this;return a(i().mark((function r(){var n;return i().wrap((function(r){for(;;)switch(r.prev=r.next){case 0:if(void 0===t&&(t=document.documentElement),t.nodeType!==document.ELEMENT_NODE||!t.matches(_)){r.next=4;break}return r.next=4,e._destroyAllFromAttribute(t);case 4:return n=Array.from(t.querySelectorAll(_)).map((function(t){return e._destroyAllFromAttribute(t)})),r.next=7,Promise.allSettled(n);case 7:case"end":return r.stop()}}),r)})))()},_getAppliedWidgets:function(t){var e=t[E];return Array.isArray(e)||(t[E]=e=[]),e},_initWidget:function(t){for(var e=this,r=this._getAppliedWidgets(t),n=[],i=arguments.length,o=new Array(i>1?i-1:0),a=1;a<i;a++)o[a-1]=arguments[a];return o.forEach((function(i){if(e._registered.has(i)){var o,a=e._registered.get(i);if(!r.includes(i))Array.isArray(a.dependencies)&&a.dependencies.forEach((function(r){n.push(e._initWidget(t,r))})),a.init&&(o=a.init(t,a)),r.push(i),o instanceof Promise?n.push(o.then((function(){A(t,"xclass:init-widget",{name:i,widgetObject:a})}))):A(t,"xclass:init-widget",{name:i,widgetObject:a})}else console.debug('Widget "'+i+'" is not registered.')})),Promise.allSettled(n)},_destroyWidget:function(t){for(var e=this,r=this._getAppliedWidgets(t),n=[],i=arguments.length,o=new Array(i>1?i-1:0),a=1;a<i;a++)o[a-1]=arguments[a];return o.forEach((function(i){if(e._registered.has(i)){var o,a=e._registered.get(i);if(r.includes(i))a.destroy&&(o=a.destroy(t,a)),w(r,i),o instanceof Promise?n.push(o.then((function(){A(t,"xclass:destroy-widget",{name:i,widgetObject:a})}))):A(t,"xclass:destroy-widget",{name:i,widgetObject:a}),Array.isArray(a.dependencies)&&a.dependencies.reverse().forEach((function(r){n.push(e._destroyWidget(t,r))}))}else console.debug('Widget "'+i+'" is not registered.')})),Promise.allSettled(n)},_applyAllFromAttribute:function(t){var e=this;return a(i().mark((function r(){var n,o;return i().wrap((function(r){for(;;)switch(r.prev=r.next){case 0:return n=t.getAttribute(x)||"",o=m(n),r.next=4,e._initWidget.apply(e,[t].concat(o));case 4:case"end":return r.stop()}}),r)})))()},_destroyAllFromAttribute:function(t){var e=this;return a(i().mark((function r(){var n,o;return i().wrap((function(r){for(;;)switch(r.prev=r.next){case 0:return n=t.getAttribute(x)||"",o=m(n),r.next=4,e._destroyWidget.apply(e,[t].concat(o));case 4:case"end":return r.stop()}}),r)})))()}}}}]);
//# sourceMappingURL=npm.data-xclass.ccbc1a6193588095cbd8.js.map