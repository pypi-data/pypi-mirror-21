(function(){var k=window.AmCharts;k.AmSlicedChart=k.Class({inherits:k.AmChart,construct:function(a){this.createEvents("rollOverSlice","rollOutSlice","clickSlice","pullOutSlice","pullInSlice","rightClickSlice");k.AmSlicedChart.base.construct.call(this,a);this.colors="#FF0F00 #FF6600 #FF9E01 #FCD202 #F8FF01 #B0DE09 #04D215 #0D8ECF #0D52D1 #2A0CD0 #8A0CCF #CD0D74 #754DEB #DDDDDD #999999 #333333 #000000 #57032A #CA9726 #990000 #4B0C25".split(" ");this.alpha=1;this.groupPercent=0;this.groupedTitle="Other";
this.groupedPulled=!1;this.groupedAlpha=1;this.marginLeft=0;this.marginBottom=this.marginTop=10;this.marginRight=0;this.hoverAlpha=1;this.outlineColor="#FFFFFF";this.outlineAlpha=0;this.outlineThickness=1;this.startAlpha=0;this.startDuration=1;this.startEffect="bounce";this.sequencedAnimation=!0;this.pullOutDuration=1;this.pullOutEffect="bounce";this.pullOnHover=this.pullOutOnlyOne=!1;this.labelsEnabled=!0;this.labelTickColor="#000000";this.labelTickAlpha=.2;this.hideLabelsPercent=0;this.urlTarget=
"_self";this.autoMarginOffset=10;this.gradientRatio=[];this.maxLabelWidth=200;k.applyTheme(this,a,"AmSlicedChart")},initChart:function(){k.AmSlicedChart.base.initChart.call(this);this.dataChanged&&(this.parseData(),this.dispatchDataUpdated=!0,this.dataChanged=!1,this.setLegendData(this.chartData));this.drawChart()},handleLegendEvent:function(a){var b=a.type,c=a.dataItem,d=this.legend;if(!d.data&&c){var g=c.hidden;a=a.event;switch(b){case "clickMarker":g||d.switchable||this.clickSlice(c,a);break;case "clickLabel":g||
this.clickSlice(c,a,!1);break;case "rollOverItem":g||this.rollOverSlice(c,!1,a);break;case "rollOutItem":g||this.rollOutSlice(c,a);break;case "hideItem":this.hideSlice(c,a);break;case "showItem":this.showSlice(c,a)}}},invalidateVisibility:function(){this.recalculatePercents();this.initChart();var a=this.legend;a&&a.invalidateSize()},addEventListeners:function(a,b){var c=this;a.mouseover(function(a){c.rollOverSlice(b,!0,a)}).mouseout(function(a){c.rollOutSlice(b,a)}).touchend(function(a){c.rollOverSlice(b,
a)}).touchstart(function(a){}).mouseup(function(a){c.clickSlice(b,a)}).contextmenu(function(a){c.handleRightClick(b,a)})},formatString:function(a,b,c){a=k.formatValue(a,b,["value"],this.nf,"",this.usePrefixes,this.prefixesOfSmallNumbers,this.prefixesOfBigNumbers);var d=this.pf.precision;isNaN(this.tempPrec)||(this.pf.precision=this.tempPrec);a=k.formatValue(a,b,["percents"],this.pf);a=k.massReplace(a,{"[[title]]":b.title,"[[description]]":b.description});this.pf.precision=d;-1!=a.indexOf("[[")&&(a=
k.formatDataContextValue(a,b.dataContext));a=c?k.fixNewLines(a):k.fixBrakes(a);return a=k.cleanFromEmpty(a)},startSlices:function(){var a;for(a=0;a<this.chartData.length;a++)0<this.startDuration&&this.sequencedAnimation?this.setStartTO(a):this.startSlice(this.chartData[a])},setStartTO:function(a){var b=this;a=setTimeout(function(){b.startSequenced.call(b)},b.startDuration/b.chartData.length*500*a);b.timeOuts.push(a)},pullSlices:function(a){var b=this.chartData,c;for(c=0;c<b.length;c++){var d=b[c];
d.pulled&&this.pullSlice(d,1,a)}},startSequenced:function(){var a=this.chartData,b;for(b=0;b<a.length;b++)if(!a[b].started){this.startSlice(this.chartData[b]);break}},startSlice:function(a){a.started=!0;var b=a.wedge,c=this.startDuration,d=a.labelSet;b&&0<c&&(0<a.alpha&&b.show(),b.translate(a.startX,a.startY),this.animatable.push(b),b.animate({opacity:1,translate:"0,0"},c,this.startEffect));d&&0<c&&(0<a.alpha&&d.show(),d.translate(a.startX,a.startY),d.animate({opacity:1,translate:"0,0"},c,this.startEffect))},
showLabels:function(){var a=this.chartData,b;for(b=0;b<a.length;b++){var c=a[b];if(0<c.alpha){var d=c.label;d&&d.show();(c=c.tick)&&c.show()}}},showSlice:function(a){isNaN(a)?a.hidden=!1:this.chartData[a].hidden=!1;this.invalidateVisibility()},hideSlice:function(a){isNaN(a)?a.hidden=!0:this.chartData[a].hidden=!0;this.hideBalloon();this.invalidateVisibility()},rollOverSlice:function(a,b,c){isNaN(a)||(a=this.chartData[a]);clearTimeout(this.hoverInt);if(!a.hidden){this.pullOnHover&&this.pullSlice(a,
1);1>this.hoverAlpha&&a.wedge&&a.wedge.attr({opacity:this.hoverAlpha});var d=a.balloonX,g=a.balloonY;a.pulled&&(d+=a.pullX,g+=a.pullY);var f=this.formatString(this.balloonText,a,!0),h=this.balloonFunction;h&&(f=h(a,f));h=k.adjustLuminosity(a.color,-.15);f?this.showBalloon(f,h,b,d,g):this.hideBalloon();0===a.value&&this.hideBalloon();this.fire({type:"rollOverSlice",dataItem:a,chart:this,event:c})}},rollOutSlice:function(a,b){isNaN(a)||(a=this.chartData[a]);a.wedge&&a.wedge.attr({opacity:1});this.hideBalloon();
this.fire({type:"rollOutSlice",dataItem:a,chart:this,event:b})},clickSlice:function(a,b,c){isNaN(a)||(a=this.chartData[a]);a.pulled?this.pullSlice(a,0):this.pullSlice(a,1);k.getURL(a.url,this.urlTarget);c||this.fire({type:"clickSlice",dataItem:a,chart:this,event:b})},handleRightClick:function(a,b){isNaN(a)||(a=this.chartData[a]);this.fire({type:"rightClickSlice",dataItem:a,chart:this,event:b})},drawTicks:function(){var a=this.chartData,b;for(b=0;b<a.length;b++){var c=a[b];if(c.label&&!c.skipTick){var d=
c.ty,d=k.line(this.container,[c.tx0,c.tx,c.tx2],[c.ty0,d,d],this.labelTickColor,this.labelTickAlpha);k.setCN(this,d,this.type+"-tick");k.setCN(this,d,c.className,!0);c.tick=d;c.wedge.push(d)}}},initialStart:function(){var a=this,b=a.startDuration,c=setTimeout(function(){a.showLabels.call(a)},1E3*b);a.timeOuts.push(c);a.chartCreated?a.pullSlices(!0):(a.startSlices(),0<b?(b=setTimeout(function(){a.pullSlices.call(a)},1200*b),a.timeOuts.push(b)):a.pullSlices(!0))},pullSlice:function(a,b,c){var d=this.pullOutDuration;
!0===c&&(d=0);if(c=a.wedge)0<d?(c.animate({translate:b*a.pullX+","+b*a.pullY},d,this.pullOutEffect),a.labelSet&&a.labelSet.animate({translate:b*a.pullX+","+b*a.pullY},d,this.pullOutEffect)):(a.labelSet&&a.labelSet.translate(b*a.pullX,b*a.pullY),c.translate(b*a.pullX,b*a.pullY));1==b?(a.pulled=!0,this.pullOutOnlyOne&&this.pullInAll(a.index),a={type:"pullOutSlice",dataItem:a,chart:this}):(a.pulled=!1,a={type:"pullInSlice",dataItem:a,chart:this});this.fire(a)},pullInAll:function(a){var b=this.chartData,
c;for(c=0;c<this.chartData.length;c++)c!=a&&b[c].pulled&&this.pullSlice(b[c],0)},pullOutAll:function(){var a=this.chartData,b;for(b=0;b<a.length;b++)a[b].pulled||this.pullSlice(a[b],1)},parseData:function(){var a=[];this.chartData=a;var b=this.dataProvider;isNaN(this.pieAlpha)||(this.alpha=this.pieAlpha);if(void 0!==b){var c=b.length,d=0,g,f,h;for(g=0;g<c;g++){f={};var e=b[g];f.dataContext=e;null!==e[this.valueField]&&(f.value=Number(e[this.valueField]));(h=e[this.titleField])||(h="");f.title=h;f.pulled=
k.toBoolean(e[this.pulledField],!1);(h=e[this.descriptionField])||(h="");f.description=h;f.labelRadius=Number(e[this.labelRadiusField]);f.switchable=!0;f.className=e[this.classNameField];f.url=e[this.urlField];h=e[this.patternField];!h&&this.patterns&&(h=this.patterns[g]);f.pattern=h;f.visibleInLegend=k.toBoolean(e[this.visibleInLegendField],!0);h=e[this.alphaField];f.alpha=void 0!==h?Number(h):this.alpha;h=e[this.colorField];void 0!==h&&(f.color=h);f.labelColor=k.toColor(e[this.labelColorField]);
d+=f.value;f.hidden=!1;a[g]=f}for(g=b=0;g<c;g++)f=a[g],f.percents=f.value/d*100,f.percents<this.groupPercent&&b++;1<b&&(this.groupValue=0,this.removeSmallSlices(),a.push({title:this.groupedTitle,value:this.groupValue,percents:this.groupValue/d*100,pulled:this.groupedPulled,color:this.groupedColor,url:this.groupedUrl,description:this.groupedDescription,alpha:this.groupedAlpha,pattern:this.groupedPattern,className:this.groupedClassName,dataContext:{}}));c=this.baseColor;c||(c=this.pieBaseColor);d=this.brightnessStep;
d||(d=this.pieBrightnessStep);for(g=0;g<a.length;g++)c?h=k.adjustLuminosity(c,g*d/100):(h=this.colors[g],void 0===h&&(h=k.randomColor())),void 0===a[g].color&&(a[g].color=h);this.recalculatePercents()}},recalculatePercents:function(){var a=this.chartData,b=0,c,d;for(c=0;c<a.length;c++)d=a[c],!d.hidden&&0<d.value&&(b+=d.value);for(c=0;c<a.length;c++)d=this.chartData[c],d.percents=!d.hidden&&0<d.value?100*d.value/b:0},removeSmallSlices:function(){var a=this.chartData,b;for(b=a.length-1;0<=b;b--)a[b].percents<
this.groupPercent&&(this.groupValue+=a[b].value,a.splice(b,1))},animateAgain:function(){var a=this;a.startSlices();for(var b=0;b<a.chartData.length;b++){var c=a.chartData[b];c.started=!1;var d=c.wedge;d&&(d.setAttr("opacity",a.startAlpha),d.translate(c.startX,c.startY));if(d=c.labelSet)d.setAttr("opacity",a.startAlpha),d.translate(c.startX,c.startY)}b=a.startDuration;0<b?(b=setTimeout(function(){a.pullSlices.call(a)},1200*b),a.timeOuts.push(b)):a.pullSlices()},measureMaxLabel:function(){var a=this.chartData,
b=0,c;for(c=0;c<a.length;c++){var d=a[c],g=this.formatString(this.labelText,d),f=this.labelFunction;f&&(g=f(d,g));d=k.text(this.container,g,this.color,this.fontFamily,this.fontSize);g=d.getBBox().width;g>b&&(b=g);d.remove()}return b}})})();(function(){var k=window.AmCharts;k.AmPieChart=k.Class({inherits:k.AmSlicedChart,construct:function(a){this.type="pie";k.AmPieChart.base.construct.call(this,a);this.cname="AmPieChart";this.pieBrightnessStep=30;this.minRadius=10;this.depth3D=0;this.startAngle=90;this.angle=this.innerRadius=0;this.startRadius="500%";this.pullOutRadius="20%";this.labelRadius=20;this.labelText="[[title]]: [[percents]]%";this.balloonText="[[title]]: [[percents]]% ([[value]])\n[[description]]";this.previousScale=1;this.adjustPrecision=
!1;this.gradientType="radial";k.applyTheme(this,a,this.cname)},drawChart:function(){k.AmPieChart.base.drawChart.call(this);var a=this.chartData;if(k.ifArray(a)){if(0<this.realWidth&&0<this.realHeight){k.VML&&(this.startAlpha=1);var b=this.startDuration,c=this.container,d=this.updateWidth();this.realWidth=d;var g=this.updateHeight();this.realHeight=g;var f=k.toCoordinate,h=f(this.marginLeft,d),e=f(this.marginRight,d),z=f(this.marginTop,g)+this.getTitleHeight(),n=f(this.marginBottom,g),A,B,l,x=k.toNumber(this.labelRadius),
p=this.measureMaxLabel();p>this.maxLabelWidth&&(p=this.maxLabelWidth);this.labelText&&this.labelsEnabled||(x=p=0);A=void 0===this.pieX?(d-h-e)/2+h:f(this.pieX,this.realWidth);B=void 0===this.pieY?(g-z-n)/2+z:f(this.pieY,g);l=f(this.radius,d,g);l||(d=0<=x?d-h-e-2*p:d-h-e,g=g-z-n,l=Math.min(d,g),g<d&&(l/=1-this.angle/90,l>d&&(l=d)),g=k.toCoordinate(this.pullOutRadius,l),l=(0<=x?l-1.8*(x+g):l-1.8*g)/2);l<this.minRadius&&(l=this.minRadius);g=f(this.pullOutRadius,l);z=k.toCoordinate(this.startRadius,l);
f=f(this.innerRadius,l);f>=l&&(f=l-1);n=k.fitToBounds(this.startAngle,0,360);0<this.depth3D&&(n=270<=n?270:90);n-=90;360<n&&(n-=360);d=l-l*this.angle/90;for(h=p=0;h<a.length;h++)e=a[h],!0!==e.hidden&&(p+=k.roundTo(e.percents,this.pf.precision));p=k.roundTo(p,this.pf.precision);this.tempPrec=NaN;this.adjustPrecision&&100!=p&&(this.tempPrec=this.pf.precision+1);for(var D,h=0;h<a.length;h++)if(e=a[h],!0!==e.hidden&&(this.showZeroSlices||0!==e.percents)){var r=360*e.percents/100,p=Math.sin((n+r/2)/180*
Math.PI),C=d/l*-Math.cos((n+r/2)/180*Math.PI),q=this.outlineColor;q||(q=e.color);var v=this.alpha;isNaN(e.alpha)||(v=e.alpha);q={fill:e.color,stroke:q,"stroke-width":this.outlineThickness,"stroke-opacity":this.outlineAlpha,"fill-opacity":v};e.url&&(q.cursor="pointer");q=k.wedge(c,A,B,n,r,l,d,f,this.depth3D,q,this.gradientRatio,e.pattern,this.path,this.gradientType);k.setCN(this,q,"pie-item");k.setCN(this,q.wedge,"pie-slice");k.setCN(this,q,e.className,!0);this.addEventListeners(q,e);e.startAngle=
n;a[h].wedge=q;0<b&&(this.chartCreated||q.setAttr("opacity",this.startAlpha));e.ix=p;e.iy=C;e.wedge=q;e.index=h;e.label=null;v=c.set();if(this.labelsEnabled&&this.labelText&&e.percents>=this.hideLabelsPercent){var m=n+r/2;0>m&&(m+=360);360<m&&(m-=360);var t=x;isNaN(e.labelRadius)||(t=e.labelRadius,0>t&&(e.skipTick=!0));var r=A+p*(l+t),E=B+C*(l+t),w,u=0;isNaN(D)&&350<m&&1<a.length-h&&(D=h-1+Math.floor((a.length-h)/2));if(0<=t){var y;90>=m&&0<=m?(y=0,w="start",u=8):90<=m&&180>m?(y=1,w="start",u=8):
180<=m&&270>m?(y=2,w="end",u=-8):270<=m&&354>=m?(y=3,w="end",u=-8):354<=m&&(h>D?(y=0,w="start",u=8):(y=3,w="end",u=-8));e.labelQuarter=y}else w="middle";m=this.formatString(this.labelText,e);(t=this.labelFunction)&&(m=t(e,m));t=e.labelColor;t||(t=this.color);""!==m&&(m=k.wrappedText(c,m,t,this.fontFamily,this.fontSize,w,!1,this.maxLabelWidth),k.setCN(this,m,"pie-label"),k.setCN(this,m,e.className,!0),m.translate(r+1.5*u,E),m.node.style.pointerEvents="none",e.ty=E,e.textX=r+1.5*u,v.push(m),this.axesSet.push(v),
e.labelSet=v,e.label=m);e.tx=r;e.tx2=r+u;e.tx0=A+p*l;e.ty0=B+C*l}r=f+(l-f)/2;e.pulled&&(r+=this.pullOutRadiusReal);e.balloonX=p*r+A;e.balloonY=C*r+B;e.startX=Math.round(p*z);e.startY=Math.round(C*z);e.pullX=Math.round(p*g);e.pullY=Math.round(C*g);this.graphsSet.push(q);if(0===e.alpha||0<b&&!this.chartCreated)q.hide(),v&&v.hide();n+=360*e.percents/100;360<n&&(n-=360)}0<x&&this.arrangeLabels();this.pieXReal=A;this.pieYReal=B;this.radiusReal=l;this.innerRadiusReal=f;0<x&&this.drawTicks();this.initialStart();
this.setDepths()}(a=this.legend)&&a.invalidateSize()}else this.cleanChart();this.dispDUpd()},setDepths:function(){var a=this.chartData,b;for(b=0;b<a.length;b++){var c=a[b],d=c.wedge,c=c.startAngle;0<=c&&180>c?d.toFront():180<=c&&d.toBack()}},arrangeLabels:function(){var a=this.chartData,b=a.length,c,d;for(d=b-1;0<=d;d--)c=a[d],0!==c.labelQuarter||c.hidden||this.checkOverlapping(d,c,0,!0,0);for(d=0;d<b;d++)c=a[d],1!=c.labelQuarter||c.hidden||this.checkOverlapping(d,c,1,!1,0);for(d=b-1;0<=d;d--)c=a[d],
2!=c.labelQuarter||c.hidden||this.checkOverlapping(d,c,2,!0,0);for(d=0;d<b;d++)c=a[d],3!=c.labelQuarter||c.hidden||this.checkOverlapping(d,c,3,!1,0)},checkOverlapping:function(a,b,c,d,g){var f,h,e=this.chartData,k=e.length,n=b.label;if(n){if(!0===d)for(h=a+1;h<k;h++)e[h].labelQuarter==c&&(f=this.checkOverlappingReal(b,e[h],c))&&(h=k);else for(h=a-1;0<=h;h--)e[h].labelQuarter==c&&(f=this.checkOverlappingReal(b,e[h],c))&&(h=0);!0===f&&100>g&&isNaN(b.labelRadius)&&(f=b.ty+3*b.iy,b.ty=f,n.translate(b.textX,
f),this.checkOverlapping(a,b,c,d,g+1))}},checkOverlappingReal:function(a,b,c){var d=!1,g=a.label,f=b.label;a.labelQuarter!=c||a.hidden||b.hidden||!f||(g=g.getBBox(),c={},c.width=g.width,c.height=g.height,c.y=a.ty,c.x=a.tx,a=f.getBBox(),f={},f.width=a.width,f.height=a.height,f.y=b.ty,f.x=b.tx,k.hitTest(c,f)&&(d=!0));return d}})})();