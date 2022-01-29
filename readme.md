![image-20220130000139599](https://s2.loli.net/2022/01/30/nkI5B9DcPQzX3Us.png)

Usage:

+ Modify `config.yml`
+ Mkdir `./output/`
+ Run `python3 crawler.py`

GitHub Repo: https://github.com/c7w/TsinghuaMoocCaptionCrawler

Blog: https://c7w.tech/yuketang-caption-crawler/

<!--more-->

## 爬取过程

### 乱抓

+ **利用 Break on change 查看脚本运行状况**

首先自然是取字幕所在的那个 xt-caption 元素，然后打上 Break on change.

> 在 Javascript 调试中，我们经常会使用到断点调试。
>
> 其实，在 DOM 结构的调试中，我们也可以使用断点方法，这就是 DOM Breakpoint（DOM 断点）。
>
> 具体的使用方法：
>
> 在 Chrome 浏览器中，打开开发者工具，先选中一个页面元素，然后点击鼠标右键，依次点击菜单中的 “Break on …” —— 勾选 “Attributes modifications”。
>
> 刷新页面，当该元素的属性发生变化时，就会暂停脚本的执行，并且定位到改变发生的地方。
>
> 除了可以监视 DOM 元素本身的属性变化，Chrome 还可以监视其子元素的变化，以及何时元素被删除。

![image-20220129222222643](https://s2.loli.net/2022/01/29/xYiujWzwTfM7mIv.png)

+ **查看调用栈**

然后是当 Trigger 了字幕更改 Event 之后，逐个检查这里的调用栈。

![image-20220127155350265](https://s2.loli.net/2022/01/27/e9qdIOvc2butLP3.png)

逐级查看后，这里（页面加载 caption 属性的时候）看起来像是在发可疑的请求，然后找到了一个地址：

![image-20220127155631381](https://s2.loli.net/2022/01/27/NoOutDYEpwHPzy3.png)

然后在 HTML 里面全文检索竟然找到了一样的地址。于是我们就得到了我们的第一个关键词 `subtitle_parse`。

![image-20220127155810865](https://s2.loli.net/2022/01/27/HdU58pV4NkJyASC.png)

+ **查看字幕源数据**

打开这个网页，发现里面就是纯字母数据。

![image-20220127160055541](https://s2.loli.net/2022/01/27/uGwhPFHA176dXKy.png)

即使是开无痕浏览也可以打开，说明不记录 Cookies。

![image-20220129222439327](https://s2.loli.net/2022/01/29/dJBibYkN9enuEtx.png)

然后本来想直接用 Python 写批量抓取脚本，结果写了一段发现这个字幕元素竟然也是晚加载：

+ `Crawler.py`

```python
import requests
from bs4 import BeautifulSoup

def getCookies(filename):
    f = open(filename)
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    data = f.readline().replace(" ", "").replace("\"", "").replace("\n", "").split(";")
    result = {}
    for entry in data:
        if '=' in entry:
            entryGroup = entry.split("=")
            result[entryGroup[0]] = entryGroup[1]
    return result

def trim(str):
    return str.replace(" ", '')\
              .replace("\n", '')

def fetch_single_video(url):
    url = 'https://tsinghua.yuketang.cn/pro/lms/8NpUsbr6GZH/3029907/video/2224317'
    cookies = getCookies('./cookies')
    
    response = requests.get(url, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'},
                            cookies=getCookies("./cookies"))
    
    response.encoding = 'utf-8'

    html = response.text.strip()
    soup = BeautifulSoup(html, 'html.parser')
    f = open('./a.txt', 'w+', encoding='utf-8')
    f.write(soup.prettify())

if __name__ == "__main__":
    fetch_single_video(2)
```

其中 `./cookies` 里面放的是使用 `EditThisCookie` extension 导出的 txt 格式的 Cookies.

![image-20220129222822889](https://s2.loli.net/2022/01/29/8CIt4g7kFJLoxXp.png)

发现这就是个 Vue 搭的前端网站，而且是晚加载的模式：

```html
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8"/>
  <meta content="text/html; charset=utf-8" http-equiv="content-type"/>
  <meta content="width=device-width,initial-scale=1,user-scalable=no" name="viewport"/>
  <meta content="no-cache" http-equiv="Pragma"/>
  <meta content="no-transform " http-equiv="Cache-Control"/>
  <meta content="no-siteapp" http-equiv="Cache-Control"/>
  <meta content="no-cache" http-equiv="Cache-Control"/>
  <meta content="0" http-equiv="Expires"/>
  <meta content="雨课堂, 清华大学, 智慧教学, 翻转课堂, 混合式教学, 教学工具, 教学软件" name="keywords"/>
  <meta content="雨课堂是清华大学和学堂在线共同推出的新型智慧教学解决方案，是教育部在线教育研究中心的最新研究成果，致力于快捷免费的为所有教学过程提供数据化、智能化的信息支持。" name="Description"/>
  <link href="//proxt-cdn.xuetangx.com" rel="dns-prefetch"/>
  <link href="//static-cdn.xuetangx.com" rel="dns-prefetch"/>
  <link href="//qn-next.xuetangx.com" rel="dns-prefetch"/>
  <link href="//s.xuetangx.com" ref="dns-prefetch"/>
  <link href="//storagecdn.xuetangx.com" rel="dns-prefetch"/>
  <link href="/static/images/favicon.ico" id="J_logo_ico" rel="shortcut icon" type="image/x-icon"/>
  <link href="//at.alicdn.com/t/font_2914297_aiu6672k7jm.css" rel="stylesheet"/>
  <script src="//at.alicdn.com/t/font_2914297_aiu6672k7jm.js">
  </script>
  <link href="//at.alicdn.com/t/font_956123_fw8xrxx7a4u.css" rel="stylesheet"/>
  <script src="//at.alicdn.com/t/font_956123_fw8xrxx7a4u.js">
  </script>
  <script defer="defer" src="https://code.bdstatic.com/npm/@baiducloud/sdk@1.0.0-rc.19/dist/baidubce-sdk.bundle.min.js">
  </script>
  <script src="https://storagecdn.xuetangx.com/public_assets/xuetangx/aliyun-upload-sdk/lib/aliyun-oss-sdk-5.3.1.min.js">
  </script>
  <script src="https://storagecdn.xuetangx.com/public_assets/xuetangx/aliyun-upload-sdk/aliyun-upload-sdk-1.5.0.min.js">
  </script>
  <script src="https://ssl.captcha.qq.com/TCaptcha.js">
  </script>
  <script src="https://web-stat.jiguang.cn/web-janalytics/scripts/janalytics-web.min.js" type="text/javascript">
  </script>
  <title>
  </title>
  <style>
   .ie-hint{display:none;position:relative;left:0;top:0;z-index:100000;width:100%;height:40px;line-height:40px;font-size:16px;text-align:center;background:#fff8bf;color:#4a4a4a}.ie-hint img{vertical-align:middle}.ie-hint a{color:#639ef4}.ie-hint .icon{font-size:19px;vertical-align:middle}#close-ie-hint{position:absolute;right:10px;top:10px;width:20px}@media print{.no-print{visibility:hidden}}
  </style>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/styles.929a58a998b9713fd859.css" rel="stylesheet"/>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/142.c165ba72220097b7a058.css" rel="stylesheet"/>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/572.05955aff5704fb65b9f1.css" rel="stylesheet"/>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/1281.eb0a92d7006955f1e691.css" rel="stylesheet"/>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/1269.ecf512d0ea931c4302bf.css" rel="stylesheet"/>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/1255.a02392a53202a02f00cd.css" rel="stylesheet"/>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/1300.4c085e415259addde382.css" rel="stylesheet"/>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/1291.3fe43df5becd9c98e83b.css" rel="stylesheet"/>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/1301.d0128c8af9fd07b09a38.css" rel="stylesheet"/>
  <link href="https://proxt-cdn.xuetangx.com/fe-proxtassets/1302.d0128c8af9fd07b09a38.css" rel="stylesheet"/>
 </head>
 <body>
  <div class="ie-hint" id="ie-hint">
   <img alt="" class="icon" src="https://qn-sfe.yuketang.cn/o_1ecmgnntbah3150231eevqmpja.png"/>
   当前浏览器可能无法正常使用
   <span id="school-name">
   </span>
   ， 推荐使用
   <a href="http://xiazai.sogou.com/detail/34/8/6262355089742005676.html" target="_blank" title="chrome">
    chrome浏览器、
   </a>
   <a href="http://www.firefox.com.cn/download/" target="_blank" title="火狐">
    火狐浏览器
   </a>
   或
   <a href="http://browser.qq.com/?adtag=SEM1" target="_blank" title="QQ浏览器">
    QQ浏览器
   </a>
   。
   <img alt="" id="close-ie-hint" src="https://qn-sfe.yuketang.cn/o_1ecmgnntcn761v2p1vcn1i851jqcb.png"/>
  </div>
  <div id="app">
  </div>
  <script type="text/x-mathjax-config">
   window.MathJax.Hub.Config({
				showProcessingMessages: false, //关闭js加载过程信息
				messageStyle: "none", //不显示信息
				jax: ["input/TeX", "output/HTML-CSS"],
				showMathMenu: false, //关闭右击菜单显示
				tex2jax: {
				inlineMath: [
					['$','$'],
					["\\(","\\)"],
					['[mathjaxinline]','[/mathjaxinline]']
				],
				displayMath: [
					['$$','$$'],
					["\\[","\\]"],
					['[mathjax]','[/mathjax]']
				],
				processEscapes: true
				},
				"HTML-CSS": { availableFonts: ["TeX"] }
			});
  </script>
  <script defer="true" src="https://s.xuetangx.com/resource/mathjax/MathJax.js?config=TeX-MML-AM_HTMLorMML-full" type="text/javascript">
  </script>
  <script>
   var _mtac={performanceMonitor:1,senseQuery:1};!function(){var t=document.createElement("script");t.src="https://pingjs.qq.com/h5/stats.js?v2.0.4",t.setAttribute("name","MTAH5"),t.setAttribute("sid","500535776"),t.setAttribute("cid","500613279");var e=document.getElementsByTagName("script")[0];e.parentNode.insertBefore(t,e)}()
  </script>
  <script>
   window.UEDITOR_HOME_URL="/vue_images/js/ueditor/"
  </script>
  <script>
   var ieHint=document.getElementById("ie-hint"),closeIeHintBtn=document.getElementById("close-ie-hint");closeIeHintBtn.onclick=function(){ieHint.style.display="none"};var ua=navigator.userAgent.toLocaleLowerCase();null==ua.match(/msie/)&&null==ua.match(/trident/)||(ieHint.style.display="block");var el=document.getElementById("school-name");el.innerText=/gdufemooc\.cn|gc\.xuetangonline\.com/g.test(window.location.host)?"广财慕课":"雨课堂"
  </script>
  <script>
   window.JAnalyticsInterface&&window.JAnalyticsInterface.init({appkey:"d651262356d93f6497b466bc",debugMode:!1,channel:"web",loc:!1,singlePage:!0})
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/manifest_c74775d18d54217265e2.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/231_38a88de77e34999627ab.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/569_bc3c767e5675a607dbbd.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1282_f9bb16a2941af9a9732e.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/133_78b4a2f4ec1e774e0cd7.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1236_3946732fbcdc70b913ab.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/99_a1791a23a69e2309f9f1.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/46_492686a3fb63a70f8537.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/55_29d1ee187d2ac1bf8576.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/63_7e9066f450ffae3dbf1f.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1256_7a55b42b33475074b3d3.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/119_75b24be79cbc0f38e9b5.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/117_59618d0ce41a577cd0a2.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/232_5b17f99d4219ca1a5b59.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/339_18c69c22659d338f44af.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/100_29dabc580c2213c93d8c.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/56_ca3e56863eb65145d5ef.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/47_1a6f41d3f0d03e528606.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1264_4f1e99a3b8cdc6a85310.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/336_48448e96f180a901248e.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/101_317e4792ce1ff0603658.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/60_1f97ad5d40dccb242d3c.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/59_0b81e0afe51de42239f4.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/48_f696c92ebfa6dbe3a1ac.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/50_9da5f4380a1dd62a4349.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/70_c7d3361bfc7496f5d803.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1265_046603f30d395e0e1099.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/230_43fd774de4f928a81aa1.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1283_cdf10be9a5df97cb7d46.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/338_f4f2d394eb1bd2e4a76e.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/116_b722a9793903aa54c4a3.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1266_b1f6eab4866937cd2334.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/335_2f5c77a15099004dd76d.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/132_67afce490fea2dc1441a.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1274_53106a71aa695ff1e11d.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/337_5f023640d90421312cf8.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1258_0513b6935105b9242092.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/187_1d921a816015be88fc98.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/140_1429b54afac3f6055d28.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/189_312d72f77e83bd9f27d2.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/236_dd7f542d4cd9f02617d4.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1220_07a737b91c2b22ee2d3f.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/137_274aba69f9f08e27032a.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/118_03f55e7d8630c32b7003.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/139_32cd669c513bcc12f0d8.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1239_00c23825dfd87a3592d2.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/135_f61430536202b9abeb3f.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/138_e9b0ca84dbbf77e36067.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/141_b23872740ac87e16f8a0.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/188_f2c1d703e3c638123d7c.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/136_62c77544e64cd5ab11f5.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1296_9a4770963b01517ef057.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/121_8311183faa6fc009705d.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/134_592e67bb4735225d8109.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/styles_58dd88566a7c28f3ead9.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1235_8188f874883aec589e8d.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1288_777c8223f036e812be31.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/571_10162dcb435848dccc4a.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/234_46302fa6da910e733695.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1289_24f0da49aa9672e5f66b.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/235_9c17d4274dbb108f05a0.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/142_5298840037f69140cb58.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1290_37149584899447655329.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/574_83911d6a3fc0bac17622.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/120_4d32aa2ec1486063ffd5.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1237_e7ef338fbf8b5abae028.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1254_e17ce52fb300bba23ecb.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/572_6009ef3a4252cf76550d.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1281_ac1f61a1ceac82ef5c3a.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1269_1f2a8d4c2f0d32f8015c.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1255_64cf7487e3b6ed9cf088.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1300_7963eccd7914586cfe07.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1291_0619decfb4f04b856012.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1301_d74f386080e2a40bf9ed.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1302_a6924788437f7f6a7f03.js">
  </script>
  <script src="https://proxt-cdn.xuetangx.com/fe-proxtassets/1287_07a707cc838c899e0e6a.js">
  </script>
 </body>
</html>
```

### 模拟

于是...想法就是模拟 JS 页面的加载...

仍然心存侥幸，想着不用油猴去写页面加载后运行的抓取脚本，或是不用 `PhantomJS` 写 JS 模拟（这两者都不够优雅），于是打开 DevTools 的 Network 页面模拟整个页面的加载过程：

![image-20220129225952673](https://s2.loli.net/2022/01/29/4OnxEIr7pWPLtUV.png)

我们想要搜索的信息是这个视频的字幕 ID，也就是 `https://tsinghua.yuketang.cn/mooc-api/v1/lms/service/subtitle_parse/?c_d=07AA3C78762F81A09C33DC5901307461&lg=0` 中的 `07AA3C78762F81A09C33DC5901307461`。对所有请求全文检索：

![image-20220129230159693](https://s2.loli.net/2022/01/29/c8YTzbfE2x9RjNr.png)

首先，因为我们最初并不知道这个 ID 是多少，所以以这个 ID 为目标 URL 的直接略去，因为这个 ID 肯定是以某种方式传到前端的。所以目光就放在了第三个和第四个两个请求上面，其中第三个请求的 URL 似乎很合适：

`[GET] https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/3029907/2224317/?sign=8NpUsbr6GZH&term=latest&uv_id=2598`

对照一下：

+ 3029907 是课程 ID
+ 2224317 是这个视频的 ID
+ 8NpUsbr6GZH 似乎是我这个学生的 ID（因为别的课程界面里面也带有这个 ID）
+ 2598 应该是 univ_ID，学校 ID

而且是 GET 请求，除了 Cookies 之外不需要别的 POST 参数。

尝试访问：

![image-20220129230600173](https://s2.loli.net/2022/01/29/qrRzEHdeusWP72N.png)

`XTBZ` 是个啥？难道 GET 请求还需要验证？回到发请求那里认真看了下 headers：

![image-20220129230701817](https://s2.loli.net/2022/01/29/2Ux9jtNVL13raCT.png)

好吧，确实有个 `xtbz` 字段，于是照着填上去...

```python
response = requests.get("https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/3029907/2224317/?sign=8NpUsbr6GZH&term=latest&uv_id=2598", headers={\
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                            'xtbz': 'cloud'},
                            cookies = getCookies("./cookies"))
```

结果：

```json
{'msg': '', 'data': {'sku_id': 813523, 'is_assessed': False, 'locked_reason': None, 'course_id': 1360275, 'classroom_short_name': None, 'university_id': '2598', 'score_deadline': 0, 'current_price': 0, 'id': 2224317, 'user_id': 20970575, 'content_info': {'status': 'post', 'video_user_play': None, 'expand_discuss': False, 'score_evaluation': {'score_proportion': {'proportion': 0.0}, 'score': 1.0, 'id': 6, 'name': '视 
频单元考核'}, 'download': [], 'is_score': True, 'is_discuss': True, 'remark': {'remark': ''}, 'cover_desc': '', 'cover_thumbnail': 'https://qn-next.xuetangx.com/15659303522988.jpg?imageView2/0/h/500', 'media': 
{'lecturer': 0, 'ccid': '07AA3C78762F81A09C33DC5901307461', 'start_time': 0, 'cover': 'https://qn-next.xuetangx.com/15659303522988.jpg', 'ccurl': '07AA3C78762F81A09C33DC5901307461', 'duration': 550, 'end_time': 0, 'live_palyback_url': '', 'live_url': '', 'type': 'video', 'teacher': []}, 'cover': 'https://qn-next.xuetangx.com/15659303522988.jpg', 'leaf_type_id': None, 'context': '<!DOCTYPE html><html><head></head><body>\n</body></html>'}, 'classroom_id': '3029907', 'leaf_type': 0, 'has_classend': True, 'upgrade_sku_status': None, 'price': 0, 'user_role': 
3, 'class_start_time': 1613959200000, 'upgrade_sku_id': None, 'be_in_force': False, 'teacher': {'org_name': '清华大学', 'picture': 'https://qn-next.xuetangx.com/15659303632348.jpg', 'name': '【教师名字】', 'department_name': '【教师院系】', 'intro': '【教师介绍】', 'job_title': '副教授'}, 'is_score': True, 'is_deleted': False, 'name': '开篇的话', 'is_locked': False, 'class_end_time': 1623596400000}, 'success': True}
```

好吧，看到 ccid 我们终于是拿到想要的东西了。这个 Response 里面打码了一些跟课程有关的内容（虽然已经泄露的差不多了吧x）

好的，现在来整理一下思路，截至目前我们已经获得了从一个视频在网页上外显的 ID 转换成其 CCID 的方法，也就是 `[GET] https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/[课程号]/[视频外显ID]/?sign=[学生ID]&term=latest&uv_id=2598`，然后`CCID = response.json()['data']['content_info']['media']['ccid']`，接着我们就能通过 `[GET] https://tsinghua.yuketang.cn/mooc-api/v1/lms/service/subtitle_parse/?c_d=[CCID]&lg=0` 来获取对应视频字幕。

下面我们还想优化，就是怎么把一个课程所有的 `[视频外显ID]` 全部拿出来，事实上这也是可以做到的，因为我们再仔细检查一下发送的这一堆请求，找到了：

`[GET] https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/course/chapter?cid=3029907&sign=8NpUsbr6GZH&term=latest&uv_id=2598`，请求了整个课程的信息，我们对其返回的 JSON 解码得到：

![image-20220129232309709](https://s2.loli.net/2022/01/29/KftCcXuOY73v5NR.png)

从这个 Response 里面我们能拿到所有视频的外显 ID。

### 调 API

+ `[GET] https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/course/chapter?cid=[课程ID]&sign=[学生ID]&term=latest&uv_id=2598` -> 视频外显 ID 的列表
+ `[GET] https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/[课程ID]/[视频外显ID]/?sign=[学生ID]&term=latest&uv_id=2598` -> 视频 CCID
+ `[GET] https://tsinghua.yuketang.cn/mooc-api/v1/lms/service/subtitle_parse/?c_d=[CCID]&lg=0` -> 视频字幕

整理成代码如下：

```python
def get_course_info(cid, sid):
    
    video_list = []
    
    url = f'''https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/course/chapter?cid={cid}&sign={sid}&term=latest&uv_id=2598'''
    cookies = getCookies('./cookies')
    response = requests.get(url, headers={\
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                            'xtbz': 'cloud'},
                            cookies = getCookies("./cookies"))
    
    data = response.json()
    chapter_list = data['data']['course_chapter']
    
    for chapter in chapter_list:
        leaves = chapter['section_leaf_list']
        for leaf in leaves:
            try:
                video_list.append(leaf['leaf_list'][0]['id'])
            except:
                pass
    
    return video_list

def get_caption(cid, sid, vid):
    url = f'''https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/{cid}/{vid}/?sign={sid}&term=latest&uv_id=2598'''
    cookies = getCookies('./cookies')
    response = requests.get(url, headers={\
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                            'xtbz': 'cloud'},
                            cookies = getCookies("./cookies"))
    
    data = response.json()
    video_name = data['data']['name']
    
    try:
        ccid = data['data']['content_info']['media']['ccid']
        if not ccid: raise BaseException("HTML Introduction. No video.")
        
        url = f'''https://tsinghua.yuketang.cn/mooc-api/v1/lms/service/subtitle_parse/?c_d={ccid}&lg=0'''
        cookies = getCookies('./cookies')
        response = requests.get(url, headers={\
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                                'xtbz': 'cloud'},
                                cookies = getCookies("./cookies"))
        
        data = response.json()
        data['start'] = [int(s) for s in data['start']]
        caption_list = list(zip(data['start'], data['text']))
        
        f = open(f"./output/[{vid}] {video_name}.txt", 'w+', encoding='utf-8')
        
        for caption in caption_list:
            f.write("%-10d  %s\n" % (caption[0], caption[1]))
        
        f.close()
        
    except:
        pass
```

效果如下：

![image-20220129235837541](https://s2.loli.net/2022/01/29/klDeE37nTJ6QPgb.png)


## 碎碎念

清华雨课堂用来放 MOOC 的这个平台和学堂在线那个平台前端是一样的。

这简直就和 net9.org 和 stu.cs.tsinghua.edu.cn 的后台一样，写一份账户管理工具，一份自己用，另一份拿出去用。

这篇博文仅供练习使用，不保证能复现，更不会提供爬取后的慕课字幕数据。以上。
