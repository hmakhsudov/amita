import { onBeforeUnmount, onMounted } from "vue";

/**
 * Lightweight IntersectionObserver hook for scroll-in animations.
 * Attach via :ref="revealRef".
 */
export function useReveal() {
  const elements = new Set();
  let observer;

  const register = (el) => {
    if (!el) return;
    elements.add(el);
    if (observer) observer.observe(el);
  };

  const refresh = () => {
    observer?.disconnect();
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("show");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    elements.forEach((el) => observer.observe(el));
  };

  onMounted(() => {
    refresh();
    window.addEventListener("reveal:refresh", refresh);
  });

  onBeforeUnmount(() => {
    observer?.disconnect();
    window.removeEventListener("reveal:refresh", refresh);
    elements.clear();
  });

  return { revealRef: register };
}
