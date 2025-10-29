import streamlit as st
from auth.rbac_utils import require_role
from helperfunctions import word_generator

@require_role(['passenger', 'staff', 'supervisor', 'admin', 'analyst'])
def show():
    st.sidebar.markdown("\n\n\n")
    st.markdown('<h1 class="gradient-text">Rail Madad AI Assitant</h1>', unsafe_allow_html=True)
    st.markdown("<hr class='gradient-line' />", unsafe_allow_html=True)
    st.sidebar.image("aibot.png")
    st.sidebar.markdown("\n\n\n")
    st.sidebar.write("Namaste 🙏, I am the Rail madad AI chatbot. Ask me any questions about Indian Railways and i will give you real time info for all of them. Thank you.")
    
    for msg in st.session_state['messages']: 
         with st.chat_message(msg["role"]):
              st.write(msg["content"]) 

    # Lazy import crew only when secrets are available
    gemini_key = None
    try:
        gemini_key = st.secrets['api_keys']['GEMINI_API_KEY']
    except Exception:
        import os
        gemini_key = os.getenv('GEMINI_API_KEY')

    if not gemini_key:
        st.info("🔧 LiveChat requires GEMINI_API_KEY. Add it to `.streamlit/secrets.toml` or environment to enable chat.")
        return

    from main import chatcrew

    prompt = st.chat_input("Ask anything about Indian railways...")
    if prompt: 
        with st.chat_message("user"):
            st.write(prompt)

        inputs = {'prompt': prompt, 'history': st.session_state['messages'][:-4]} 
        response = chatcrew.kickoff(inputs = inputs)

        st.session_state['messages'].append({"role":"user","content": prompt})
        with st.chat_message("assistant"):
            st.write_stream(word_generator(response.raw))
        st.session_state['messages'].append({"role": "assistant", "content": response.raw})

if __name__ == "__main__":
    show()
