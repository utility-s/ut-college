import os

css_append = """
/* Animations */
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}
.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Dropdown Menu */
.has-dropdown {
  position: relative;
}
.dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: #fff;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  padding: 10px 0;
  border-radius: 4px;
  min-width: 200px;
  z-index: 100;
}
.dropdown-menu li {
  display: block;
}
.dropdown-menu li a {
  display: block;
  padding: 10px 20px;
  color: var(--text-color);
  font-size: 0.9rem;
}
.dropdown-menu li a:hover {
  background: var(--bg-light);
  color: var(--primary-color);
}
.has-dropdown:hover .dropdown-menu {
  display: block;
}

/* Mobile Dropdown */
@media (max-width: 768px) {
  .dropdown-menu {
    position: static;
    box-shadow: none;
    padding: 0;
    padding-left: 20px;
    display: none;
  }
  .has-dropdown.active .dropdown-menu {
    display: block;
  }
}

/* Card Hover Effects */
.service-card, .price-card, .flow-item, .content-box {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.service-card:hover, .price-card:hover, .flow-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
"""

with open("css/style.css", "a", encoding="utf-8") as f:
    f.write(css_append)

js_append = """
  // Intersection Observer for fade-in animations
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };
  
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
  });

  // Mobile Dropdown Toggle
  document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        toggle.parentElement.classList.toggle('active');
      }
    });
  });
"""

with open("js/main.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Insert before the last }); if it exists, or just append inside DOMContentLoaded
js_content = js_content.replace('});\n', js_append + '});\n', 1)

with open("js/main.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("CSS and JS updated.")
