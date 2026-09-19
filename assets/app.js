(function(){
"use strict";
var $=function(s,r){return (r||document).querySelector(s)};
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var usd=function(n,d){if(!isFinite(n))return "—";return n.toLocaleString("en-US",{style:"currency",currency:"USD",maximumFractionDigits:d==null?0:d})};
var pct=function(n,d){if(!isFinite(n))return "—";return n.toFixed(d==null?2:d)+"%"};
var num=function(id){var el=document.getElementById(id);if(!el)return NaN;var v=parseFloat(String(el.value).replace(/[^0-9.\-]/g,""));return isNaN(v)?0:v};
var set=function(id,v){var el=document.getElementById(id);if(el)el.textContent=v};
var R=window.CP_RATES||{prime:6.75};
var C=window.CP_CONFIG||{partners:{}};

/* nav */
var t=$(".menu-toggle");if(t)t.addEventListener("click",function(){var n=$(".nav");n.classList.toggle("open");t.setAttribute("aria-expanded",n.classList.contains("open"))});

/* finance core */
function pmt(P,aprPct,n){var r=aprPct/100/12;if(n<=0)return NaN;if(r===0)return P/n;return P*r/(1-Math.pow(1+r,-n))}
/* periodic IRR by bisection: net cash received now vs equal payments */
function irr(net,pay,n){var lo=0,hi=1;if(pay*n<=net)return 0;for(var i=0;i<200;i++){var m=(lo+hi)/2;var pv=m===0?pay*n:pay*(1-Math.pow(1+m,-n))/m;if(pv>net)lo=m;else hi=m}return (lo+hi)/2}
function sbaSpread(amount){if(amount<=50000)return 6.5;if(amount<=250000)return 6.0;if(amount<=350000)return 4.5;return 3.0}

/* delegated recalculation */
var calcs={
  loan:function(){
    var P=num("amount"),apr=num("apr"),n=num("term"),fee=num("fee");
    var m=pmt(P,apr,n),total=m*n,interest=total-P,feeAmt=P*fee/100;
    var eff=irr(P-feeAmt,m,n)*12*100;
    set("o-payment",usd(m));set("o-interest",usd(interest));set("o-fee",usd(feeAmt));
    set("o-total",usd(total+feeAmt));set("o-eff",pct(eff));
  },
  sba:function(){
    var P=num("amount"),n=num("term")*12,spread=sbaSpread(P),max=R.prime+spread;
    var rateEl=document.getElementById("rate");
    if(rateEl&&!rateEl.dataset.touched){rateEl.value=max.toFixed(2)}
    var apr=num("rate");
    var m=pmt(P,apr,n),total=m*n;
    set("o-payment",usd(m));set("o-interest",usd(total-P));set("o-total",usd(total));
    set("o-max",pct(max)+" (Prime "+pct(R.prime)+" + "+spread.toFixed(1)+"%)");
    set("o-guar",P<=150000?"85%":"75%");
    var w=document.getElementById("o-warn");
    if(w)w.textContent=P>5000000?"Standard 7(a) loans cap at $5,000,000.":(apr>max?"This rate is above the SBA variable-rate maximum for this loan size.":"");
  },
  mca:function(){
    var adv=num("advance"),fr=num("factor"),days=num("days"),fees=num("fees");
    var payback=adv*fr,daily=days>0?payback/days:NaN,cost=payback-adv+fees;
    var r=irr(adv-fees,daily,days),apr=r*252*100;
    set("o-payback",usd(payback));set("o-daily",usd(daily,2));set("o-cost",usd(cost));set("o-apr",pct(apr,1));
    var w=document.getElementById("o-warn");if(w){w.className=apr>60?"warn":"good";w.textContent=apr>60?"Triple-digit or high double-digit APR territory. Compare a line of credit or term loan first.":"Relatively low cost for an MCA."}
  },
  factoring:function(){
    var inv=num("invoice"),advPct=num("advpct"),fee=num("feepct"),days=num("days");
    var advance=inv*advPct/100,feeAmt=inv*fee/100*Math.max(1,Math.ceil(days/30));
    var rebate=inv-advance-feeAmt,apr=advance>0&&days>0?feeAmt/advance*365/days*100:NaN;
    set("o-advance",usd(advance));set("o-fee",usd(feeAmt));set("o-rebate",usd(rebate));set("o-apr",pct(apr,1));
  },
  dscr:function(){
    var noi=num("noi"),debt=num("existing"),P=num("amount"),apr=num("apr"),n=num("term");
    var newDs=pmt(P,apr,n)*12,total=debt+newDs,d=total>0?noi/total:NaN;
    var capacity=Math.max(0,noi/1.25-debt),r=apr/100/12,maxLoan=r>0?(capacity/12)*(1-Math.pow(1+r,-n))/r:capacity/12*n;
    set("o-dscr",isFinite(d)?d.toFixed(2)+"x":"—");set("o-newds",usd(newDs));set("o-max",usd(maxLoan));
    var w=document.getElementById("o-warn");if(w){if(d>=1.25){w.className="good";w.textContent="Meets the common 1.25x lender threshold."}else{w.className="warn";w.textContent="Below 1.25x. Most bank and SBA lenders will push back."}}
  },
  equipment:function(){
    var price=num("price"),down=num("down"),apr=num("apr"),n=num("term"),lease=num("lease"),buyout=num("buyout");
    var P=Math.max(0,price-down),m=pmt(P,apr,n),loanTotal=m*n+down,leaseTotal=lease*n+buyout;
    set("o-payment",usd(m));set("o-loantotal",usd(loanTotal));set("o-leasetotal",usd(leaseTotal));
    set("o-diff",(leaseTotal>loanTotal?"Loan saves ":"Lease saves ")+usd(Math.abs(leaseTotal-loanTotal)));
  },
  valuation:function(){
    var sde=num("sde"),lo=num("mlo"),hi=num("mhi"),debt=num("debt");
    set("o-low",usd(sde*lo-debt));set("o-high",usd(sde*hi-debt));set("o-mid",usd(sde*(lo+hi)/2-debt));
    set("o-sba",usd(sde*(lo+hi)/2*0.9));
  },
  runway:function(){
    var cash=num("cash"),burn=num("burn"),rev=num("rev"),g=num("growth")/100,months=0,c=cash,r=rev;
    if(burn<=rev){set("o-months","Default alive");set("o-date","Revenue covers costs");set("o-raise","—");return}
    while(c>0&&months<240){c-=(burn-r);r*=1+g;months++;if(r>=burn)break}
    var alive=r>=burn&&c>0;
    set("o-months",alive?"Default alive":months+" months");
    var d=new Date();d.setMonth(d.getMonth()+months);
    set("o-date",alive?"Break-even in "+months+" months":d.toLocaleDateString("en-US",{month:"short",year:"numeric"}));
    set("o-raise",alive?"—":d.getMonth()>5?"Start raising by "+new Date(d.getFullYear(),d.getMonth()-6,1).toLocaleDateString("en-US",{month:"short",year:"numeric"}):"Start raising now");
  }
};
var form=$("form.calc-form");
if(form&&calcs[form.dataset.calc]){
  var run=calcs[form.dataset.calc];
  form.addEventListener("input",function(e){if(e.target.id==="rate")e.target.dataset.touched="1";run()});
  form.addEventListener("submit",function(e){e.preventDefault();run()});
  run();
}

/* funding matcher */
var mf=$("#matcher");
if(mf){
  var products={
    sba:{name:"SBA 7(a) loan",desc:"Lowest-cost government-backed debt. Slow (30–90 days) and paperwork-heavy.",guide:"/guides/sba-7a-loans/"},
    term:{name:"Online term loan",desc:"Lump sum, fixed payments, funded in days. Costs more than a bank.",guide:"/guides/business-line-of-credit/"},
    loc:{name:"Business line of credit",desc:"Draw only what you need, pay interest only on what you use.",guide:"/guides/business-line-of-credit/"},
    equipment:{name:"Equipment financing",desc:"The equipment is the collateral, so approval is easier.",guide:"/guides/equipment-financing/"},
    factoring:{name:"Invoice factoring",desc:"Turn unpaid B2B invoices into cash within 1–2 days.",guide:"/guides/invoice-factoring/"},
    rbf:{name:"Revenue-based financing",desc:"Repay as a share of revenue. Fits SaaS and e-commerce.",guide:"/guides/revenue-based-financing/"},
    mca:{name:"Merchant cash advance",desc:"Fastest and easiest approval, and the most expensive. Use it as a last resort.",guide:"/guides/merchant-cash-advance-vs-loan/"},
    equity:{name:"Equity / angel investment",desc:"For high-growth startups. No repayment, but you give up ownership.",guide:"/guides/startup-funding-options/"}
  };
  var val=function(n){var el=$('input[name="'+n+'"]:checked',mf);return el?el.value:null};
  var score=function(){
    var tib=val("tib"),rev=val("rev"),cr=val("credit"),sp=val("speed"),use=val("use"),amt=val("amt");
    if(!tib||!rev||!cr||!sp||!use||!amt)return null;
    var s={sba:0,term:0,loc:0,equipment:0,factoring:0,rbf:0,mca:0,equity:0};
    var tibN={"0":0,"1":1,"2":2,"3":3}[tib],revN={"0":0,"1":1,"2":2,"3":3}[rev],crN={"0":0,"1":1,"2":2,"3":3}[cr];
    s.sba+=(tibN>=2?3:-4)+(crN>=2?3:-4)+(sp==="slow"?3:-3)+(revN>=1?1:-2)+(amt==="xl"||amt==="l"?2:0);
    s.term+=(tibN>=1?2:-3)+(crN>=1?2:-2)+(revN>=1?2:-3)+(sp!=="slow"?1:0);
    s.loc+=(tibN>=1?2:-3)+(crN>=2?2:-1)+(revN>=1?2:-3)+(use==="working"?3:0)+(amt==="s"||amt==="m"?1:-1);
    s.equipment+=(use==="equipment"?7:-6)+(crN>=1?1:0);
    s.factoring+=(use==="invoices"?7:-5)+(crN===0?1:0);
    s.rbf+=(revN>=2?3:-3)+(use==="growth"?3:0)+(crN<=1?1:0);
    s.mca+=(sp==="now"?2:-1)+(crN===0?2:-2)+(revN>=1?1:-3)-2;
    s.equity+=(use==="growth"?2:-2)+(tibN===0?3:-2)+(revN===0?2:-1)+(amt==="xl"?2:0);
    return Object.keys(s).map(function(k){return {k:k,v:s[k]}}).sort(function(a,b){return b.v-a.v}).slice(0,3);
  };
  var render=function(){
    var top=score(),box=$("#match-results");if(!box)return;
    if(!top){box.innerHTML='<p class="small muted">Answer all six questions to see your matches.</p>';return}
    box.innerHTML=top.map(function(x,i){
      var p=products[x.k],partner=(C.partners||{})[x.k],href=partner&&partner.url?partner.url:p.guide,
          label=partner&&partner.url?("Check rates with "+partner.name):"Read the guide",
          rel=partner&&partner.url?' rel="sponsored noopener" target="_blank"':"";
      return '<div class="result"><div><span class="fit'+(i?' mid':'')+'">'+(i?"Also consider":"Best fit")+'</span><h4>'+p.name+'</h4><p>'+p.desc+'</p></div><a class="btn sm'+(i?' ghost':'')+'" href="'+href+'"'+rel+' data-evt="match_click" data-product="'+x.k+'">'+label+'</a></div>';
    }).join("");
    if(window.gtag)window.gtag("event","match_complete",{top:top[0].k});
  };
  mf.addEventListener("change",render);render();
}

/* outbound tracking */
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[rel~=sponsored]");if(a&&window.gtag)window.gtag("event","affiliate_click",{partner:a.dataset.product||a.hostname,page:location.pathname})});
})();
