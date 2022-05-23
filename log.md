시작하기에 앞서 자바스크립트를 배운적이 없으며 파이썬과 동시에 개발하고 있기에 파이썬 문법과 자바스크립트에는 적절치 않는 로직이 잔뜩 섞여있음을 알린다.

<br/>

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

이 과정에서 상당한 어려움이 있었다. ~~자바스크립트를 배운적이 없다는게 일단 가장 크게 작용한 것 같다.~~ 기본적으로 카카오에서는 마커 생성 후 마커 속성 변경을 권장하지 않으려 하는 것 같았다. 드래그만 가능할 뿐 드래그 위치를 지정한다던지, 드래그 가능 여부를 변경한다던지 하는 식의 변경을 불가능해 보였다. 처음 마커 생성 시에만 속성을 건드릴 수 있도록 하는 것 같았으나 마커를 드래그하고 해당 마커를 <code>setMap(null);</code>으로 지도에서 지우고 <code>setMap(map);</code>으로 다시 생성하였을 때 드래그한 후의 위치가 적용되는것으로 보아 드래그를 통해서는 마커의 위치 속성을 변경 할 수 있는 것으로 보였다. 또 하나 문제는 인터랙티브한 마커 위치 반영을 위해 <code>setInterval</code>으로 마커를 삭제, 생성 하려고 하였는데 이때 같은 이름의 같은 속성의 객체가 무한정 생성될 거라고 생각하지 못하였다 -> 마커를 치워도 같은 마커가 무한정 생성되는 이슈가 있었다. 이러한 이슈가 있었음에도 인터랙티브하게 구현해야하는 이유가 있었다. 도로명 주소로 주소를 입력하거나 현위치를 받아 마커를 띄울 때에 정확한 위차가 아닌 곳에 마커가 떠 있을 수 있어 한번의 입력이 아닌 여러 방식으로 (도로명주소와 드래그 등의) 입력하는 케이스를 염두해두고 개발하였기 떄문에 포기 할 수 없는 기능이였다. 

<br/>

이게 그 비효율적인 로직이다.

<br/>

~~~javascript
setInterval(function () {
  if (document.getElementById('flexCheckChecked').checked) {
    showMarkers();
    document.getElementById('SP').value = String(startMarker.getPosition());
    document.getElementById('DP').value = String(arriveMarker.getPosition());
  } 
  else {
    hideMarkers();
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



