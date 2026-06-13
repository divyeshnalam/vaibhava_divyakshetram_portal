"use strict";

(function () {
  // Pairs: [english_field_id_suffix, telugu_field_id_suffix]
  const FIELD_PAIRS = [
    ["temple_name_en", "temple_name_te"],
    ["history_en",     "history_te"],
    ["address_en",     "address_te"],
    ["title_en",       "title_te"],
    ["subtitle_en",    "subtitle_te"],
    ["content_en",     "content_te"],
    ["description_en", "description_te"],
    ["significance_en","significance_te"],
    ["name_en",        "name_te"],
    ["caption_en",     "caption_te"],
    ["subject",        null],   // contact — no telugu pair, skip
  ];

  const TRANSLATE_URL = "/api/translate/";

  function getCsrfToken() {
    const cookie = document.cookie.split(";").find(c => c.trim().startsWith("csrftoken="));
    return cookie ? cookie.trim().split("=")[1] : "";
  }

  function addTranslateButton(enField, teField) {
    // Don't add twice
    if (enField.dataset.translateWired) return;
    enField.dataset.translateWired = "true";

    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Translate → Telugu";
    btn.title = "Auto-translate English to Telugu using Gemini";
    btn.style.cssText = [
      "margin-top: 6px",
      "margin-bottom: 2px",
      "padding: 4px 12px",
      "font-size: 12px",
      "background: #8B0000",
      "color: #fff",
      "border: none",
      "border-radius: 4px",
      "cursor: pointer",
      "display: block",
    ].join(";");

    btn.addEventListener("mouseenter", () => btn.style.background = "#a00000");
    btn.addEventListener("mouseleave", () => btn.style.background = "#8B0000");

    btn.addEventListener("click", async () => {
      const text = enField.value.trim();
      if (!text) {
        alert("Please enter English text first.");
        return;
      }
      btn.textContent = "Translating…";
      btn.disabled = true;

      try {
        const resp = await fetch(TRANSLATE_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({ text }),
        });
        const data = await resp.json();
        if (data.translated) {
          teField.value = data.translated;
          // Trigger Django/Jazzmin change detection
          teField.dispatchEvent(new Event("input", { bubbles: true }));
          teField.dispatchEvent(new Event("change", { bubbles: true }));
          btn.textContent = "✓ Translated";
          setTimeout(() => { btn.textContent = "Translate → Telugu"; }, 2500);
        } else {
          alert("Translation failed: " + (data.error || "Unknown error"));
          btn.textContent = "Translate → Telugu";
        }
      } catch (err) {
        alert("Network error: " + err.message);
        btn.textContent = "Translate → Telugu";
      } finally {
        btn.disabled = false;
      }
    });

    // Insert button right after the English field
    enField.insertAdjacentElement("afterend", btn);
  }

  function wireAllPairs() {
    FIELD_PAIRS.forEach(([enSuffix, teSuffix]) => {
      if (!teSuffix) return;

      // Django admin field IDs are like: id_title_en, id_history_en, etc.
      const enField = document.getElementById("id_" + enSuffix);
      const teField = document.getElementById("id_" + teSuffix);

      if (enField && teField) {
        addTranslateButton(enField, teField);
      }
    });
  }

  // Run on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wireAllPairs);
  } else {
    wireAllPairs();
  }

  // Also handle Jazzmin's tabbed UI — re-wire when tabs are clicked
  document.addEventListener("click", (e) => {
    if (e.target.closest(".nav-tabs a, .tab-content")) {
      setTimeout(wireAllPairs, 150);
    }
  });
})();