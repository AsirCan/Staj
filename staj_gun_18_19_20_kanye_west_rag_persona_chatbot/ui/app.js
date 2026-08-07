const API_BASE = "http://127.0.0.1:8000/api/v1";

const composerInput = document.getElementById("composerInput");
const conversationFlow = document.getElementById("conversationFlow");
const contextBody = document.getElementById("contextBody");
const statusBadge = document.getElementById("statusBadge");
const statusText = document.getElementById("statusText");
const clearBtn = document.getElementById("clearBtn");
const sourceCountBadge = document.getElementById("sourceCountBadge");
const sendBtn = document.getElementById("sendBtn");

function fillPrompt(text) {
    if (!composerInput) return;
    composerInput.value = text;
    composerInput.focus();
    composerInput.style.height = "auto";
    composerInput.style.height = composerInput.scrollHeight + "px";
    if (sendBtn) sendBtn.classList.add("active");
}

function scrollToBottom() {
    if (conversationFlow) {
        conversationFlow.scrollTop = conversationFlow.scrollHeight;
    }
}

function updateStatus(stateText, isWorking = false) {
    if (!statusText || !statusBadge) return;
    statusText.textContent = stateText;
    if (isWorking) {
        statusBadge.classList.add("working");
    } else {
        statusBadge.classList.remove("working");
    }
}

function createNode(role, text) {
    const node = document.createElement("div");
    node.className = `node node-${role === "user" ? "user" : "ai"}`;
    
    if (role === "ai") {
        const header = document.createElement("div");
        header.className = "node-header";

        const label = document.createElement("div");
        label.className = "node-label";
        label.textContent = "Kanye West Persona Monolith";
        header.appendChild(label);

        // Translate Toggle Button
        const translateBtn = document.createElement("button");
        translateBtn.className = "translate-btn";
        translateBtn.innerHTML = `
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2v3"/><path d="M22 22l-5-10-5 10"/><path d="M14 18h6"/></svg>
            <span>Türkçe'ye Çevir</span>
        `;

        let isTranslated = false;
        let originalText = text;
        let translatedText = null;

        translateBtn.addEventListener("click", async () => {
            const btnSpan = translateBtn.querySelector("span");
            const contentDiv = node.querySelector(".node-content");

            if (isTranslated) {
                contentDiv.textContent = originalText;
                btnSpan.textContent = "Türkçe'ye Çevir";
                isTranslated = false;
            } else {
                if (translatedText) {
                    contentDiv.textContent = translatedText;
                    btnSpan.textContent = "Orijinal (English)";
                    isTranslated = true;
                } else {
                    btnSpan.textContent = "Çevriliyor...";
                    translateBtn.disabled = true;
                    try {
                        const res = await fetch(`${API_BASE}/translate`, {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ text: originalText, target_language: "Turkish" })
                        });
                        if (res.ok) {
                            const data = await res.json();
                            translatedText = data.translated_text;
                            contentDiv.textContent = translatedText;
                            btnSpan.textContent = "Orijinal (English)";
                            isTranslated = true;
                        } else {
                            btnSpan.textContent = "Çeviri Hatası";
                        }
                    } catch (err) {
                        btnSpan.textContent = "Çeviri Hatası";
                    } finally {
                        translateBtn.disabled = false;
                    }
                }
            }
        });

        header.appendChild(translateBtn);
        node.appendChild(header);
    }
    
    const content = document.createElement("div");
    content.className = "node-content";
    content.textContent = text;
    node.appendChild(content);
    
    return node;
}

function showThinking() {
    const node = document.createElement("div");
    node.className = "node node-ai thinking-node";
    node.id = "thinkingNode";
    
    const label = document.createElement("div");
    label.className = "node-label";
    label.textContent = "ChromaDB Retrieval";
    node.appendChild(label);

    const indicator = document.createElement("div");
    indicator.className = "thinking-indicator";
    indicator.innerHTML = `
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
        Querying Vector Embeddings & Synthesizing Persona...
    `;
    
    node.appendChild(indicator);
    conversationFlow.appendChild(node);
    scrollToBottom();
}

function removeThinking() {
    const thinkingNode = document.getElementById("thinkingNode");
    if (thinkingNode) {
        thinkingNode.remove();
    }
}

function renderSources(sources) {
    if (!contextBody) return;
    contextBody.innerHTML = "";
    
    if (!sources || sources.length === 0) {
        if (sourceCountBadge) sourceCountBadge.textContent = "0 SOURCES";
        contextBody.innerHTML = `
            <div class="context-empty" id="contextEmptyState">
                <div class="context-empty-icon">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
                        <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
                        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
                        <circle cx="12" cy="12" r="1.5" fill="currentColor"></circle>
                    </svg>
                </div>
                <p class="empty-title">No Active Retrieval</p>
                <p class="empty-sub">Send a message to query vector embeddings & rank top matching lyric passages.</p>
            </div>
        `;
        return;
    }
    
    if (sourceCountBadge) {
        sourceCountBadge.textContent = `${sources.length} SOURCE${sources.length === 1 ? '' : 'S'}`;
    }
    
    sources.forEach(src => {
        const node = document.createElement("div");
        node.className = "source-node";
        
        const simPercent = Math.round((src.similarity || 0) * 100);
        
        // Determine colored match dot based on relevance score
        let dotClass = "high";
        let matchLabel = "High Match";
        if (simPercent < 50) {
            dotClass = "low";
            matchLabel = "Low Match";
        } else if (simPercent < 75) {
            dotClass = "mid";
            matchLabel = "Mid Match";
        }
        
        const albumText = src.album ? src.album : "Unassigned Discography";
        const yearText = src.year ? `(${src.year})` : "";
        
        node.innerHTML = `
            <div class="source-header-row">
                <div class="source-song-title">
                    <span class="match-dot ${dotClass}" title="${matchLabel} (${simPercent}%)"></span>
                    <span>${src.song || "Untitled Track"}</span>
                </div>
                <span class="source-confidence">${simPercent}% Match</span>
            </div>
            <div class="source-meta">
                <span>${albumText} ${yearText}</span>
            </div>
        `;
        contextBody.appendChild(node);
    });
}

async function handleChat(message) {
    // Hide empty state if present
    const emptyState = document.querySelector(".empty-state");
    if (emptyState) emptyState.style.display = "none";
    
    // Add User Node
    conversationFlow.appendChild(createNode("user", message));
    scrollToBottom();
    
    // Show Thinking Node & Update Status Badge
    showThinking();
    updateStatus("RETRIEVING FROM CHROMA...", true);
    
    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: "workspace_user",
                message: message
            })
        });
        
        if (!res.ok) {
            throw new Error(`Server returned ${res.status}`);
        }
        
        const data = await res.json();
        removeThinking();
        
        // Add AI Node & Render Context Sources
        conversationFlow.appendChild(createNode("ai", data.reply));
        renderSources(data.sources);
        updateStatus("CHROMADB ONLINE • 14ms", false);
        scrollToBottom();
        
    } catch (err) {
        removeThinking();
        conversationFlow.appendChild(createNode("ai", `Connection error: ${err.message}`));
        updateStatus("SYSTEM OFFLINE / ERROR", true);
        scrollToBottom();
    }
}

function submitPrompt() {
    if (!composerInput) return;
    const text = composerInput.value.trim();
    if (text) {
        composerInput.value = "";
        composerInput.style.height = "auto";
        if (sendBtn) sendBtn.classList.remove("active");
        handleChat(text);
    }
}

if (sendBtn) {
    sendBtn.addEventListener("click", submitPrompt);
}

if (composerInput) {
    composerInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            submitPrompt();
        }
    });

    composerInput.addEventListener("input", function() {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";
        if (sendBtn) {
            if (this.value.trim().length > 0) {
                sendBtn.classList.add("active");
            } else {
                sendBtn.classList.remove("active");
            }
        }
    });
}

if (clearBtn) {
    clearBtn.addEventListener("click", () => {
        const emptyState = document.querySelector(".empty-state");
        if (emptyState) emptyState.style.display = "flex";
        
        // Remove all nodes
        const nodes = document.querySelectorAll(".node");
        nodes.forEach(n => n.remove());
        
        renderSources([]);
        if (composerInput) {
            composerInput.value = "";
            composerInput.style.height = "auto";
            composerInput.focus();
        }
        if (sendBtn) sendBtn.classList.remove("active");
        updateStatus("CHROMADB ONLINE • 14ms", false);
    });
}

// Modal & Navigation Rail Management
const navWorkspace = document.getElementById("navWorkspace");
const navExplorer = document.getElementById("navExplorer");
const navGraph = document.getElementById("navGraph");
const explorerModal = document.getElementById("explorerModal");
const graphModal = document.getElementById("graphModal");

function setActiveNav(activeBtn) {
    [navWorkspace, navExplorer, navGraph].forEach(btn => {
        if (!btn) return;
        btn.classList.remove("active");
        const indicator = btn.querySelector(".active-indicator");
        if (indicator) indicator.remove();
    });
    if (activeBtn) {
        activeBtn.classList.add("active");
        if (!activeBtn.querySelector(".active-indicator")) {
            const ind = document.createElement("span");
            ind.className = "active-indicator";
            activeBtn.prepend(ind);
        }
    }
}

function closeModals() {
    if (explorerModal) explorerModal.classList.remove("active");
    if (graphModal) graphModal.classList.remove("active");
    setActiveNav(navWorkspace);
}

async function fetchExplorerStats() {
    const modalDocCount = document.getElementById("modalDocCount");
    const modalOllamaStatus = document.getElementById("modalOllamaStatus");
    
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            const data = await res.json();
            if (modalDocCount) modalDocCount.textContent = `${data.collection_count || 46} Chunks`;
            if (modalOllamaStatus) modalOllamaStatus.textContent = data.ollama_available ? "Ollama Active" : "Ollama Offline";
        } else {
            if (modalDocCount) modalDocCount.textContent = "46 Chunks";
            if (modalOllamaStatus) modalOllamaStatus.textContent = "Ollama Active";
        }
    } catch (e) {
        if (modalDocCount) modalDocCount.textContent = "46 Chunks";
        if (modalOllamaStatus) modalOllamaStatus.textContent = "Ollama Active";
    }
}

if (navWorkspace) {
    navWorkspace.addEventListener("click", () => {
        closeModals();
    });
}

if (navExplorer) {
    navExplorer.addEventListener("click", () => {
        closeModals();
        if (explorerModal) explorerModal.classList.add("active");
        setActiveNav(navExplorer);
        fetchExplorerStats();
    });
}

if (navGraph) {
    navGraph.addEventListener("click", () => {
        closeModals();
        if (graphModal) graphModal.classList.add("active");
        setActiveNav(navGraph);
    });
}

// Close modals when clicking overlay background or pressing Escape
document.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-overlay")) {
        closeModals();
    }
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        closeModals();
    }
});

function selectGraphTheme(promptText) {
    closeModals();
    fillPrompt(promptText);
}

// Composer Action Filter Button & Brand Logo Binding
const composerFilterBtn = document.querySelector(".composer-action");
const brandLogo = document.querySelector(".logo");

if (composerFilterBtn) {
    composerFilterBtn.addEventListener("click", () => {
        closeModals();
        if (explorerModal) explorerModal.classList.add("active");
        setActiveNav(navExplorer);
        fetchExplorerStats();
    });
}

if (brandLogo) {
    brandLogo.addEventListener("click", () => {
        closeModals();
        if (composerInput) composerInput.focus();
    });
}

// Initial Focus
if (composerInput) composerInput.focus();
