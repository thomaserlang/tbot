"use strict";(self.webpackChunkbotashell=self.webpackChunkbotashell||[]).push([[621],{3905:function(e,t,n){n.d(t,{Zo:function(){return u},kt:function(){return m}});var r=n(7294);function l(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){l(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function o(e,t){if(null==e)return{};var n,r,l=function(e,t){if(null==e)return{};var n,r,l={},a=Object.keys(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||(l[n]=e[n]);return l}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(l[n]=e[n])}return l}var c=r.createContext({}),p=function(e){var t=r.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},u=function(e){var t=p(e.components);return r.createElement(c.Provider,{value:t},e.children)},f={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},s=r.forwardRef((function(e,t){var n=e.components,l=e.mdxType,a=e.originalType,c=e.parentName,u=o(e,["components","mdxType","originalType","parentName"]),s=p(n),m=l,d=s["".concat(c,".").concat(m)]||s[m]||f[m]||a;return n?r.createElement(d,i(i({ref:t},u),{},{components:n})):r.createElement(d,i({ref:t},u))}));function m(e,t){var n=arguments,l=t&&t.mdxType;if("string"==typeof e||l){var a=n.length,i=new Array(a);i[0]=s;var o={};for(var c in t)hasOwnProperty.call(t,c)&&(o[c]=t[c]);o.originalType=e,o.mdxType="string"==typeof e?e:l,i[1]=o;for(var p=2;p<a;p++)i[p]=n[p];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}s.displayName="MDXCreateElement"},202:function(e,t,n){n.r(t),n.d(t,{assets:function(){return u},contentTitle:function(){return c},default:function(){return m},frontMatter:function(){return o},metadata:function(){return p},toc:function(){return f}});var r=n(3117),l=n(102),a=(n(7294),n(3905)),i=["components"],o={id:"faceit",title:"Faceit"},c=void 0,p={unversionedId:"faceit",id:"faceit",title:"Faceit",description:"Example usage:",source:"@site/docs/faceit.md",sourceDirName:".",slug:"/faceit",permalink:"/docs/faceit",tags:[],version:"current",frontMatter:{id:"faceit",title:"Faceit"},sidebar:"tutorialSidebar",previous:{title:"Countdown",permalink:"/docs/countdown"},next:{title:"Followage",permalink:"/docs/followage"}},u={},f=[{value:"faceit.username",id:"faceitusername",level:2},{value:"faceit.elo",id:"faceitelo",level:2},{value:"faceit.level",id:"faceitlevel",level:2},{value:"faceit.next_level_points",id:"faceitnext_level_points",level:2},{value:"faceit.next_level",id:"faceitnext_level",level:2}],s={toc:f};function m(e){var t=e.components,n=(0,l.Z)(e,i);return(0,a.kt)("wrapper",(0,r.Z)({},s,n,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("p",null,"Example usage:"),(0,a.kt)("p",null,(0,a.kt)("inlineCode",{parentName:"p"},"@{user}, Faceit level: {faceit.level} ({faceit.elo} elo) - {faceit.next_level_points} elo needed for next level {faceit.username ErlePerle}")),(0,a.kt)("h2",{id:"faceitusername"},"faceit.username"),(0,a.kt)("p",null,"Set the name of the faceit user to lookup"),(0,a.kt)("p",null,(0,a.kt)("inlineCode",{parentName:"p"},"{faceit.username ErlePerle}")),(0,a.kt)("p",null,"Returns an empty string."),(0,a.kt)("h2",{id:"faceitelo"},"faceit.elo"),(0,a.kt)("p",null,"The user's current elo."),(0,a.kt)("p",null,(0,a.kt)("inlineCode",{parentName:"p"},"{faceit.elo}")),(0,a.kt)("p",null,"Example response: ",(0,a.kt)("inlineCode",{parentName:"p"},"1024")),(0,a.kt)("h2",{id:"faceitlevel"},"faceit.level"),(0,a.kt)("p",null,"The user's current level."),(0,a.kt)("p",null,(0,a.kt)("inlineCode",{parentName:"p"},"{faceit.level}")),(0,a.kt)("p",null,"Example response: ",(0,a.kt)("inlineCode",{parentName:"p"},"6")),(0,a.kt)("h2",{id:"faceitnext_level_points"},"faceit.next_level_points"),(0,a.kt)("p",null,"The amount of points needed for the next level."),(0,a.kt)("p",null,(0,a.kt)("inlineCode",{parentName:"p"},"{faceit.next_level_points}")),(0,a.kt)("p",null,"Example response: ",(0,a.kt)("inlineCode",{parentName:"p"},"106")),(0,a.kt)("h2",{id:"faceitnext_level"},"faceit.next_level"),(0,a.kt)("p",null,"The name of the next level."),(0,a.kt)("p",null,(0,a.kt)("inlineCode",{parentName:"p"},"{faceit.next_level}")),(0,a.kt)("p",null,"Example response: ",(0,a.kt)("inlineCode",{parentName:"p"},"7")))}m.isMDXComponent=!0}}]);