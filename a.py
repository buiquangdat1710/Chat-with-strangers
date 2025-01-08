import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as com

com.iframe("https://lottie.host/embed/93f9466d-a267-4078-ad98-a29abbdc8844/sFVT8gWDzp.json")

page_bg_img = '''
<style>
html, body, .stApp {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.stApp {
  background-image: url("https://wpamelia.com/wp-content/uploads/2019/02/7644.jpg");
  background-size: cover;
  background-position: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


st.title("Chat with strangers")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:  # Chỉ hiển thị "user" và "assistant"
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    response = "Bạn là một người lạ nóng giận và luôn có từ mày tao trong câu nói, lúc nào cũng chửi thề, có cái tôi cao , không có ý định giúp đỡ người khác. Nói chuyện nghe rất mất dạy, đời thường. Có thể thêm một số câu chửi bậy như kiểu: đéo, đcm, đm, đcmm, vãi. Dùng emoij với tần suất thấp. Trả lời ngắn ngọn, bố đời, bố láo."
    st.session_state.messages.append({"role": "developer", "content": response})
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages 
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
