var timeout;
        
async function getStatus() {

  let get;
  
  try {
    const res = await fetch("/status");
    get = await res.json();
  } catch (e) {
    console.error("Error: ", e);
  }
  
  document.getElementById("status").innerHTML = get.status / 1.5 + "&percnt;";
  
  if (get.status == 150){
    document.getElementById("status").innerHTML += " Done.";
    clearTimeout(timeout);
    return false;
  }
   
  timeout = setTimeout(getStatus, 1000);
}

    getStatus();