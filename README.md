# nunchi.ai

**A practical tool designed to help remote Vietnamese engineers adapt to South Korean corporate culture.**

nunchi.ai helps remote Vietnamese software engineers navigate subtle communication expectations in South Korean corporate environments.

The project focuses on cultural interpretation, privacy-preserving AI assistance, and safe human escalation. It is designed for cross-border engineering teams where technical ability is not the main blocker, but communication style, hierarchy, indirect feedback, and unspoken expectations often create friction.

---

## The Problem

Remote development across borders often fails not because of coding skill, but because of communication mismatch.

In Vietnam-Korea collaborations, many problems come from unwritten communication rules. A short response like:

```text
Yes.
```

may be interpreted by one side as complete agreement and full understanding. However, it may actually mean:

```text
I heard you.
```

or:

```text
I do not want to disagree directly.
```

This difference can lead to:

- Misunderstood requirements.
- Missed deadlines.
- Silent blockers.
- Delayed escalation.
- Stress for remote engineers.
- Reduced trust between teams.

nunchi.ai helps engineers understand these unspoken expectations without fear of judgment.

---

## What is "Nunchi"?

**Nunchi** is a Korean concept often translated as the ability to read the room.

In a workplace context, it means understanding:

- What is said directly.
- What is implied indirectly.
- When to speak.
- How strongly to disagree.
- How to raise problems without damaging trust.
- How hierarchy affects communication.

nunchi.ai brings this cultural awareness into a practical developer tool.

---

## Core Features

- Physical NFC-based access point for remote engineers.
- Privacy filtering before data reaches external AI systems.
- Local retrieval of company communication guidelines.
- Interactive manager simulator for practice conversations.
- Voice-based roleplay for difficult workplace scenarios.
- Tone and phrasing feedback.
- Human peer handoff when stress or misunderstanding is detected.

---

## System Architecture

The system is divided into four major parts.

---

## Part 1: The Physical Anchor

Remote work can feel isolating. Engineers often interact only through screens, tickets, and chat messages.

To create a stronger connection between the physical workspace and the digital support system, nunchi.ai uses a physical NFC token placed on the engineer's desk.

### How it works

1. The engineer taps the NFC card.
2. The card opens a secure portal.
3. The portal authenticates the session.
4. The engineer can access the cultural support interface.

### Why this matters

The NFC card acts as a small physical ritual. It gives remote engineers a clear entry point into a support environment instead of making the tool feel like another browser tab or corporate dashboard.

---

## Part 2: Privacy and Context Filtering

Enterprise communication tools require strict data privacy. Engineers may paste messages, tickets, or workplace conversations into the system, so sensitive information must be filtered before any external model is called.

This layer works as a privacy gateway.

### Sensitive Data Redaction

The system removes sensitive data using regular expressions before sending content to the AI reasoning layer.

Examples of redacted data include:

- Email addresses.
- API keys.
- Database credentials.
- Access tokens.
- Internal URLs.
- Private identifiers.

Example:

```text
Before:
Please check the database at postgres://admin:password123@internal.company.com:5432/prod

After:
Please check the database at [REDACTED_DATABASE_CREDENTIAL]
```

### Local Cultural Context Retrieval

Corporate communication guidelines are stored in a local vector database.

The system retrieves relevant internal guidance before asking the AI model to respond. This helps the assistant give advice that matches the company's actual communication norms instead of producing generic cultural advice.

### Compliance Goals

The privacy layer is designed to support compliance with:

- South Korean PIPA.
- Vietnamese Decree 13.
- Internal enterprise data protection policies.

The goal is to minimize unnecessary data exposure while still giving useful communication support.

---

## Part 3: Interactive Manager Simulator

nunchi.ai is not designed as a normal chatbot.

Instead, it acts as an interactive workplace simulator trained to behave like a traditional South Korean manager. This allows engineers to safely practice difficult conversations before having them in the real workplace.

### Example Scenarios

Engineers can practice:

- Asking for a deadline extension.
- Raising a technical blocker.
- Clarifying ambiguous requirements.
- Disagreeing with a proposed approach.
- Explaining that a task is not feasible within the current timeline.
- Asking whether a request is urgent or only exploratory.
- Responding to indirect feedback.

### Hidden Meaning Explanation

The simulator can explain what a manager may actually mean behind common workplace phrases.

Example:

```text
Manager:
Please check this again when you have time.

Possible hidden meaning:
This may not be optional. The manager may expect you to review it soon, but is expressing the request indirectly.
```

### Voice-Based Practice

Engineers can use natural voice messages to practice real conversations.

The system processes audio input and provides feedback on:

- Tone.
- Directness.
- Formality.
- Clarity.
- Risk of sounding dismissive.
- Whether the response acknowledges hierarchy appropriately.
- Whether the message gives enough context for the manager.

---

## Part 4: The Human Network

Software cannot replace human empathy.

If the system detects signs of high stress, repeated misunderstanding, or a critical communication issue, it triggers a handoff to an assigned human peer.

### Handoff Conditions

A handoff may be triggered when:

- The engineer expresses high stress.
- The conversation involves a serious cultural misunderstanding.
- The engineer appears unsure how to respond to a manager.
- The issue may affect delivery timelines.
- The AI cannot provide safe or confident guidance.
- The situation requires human judgment.

### Human Peer Role

The assigned peer can help the engineer:

- Interpret the situation.
- Rewrite a message.
- Decide whether to escalate.
- Prepare for a live conversation.
- Understand expectations from the Korean team.
- Reduce emotional pressure.

---

## Technology Stack

### Backend

The backend is built with:

- Python 3.11.
- FastAPI.
- Async request handling.
- REST APIs for frontend communication.
- Webhook support for NFC and escalation events.

FastAPI is used to handle asynchronous data streams efficiently, especially for audio input, AI processing, and real-time user feedback.

---

### Retrieval Layer

Document retrieval is managed with:

- LangChain.
- ChromaDB.
- Local vector embeddings.

This layer stores and retrieves company-specific cultural guidelines, communication examples, and internal policies.

Example retrieved context:

```text
When requesting deadline changes, engineers should explain the reason, impact, and proposed alternative date.
```

---

### Reasoning Engine

The reasoning layer uses the Gemini API.

The model is instructed to return strict JSON output so the backend can parse responses reliably.

Example response structure:

```json
{
  "intent": "deadline_extension_practice",
  "risk_level": "medium",
  "cultural_context": "The message is too direct and may sound like refusal.",
  "suggested_response": "I understand the priority. I found one blocker that may affect the deadline. Could I share the details and propose an adjusted timeline?",
  "tone_feedback": {
    "directness": "medium",
    "politeness": "high",
    "clarity": "high"
  },
  "handoff_required": false
}
```

---

### Frontend

The frontend is built with:

- React.
- Tailwind CSS.
- Web Audio APIs.
- NFC interaction support where available.

The interface focuses on simplicity and low cognitive overhead. Engineers should be able to start a practice session quickly without navigating a complex dashboard.

---

## Example User Flow

### 1. Start Session

The engineer taps the NFC card on their desk.

```text
NFC card tapped
```

The secure portal opens.

---

### 2. Submit Workplace Situation

The engineer enters or speaks a message.

```text
My manager said: "Please check this again when you have time."
I am not sure if this is urgent.
```

---

### 3. Privacy Filtering

The system removes sensitive information.

```text
Sensitive information redacted successfully.
```

---

### 4. Context Retrieval

The retrieval layer searches local company guidelines for relevant communication norms.

```text
Retrieved context:
- Indirect requests from managers should usually be treated as expected action.
- If priority is unclear, ask politely with a proposed timeline.
```

---

### 5. AI Interpretation

The simulator explains the likely hidden meaning and recommends a response.

```text
This request may be more urgent than it sounds. The phrase "when you have time" can still imply that the manager expects follow-up soon.
```

Suggested response:

```text
Understood. I will review it today and share an update by the afternoon. If there is a specific priority or deadline, please let me know.
```

---

### 6. Human Handoff if Needed

If the situation appears stressful or high-risk, the system routes the conversation to a human peer.

```text
Human peer handoff triggered.
```

---

## Local Development Setup

### Prerequisites

Make sure the following are installed:

- Python 3.11+
- Node.js 18+
- npm or pnpm
- Gemini API key
- ChromaDB
- NFC-compatible device or NFC emulator
- Modern browser with microphone support

---

## Backend Installation

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend will run by default at:

```text
http://localhost:8000
```

---

## Frontend Installation

Install frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will run by default at:

```text
http://localhost:5173
```

---

## Environment Configuration

Create a `.env` file in the backend root directory.

```env
GEMINI_API_KEY=your-gemini-api-key

CHROMA_DB_PATH=./chroma
COMPANY_GUIDELINES_PATH=./data/company_guidelines

NFC_PORTAL_SECRET=your-secure-token
SESSION_SECRET=your-session-secret

FRONTEND_URL=http://localhost:5173
BACKEND_PORT=8000
```

For frontend configuration, create a `.env` file in the frontend root directory.

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_ENABLE_NFC=true
VITE_ENABLE_VOICE=true
```

---

## Suggested Repository Structure

```text
nunchi.ai/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes_nfc.py
│   │   │   ├── routes_simulator.py
│   │   │   └── routes_handoff.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── privacy/
│   │   │   ├── redactor.py
│   │   │   └── patterns.py
│   │   ├── retrieval/
│   │   │   ├── vector_store.py
│   │   │   └── guidelines_loader.py
│   │   ├── simulator/
│   │   │   ├── manager_agent.py
│   │   │   └── response_schema.py
│   │   └── handoff/
│   │       └── peer_router.py
│   └── data/
│       └── company_guidelines/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoiceRecorder.tsx
│   │   │   ├── ScenarioInput.tsx
│   │   │   └── FeedbackPanel.tsx
│   │   ├── pages/
│   │   │   └── SimulatorPage.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── main.tsx
│   └── tailwind.config.js
├── README.md
└── .gitignore
```

Adjust the structure based on the actual implementation.

---

## API Design

### Start NFC Session

```http
POST /api/nfc/session
```

Example response:

```json
{
  "session_id": "session_123",
  "status": "active",
  "portal_url": "http://localhost:5173/session/session_123"
}
```

---

### Submit Text Scenario

```http
POST /api/simulator/text
```

Example request:

```json
{
  "session_id": "session_123",
  "message": "My manager said I should check this again when I have time. Is it urgent?"
}
```

Example response:

```json
{
  "interpretation": "This may be an indirect request for timely follow-up.",
  "suggested_response": "Understood. I will review it today and share an update by the afternoon.",
  "tone_feedback": {
    "clarity": "high",
    "politeness": "high",
    "directness": "medium"
  },
  "handoff_required": false
}
```

---

### Submit Voice Scenario

```http
POST /api/simulator/audio
```

Expected input:

```text
multipart/form-data with audio file
```

Example response:

```json
{
  "transcript": "I need more time for this task because the requirement changed.",
  "feedback": "The message is clear, but it may sound too abrupt. Add acknowledgement and propose a concrete next step.",
  "suggested_response": "I understand the priority of this task. Because the requirement changed, I may need additional time to complete it properly. Could I share an updated timeline today?"
}
```

---

### Trigger Human Handoff

```http
POST /api/handoff
```

Example request:

```json
{
  "session_id": "session_123",
  "reason": "high_stress_detected",
  "summary": "Engineer is unsure how to respond to repeated indirect deadline pressure."
}
```

Example response:

```json
{
  "handoff_required": true,
  "assigned_peer": "peer_01",
  "status": "queued"
}
```

---

## Privacy and Security Notes

nunchi.ai should never send raw sensitive workplace data directly to an external AI model.

Recommended safeguards:

- Redact secrets before model calls.
- Keep company guidelines in a local vector database.
- Use strict output schemas for AI responses.
- Log only redacted text.
- Do not store raw audio longer than necessary.
- Encrypt session tokens.
- Use short-lived NFC session links.
- Add rate limiting to public endpoints.
- Keep `.env` files out of version control.

Add the following to `.gitignore`:

```gitignore
.env
.env.local
__pycache__/
*.pyc
node_modules/
dist/
chroma/
*.log
```

---

## Development Reflection

Building this project solo within a tight timeframe highlighted the importance of clear priorities.

### Focus on the Core System

A secure, functional pipeline is more valuable than a polished UI with no working backend.

The highest-priority path should be:

```text
Input -> Privacy Filter -> Context Retrieval -> AI Reasoning -> Structured Output -> User Feedback
```

Once this pipeline works, the UI can be improved incrementally.

### Plan for Team Dynamics

Building a product alone is demanding because one person must handle:

- Architecture.
- Backend implementation.
- Security.
- Frontend interface.
- AI prompting.
- Data schema design.
- Final presentation.

For future development, the project would benefit from clearer role separation across backend, frontend, AI, and product design.

---

## Future Improvements

Potential next steps:

- Add OAuth-based enterprise login.
- Add Slack or Microsoft Teams integration.
- Support multiple company communication profiles.
- Add Korean and Vietnamese bilingual response mode.
- Add analytics for recurring communication blockers.
- Improve stress detection with opt-in sentiment signals.
- Add admin dashboard for peer handoff routing.
- Add automated tests for redaction patterns.
- Add stricter schema validation with Pydantic.
- Add deployment support with Docker.

---
