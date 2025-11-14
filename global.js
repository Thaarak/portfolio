const BASE_PATH = (location.hostname === "localhost" || location.hostname === "127.0.0.1")
  ? "/"                  // Local server
  : "/portfolio/";         // GitHub Pages repo name

console.log('IT\'S ALIVE!');

function $$(selector, context = document) {
  return Array.from(context.querySelectorAll(selector));
}

let navLinks = $$("nav a");

let currentLink = navLinks.find(
    (a) => a.host === location.host && a.pathname === location.pathname,
  );

currentLink?.classList.add('current');

// Array of pages for the navigation menu
let pages = [
    { url: '', title: 'Home' },
    { url: 'projects/', title: 'Projects' },
    { url: 'contact/', title: 'Contact' },
    { url: 'https://github.com/Thaarak', title: 'GitHub' },
    { url: 'https://drive.google.com/file/d/1aN325M610I_HJYvvFylgdWz8b7_Db5cn/view?usp=sharing', title: 'Resume' }
    // Add more pages as needed
  ];

// Create the nav element and add it to the top of the page
let nav = document.createElement('nav');
document.body.prepend(nav);

// Theme switcher
document.body.insertAdjacentHTML(
    'afterbegin',
    `
    <label class="color-scheme">
      Theme:
      <select id="color-scheme-select">
        <option value="light">Light</option>
        <option value="dark">Dark</option>
        <option value="auto">Automatic</option>
      </select>
    </label>
    `
  );

let select = document.querySelector('#color-scheme-select');

// When page loads, check for previous value
if ("colorScheme" in localStorage) {
    document.documentElement.setAttribute('data-theme', localStorage.colorScheme);
    select.value = localStorage.colorScheme;
}

select.addEventListener('input', function(event) {
  // Save the chosen scheme to localStorage
  localStorage.colorScheme = event.target.value;
  document.documentElement.setAttribute('data-theme', event.target.value);
});

for (let p of pages) {
    let url = p.url;
    let title = p.title;

    // Create link and add it to nav
    let a = document.createElement('a');
    // Use BASE_PATH for relative URLs, keep full URLs as-is
    a.href = url.startsWith('http') ? url : BASE_PATH + url;
    a.textContent = title;
    nav.append(a);
  }

if (a.host === location.host && a.pathname === location.pathname) {
    a.classList.add('current');
}

a.classList.toggle(
    'current',
    a.host === location.host && a.pathname === location.pathname,
  );