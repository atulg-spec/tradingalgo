"use strict";(self.webpackChunkpaper_admin=self.webpackChunkpaper_admin||[]).push([[735],{3016:(e,r,t)=>{var n=t(453),o=n("%Array.prototype%"),i=n("%RangeError%"),a=n("%SyntaxError%"),u=n("%TypeError%"),s=t(1087),f=Math.pow(2,32)-1,p=t(24)(),l=n("%Object.setPrototypeOf%",!0)||(p?function(e,r){return e.__proto__=r,e}:null);e.exports=function(e){if(!s(e)||e<0)throw new u("Assertion failed: `length` must be an integer Number >= 0");if(e>f)throw new i("length is greater than (2**32 - 1)");var r=arguments.length>1?arguments[1]:o,t=[];if(r!==o){if(!l)throw new a("ArrayCreate: a `proto` argument that is not `Array.prototype` is not supported in an environment that does not support setting the [[Prototype]]");l(t,r)}return 0!==e&&(t.length=e),t}},4076:(e,r,t)=>{var n=t(453),o=n("%Symbol.species%",!0),i=n("%TypeError%"),a=t(3016),u=t(4281),s=t(9268),f=t(9801),p=t(8501),l=t(1087);e.exports=function(e,r){if(!l(r)||r<0)throw new i("Assertion failed: length must be an integer >= 0");if(!s(e))return a(r);var t=u(e,"constructor");if(o&&"Object"===p(t)&&null===(t=u(t,o))&&(t=void 0),void 0===t)return a(r);if(!f(t))throw new i("C must be a constructor");return new t(r)}},545:(e,r,t)=>{var n=t(453),o=t(456),i=n("%TypeError%"),a=t(9268),u=n("%Reflect.apply%",!0)||o("Function.prototype.apply");e.exports=function(e,r){var t=arguments.length>2?arguments[2]:[];if(!a(t))throw new i("Assertion failed: optional `argumentsList`, if provided, must be a List");return u(e,r,t)}},3288:(e,r,t)=>{var n=t(453)("%TypeError%"),o=t(5637),i=t(6175),a=t(8501);e.exports=function(e,r,t){if("Object"!==a(e))throw new n("Assertion failed: Type(O) is not Object");if(!o(r))throw new n("Assertion failed: IsPropertyKey(P) is not true");return i(e,r,{"[[Configurable]]":!0,"[[Enumerable]]":!0,"[[Value]]":t,"[[Writable]]":!0})}},2189:(e,r,t)=>{var n=t(453)("%TypeError%"),o=t(3288),i=t(5637),a=t(8501);e.exports=function(e,r,t){if("Object"!==a(e))throw new n("Assertion failed: Type(O) is not Object");if(!i(r))throw new n("Assertion failed: IsPropertyKey(P) is not true");if(!o(e,r,t))throw new n("unable to create data property")}},8780:(e,r,t)=>{var n=t(453)("%TypeError%"),o=t(6157),i=t(4769),a=t(9173),u=t(6951),s=t(7856),f=t(5637),p=t(6654),l=t(9576),c=t(8501);e.exports=function(e,r,t){if("Object"!==c(e))throw new n("Assertion failed: Type(O) is not Object");if(!f(r))throw new n("Assertion failed: IsPropertyKey(P) is not true");var b=o({Type:c,IsDataDescriptor:s,IsAccessorDescriptor:u},t)?t:l(t);if(!o({Type:c,IsDataDescriptor:s,IsAccessorDescriptor:u},b))throw new n("Assertion failed: Desc is not a valid Property Descriptor");return i(s,p,a,e,r,b)}},9173:(e,r,t)=>{var n=t(9446),o=t(2997),i=t(8501);e.exports=function(e){return void 0!==e&&n(i,"Property Descriptor","Desc",e),o(e)}},4281:(e,r,t)=>{var n=t(453)("%TypeError%"),o=t(8859),i=t(5637),a=t(8501);e.exports=function(e,r){if("Object"!==a(e))throw new n("Assertion failed: Type(O) is not Object");if(!i(r))throw new n("Assertion failed: IsPropertyKey(P) is not true, got "+o(r));return e[r]}},3772:(e,r,t)=>{var n=t(453)("%TypeError%"),o=t(5637),i=t(8501);e.exports=function(e,r){if("Object"!==i(e))throw new n("Assertion failed: `O` must be an Object");if(!o(r))throw new n("Assertion failed: `P` must be a Property Key");return r in e}},6951:(e,r,t)=>{var n=t(9957),o=t(8501),i=t(9446);e.exports=function(e){return void 0!==e&&(i(o,"Property Descriptor","Desc",e),!(!n(e,"[[Get]]")&&!n(e,"[[Set]]")))}},9268:(e,r,t)=>{e.exports=t(1412)},4377:(e,r,t)=>{e.exports=t(9600)},9801:(e,r,t)=>{var n=t(1376)("%Reflect.construct%",!0),o=t(8780);try{o({},"",{"[[Get]]":function(){}})}catch(e){o=null}if(o&&n){var i={},a={};o(a,"length",{"[[Get]]":function(){throw i},"[[Enumerable]]":!0}),e.exports=function(e){try{n(e,a)}catch(e){return e===i}}}else e.exports=function(e){return"function"==typeof e&&!!e.prototype}},7856:(e,r,t)=>{var n=t(9957),o=t(8501),i=t(9446);e.exports=function(e){return void 0!==e&&(i(o,"Property Descriptor","Desc",e),!(!n(e,"[[Value]]")&&!n(e,"[[Writable]]")))}},908:(e,r,t)=>{var n=t(453),o=n("%Object.preventExtensions%",!0),i=n("%Object.isExtensible%",!0),a=t(6600);e.exports=o?function(e){return!a(e)&&i(e)}:function(e){return!a(e)}},9561:(e,r,t)=>{var n=t(9446),o=t(6951),i=t(7856),a=t(8501);e.exports=function(e){return void 0!==e&&(n(a,"Property Descriptor","Desc",e),!o(e)&&!i(e))}},5637:e=>{e.exports=function(e){return"string"==typeof e||"symbol"==typeof e}},6175:(e,r,t)=>{var n=t(453),o=t(5795),i=n("%SyntaxError%"),a=n("%TypeError%"),u=t(6157),s=t(6951),f=t(7856),p=t(908),l=t(5637),c=t(9576),b=t(6654),y=t(8501),w=t(6532);e.exports=function(e,r,t){if("Object"!==y(e))throw new a("Assertion failed: O must be an Object");if(!l(r))throw new a("Assertion failed: P must be a Property Key");if(!u({Type:y,IsDataDescriptor:f,IsAccessorDescriptor:s},t))throw new a("Assertion failed: Desc must be a Property Descriptor");if(!o){if(s(t))throw new i("This environment does not support accessor property descriptors.");var n=!(r in e)&&t["[[Writable]]"]&&t["[[Enumerable]]"]&&t["[[Configurable]]"]&&"[[Value]]"in t,d=r in e&&(!("[[Configurable]]"in t)||t["[[Configurable]]"])&&(!("[[Enumerable]]"in t)||t["[[Enumerable]]"])&&(!("[[Writable]]"in t)||t["[[Writable]]"])&&"[[Value]]"in t;if(n||d)return e[r]=t["[[Value]]"],b(e[r],t["[[Value]]"]);throw new i("This environment does not support defining non-writable, non-enumerable, or non-configurable properties")}var v=o(e,r),m=v&&c(v),g=p(e);return w(e,r,g,t,m)}},7358:(e,r,t)=>{var n=t(453),o=t(487),i=n("%Promise.resolve%",!0),a=i&&o(i);e.exports=function(e,r){if(!a)throw new SyntaxError("This environment does not support Promises.");return a(e,r)}},351:(e,r,t)=>{e.exports=t(2524)},6654:(e,r,t)=>{var n=t(8756);e.exports=function(e,r){return e===r?0!==e||1/e==1/r:n(e)&&n(r)}},3360:(e,r,t)=>{var n=t(453),o=n("%Number%"),i=n("%RegExp%"),a=n("%TypeError%"),u=n("%parseInt%"),s=t(456),f=t(2102),p=s("String.prototype.slice"),l=f(/^0b[01]+$/i),c=f(/^0o[0-7]+$/i),b=f(/^[-+]0x[0-9a-f]+$/i),y=f(new i("["+["","​","￾"].join("")+"]","g")),w=t(214),d=t(8501);e.exports=function e(r){if("String"!==d(r))throw new a("Assertion failed: `argument` is not a String");if(l(r))return o(u(p(r,2),2));if(c(r))return o(u(p(r,2),8));if(y(r)||b(r))return NaN;var t=w(r);return t!==r?e(t):o(r)}},4150:e=>{e.exports=function(e){return!!e}},6065:(e,r,t)=>{var n=t(453),o=n("%TypeError%"),i=n("%Number%"),a=t(6600),u=t(9163),s=t(3360);e.exports=function(e){var r=a(e)?e:u(e,i);if("symbol"==typeof r)throw new o("Cannot convert a Symbol value to a number");if("bigint"==typeof r)throw new o("Conversion from 'BigInt' to 'number' is not allowed.");return"string"==typeof r?s(r):i(r)}},8227:(e,r,t)=>{var n=t(453)("%Object%"),o=t(351);e.exports=function(e){return o(e),n(e)}},9163:(e,r,t)=>{var n=t(5437);e.exports=function(e){return arguments.length>1?n(e,arguments[1]):n(e)}},9576:(e,r,t)=>{var n=t(9957),o=t(453)("%TypeError%"),i=t(8501),a=t(4150),u=t(4377);e.exports=function(e){if("Object"!==i(e))throw new o("ToPropertyDescriptor requires an object");var r={};if(n(e,"enumerable")&&(r["[[Enumerable]]"]=a(e.enumerable)),n(e,"configurable")&&(r["[[Configurable]]"]=a(e.configurable)),n(e,"value")&&(r["[[Value]]"]=e.value),n(e,"writable")&&(r["[[Writable]]"]=a(e.writable)),n(e,"get")){var t=e.get;if(void 0!==t&&!u(t))throw new o("getter must be a function");r["[[Get]]"]=t}if(n(e,"set")){var s=e.set;if(void 0!==s&&!u(s))throw new o("setter must be a function");r["[[Set]]"]=s}if((n(r,"[[Get]]")||n(r,"[[Set]]"))&&(n(r,"[[Value]]")||n(r,"[[Writable]]")))throw new o("Invalid property descriptor. Cannot both specify accessors and a value or writable attribute");return r}},1885:(e,r,t)=>{var n=t(453),o=n("%String%"),i=n("%TypeError%");e.exports=function(e){if("symbol"==typeof e)throw new i("Cannot convert a Symbol value to a string");return o(e)}},6229:(e,r,t)=>{var n=t(3615),o=t(6065),i=t(6967),a=t(5046);e.exports=function(e){var r=o(e);if(!a(r)||0===r)return 0;var t=i(r),u=n(t,4294967296);return 0===u?0:u}},8501:(e,r,t)=>{var n=t(2439);e.exports=function(e){return"symbol"==typeof e?"Symbol":"bigint"==typeof e?"BigInt":n(e)}},6532:(e,r,t)=>{var n=t(453)("%TypeError%"),o=t(4769),i=t(8143),a=t(6157),u=t(9173),s=t(6951),f=t(7856),p=t(9561),l=t(5637),c=t(6654),b=t(8501);e.exports=function(e,r,t,y,w){var d,v,m=b(e);if("Undefined"!==m&&"Object"!==m)throw new n("Assertion failed: O must be undefined or an Object");if(!l(r))throw new n("Assertion failed: P must be a Property Key");if("Boolean"!==b(t))throw new n("Assertion failed: extensible must be a Boolean");if(!a({Type:b,IsDataDescriptor:f,IsAccessorDescriptor:s},y))throw new n("Assertion failed: Desc must be a Property Descriptor");if("Undefined"!==b(w)&&!a({Type:b,IsDataDescriptor:f,IsAccessorDescriptor:s},w))throw new n("Assertion failed: current must be a Property Descriptor, or undefined");if("Undefined"===b(w))return!!t&&("Undefined"===m||(s(y)?o(f,c,u,e,r,y):o(f,c,u,e,r,{"[[Configurable]]":!!y["[[Configurable]]"],"[[Enumerable]]":!!y["[[Enumerable]]"],"[[Value]]":y["[[Value]]"],"[[Writable]]":!!y["[[Writable]]"]})));if(!i({IsAccessorDescriptor:s,IsDataDescriptor:f},w))throw new n("`current`, when present, must be a fully populated and valid Property Descriptor");if(!w["[[Configurable]]"]){if("[[Configurable]]"in y&&y["[[Configurable]]"])return!1;if("[[Enumerable]]"in y&&!c(y["[[Enumerable]]"],w["[[Enumerable]]"]))return!1;if(!p(y)&&!c(s(y),s(w)))return!1;if(s(w)){if("[[Get]]"in y&&!c(y["[[Get]]"],w["[[Get]]"]))return!1;if("[[Set]]"in y&&!c(y["[[Set]]"],w["[[Set]]"]))return!1}else if(!w["[[Writable]]"]){if("[[Writable]]"in y&&y["[[Writable]]"])return!1;if("[[Value]]"in y&&!c(y["[[Value]]"],w["[[Value]]"]))return!1}}return"Undefined"===m||(f(w)&&s(y)?(d=("[[Configurable]]"in y?y:w)["[[Configurable]]"],v=("[[Enumerable]]"in y?y:w)["[[Enumerable]]"],o(f,c,u,e,r,{"[[Configurable]]":!!d,"[[Enumerable]]":!!v,"[[Get]]":("[[Get]]"in y?y:w)["[[Get]]"],"[[Set]]":("[[Set]]"in y?y:w)["[[Set]]"]})):s(w)&&f(y)?(d=("[[Configurable]]"in y?y:w)["[[Configurable]]"],v=("[[Enumerable]]"in y?y:w)["[[Enumerable]]"],o(f,c,u,e,r,{"[[Configurable]]":!!d,"[[Enumerable]]":!!v,"[[Value]]":("[[Value]]"in y?y:w)["[[Value]]"],"[[Writable]]":!!("[[Writable]]"in y?y:w)["[[Writable]]"]})):o(f,c,u,e,r,y))}},8091:(e,r,t)=>{var n=t(8501),o=Math.floor;e.exports=function(e){return"BigInt"===n(e)?e:o(e)}},3615:(e,r,t)=>{var n=t(113);e.exports=function(e,r){return n(e,r)}},6967:(e,r,t)=>{var n=t(453),o=t(8091),i=n("%TypeError%");e.exports=function(e){if("number"!=typeof e&&"bigint"!=typeof e)throw new i("argument must be a Number or a BigInt");var r=e<0?-o(-e):o(e);return 0===r?0:r}},2524:(e,r,t)=>{var n=t(453)("%TypeError%");e.exports=function(e,r){if(null==e)throw new n(r||"Cannot call method on "+e);return e}},2439:e=>{e.exports=function(e){return null===e?"Null":void 0===e?"Undefined":"function"==typeof e||"object"==typeof e?"Object":"number"==typeof e?"Number":"boolean"==typeof e?"Boolean":"string"==typeof e?"String":void 0}},1376:(e,r,t)=>{e.exports=t(453)},4769:(e,r,t)=>{var n=t(592),o=t(453),i=n()&&o("%Object.defineProperty%",!0),a=n.hasArrayLengthDefineBug(),u=a&&t(1412),s=t(456)("Object.prototype.propertyIsEnumerable");e.exports=function(e,r,t,n,o,f){if(!i){if(!e(f))return!1;if(!f["[[Configurable]]"]||!f["[[Writable]]"])return!1;if(o in n&&s(n,o)!==!!f["[[Enumerable]]"])return!1;var p=f["[[Value]]"];return n[o]=p,r(n[o],p)}return a&&"length"===o&&"[[Value]]"in f&&u(n)&&n.length!==f["[[Value]]"]?(n.length=f["[[Value]]"],n.length===f["[[Value]]"]):(i(n,o,t(f)),!0)}},1412:(e,r,t)=>{var n=t(453)("%Array%"),o=!n.isArray&&t(456)("Object.prototype.toString");e.exports=n.isArray||function(e){return"[object Array]"===o(e)}},9446:(e,r,t)=>{var n=t(453),o=n("%TypeError%"),i=n("%SyntaxError%"),a=t(9957),u=t(1087),s={"Property Descriptor":function(e){var r={"[[Configurable]]":!0,"[[Enumerable]]":!0,"[[Get]]":!0,"[[Set]]":!0,"[[Value]]":!0,"[[Writable]]":!0};if(!e)return!1;for(var t in e)if(a(e,t)&&!r[t])return!1;var n=a(e,"[[Value]]"),i=a(e,"[[Get]]")||a(e,"[[Set]]");if(n&&i)throw new o("Property Descriptors may not be both accessor and data descriptors");return!0},"Match Record":t(2897),"Iterator Record":function(e){return a(e,"[[Iterator]]")&&a(e,"[[NextMethod]]")&&a(e,"[[Done]]")},"PromiseCapability Record":function(e){return!!e&&a(e,"[[Resolve]]")&&"function"==typeof e["[[Resolve]]"]&&a(e,"[[Reject]]")&&"function"==typeof e["[[Reject]]"]&&a(e,"[[Promise]]")&&e["[[Promise]]"]&&"function"==typeof e["[[Promise]]"].then},"AsyncGeneratorRequest Record":function(e){return!!e&&a(e,"[[Completion]]")&&a(e,"[[Capability]]")&&s["PromiseCapability Record"](e["[[Capability]]"])},"RegExp Record":function(e){return e&&a(e,"[[IgnoreCase]]")&&"boolean"==typeof e["[[IgnoreCase]]"]&&a(e,"[[Multiline]]")&&"boolean"==typeof e["[[Multiline]]"]&&a(e,"[[DotAll]]")&&"boolean"==typeof e["[[DotAll]]"]&&a(e,"[[Unicode]]")&&"boolean"==typeof e["[[Unicode]]"]&&a(e,"[[CapturingGroupsCount]]")&&"number"==typeof e["[[CapturingGroupsCount]]"]&&u(e["[[CapturingGroupsCount]]"])&&e["[[CapturingGroupsCount]]"]>=0}};e.exports=function(e,r,t,n){var a=s[r];if("function"!=typeof a)throw new i("unknown record type: "+r);if("Object"!==e(n)||!a(n))throw new o(t+" must be a "+r)}},2997:e=>{e.exports=function(e){if(void 0===e)return e;var r={};return"[[Value]]"in e&&(r.value=e["[[Value]]"]),"[[Writable]]"in e&&(r.writable=!!e["[[Writable]]"]),"[[Get]]"in e&&(r.get=e["[[Get]]"]),"[[Set]]"in e&&(r.set=e["[[Set]]"]),"[[Enumerable]]"in e&&(r.enumerable=!!e["[[Enumerable]]"]),"[[Configurable]]"in e&&(r.configurable=!!e["[[Configurable]]"]),r}},5046:(e,r,t)=>{var n=t(8756);e.exports=function(e){return("number"==typeof e||"bigint"==typeof e)&&!n(e)&&e!==1/0&&e!==-1/0}},8143:e=>{e.exports=function(e,r){return!!r&&"object"==typeof r&&"[[Enumerable]]"in r&&"[[Configurable]]"in r&&(e.IsAccessorDescriptor(r)||e.IsDataDescriptor(r))}},1087:(e,r,t)=>{var n=t(453),o=n("%Math.abs%"),i=n("%Math.floor%"),a=t(8756),u=t(5046);e.exports=function(e){if("number"!=typeof e||a(e)||!u(e))return!1;var r=o(e);return i(r)===r}},2897:(e,r,t)=>{var n=t(9957);e.exports=function(e){return n(e,"[[StartIndex]]")&&n(e,"[[EndIndex]]")&&e["[[StartIndex]]"]>=0&&e["[[EndIndex]]"]>=e["[[StartIndex]]"]&&String(parseInt(e["[[StartIndex]]"],10))===String(e["[[StartIndex]]"])&&String(parseInt(e["[[EndIndex]]"],10))===String(e["[[EndIndex]]"])}},8756:e=>{e.exports=Number.isNaN||function(e){return e!=e}},6600:e=>{e.exports=function(e){return null===e||"function"!=typeof e&&"object"!=typeof e}},6157:(e,r,t)=>{var n=t(453),o=t(9957),i=n("%TypeError%");e.exports=function(e,r){if("Object"!==e.Type(r))return!1;var t={"[[Configurable]]":!0,"[[Enumerable]]":!0,"[[Get]]":!0,"[[Set]]":!0,"[[Value]]":!0,"[[Writable]]":!0};for(var n in r)if(o(r,n)&&!t[n])return!1;if(e.IsDataDescriptor(r)&&e.IsAccessorDescriptor(r))throw new i("Property Descriptors may not be both accessor and data descriptors");return!0}},113:e=>{var r=Math.floor;e.exports=function(e,t){var n=e%t;return r(n>=0?n:n+t)}}}]);
//# sourceMappingURL=npm.es-abstract.6e933b791c5d146285cd.js.map