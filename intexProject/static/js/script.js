window.addEventListener("DOMContentLoaded", () => {
    document.querySelector(".menu-icon").addEventListener("click", () => {
        document.querySelector(".main-menu").classList.toggle("menu-show");
    });
  });

  /*daily stats overlay*/
function openDaily() {
    document.getElementById("dailyStats").style.height = "100%";
    document.getElementById("dailyStats").style.right = "33%";
  }
  
function closeDaily() {
document.getElementById("dailyStats").style.height = "";
document.getElementById("dailyStats").style.right = "";
}

/*water overlay*/
function openWater() {
    document.getElementById("water").style.height = "100%";
    document.getElementById("water").style.right = "33%";
  }
  
function closeWater() {
document.getElementById("water").style.height = "";
document.getElementById("water").style.right = "";
}

/*lab results overlay*/
function openLab() {
    document.getElementById("lab").style.height = "100%";
    document.getElementById("lab").style.right = "33%";
  }
  
function closeLab() {
document.getElementById("lab").style.height = "";
document.getElementById("lab").style.right = "";
}

/*search food overlay*/
function openFood() {
  document.getElementById("food").style.height = "100%";
  document.getElementById("food").style.right = "33%";
}

function closeFood() {
  document.getElementById("food").style.height = "";
  document.getElementById("food").style.right = "";
}