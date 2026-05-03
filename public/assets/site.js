async function loadSchemes() {
  const res = await fetch("/assets/schemes.json");
  return res.json();
}

function setActiveNav() {
  const path = window.location.pathname.replace(/\/+$/, "") || "/";
  document.querySelectorAll("[data-nav]").forEach((link) => {
    const target = link.getAttribute("href").replace(/\/+$/, "") || "/";
    if (target === path) link.classList.add("active");
  });
}

function normalize(text) {
  return (text || "").toLowerCase().replace(/[^a-z0-9\s]/g, " ");
}

function chatReply(text, schemes) {
  const lower = normalize(text);

  if (!lower.trim()) return "Please type a message so I can help.";
  if (/(hello|hi|namaste|hey)/.test(lower)) {
    return "Namaste. I'm AI Sakhi, your women-focused scheme assistant. Ask me about education, finance, health, or eligibility.";
  }

  const categories = [
    ["education", "education"],
    ["study", "education"],
    ["finance", "finance"],
    ["money", "finance"],
    ["health", "health"],
    ["job", "employment"],
    ["employment", "employment"],
    ["skill", "employment"]
  ];

  for (const [needle, category] of categories) {
    if (lower.includes(needle)) {
      const matches = schemes.filter((s) => s.category === category);
      if (!matches.length) break;
      return [
        `I found ${matches.length} scheme(s) in ${category}:`,
        ...matches.slice(0, 5).map((s) => `- ${s.name}: ${s.eligibility}`)
      ].join("\n");
    }
  }

  const parsedAge = lower.match(/\b(\d{1,2})\b/);
  const parsedIncome = lower.match(/income\s*(?:is|=)?\s*(\d{3,8})/);
  const gender = /(female|woman|women|mahila|ladki|bahin)/.test(lower) ? "female" : "any";

  if (parsedAge) {
    const age = Number(parsedAge[1]);
    const income = parsedIncome ? Number(parsedIncome[1]) : 0;
    const eligible = schemes.filter((s) => {
      const minAge = Number(s.min_age ?? 0);
      const maxAge = Number(s.max_age ?? 100);
      const incomeLimit = Number(s.income_limit ?? Number.MAX_SAFE_INTEGER);
      const genderOk = s.gender === "any" || s.gender === gender;
      return age >= minAge && age <= maxAge && income <= incomeLimit && genderOk;
    });

    if (eligible.length) {
      return [
        "These schemes look like a fit based on the details you gave:",
        ...eligible.slice(0, 6).map((s) => `- ${s.name} (${s.category})`)
      ].join("\n");
    }
  }

  const tokens = normalize(text).split(/\s+/).filter(Boolean);
  const matches = schemes.filter((scheme) => {
    const haystack = normalize([
      scheme.name,
      scheme.category,
      scheme.description,
      scheme.eligibility
    ].join(" "));
    return tokens.some((token) => haystack.includes(token));
  });

  if (matches.length) {
    return [
      "I found these matching schemes:",
      ...matches.slice(0, 6).map((s) => `- ${s.name} (${s.category})`)
    ].join("\n");
  }

  return "Tell me your age, income, and the kind of help you need. I can suggest relevant schemes in seconds.";
}

function mountHome() {
  const year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();
}

async function mountSchemes() {
  const root = document.querySelector("[data-scheme-grid]");
  if (!root) return;
  const schemes = await loadSchemes();
  const searchInput = document.querySelector("[data-search]");
  const categoryFilter = document.querySelector("[data-category]");

  function render(list) {
    root.innerHTML = list
      .map(
        (scheme) => `
      <article class="card scheme">
        <span class="badge">${scheme.category}</span>
        <h3>${scheme.name}</h3>
        <p class="muted">${scheme.description}</p>
        <p class="meta"><strong>Eligibility:</strong> ${scheme.eligibility}</p>
        <p class="meta"><strong>Age:</strong> ${scheme.min_age} to ${scheme.max_age}</p>
        <p class="meta"><strong>Income limit:</strong> ${Number(scheme.income_limit).toLocaleString()}</p>
        <a class="btn btn-primary apply" href="${scheme.url}" target="_blank" rel="noreferrer">Apply Now</a>
      </article>
    `
      )
      .join("");
  }

  function filter() {
    const search = normalize(searchInput.value);
    const category = categoryFilter.value;
    render(
      schemes.filter((scheme) => {
        const haystack = normalize([scheme.name, scheme.category, scheme.description, scheme.eligibility].join(" "));
        return (!search || haystack.includes(search)) && (!category || scheme.category === category);
      })
    );
  }

  searchInput.addEventListener("input", filter);
  categoryFilter.addEventListener("change", filter);
  render(schemes);
}

async function mountChat() {
  const log = document.querySelector("[data-chat-log]");
  if (!log) return;
  const input = document.querySelector("[data-chat-input]");
  const send = document.querySelector("[data-send]");
  const schemes = await loadSchemes();
  let typingNode = null;

  function append(text, role) {
    const node = document.createElement("div");
    node.className = `message ${role}`;
    node.textContent = text;
    log.appendChild(node);
    log.scrollTop = log.scrollHeight;
  }

  function showTyping() {
    typingNode = document.createElement("div");
    typingNode.className = "message bot typing";
    typingNode.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
    log.appendChild(typingNode);
    log.scrollTop = log.scrollHeight;
  }

  function hideTyping() {
    if (typingNode) typingNode.remove();
    typingNode = null;
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    append(text, "user");
    input.value = "";
    showTyping();
    window.setTimeout(() => {
      hideTyping();
      append(chatReply(text, schemes), "bot");
    }, 350);
  }

  send.addEventListener("click", sendMessage);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });

  window.prefill = (value) => {
    input.value = value;
    input.focus();
  };

  append("Hello, I'm AI Sakhi. Ask me about schemes, eligibility, education support, finance support, or health support.", "bot");
}

setActiveNav();
mountHome();
mountSchemes();
mountChat();
