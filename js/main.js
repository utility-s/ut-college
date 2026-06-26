document.addEventListener('DOMContentLoaded', () => {
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        const header = document.querySelector('.header');
        const headerOffset = header ? header.offsetHeight : 0;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset - 20;
  
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // Accordion for FAQ
  const accordionHeaders = document.querySelectorAll('.faq-question');
  if (accordionHeaders.length > 0) {
    accordionHeaders.forEach(header => {
      header.addEventListener('click', () => {
        const item = header.parentElement;
        if (item) {
          const isActive = item.classList.contains('active');
          if (!isActive) {
            item.classList.add('active');
          } else {
            item.classList.remove('active');
          }
        }
      });
    });
  }

  // Intersection Observer for fade-in animations
  try {
    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.remove('js-hidden');
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(el => {
      // JS is running, so hide initially for animation
      el.classList.add('js-hidden');
      observer.observe(el);
    });
  } catch (e) {
    console.warn('IntersectionObserver is not supported or failed', e);
    // Fallback: make everything visible immediately
    document.querySelectorAll('.fade-in').forEach(el => {
      el.classList.remove('js-hidden');
      el.classList.add('visible');
    });
  }

  // Mobile Dropdown Toggle
  const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
  if (dropdownToggles.length > 0) {
    dropdownToggles.forEach(toggle => {
      toggle.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          const parent = toggle.parentElement;
          if (parent) {
            parent.classList.toggle('active');
          }
        }
      });
    });
  }
});
