<script>
/**
* Original script is created by Lunametrics 
* https://www.lunametrics.com/labs/recipes/utmz-cookie-replicator-for-gtm/
* Modified by Analytics Mania https://www.analyticsmania.com/
*
* Data is stored in the __initialTrafficSource cookie in the following format; brackets
* indicate optional data and are aexcluded from the stored string:
*
* utmcsr=SOURCE|utmcmd=MEDIUM[|utmccn=CAMPAIGN][|utmcct=CONTENT]
* [|utmctr=TERM/KEYWORD]
*
* e.g.:
* utmcsr=example.com|utmcmd=affl-link|utmccn=foo|utmcct=bar|utmctr=biz
*/
(function(document) {

  var referrer = document.referrer;
  var gaReferral = {
    'utmcsr': '(direct)',
    'utmcmd': '(none)',
    'utmccn': '(not set)'
  };
  var thisHostname = document.location.hostname;
  var thisDomain = getDomain_(thisHostname);
  var referringDomain = getDomain_(document.referrer);
  var sessionCookie = getCookie_('__utmzzses');
  var cookieExpiration = new Date(+new Date() + 1000 * 60 * 60 * 24 * 30 * 24);
  var qs = document.location.search.replace('?', '');
  var hash = document.location.hash.replace('#', '');
  var gaParams = parseGoogleParams(qs + '#' + hash);
  //test//
  //test//
  var referringInfo = parseGaReferrer(referrer);
  var storedVals = getCookie_('__utmz') || getCookie_('__utmzz');
  var newCookieVals = [];
  var keyMap = {
    'utm_source': 'utmcsr',
    'utm_medium': 'utmcmd',
    'utm_campaign': 'utmccn',
    'utm_content': 'utmcct',
    'utm_term': 'utmctr',
    'gclid': 'utmgclid',
    'dclid': 'utmdclid'
  };

  var keyFilter = ['utmcsr', 'utmcmd', 'utmccn', 'utmcct', 'utmctr'];
  var keyName,
     values,
    _val,
    _key,
    raw,
    key,
    len,
    i;
    
  if (sessionCookie && referringDomain === thisDomain) {

    gaParams = null;
    referringInfo = null;

  }

  if (gaParams && (gaParams.utm_source || gaParams.gclid || gaParams.dclid)) {

    for (key in gaParams) {

      if (typeof gaParams[key] !== 'undefined') {

        keyName = keyMap[key];
        gaReferral[keyName] = gaParams[key];

      }

    }

   if (gaParams.gclid || gaParams.dclid) {

    gaReferral.utmcsr = 'google';
    gaReferral.utmcmd = gaReferral.utmgclid ? 'cpc' : 'cpm';

   }

  } else if (referringInfo) {

    gaReferral.utmcsr = referringInfo.source;
    gaReferral.utmcmd = referringInfo.medium;
    if (referringInfo.campaign) gaReferral.utmccn = referringInfo.campaign
    if (referringInfo.term) gaReferral.utmctr = referringInfo.term;

  } else if (storedVals) {

    values = {};
    raw = storedVals.split('|');
    len = raw.length;

    for (i = 0; i < len; i++) {

      _val = raw[i].split('=');
      _key = _val[0].split('.').pop();
      values[_key] = _val[1];

    }

    gaReferral = values;

  }

  for (key in gaReferral) {

    if (typeof gaReferral[key] !== 'undefined' && keyFilter.indexOf(key) >-1) {

      newCookieVals.push(key + '=' + gaReferral[key]);

    }

  }

  if (!getCookie_('initialTrafficSource')) {
    writeCookie_('initialTrafficSource', newCookieVals.join('|'), cookieExpiration, '/', thisDomain);
  }

  writeCookie_('__utmzzses', 1, null, '/', thisDomain);

//test
  function parseNaverGroupToCampaign(v){
     var NSA_cnc = [
      'grp-a001-01-000000018624529',
      'grp-a001-01-000000018624551',
      'grp-a001-01-000000018624538',
      'grp-a001-01-000000018624548',
      'grp-a001-01-000000018624554',
      'grp-a001-01-000000018624565',
      'grp-a001-01-000000018624539',
      'grp-a001-01-000000018624556',
      'grp-a001-01-000000018624516',
      'grp-a001-01-000000018624546',
      'grp-a001-01-000000018624526',
      'grp-a001-01-000000018624560',
      'grp-a001-01-000000018624520',
      'grp-a001-01-000000018624515',
      'grp-a001-01-000000018624629',
      'grp-a001-01-000000018624580',
      'grp-a001-01-000000018624624',
      'grp-a001-01-000000018624594',
      'grp-a001-01-000000018624569',
      'grp-a001-01-000000018624607',
      'grp-a001-01-000000018624568'
  ]
    var NSA_cnc_contents = [
      'grp-a001-01-000000017680533',
      'grp-a001-01-000000017680534',
      'grp-a001-01-000000017680535',
      'grp-a001-01-000000017680536',
      'grp-a001-01-000000017680537',
      'grp-a001-01-000000017680538',
      'grp-a001-01-000000017680539',
      'grp-a001-01-000000017680540',
      'grp-a001-01-000000017680543',
      'grp-a001-01-000000017680544',
      'grp-a001-01-000000017680545',
      'grp-a001-01-000000017680546'
  ]
    var NSA_3dp = [
      'grp-a001-01-000000019003691',
      'grp-a001-01-000000019003690',
      'grp-a001-01-000000019003697',
      'grp-a001-01-000000019003693',
      'grp-a001-01-000000019003692',
  ]
    var NSA_INJ = [
      'grp-a001-01-000000019177972',
      'grp-a001-01-000000019177971',
      'grp-a001-01-000000019177974',
      'grp-a001-01-000000019177973'
  ]
    var Brand = [
      "grp-a001-01-000000018667784",
      "grp-a001-01-000000018667776"
  ]
var NSA_cnc_Mobile = ['grp-a001-01-000000019162060']
var NSA_3dp_Mobile = ['grp-a001-01-000000019162086']
var NSA_INJ_Mobile = ['grp-a001-01-000000019178440']

    var testerVal = 0;

    if (NSA_cnc_contents.includes(v)){
      var testerVal = "NSA_cnc_contents"
  }else if ( NSA_cnc.includes(v)){
      var testerVal = "NSA_cnc"            
  }else if ( NSA_3dp.includes(v)){
      var testerVal = "NSA_3dp"
  }else if ( NSA_INJ.includes(v)){
      var testerVal = "NSA_INJ"
  }else if ( Brand.includes(v)){
      var testerVal = "NSA_Brand"
  }else if (NSA_cnc_Mobile.includes(v)){
      var testerVal = "NSA_cnc_Mobile"
  }else if (NSA_3dp_Mobile.includes(v)){
      var testerVal = "NSA_3dp_Mobile"
  }else if (NSA_INJ_Mobile.includes(v)){
      var testerVal = "NSA_INJ_Mobile"
  }else {
      var testerVal = "naver_broken"
  }
   return testerVal
  }
  //test
  function parseNaverParams(str) {
    if(str.includes('n_media')){
        paramObj = {};
        //그룹 전후방 탐색 정규표현식
        //var re = /(?<=\Wn_ad_group=).*?(?=\&)/
        var re = /(?=n_ad_group=).*?(?=\&)/
        var naverAdGroup = re.exec(str)[0]
        var naverAdGroup_replaced = naverAdGroup.replace('n_ad_group=','')
      }
          return naverAdGroup_replaced ;
    };
//test

  function parseGoogleParams(str) {

    var campaignParams = ['source', 'medium', 'campaign', 'term', 'content'];
    var regex = new RegExp('(utm_(' + campaignParams.join('|') + ')|(d|g)clid)=.*?([^&#]*|$)', 'gi');
    var gaParams = str.match(regex);
    var paramsObj,
      vals,
      len,
      i;

    if (gaParams) {

      paramsObj = {};
      len = gaParams.length;

      for (i = 0; i < len; i++) {

        vals = gaParams[i].split('=');

        if (vals) {

          paramsObj[vals[0]] = vals[1];

        }

       }

     }

     return paramsObj;

  }

  function parseGaReferrer(referrer) {

    if (!referrer) return;

    var searchEngines = {
      'daum.net': {
        'p': 'q',
        'n': 'daum'
      },
      'eniro.se': {
        'p': 'search_word',
        'n': 'eniro'
       },
      'naver.com': {
        'p': 'query',
        'n': 'naver'
      },
      'yahoo.com': {
        'p': 'p',
        'n': 'yahoo'
      },
      'msn.com': {
        'p': 'q',
        'n': 'msn'
      },
      'bing.com': {
        'p': 'q',
        'n': 'live'
      },
      'aol.com': {
        'p': 'q',
        'n': 'aol'
      },
      'lycos.com': {
        'p': 'q',
        'n': 'lycos'
      },
      'ask.com': {
        'p': 'q',
        'n': 'ask'
      },
      'altavista.com': {
        'p': 'q',
        'n': 'altavista'
      },
      'search.netscape.com': {
        'p': 'query',
        'n': 'netscape'
      },
      'cnn.com': {
        'p': 'query',
        'n': 'cnn'
      },
      'about.com': {
        'p': 'terms',
        'n': 'about'
      },
      'mamma.com': {
        'p': 'query',
        'n': 'mama'
      },
      'alltheweb.com': {
        'p': 'q',
        'n': 'alltheweb'
      },
      'voila.fr': {
        'p': 'rdata',
        'n': 'voila'
      },
      'search.virgilio.it': {
        'p': 'qs',
        'n': 'virgilio'
      },
      'baidu.com': {
        'p': 'wd',
        'n': 'baidu'
      },
      'alice.com': {
        'p': 'qs',
        'n': 'alice'
      },
      'yandex.com': {
        'p': 'text',
        'n': 'yandex'
      },
      'najdi.org.mk': {
        'p': 'q',
        'n': 'najdi'
      },
      'seznam.cz': {
        'p': 'q',
        'n': 'seznam'
      },
      'search.com': {
        'p': 'q',
        'n': 'search'
      },
      'wp.pl': {
        'p': 'szukaj ',
        'n': 'wirtulana polska'
      },
      'online.onetcenter.org': {
        'p': 'qt',
        'n': 'o*net'
      },
      'szukacz.pl': {
        'p': 'q',
        'n': 'szukacz'
      },
      'yam.com': {
        'p': 'k',
        'n': 'yam'
      },
      'pchome.com': {
        'p': 'q',
        'n': 'pchome'
      },
      'kvasir.no': {
        'p': 'q',
        'n': 'kvasir'
      },
      'sesam.no': {
        'p': 'q',
        'n': 'sesam'
      },
      'ozu.es': {
        'p': 'q',
        'n': 'ozu '
      },
      'terra.com': {
        'p': 'query',
        'n': 'terra'
      },
      'mynet.com': {
        'p': 'q',
        'n': 'mynet'
      },
     'ekolay.net': {
        'p': 'q',
        'n': 'ekolay'
     },
     'rambler.ru': {
       'p': 'words',
       'n': 'rambler'
     },
     'google': {
       'p': 'q',
       'n': 'google'
     }
   };
   var a = document.createElement('a');
   var values = {};
   var searchEngine,
     termRegex,
     term;

   a.href = referrer;

   // Shim for the billion google search engines
   if (a.hostname.indexOf('google') > -1) {

    referringDomain = 'google';

   }

  if (searchEngines[referringDomain]) {

    searchEngine = searchEngines[referringDomain];
    termRegex = new RegExp(searchEngine.p + '=.*?([^&#]*|$)', 'gi');
    term = a.search.match(termRegex);
    
    //test//
    if(searchEngine.n == 'naver'){
      naverAdGroup = parseNaverParams(qs);
      var naverCampaign = parseNaverGroupToCampaign(naverAdGroup);

      if(naverAdGroup){
        values.source = 'search.naver.com'
        values.campaign = naverCampaign
        values.medium = 'cpc';
        values.term = (term ? term[0].split('=')[1] : '') || '(not provided)';        
      }else{
        values.source = searchEngine.n;
        values.medium = 'organic';
        values.term = (term ? term[0].split('=')[1] : '') || '(not provided)';
      }
    } else if (searchEngine.n != 'naver'){
        values.source = searchEngine.n;
        values.medium = 'organic';
        values.term = (term ? term[0].split('=')[1] : '') || '(not provided)';

    }
   } else if (referringDomain !== thisDomain) {

    values.source = a.hostname;
    values.medium = 'referral';

  }

   return values;
  }
    
function writeCookie_(name, value, expiration, path, domain) {

    var str = name + '=' + value + ';';
    if (expiration) str += 'Expires=' + expiration.toGMTString() + ';';
    if (path) str += 'Path=' + path + ';';
    if (domain) str += 'Domain=' + domain + ';';

    document.cookie = str;

}

      function getCookie_(name) {

        var cookies = '; ' + document.cookie
        var cvals = cookies.split('; ' + name + '=');

        if (cvals.length > 1) return cvals.pop().split(';')[0];

      }

function getDomain_(url) {

  if (!url) return;

  var a = document.createElement('a');
  a.href = url;

  try {

    return a.hostname.match(/[^.]*\.[^.]{2,3}(?:\.[^.]{2,3})?$/)[0];

  } catch(squelch) {}

 }

})(document);
</script>