https://apis.map.kakao.com/web/sample/addDraggableMarkerDragEvent/

<br/>

kakako draggable 마커 이벤트를 두고 커스텀하여 사용하기로 하였다. 첫 지도 생성 위치를 현 위치로 잡기 위해 페이지 로딩에 <code>getUserLocation();</code>을 호출하였으나 캐시 없이 현위치를 받아오는 것이 오래걸려 <code>setInterval</code>로 0.15초 마다 위치가 받아졌는지 확인 후 지도를 생성하였다. 
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

지도 생성 후 드래그 가능한 출발, 도착 마커는 겹치지 않도록 현위치 주변에 생성되도록 하였다. '마커로 주소 입력' 버튼이 활성화 된 상태라면 드래그하는 동안 상단의 Starting Point, Destination 안의 값이 인터랙티브하게 적용되도록 하였다. '마커로 주소 입력' 버튼이 비뢀성화 된 상태라면 마커 주소를 받지 않고 지도 아래의 인풋 태그 중 id = sample3_address (placeholder: 주소 또는 좌표)안의 값을 수시로 받아 구글 js 지오코딩 후 지도에 표시되도록 하였다. 

<br/> 

이 과정에서 상당한 어려움이 있었다. ~~자바스크립트를 배운적이 없다는게 일단 가장 크게 작용한 것 같다.~~ 
