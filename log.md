## input.html

https://apis.map.kakao.com/web/sample/addDraggableMarkerDragEvent/

<br/>

kakako draggable 마커 이벤트를 두고 커스텀하여 사용하기로 하였다. 첫 지도 생성 위치를 현 위치로 잡기 위해 페이지 로딩에 <code>getUserLocation();</code>을 호출하였으나 캐시 없이 현위치를 받아오는 것이 오래걸려 <code>setInterval</code>로 0.15초 마다 위치가 받아졌는지 확인 후 지도를 생성하였다. 

<br/>

JS
~~~javascript
let ifMapIinited = false;
let nyt = false;

function MAP() {
  getUserLoaction();
  setTimeout(function () {
    sit = setInterval(function () {
      if (document.getElementById('sample3_address').value != "") {
        if (ifMapIinited == false) {
          initloc = document.getElementById('sample3_address').value
          nyt = true;
          setTimeout(function () {
            document.getElementById('sample3_address').value = "";
            initMap(initloc);
          }, 50)
        }
      }
      else if (document.getElementById('sample3_address').value == "") {
        if (nyt == true) {
          clearInterval(sit);
        }
        else {
          console.log('not yet');
        }
      }
    }, 100)
  }, 100)
}        
~~~

<br/>

HTML

<br/>

~~~html
<div id="map" style="width:100%; height:300px;"></div>
~~~

<br/> 

지도 생성 후 드래그 가능한 출발, 도착 마커는 겹치지 않도록 현위치 주변에 생성되도록 하였다. '마커로 주소 입력' 버튼이 활성화 된 상태라면 드래그하는 동안 상단의 Starting Point, Destination 안의 값이 인터랙티브하게 적용되도록 하였다. 이 또한 <code>setInterval</code>를 통해 구현하였으나 나중에 보니 kakao에서 제공하는 <code>kakao.maps.event.addListener(map, 'dragend', function() {});</code>을 통해 간결하고 적은 메모리 사용으로 구현할 수 있었다. (다만 <code>setInterval</code>로 받아올 떄보다는 반응이 느린감이 있었다) '마커로 주소 입력' 버튼이 비뢀성화 된 상태라면 마커 주소를 받지 않고 지도 아래의 인풋 태그 중 id = sample3_address (placeholder: 주소 또는 좌표)안의 값을 수시로 받아 구글 js 지오코딩 후 지도에 표시되도록 하였다. 

<br/> 

이 과정에서 상당한 어려움이 있었다. ~~자바스크립트를 배운적이 없다는게 일단 가장 크게 작용한 것 같다.~~ 기본적으로 카카오에서는 마커 생성 후 마커 속성 변경을 권장하지 않으려 하는 것 같았다. 드래그만 가능할 뿐 드래그 위치를 지정한다던지, 드래그 가능 여부를 변경한다던지 하는 식의 변경을 불가능해 보였다. 처음 마커 생성 시에만 속성을 건드릴 수 있도록 하는 것 같았으나 마커를 드래그하고 해당 마커를 <code>setMap(null);</code>으로 지도에서 지우고 <code>setMap(map);</code>으로 다시 생성하였을 때 드래그한 후의 위치가 적용되는것으로 보아 드래그를 통해서는 마커의 위치 속성을 변경 할 수 있는 것으로 보였다. 또 하나 문제는 인터랙티브한 마커 위치 반영을 위해 <code>setInterval</code>으로 마커를 삭제, 생성 하려고 하였는데 이때 같은 이름의 같은 속성의 객체가 무한정 생성될 거라고 생각하지 못하였다 -> 마커를 치워도 같은 마커가 무한정 생성되는 이슈가 있었다. 이러한 이슈가 있었음에도 인터랙티브하게 구현해야하는 이유가 있었다. 도로명 주소로 주소를 입력하거나 현위치를 받아 마커를 띄울 때에 정확한 위차가 아닌 곳에 마커가 떠 있을 수 있어 한번의 입력이 아닌 여러 방식으로 (도로명주소와 드래그 등의) 입력하는 케이스를 염두해두고 개발하였기 떄문에 포기 할 수 없는 기능이였다. 다큐멘트에 <code>marker.setPosition(lat, lng)</code>이 있었는데 못봤다...

<br/>

이게 그 비효율적인 로직이다.

<br/>

~~~javascript
setInterval(function () {
  if (document.getElementById('flexCheckChecked').checked) {
    document.getElementById('SP').value = String(startMarker.getPosition());
    document.getElementById('DP').value = String(arriveMarker.getPosition());
  } 
  else {
    spl = document.getElementById('SP').value.split(" / ")
    console.log(jsgeocode(spl[0]))
    console.log(spl[0])
  }
}, 200)
~~~

<br/>

![Screen Shot 2022-05-23 at 4 27 51](https://user-images.githubusercontent.com/96364048/169712606-b5f153b5-5d06-4ba2-a0ba-078319932aa1.png)

지도 좌측 상단의 지도, 스카이뷰 토글과 줌 컨트롤은 
~~~javascript
// 일반 지도와 스카이뷰로 지도 타입을 전환할 수 있는 지도타입 컨트롤을 생성합니다
var mapTypeControl = new kakao.maps.MapTypeControl();

// 지도에 컨트롤을 추가해야 지도위에 표시됩니다
// kakao.maps.ControlPosition은 컨트롤이 표시될 위치를 정의하는데 TOPRIGHT는 오른쪽 위를 의미합니다
map.addControl(mapTypeControl, kakao.maps.ControlPosition.TOPRIGHT);

// 지도 확대 축소를 제어할 수 있는  줌 컨트롤을 생성합니다
var zoomControl = new kakao.maps.ZoomControl();
map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);
~~~
로 구현하였다

<br/>

위의 지도 로딩에서 현위치를 불러올 떄 사용하는 geolocation 로직은 아래와 같이 구현하였다

~~~javascript
var options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

const errorCallback = (error) => {
  console.error(error);
};

function getUserLoaction() {
  navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
}

function successCallback(event) {
  document.getElementById('sample3_address').value = String(event.coords.latitude) + ", " + String(event.coords.longitude);
}
~~~

<br/>

도로명 주소 입력 후 지도에 표시하기 위하여 구성한 google js geocode는 다음과 같다

~~~javascript
let geocoder;
function jsgeocode(to_geocode) {
  geocoder = new google.maps.Geocoder()
  latlng = [];
  geocoder.geocode({ 'address': to_geocode }, function (result, status) {            
    lat = parseFloat(result[0].geometry.location.lat());
    lng = parseFloat(result[0].geometry.location.lng());
    latlng.push(lat);
    latlng.push(lng);
  }) 
  return latlng;
}
~~~

<br/>

마지막으로 다음 우편번호 api이다. 

<br/>

JS
~~~javascript
<script src="https://t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
<script>
// 우편번호 찾기 찾기 화면을 넣을 element
var element_wrap = document.getElementById('wrap');

function foldDaumPostcode() {
  // iframe을 넣은 element를 안보이게 한다.
  element_wrap.style.display = 'none';
}

function sample3_execDaumPostcode() {
  // 현재 scroll 위치를 저장해놓는다.
  var currentScroll = Math.max(document.body.scrollTop, document.documentElement.scrollTop);
  new daum.Postcode({
    oncomplete: function (data) {
      // 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

      // 각 주소의 노출 규칙에 따라 주소를 조합한다.
      // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
      var addr = ''; // 주소 변수
      var extraAddr = ''; // 참고항목 변수

      //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
      if (data.userSelectedType === 'R') { // 사용자가 도로명 주소를 선택했을 경우
        addr = data.roadAddress;
      } else { // 사용자가 지번 주소를 선택했을 경우(J)
        addr = data.jibunAddress;
      }

      // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
      if (data.userSelectedType === 'R') {
        // 법정동명이 있을 경우 추가한다. (법정리는 제외)
        // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
        if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
          extraAddr += data.bname;
        }
        // 건물명이 있고, 공동주택일 경우 추가한다.
        if (data.buildingName !== '' && data.apartment === 'Y') {
          extraAddr += (extraAddr !== '' ? ', ' + data.buildingName : data.buildingName);
        }
        // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
        if (extraAddr !== '') {
          extraAddr = ' (' + extraAddr + ')';
        }
        // 조합된 참고항목을 해당 필드에 넣는다.
        document.getElementById("sample3_extraAddress").value = extraAddr;

      } else {
        document.getElementById("sample3_extraAddress").value = '';
      }

      // 우편번호와 주소 정보를 해당 필드에 넣는다.
      document.getElementById('sample3_postcode').value = data.zonecode;
      document.getElementById("sample3_address").value = addr;
      // 커서를 상세주소 필드로 이동한다.
      document.getElementById("sample3_detailAddress").focus();

      // iframe을 넣은 element를 안보이게 한다.
      // (autoClose:false 기능을 이용한다면, 아래 코드를 제거해야 화면에서 사라지지 않는다.)
      element_wrap.style.display = 'none';

      // 우편번호 찾기 화면이 보이기 이전으로 scroll 위치를 되돌린다.
      document.body.scrollTop = currentScroll;
    },
    // 우편번호 찾기 화면 크기가 조정되었을때 실행할 코드를 작성하는 부분. iframe을 넣은 element의 높이값을 조정한다.
    onresize: function (size) {
      element_wrap.style.height = size.height + 'px';
    },
    width: '100%',
    height: '100%'
  }).embed(element_wrap);

  // iframe을 넣은 element를 보이게 한다.
  element_wrap.style.display = 'block';
}
</script>
~~~

<br/>

HTML

<br/>

~~~html
<input type="text" class="form-control" name="SP_postcode" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" id="sample3_postcode" placeholder="우편번호">
<input type="text" class="form-control" name="SP_address" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" id="sample3_address" placeholder="주소 또는 좌표">
<input type="text" class="form-control" name="SP_detailAddress" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" id="sample3_detailAddress" placeholder="상세주소">
<input type="text" class="form-control" name="SP_exrtraAddress" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" id="sample3_extraAddress"  placeholder="참고항목">

<div id="wrap" style="display:none;border:1px solid;width:500px;height:300px;margin:5px 0;position:relative">
  <img src="//t1.daumcdn.net/postcode/resource/images/close.png" id="btnFoldWrap" style="cursor:pointer;position:absolute;right:0px;top:-1px;z-index:1" onclick="foldDaumPostcode()" alt="접기 버튼">
</div>
~~~

<br/>

가장 오래 걸렸던 마커 포지션 변경에도 이런저런 이슈들이 있었다. 위의 geolocation 함수에서 리스트 형태로 반환을 해야하는데 콘솔에서는 빈 리스트로 보이고 더보기를 누르면 비어있는 것처럼 생긴 리스트 안에 값이 있는 보여졌다(typeof로 찍어보았을 떄도 array가 아닌 object로 나왔다. object.values도 안되었다). 문제는 인덱싱이 안됐다는 것이였는데 결국은 빈 리스트 선언 -> 값 푸시 -> 리스트 반환 이였던 과정을 <code>rslt = [lat, lng];</code> 식으로 바꾸었더니 정상적으로 작동하였다. 그리고 현위치를 받고 그 위치를 중심으로 지도를 생성하였기 떄문에 지도 생성 변수와 로직을 전부 함수로 감쌌다. 그리고 그 과정에서 변수가 함수 안에 들어가있어서 외부에서 함수 안의 함수(onclick에서 initMap안의 변수로 마커 설정하는 함수)를 호출할 수 없어 jquery를 조금 사용했다 다음은 그 함수이다. 

<br/>

~~~javascript
$('#radioSP').click(function () {
  setTimeout(function(){
    var sp = [];
    sp = jsgeocode(document.getElementById('SP').value.split(" / ")[1]);
    console.log(sp[0])
    console.log(sp[1])
    // startMarker.setPosition(new kakao.maps.LatLng(sp[0], sp[1]));
    setTimeout(function() {
      var sp = [];
      sp = jsgeocode(document.getElementById('SP').value.split(" / ")[1]);
      console.log(sp[0])
      console.log(sp[1])
      startMarker.setPosition(new kakao.maps.LatLng(sp[0], sp[1]));
    }, 500)
  }, 500)
})
~~~

<br/>

불필요한 부분이 꽤 있지만 괜히 지웠다가 문제 생길까봐 그냥 놔두었다. setTimeout 500은 되는데 200은 현위치로 가버린다(또 이유는 모른다). setTimeout 500, setTimeout 500은 되고 setTimeout 1000은 안된다. 안쓰는 값이여도 일단 한번 불러와줘야 하는 것 같았다. 

<br/>

최종적으로 도로명주소로 마커 위치를 변경하는 로직에서 정말 신기한 이슈가 있었다. send to SP, DP를 누르면 Starting Point의 밸류를 지오코딩해서 마커 위치를 변경하는 식이였는데 밸류를 받아오고 split후 인덱싱까지 정상적으로 되었으나 마커가 현위치 기준 오른 위에 있었다가 현위치로 이동했다. 정말 신기한 것은 두번째 버튼 클릭시에는 정상적인 위치로 간다는 것이다. 이해가 전혀 안되는 부분은 1. 현위치는 지도 로딩 떄 이후로 받아온 적이 없는데 마커가 현위치로 이동하는 것 2. 지도 로딩시에 디폴트 마커 위치는 현위치lat+0.001, 현위치lng+0.001인데 어떻게 현위치 오른 위가 아니라 딱 현위치로 오는지 3. 왜 두번째에는 되는지. 추측컨대 1. 빈 값을 받아와서 지도 중심으로 마커 위치가 설정됐다 2. 지도 로딩 떄 불러온 현위치가 들어가버렸다 (어떻게?) 인거 같은데 모르겠다. 

<br/>

위에서 마커로 주소 입력 로직을 <code>kakao.maps.event.addListener(map, 'dragend', function() {});</code>으로 구현하였으나 드래그를 하고 드래그가 끝나야만 주소가 입력되는 탓에 체크되지 않은상태에서 이동한 마커의 값을 넣으려면 체크 후 다시 움직여야 했다. 결국 다시 setInterval로 구현하였다

<br/>

이외의 자잘한 html, js 세팅이 있었다. Starting_Point, Destination 인풋 태그는 <code>readonly</code>와 <code>required</code>속성을 지정하였다. (파이썬 로직 내에서 예상치 못한 포맷으로 인한 에러 방지, 어차피 send to SP,DP, 마커로 주소입력 등으로 함수를 통해서만 값 입력. Max_Length 인풋 태그에는 <code>type="number" step = "100"</code>으로 정수값만 입력받도록 하였다. 

<br/>

Staring Point 기준으로 Max_Length (m) 내에 있는 편의점, 마트를 불러오는 로직인 search_MT1, search_CS2에서 범위 내 편의점 마트를 불러올떄 누락되는 편의점이 있어 함수를 추가적으로 구현하였다. (Max_Length == 900m 정도면 100m~400m는 제외되고 700m~900m 범위 내만 불러옴, 이유는 X, 다른 사람도 결국 for문 돌림)



<br/>

* * * *

<br/>

## views.py 

<br/>

* * * *

<br/>

## show_options.html

![Screen Shot 2022-05-26 at 5 57 35](https://user-images.githubusercontent.com/96364048/170366053-0a1dbdeb-b2ce-4780-9fc5-0d639cf9f01c.png)

가장 위 이미지는 osmnx를 사용해 지도를 그래프로 그린 것이다. OSMnx와 연관된 라이브러리의 관계는 다음과 같다. OSMnx 메서드로 입력한 주소는 folium 또는 OSM을 통해 받아온 지도를 node와 edge를 가지는 networkX 라이브러리의 MultiDiGraph 형태의 그래프로 반환한다. 생성된 networkX형태의 MultiDiGraph는 matplotlib로 그려지는 것이기 때문에 html 상에 그래프를 띄우려면 matplotlib의 메서드를 사용해야 하는데 matplotlib에는 plotly 라이브러리와 같이 html로 div 형태로 반환시켜주는 메서드가 없다(적어도 내가 찾기론). 결국 이미지 형태로 로컬에 저장해서 로컬 이미지를 바로 띄워주어야 하는데 문제는 django-html 상에서 보안상의 이유로 로컬 파일 접근이 불가능하다는 것이다. 결국 생각해낸 방법이 1. 로컬 이미지를 수시로 DB에 업로드 2. 로컬 이미지를 저장 후 바로 링크화 시켜서 html에 링크로 표시 3. static 파일에 저장할 떄마다 자동으로 collectstatic하여 html상에서 static파일로 접근하여 보여주는 방법 등이다. 1번은 장고 공식 문서에서 보안상의 이유로 권장하지 않는 탓에 불가능했고 2번은 이미지를 링크화하는 마땅한 방법이 없어 포기해야 했다 (장고 라이브러리에서 file to uri가 가능하나 file///:user/document/~ 식의 링크가 아닌 filepath를 것 밖에 없었다). 의외로 3번이 가장 쉬웠는데 <code>os.system("python manage.py collectstatic --no-input")</code> 만으로도 가능했다. <code>--no-input</code>은 collectstatic시에 파일 덮어쓰기 여부와 위치를 최종확인하는 과정에서 묻는 yes no를 스킵하겠다는 내용이다. 매번 사진을 덮어씌우고 수시로 collectstatic을 하는게 비효율적이고 그닥 맘에 안들긴 하다. 
#### ~~그래도 OSMnx 그래프 웹 상에 띄운 것은 세계최초 일듯 싶다 (검색해도 절대 안나옴 ㅋㅋ)~~

<br/>

&#x27;경기 성남시 분당구 서현동 276-1&#x27;, &#x27;CS2&#x27;, &#x27;편의점&#x27;, &#x27;가정,생활 &gt; 편의점 &gt; GS25&#x27;, &#x27;256&#x27;, &#x27;12314871&#x27;, &#x27;&#x27;, &#x27;GS25 분당시그마점&#x27;, &#x27;http://place.map.kakao.com/12314871&#x27;

<br/>

~~~javascript
for (p = 0; p < parseInt("{{lenCS2}}"); p++) {
        console.log("{{CS2}}"[p])
}
~~~




