시작하기에 앞서 자바스크립트를 배운적이 없으며 파이썬과 동시에 개발하고 있기에 파이썬 문법과 자바스크립트에는 적절치 않는 로직이 잔뜩 섞여있음을 알린다. 불편하면 보지마라 

<br/>

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

지도 생성 후 드래그 가능한 출발, 도착 마커는 겹치지 않도록 현위치 주변에 생성되도록 하였다. '마커로 주소 입력' 버튼이 활성화 된 상태라면 드래그하는 동안 상단의 Starting Point, Destination 안의 값이 인터랙티브하게 적용되도록 하였다. 이 또한 <code>setInterval</code>를 통해 구현하였으나 나중에 보니 kakao에서 제공하는 <code>kakao.maps.event.addListener(map, 'dragend', function() {});</code>을 통해 간결하고 적은 메모리 사용으로 구현할 수 있었다. '마커로 주소 입력' 버튼이 비뢀성화 된 상태라면 마커 주소를 받지 않고 지도 아래의 인풋 태그 중 id = sample3_address (placeholder: 주소 또는 좌표)안의 값을 수시로 받아 구글 js 지오코딩 후 지도에 표시되도록 하였다. 

<br/> 

이 과정에서 상당한 어려움이 있었다. ~~자바스크립트를 배운적이 없다는게 일단 가장 크게 작용한 것 같다.~~ 기본적으로 카카오에서는 마커 생성 후 마커 속성 변경을 권장하지 않으려 하는 것 같았다. 드래그만 가능할 뿐 드래그 위치를 지정한다던지, 드래그 가능 여부를 변경한다던지 하는 식의 변경을 불가능해 보였다. 처음 마커 생성 시에만 속성을 건드릴 수 있도록 하는 것 같았으나 마커를 드래그하고 해당 마커를 <code>setMap(null);</code>으로 지도에서 지우고 <code>setMap(map);</code>으로 다시 생성하였을 때 드래그한 후의 위치가 적용되는것으로 보아 드래그를 통해서는 마커의 위치 속성을 변경 할 수 있는 것으로 보였다. 또 하나 문제는 인터랙티브한 마커 위치 반영을 위해 <code>setInterval();</code>으로 마커를 삭제, 생성 하려고 하였는데 이때 같은 이름의 같은 속성의 객체가 무한정 생성될 거라고 생각하지 못하였다 -> 마커를 치워도 같은 마커가 무한정 생성되는 이슈가 있었다. 이러한 이슈가 있었음에도 인터랙티브하게 구현해야하는 이유가 있었다. 도로명 주소로 주소를 입력하거나 현위치를 받아 마커를 띄울 때에 정확한 위차가 아닌 곳에 마커가 떠 있을 수 있어 한번의 입력이 아닌 여러 방식으로 (도로명주소와 드래그 등의) 입력하는 케이스를 염두해두고 개발하였기 떄문에 포기 할 수 없는 기능이였다. 

<br/>

![Screen Shot 2022-05-23 at 4 27 51](https://user-images.githubusercontent.com/96364048/169712606-b5f153b5-5d06-4ba2-a0ba-078319932aa1.png)

지도 좌측 상단의
