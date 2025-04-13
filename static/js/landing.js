// Initialize particles.js with enhanced visibility settings
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('particles-js')) {
    particlesJS('particles-js', {
      particles: {
        number: { 
          value: 80, 
          density: { 
            enable: true, 
            value_area: 800 
          } 
        },
        color: { value: "#818cf8" },
        shape: { 
          type: "circle",
          stroke: {
            width: 0,
            color: "#000000"
          }
        },
        opacity: { 
          value: 0.8, 
          random: true,
          anim: {
            enable: true,
            speed: 1,
            opacity_min: 0.1,
            sync: false
          }
        },
        size: { 
          value: 4, 
          random: true,
          anim: {
            enable: true,
            speed: 2,
            size_min: 0.1,
            sync: false
          }
        },
        line_linked: { 
          enable: true, 
          distance: 150, 
          color: "#6366f1", 
          opacity: 0.4,
          width: 1.5
        },
        move: { 
          enable: true, 
          speed: 3,
          direction: "none", 
          random: true, 
          straight: false, 
          out_mode: "out",
          bounce: false,
          attract: {
            enable: true,
            rotateX: 600,
            rotateY: 1200
          }
        }
      },
      interactivity: {
        detect_on: "window",
        events: {
          onhover: { 
            enable: true, 
            mode: "grab",
            parallax: {
              enable: true,
              force: 60,
              smooth: 10
            }
          },
          onclick: { 
            enable: true, 
            mode: "push" 
          },
          resize: true
        },
        modes: {
          grab: {
            distance: 140,
            line_linked: {
              opacity: 1
            }
          },
          push: {
            particles_nb: 4
          }
        }
      },
      retina_detect: true
    });
  }
      // Navbar scroll effect
      window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
          navbar.classList.add('scrolled');
        } else {
          navbar.classList.remove('scrolled');
        }
      });

      // Animate elements on scroll
      const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate__animated');
        
        elements.forEach(element => {
          const elementPosition = element.getBoundingClientRect().top;
          const windowHeight = window.innerHeight;
          
          if (elementPosition < windowHeight - 100) {
            const animationClass = element.classList[1];
            element.classList.add(animationClass);
          }
        });
      };

      window.addEventListener('scroll', animateOnScroll);
      animateOnScroll(); // Run once on load
    });