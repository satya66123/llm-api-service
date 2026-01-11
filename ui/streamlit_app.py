import json
import time
import requests
import streamlit as st

st.set_page_config(page_title="LLM API Service UI", layout="wide")

st.title("🧠 LLM API Service UI")
st.caption("Streamlit UI client for FastAPI backend (Project 2 - LLM)")

# -----------------------------
# Helpers
# -----------------------------
def safe_get_json(url: str, timeout: int = 10):
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code, r.json()
    except Exception as e:
        return 0, {"error": str(e)}

def safe_post_json(url: str, payload: dict, timeout: int = 60):
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, {"raw": r.text}
    except Exception as e:
        return 0, {"error": str(e)}

def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []  # list of dicts
    if "api_url" not in st.session_state:
        st.session_state.api_url = "http://127.0.0.1:8000"
    if "last_output" not in st.session_state:
        st.session_state.last_output = ""
    if "last_prompts" not in st.session_state:
        st.session_state.last_prompts = {"system": "", "user": ""}

init_state()

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    api_base_url = st.text_input("API Base URL", value=st.session_state.api_url)
    st.session_state.api_url = api_base_url

    status_url = f"{api_base_url}/api/v1/status"
    code, status_data = safe_get_json(status_url)

    st.subheader("🔎 Backend Status")
    if code == 200:
        st.success("Backend connected ✅")
        st.write(f"**Service:** {status_data.get('service')}")
        st.write(f"**Env:** {status_data.get('env')}")
        st.write(f"**Model:** {status_data.get('model')}")
        st.metric("Cache Size", status_data.get("cache_size", 0))
        templates = status_data.get("templates", ["basic_chat_v1", "summarize_v1"])
    else:
        st.error("Backend not reachable ❌")
        st.caption("Make sure FastAPI server is running")
        st.json(status_data)
        templates = ["basic_chat_v1", "summarize_v1"]

    st.divider()

    st.subheader("🕘 History Controls")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 Clear History"):
            st.session_state.history = []
            st.success("History cleared ✅")
    with col_b:
        if st.button("🔄 Refresh Status"):
            st.rerun()

    st.caption("History stores only in browser session.")

    # Export history JSON
    st.divider()
    st.subheader("📤 Export")
    history_json = json.dumps(st.session_state.history, indent=2)
    st.download_button(
        "⬇️ Download History (JSON)",
        data=history_json,
        file_name="llm_api_history.json",
        mime="application/json",
    )

# -----------------------------
# Main Layout (two columns)
# -----------------------------
left, right = st.columns([1.15, 0.85], gap="large")

# -----------------------------
# LEFT: Input Form
# -----------------------------
with left:
    st.subheader("📩 Generate Request")

    template_id = st.selectbox("Template ID", templates)

    tone = st.selectbox("Tone (used in basic_chat_v1)", ["neutral", "simple", "professional"])

    user_input = st.text_area(
        "Input",
        value="Give 3 points why FastAPI is popular",
        height=170
    )

    # Parameters JSON
    with st.expander("Advanced Parameters (JSON)", expanded=False):
        param_text = st.text_area(
            "parameters JSON",
            value=json.dumps({"tone": tone}, indent=2),
            height=120
        )
        try:
            advanced_params = json.loads(param_text)
            st.success("Valid JSON ✅")
        except Exception as e:
            advanced_params = None
            st.error(f"Invalid JSON ❌: {e}")

    payload = {
        "template_id": template_id,
        "input": user_input,
        "parameters": advanced_params if advanced_params is not None else {"tone": tone},
    }

    st.write("### Request Payload")
    st.code(json.dumps(payload, indent=2), language="json")

    generate_btn = st.button("🚀 Generate", type="primary")

    if generate_btn:
        endpoint = f"{api_base_url}/api/v1/generate"
        start = time.time()

        with st.spinner("Calling FastAPI backend..."):
            status_code, resp_data = safe_post_json(endpoint, payload)

        elapsed_ms = int((time.time() - start) * 1000)

        st.write("### Response Status")
        st.code(f"{status_code} (took {elapsed_ms} ms)")

        if status_code != 200:
            st.error("Request failed ❌")
            st.json(resp_data)

        else:
            st.success("Generated Successfully ✅")

            # Save last prompts + output for copy/download
            st.session_state.last_output = resp_data.get("output", "") or ""
            st.session_state.last_prompts = {
                "system": resp_data.get("system_prompt", "") or "",
                "user": resp_data.get("user_prompt", "") or "",
            }

            # Save to history
            st.session_state.history.insert(
                0,
                {
                    "template_id": resp_data.get("template_id"),
                    "input": payload.get("input"),
                    "parameters": payload.get("parameters"),
                    "cached": resp_data.get("cached"),
                    "input_tokens": resp_data.get("input_tokens"),
                    "output_tokens": resp_data.get("output_tokens"),
                    "total_tokens": resp_data.get("total_tokens"),
                    "output": resp_data.get("output"),
                    "time_ms": elapsed_ms,
                    "request_id": resp_data.get("request_id"),
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                },
            )

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Cached", str(resp_data.get("cached", False)))
            col2.metric("Input Tokens", str(resp_data.get("input_tokens", 0)))
            col3.metric("Output Tokens", str(resp_data.get("output_tokens", 0)))
            col4.metric("Total Tokens", str(resp_data.get("total_tokens", 0)))

            st.write("### Output")
            st.write(resp_data.get("output", ""))

            # Download output as TXT
            st.download_button(
                "⬇️ Download Output (TXT)",
                data=resp_data.get("output", ""),
                file_name="llm_output.txt",
                mime="text/plain",
            )

            st.write("### Token Usage")
            st.json(
                {
                    "input_tokens": resp_data.get("input_tokens", 0),
                    "output_tokens": resp_data.get("output_tokens", 0),
                    "total_tokens": resp_data.get("total_tokens", 0),
                }
            )

            with st.expander("Prompts (debug)", expanded=False):
                st.write("**System Prompt**")
                st.code(resp_data.get("system_prompt", ""))
                st.write("**User Prompt**")
                st.code(resp_data.get("user_prompt", ""))

# -----------------------------
# RIGHT: History + Copy Actions
# -----------------------------
with right:
    st.subheader("📚 Response History")

    # Copy prompt buttons
    st.write("### 📋 Quick Copy")
    copy_col1, copy_col2 = st.columns(2)

    with copy_col1:
        st.text_area("Last System Prompt", value=st.session_state.last_prompts["system"], height=110)
        st.caption("Copy manually (CTRL+C)")

    with copy_col2:
        st.text_area("Last User Prompt", value=st.session_state.last_prompts["user"], height=110)
        st.caption("Copy manually (CTRL+C)")

    st.divider()

    if not st.session_state.history:
        st.info("No history yet. Click Generate to start ✅")
    else:
        for i, item in enumerate(st.session_state.history[:15], start=1):
            title = (
                f"{i}. [{item.get('created_at')}] "
                f"{item.get('template_id')} | cached={item.get('cached')} | tokens={item.get('total_tokens')}"
            )
            with st.expander(title, expanded=False):
                st.write(f"**Request ID:** `{item.get('request_id')}`")
                st.write(f"**Time:** {item.get('time_ms')} ms")

                st.write("**Input**")
                st.code(item.get("input", ""), language="text")

                st.write("**Parameters**")
                st.json(item.get("parameters", {}))

                st.write("**Output**")
                st.write(item.get("output", ""))

        st.caption("Showing latest 15 requests only.")
