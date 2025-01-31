import React from "react";
import "./cursor.styles.scss";

export function Cursor() {
  const cursorDotOutline = React.useRef();
  const cursorDot = React.useRef();
  const requestRef = React.useRef();
  const previousTimeRef = React.useRef();
  const [mousePosition, setMousePosition] = React.useState({ x: 0, y: 0 });
  const [width, setWidth] = React.useState(window.innerWidth);
  const [height, setHeight] = React.useState(window.innerHeight);
  const cursorVisible = React.useRef(false);
  const cursorEnlarged = React.useRef(false);
  
  const endX = React.useRef(window.innerWidth / 2);
  const endY = React.useRef(window.innerHeight / 2);

  /**
   * Mouse Moves
   */
  const onMouseMove = (event) => {
    const { pageX: x, pageY: y } = event;
    setMousePosition({ x, y });
    endX.current = x;
    endY.current = y;
    if (cursorDot.current) {
      cursorDot.current.style.top = y + "px";
      cursorDot.current.style.left = x + "px";
    }
  };

  const onMouseEnter = () => {
    cursorVisible.current = true;
    if (cursorDot.current && cursorDotOutline.current) {
      cursorDot.current.style.opacity = 1;
      cursorDotOutline.current.style.opacity = 1;
    }
  };

  const onMouseLeave = () => {
    cursorVisible.current = false;
    if (cursorDot.current && cursorDotOutline.current) {
      cursorDot.current.style.opacity = 0;
      cursorDotOutline.current.style.opacity = 0;
    }
  };

  const onMouseDown = () => {
    cursorEnlarged.current = true;
    if (cursorDot.current && cursorDotOutline.current) {
      cursorDot.current.style.transform = "translate(-50%, -50%) scale(0.7)";
      cursorDotOutline.current.style.transform = "translate(-50%, -50%) scale(5)";
    }
  };

  const onMouseUp = () => {
    cursorEnlarged.current = false;
    if (cursorDot.current && cursorDotOutline.current) {
      cursorDot.current.style.transform = "translate(-50%, -50%) scale(1)";
      cursorDotOutline.current.style.transform = "translate(-50%, -50%) scale(1)";
    }
  };

  const onResize = (event) => {
    setWidth(window.innerWidth);
    setHeight(window.innerHeight);
  };

  /**
   * Hooks
   */
  React.useEffect(() => {
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseenter", onMouseEnter);
    document.addEventListener("mouseleave", onMouseLeave);
    document.addEventListener("mousedown", onMouseDown);
    document.addEventListener("mouseup", onMouseUp);
    window.addEventListener("resize", onResize);
    
    handleLinkHovers();
    
    requestRef.current = requestAnimationFrame(animateDotOutline);

    return () => {
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseenter", onMouseEnter);
      document.removeEventListener("mouseleave", onMouseLeave);
      document.removeEventListener("mousedown", onMouseDown);
      document.removeEventListener("mouseup", onMouseUp);
      window.removeEventListener("resize", onResize);
      
      if (requestRef.current) {
        cancelAnimationFrame(requestRef.current);
      }
    };
  }, []);

  let { x, y } = mousePosition;
  const winDimensions = { width, height };

  /**
   * Position Dot (cursor)
   * @param {event}
   */
  function positionDot(e) {
    cursorVisible.current = true;
    if (cursorDot.current) {
      cursorDot.current.style.top = e.pageY + "px";
      cursorDot.current.style.left = e.pageX + "px";
    }
  }

  /**
   * Toggle Cursor Visiblity
   */
  function toggleCursorVisibility() {
    if (cursorVisible.current) {
      if (cursorDot.current && cursorDotOutline.current) {
        cursorDot.current.style.opacity = 1;
        cursorDotOutline.current.style.opacity = 1;
      }
    } else {
      if (cursorDot.current && cursorDotOutline.current) {
        cursorDot.current.style.opacity = 0;
        cursorDotOutline.current.style.opacity = 0;
      }
    }
  }

  /**
   * Handle LInks
   * Applies mouseover/out hooks on all links
   * to trigger cursor animation
   */
  function handleLinkHovers() {
    document.querySelectorAll("a").forEach((el) => {
      el.addEventListener("mouseenter", () => {
        if (cursorDot.current && cursorDotOutline.current) {
          cursorEnlarged.current = true;
          cursorDot.current.style.transform = "translate(-50%, -50%) scale(0.7)";
          cursorDotOutline.current.style.transform = "translate(-50%, -50%) scale(5)";
        }
      });
      
      el.addEventListener("mouseleave", () => {
        if (cursorDot.current && cursorDotOutline.current) {
          cursorEnlarged.current = false;
          cursorDot.current.style.transform = "translate(-50%, -50%) scale(1)";
          cursorDotOutline.current.style.transform = "translate(-50%, -50%) scale(1)";
        }
      });
    });
  }

  /**
   * Animate Dot Outline
   * Aniamtes cursor outline with trailing effect.
   * @param {number} time
   */
  const animateDotOutline = (time) => {
    if (previousTimeRef.current !== undefined) {
      x += (endX.current - x) / 8;
      y += (endY.current - y) / 8;
      cursorDotOutline.current.style.top = y + "px";
      cursorDotOutline.current.style.left = x + "px";
    }
    previousTimeRef.current = time;
    requestRef.current = requestAnimationFrame(animateDotOutline);
  };

  return (
    <>
      <div ref={cursorDotOutline} id="cursor-dot-outline" />
      <div ref={cursorDot} id="cursor-dot" />
    </>
  );
}