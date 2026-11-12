// ==========================================================================
// HOMEPAGE 2 (home-2.html) – INTERACTIVE LOGIC & MOTION CONTROLLER
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. Intersection Observer for Smooth Reveal Animations
  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -80px 0px',
    threshold: 0.15
  };

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.home2-fade-in').forEach(el => {
    revealObserver.observe(el);
  });

  // 2. Interactive Thermal Stage Cards Focus Effect
  const boilCards = document.querySelectorAll('.home2-boil-card');
  const tempBadge = document.querySelector('.home2-temp-badge');
  const tempMap = ['72.0°C Botanical Infusion', '88.5°C Perl Ring', '98.5°C Optimal Simmer', '100.0°C Active Rolling'];
  const thermoSvg = '<svg class="home2-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>';

  boilCards.forEach((card, index) => {
    card.addEventListener('mouseenter', () => {
      if (tempBadge && tempMap[index]) {
        tempBadge.innerHTML = `${thermoSvg} ${tempMap[index]}`;
        tempBadge.style.transform = 'scale(1.08)';
        tempBadge.style.transition = 'transform 0.3s cubic-bezier(0.16, 1, 0.3, 1)';
      }
    });

    card.addEventListener('mouseleave', () => {
      if (tempBadge) {
        tempBadge.innerHTML = `${thermoSvg} 98.5°C Optimal Simmer`;
        tempBadge.style.transform = 'scale(1)';
      }
    });
  });

  // 3. Interactive Flavour Cards Glow Focus
  const pillarCards = document.querySelectorAll('.home2-pillar-card');
  pillarCards.forEach(pillar => {
    pillar.addEventListener('mouseenter', () => {
      pillarCards.forEach(other => {
        if (other !== pillar) {
          other.style.opacity = '0.7';
          other.style.transition = 'opacity 0.3s ease';
        }
      });
    });

    pillar.addEventListener('mouseleave', () => {
      pillarCards.forEach(other => {
        other.style.opacity = '1';
      });
    });
  });
});
