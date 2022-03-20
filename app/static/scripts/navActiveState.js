/**
 * Generate ACTIVE state for navigation page links
 */

// Get all of our nav-links in an array
const navLinks = document.getElementsByClassName("nav-link");
let index, players, login, register;
console.log(navLinks);

// Assign all possible routes to their respective variables
for (let i = 0; i < navLinks.length; i++) {
  switch (navLinks[i].pathname) {
    case "/":
      index = navLinks[i];
      break;
    case "/index":
      index = navLinks[i];
      break;
    case "/auth":
      players = navLinks[i];
      break;
    case "/login":
      login = navLinks[i];
      break;
    case "/register":
      register = navLinks[i];
      break;
    default:
      console.error(`Invalid page link detected: Pathname ${navLinks[i]}`);
      break;
  }
}

// Add the .active-nav class to the link which contains the same pathname as the current page
switch (window.location.pathname) {
  case "/":
    index.classList.add("active-nav");
    break;
  case "/index":
    index.classList.add("active-nav");
    break;
  case "/players":
    players.classList.add("active-nav");
    break;
  case "/login":
    login.classList.add("active-nav");
    break;
  case "/register":
    register.classList.add("active-nav");
    break;
  default:
    break;
}
