const page = document.body.dataset.page;

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function show(el, visible) {
  if (!el) return;
  el.classList.toggle("hidden", !visible);
}

function mountMobileNav() {
  const menuToggle = document.getElementById("menuToggle");
  const siteNav = document.getElementById("siteNav");
  menuToggle?.addEventListener("click", () => {
    siteNav?.classList.toggle("open");
  });
}

function mountTiltCards() {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) return;
  document.querySelectorAll(".tilt-card").forEach((card) => {
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const px = (e.clientX - rect.left) / rect.width;
      const py = (e.clientY - rect.top) / rect.height;
      const rx = (0.5 - py) * 6;
      const ry = (px - 0.5) * 8;
      card.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg)`;
    });
    card.addEventListener("mouseleave", () => {
      card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg)";
    });
  });
}

async function handleDetectPage() {
  const uploadDrop = document.getElementById("uploadDrop");
  const fileInput = document.getElementById("fileInput");
  const browseBtn = document.getElementById("browseBtn");
  const form = document.getElementById("detectForm");
  const loading = document.getElementById("loadingWrap");
  const errorBox = document.getElementById("detectError");
  const resultGrid = document.getElementById("resultGrid");

  const openPicker = () => fileInput?.click();
  browseBtn?.addEventListener("click", openPicker);
  uploadDrop?.addEventListener("click", openPicker);

  ["dragenter", "dragover"].forEach((ev) =>
    uploadDrop?.addEventListener(ev, (e) => {
      e.preventDefault();
      uploadDrop.classList.add("dragover");
    })
  );
  const updateSelectedFile = (file) => {
    if (!file) return;
    if (browseBtn) browseBtn.textContent = file.name;
  };

  ["dragleave", "drop"].forEach((ev) =>
    uploadDrop?.addEventListener(ev, (e) => {
      e.preventDefault();
      uploadDrop.classList.remove("dragover");
      if (ev === "drop") {
        const files = e.dataTransfer?.files;
        if (files?.length && fileInput) {
          const dataTransfer = new DataTransfer();
          Array.from(files).forEach((file) => dataTransfer.items.add(file));
          fileInput.files = dataTransfer.files;
          updateSelectedFile(dataTransfer.files[0]);
        }
      }
    })
  );

  fileInput?.addEventListener("change", () => {
    const file = fileInput.files?.[0];
    if (file) updateSelectedFile(file);
  });

  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    show(errorBox, false);
    show(resultGrid, false);
    const file = fileInput?.files?.[0];
    if (!file) {
      setText("detectError", "Please upload an image first.");
      show(errorBox, true);
      return;
    }

    const formData = new FormData();
    formData.append("image", file);
    show(loading, true);
    try {
      const res = await fetch("/api/analyze", { method: "POST", body: formData });
      const payload = await res.json();
      if (!res.ok || !payload.success) throw new Error(payload.error || "Analysis failed.");

      const data = payload.data || {};
      setText("rDisease", data.disease_name || "Data unavailable");
      setText("rCauses", Array.isArray(data.causes) ? data.causes.join(", ") : "Data unavailable");
      setText("rTreatment", Array.isArray(data.treatment) ? data.treatment.join(", ") : "Data unavailable");
      setText(
        "rPrevention",
        Array.isArray(data.preventive_measures) ? data.preventive_measures.join(", ") : "Data unavailable"
      );
      show(resultGrid, true);
      resultGrid.querySelectorAll(".result-card").forEach((card, idx) => {
        setTimeout(() => card.classList.add("show"), idx * 100);
      });
    } catch (err) {
      setText("detectError", err.message || "Unable to analyze image.");
      show(errorBox, true);
    } finally {
      show(loading, false);
    }
  });
}

function handleChatPage() {
  const chatBox = document.getElementById("chatBox");
  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendChatBtn");

  const append = (text, role) => {
    const bubble = document.createElement("div");
    bubble.className = `bubble ${role}`;
    bubble.textContent = text;
    chatBox?.appendChild(bubble);
    chatBox?.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
  };

  const send = async () => {
    const message = (chatInput?.value || "").trim();
    if (!message) return;
    append(message, "user");
    chatInput.value = "";
    append("Thinking...", "ai");
    const pending = chatBox?.lastElementChild;
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const payload = await res.json();
      if (!res.ok || !payload.success) throw new Error(payload.error || "Chat failed.");
      if (pending) pending.textContent = payload.data?.answer || "No response.";
    } catch (err) {
      if (pending) pending.textContent = err.message || "Unable to answer now.";
    }
  };

  sendBtn?.addEventListener("click", send);
  chatInput?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") send();
  });
}

function handleWeatherPage() {
  const cityInput = document.getElementById("cityInput");
  const btn = document.getElementById("fetchWeatherBtn");
  const loading = document.getElementById("weatherLoading");
  const error = document.getElementById("weatherError");

  const fetchWeather = async () => {
    show(error, false);
    show(loading, true);
    const city = (cityInput?.value || "Delhi").trim();
    try {
      const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
      const payload = await res.json();
      if (!res.ok || !payload.success) throw new Error(payload.error || "Data unavailable");
      const data = payload.data || {};
      setText("wTemp", `${data.temperature_c ?? "--"}°C`);
      setText("wHumidity", `${data.humidity ?? "--"}%`);
      setText("wCondition", data.condition || "Data unavailable");
      const suggestion = Array.isArray(data.suggestions) ? data.suggestions.join(" ") : "Data unavailable";
      setText("wSuggestion", suggestion);
      const note = data.note || "";
      setText("wNote", note);
      show(document.getElementById("wNote"), Boolean(note));
    } catch (err) {
      setText("weatherError", err.message || "Data unavailable");
      show(error, true);
      setText("wTemp", "--");
      setText("wHumidity", "--");
      setText("wCondition", "Data unavailable");
      setText("wSuggestion", "Data unavailable");
      setText("wNote", "");
      show(document.getElementById("wNote"), false);
    } finally {
      show(loading, false);
    }
  };

  btn?.addEventListener("click", fetchWeather);
}

function handleVoicePage() {
  const startBtn = document.getElementById("voiceStartBtn");
  const loading = document.getElementById("voiceLoading");
  const error = document.getElementById("voiceError");
  const transcriptEl = document.getElementById("voiceTranscript");

  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) {
    setText("voiceError", "Voice input is not supported in this browser.");
    show(error, true);
    startBtn.disabled = true;
    return;
  }

  const recognition = new Recognition();
  recognition.lang = "en-IN";
  recognition.interimResults = false;

  startBtn?.addEventListener("click", () => {
    show(error, false);
    recognition.start();
  });

  recognition.onresult = async (event) => {
    const transcript = event.results[0][0].transcript;
    transcriptEl.textContent = transcript;
    show(loading, true);
    try {
      const res = await fetch("/api/voice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript }),
      });
      const payload = await res.json();
      if (!res.ok || !payload.success) throw new Error(payload.error || "Voice request failed.");
      setText("voiceAnswer", payload.data?.answer || "No response.");
    } catch (err) {
      setText("voiceError", err.message || "Unable to process voice query.");
      show(error, true);
    } finally {
      show(loading, false);
    }
  };

  recognition.onerror = () => {
    setText("voiceError", "Could not capture voice. Please try again.");
    show(error, true);
  };
}

mountMobileNav();
mountTiltCards();

if (page === "detect") handleDetectPage();
if (page === "chat") handleChatPage();
if (page === "weather") handleWeatherPage();
if (page === "voice") handleVoicePage();
