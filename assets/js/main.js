document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Close other nav dropdowns when one opens
  document.querySelectorAll(".nav details").forEach((d) => {
    d.addEventListener("toggle", () => {
      if (d.open) {
        document.querySelectorAll(".nav details").forEach((other) => {
          if (other !== d) other.open = false;
        });
      }
    });
  });

  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  // Highlights carousel with peeking neighbors
  document.querySelectorAll("[data-carousel]").forEach((carousel) => {
    const track = carousel.querySelector(".feature-track");
    const slides = Array.from(carousel.querySelectorAll(".feature-slide"));
    const dots = Array.from(carousel.querySelectorAll("[data-carousel-dots] button"));
    const prev = carousel.querySelector("[data-carousel-prev]");
    const next = carousel.querySelector("[data-carousel-next]");
    if (!track || !slides.length) return;

    let index = Math.max(
      0,
      slides.findIndex((s) => s.classList.contains("is-active"))
    );

    const syncVideos = () => {
      slides.forEach((slide, n) => {
        slide.querySelectorAll("video").forEach((video) => {
          if (n === index) {
            video.play().catch(() => {});
          } else {
            video.pause();
          }
        });
      });
    };

    const positionTrack = () => {
      const active = slides[index];
      if (!active) return;
      const viewport = carousel.querySelector(".feature-viewport") || carousel;
      const viewportCenter = viewport.clientWidth / 2;
      const slideCenter = active.offsetLeft + active.offsetWidth / 2;
      track.style.transform = `translateX(${viewportCenter - slideCenter}px)`;
    };

    const show = (i) => {
      const len = slides.length;
      index = ((i % len) + len) % len;
      slides.forEach((slide, n) => {
        const prevIdx = (index - 1 + len) % len;
        const nextIdx = (index + 1) % len;
        slide.classList.toggle("is-active", n === index);
        slide.classList.toggle("is-prev", n === prevIdx);
        slide.classList.toggle("is-next", n === nextIdx);
      });
      dots.forEach((dot, n) => {
        dot.classList.toggle("is-active", n === index);
      });
      positionTrack();
      syncVideos();
    };

    prev?.addEventListener("click", () => show(index - 1));
    next?.addEventListener("click", () => show(index + 1));
    dots.forEach((dot) => {
      dot.addEventListener("click", () => {
        show(Number(dot.dataset.index || 0));
      });
    });

    slides.forEach((slide, n) => {
      slide.addEventListener("click", (e) => {
        if (n === index) return;
        e.preventDefault();
        show(n);
      });
    });

    carousel.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(index - 1);
      if (e.key === "ArrowRight") show(index + 1);
    });

    window.addEventListener("resize", () => positionTrack());

    // Wait a frame so layout is ready before measuring
    requestAnimationFrame(() => show(index));
  });
});
