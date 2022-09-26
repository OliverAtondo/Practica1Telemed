var socket = io.connect('http://192.168.0.4:80', {'forceNew':true});

  const AUDIO = {
    CLICK: new Audio('https://assets.codepen.io/605876/click.mp3') };


socket.on('desde_servidor',function(data){
  let soltado = true;
	if (data == "ON"){
    document.querySelector(":root").style.setProperty("--on", 1);
    soltado = true;
  }
  else if (data == "OFF"){
    document.querySelector(":root").style.setProperty("--on", 0);
    soltado = true;
  }
  else if (data == "SOLTADO"){
    DUMMY_CORD.setAttribute('y2',380.5405);
    DUMMY_CORD.setAttribute('x2',98.7255);
  }
  else {
    soltado = false;
    var y2 = data - 1;
    DUMMY_CORD.setAttribute('y2',y2*1.5);
    }
});

const HIT = document.querySelector('.toggle-scene__hit-spot');
const DUMMY = document.querySelector('.toggle-scene__dummy-cord');
const DUMMY_CORD = document.querySelector('.toggle-scene__dummy-cord line');
