var timeout;
        
async function getStatus() {

  let get;
  
  try {
    const res = await fetch("/status");
    get = await res.json();
  } catch (e) {
    console.error("Error: ", e);
  }
  
  document.getElementById("book-status").innerHTML = `loading books: ${get.book_status / 1.5 + "&percnt;"}`;
  document.getElementById("mood-status").innerHTML = `loading moods: ${get.mood_status / 1.5 + "&percnt;"}`;
  
  if (get.book_status >= 150){
    document.getElementById("book-status").innerHTML = "Books loaded";
  }

  if (get.mood_status >= 150){
    document.getElementById("mood-status").innerHTML = "Moods loaded";
    clearTimeout(timeout);
    document.getElementById("ready").classList.remove("d-none")
    return false;
  }
   
  timeout = setTimeout(getStatus, 2000);
}

getStatus();