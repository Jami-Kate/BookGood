var timeout;
        
async function getStatus() {

  let booksLoaded = false;
  let moodsLoaded = false;

  let get;
  
// Make call to status endpoint to update book status and mood status
  try {
    const res = await fetch("/status");
    get = await res.json();
  } catch (e) {
    console.error("Error: ", e);
  }

  // Populate the appropriate HTML items
  
  document.getElementById("book-status").innerHTML = `loading books: ${get.book_status / 1.5 + "&percnt;"}`; 
  document.getElementById("mood-status").innerHTML = `loading moods: ${get.mood_status / 1.5 + "&percnt;"}`;

  // Signal when finished loading books
  if (get.book_status >= 150){
    document.getElementById("book-status").innerHTML = "Books loaded";
    booksLoaded = true;
  }

  // Signal when finished loading books
  if (get.mood_status >= 150){
    document.getElementById("mood-status").innerHTML = "Moods loaded";
    moodsLoaded = true;
  }

  // Cease looping function when books and moods are all loaded
  if (booksLoaded & moodsLoaded) {
    clearTimeout(timeout);
    document.getElementById("ready").classList.remove("d-none")
    return false;
  }
  
  // Run function (i.e. make status request) every two seconds
  timeout = setTimeout(getStatus, 2000);
}

getStatus();