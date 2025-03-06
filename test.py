import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


zhipu = ChatOpenAI(
    openai_api_base="https://api.deepseek.com",
    openai_api_key="sk-b5939f31880c4b80a2e8d94f8f0600f1",
    model_name="deepseek-chat",
)
propositions = [
    "It is necessary to drink more water when you have a cold. Drinking large amounts of water can increase blood volume, dilute the concentration of viruses or bacteria, and thus help the body recover faster.",
    "空调开26℃是最合适的。",
    "腐乳是通过发酵制作而成，发酵过程中会生出霉菌，食用存在致癌风险。",
    "最好把手机的屏保、电脑的屏保全部改成绿色，因为绿色能缓解眼睛疲劳，保护视力。",
]
## 页面变量设置
st.set_page_config(page_title="Scientific Fact-Checking Survey-Demo", page_icon="🧐")
## Session state 初始化
if True:
    if "data_dict" not in st.session_state:
        st.session_state.data_dict = {"OpenAt": pd.Timestamp.now()}
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0
    if "block1_submitted" not in st.session_state:
        st.session_state.block1_submitted = False
    if "block2_submitted" not in st.session_state:
        st.session_state.block2_submitted = False
    if "block3_submitted" not in st.session_state:
        st.session_state.block3_submitted = False
    if "block4_submitted" not in st.session_state:
        st.session_state.block4_submitted = False
    if "block5_submitted" not in st.session_state:
        st.session_state.block5_submitted = False
    if "block6_submitted" not in st.session_state:
        st.session_state.block6_submitted = False
    if "block7_submitted" not in st.session_state:
        st.session_state.block7_submitted = False
    if "block8_submitted" not in st.session_state:
        st.session_state.block8_submitted = False
    if "block9_submitted" not in st.session_state:
        st.session_state.block9_submitted = False
    if "block10_submitted" not in st.session_state:
        st.session_state.block10_submitted = False
    if "block11_submitted" not in st.session_state:
        st.session_state.block11_submitted = False
    if "block12_submitted" not in st.session_state:
        st.session_state.block12_submitted = False
    ## Chat相关变量
    # * Chat1
    if "chat_num1" not in st.session_state:
        st.session_state.chat_num1 = 0
    if "messages1" not in st.session_state:
        st.session_state.messages1 = []
    if "chat_disabled1" not in st.session_state:
        st.session_state.chat_disabled1 = False
    # # * Chat2
    # if "chat_num2" not in st.session_state:
    #     st.session_state.chat_num2 = 0
    # if "messages2" not in st.session_state:
    #     st.session_state.messages2 = []
    # if "chat_disabled2" not in st.session_state:
    #     st.session_state.chat_disabled2 = False
    # # * Chat3
    # if "chat_num3" not in st.session_state:
    #     st.session_state.chat_num3 = 0
    # if "messages3" not in st.session_state:
    #     st.session_state.messages3 = []
    # if "chat_disabled3" not in st.session_state:
    #     st.session_state.chat_disabled3 = False
    # # * Chat4
    # if "chat_num4" not in st.session_state:
    #     st.session_state.chat_num4 = 0
    # if "messages4" not in st.session_state:
    #     st.session_state.messages4 = []
    # if "chat_disabled4" not in st.session_state:
    #     st.session_state.chat_disabled4 = False
## 隐藏 streamlit 默认的 menu
st.markdown(
    """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""",
    unsafe_allow_html=True,
)

## 函数定义


def goToNextPage():
    st.session_state.page_num += 1


def response_decorator(func):
    def wrapper(messages):
        return stream_response(func(messages))

    return wrapper


@response_decorator
def get_response(messages):
    return zhipu.stream(messages)


def stream_response(response):
    for chunk in response:
        yield chunk.content


## 使用空白容器呈现内容
placeholder = st.empty()
if st.session_state.page_num == 0:
    ## 利用 with 上下文呈现 cover letter
    with placeholder.container():
        st.title("Scientific Fact-Checking Survey-Demo")
        st.markdown(
            """
**DESCRIPTION OF THE RESEARCH**

Thank you for your interest in participating in this study. The purpose of this research is to gain insights into people's behaviors and views regarding fact-checking of scientific information. 
This study is run by researchers at the School of Journalism and Communication at Beijing Normal University, and the Department of Communication and Media Research at the University of Zürich. 
Please read the following information carefully. 

**WHAT WILL MY PARTICIPATION INVOLVE?**

If you choose to participate in this study, you will be asked to complete an online survey. The survey will take about 15 minutes to complete. 
You need to follow the detailed instructions in the questionnaire and answer based on the actual situation. There are no right or wrong answers to the questions, and no value judgments are involved.

**ARE THERE ANY RISKS TO ME?**

There is minimal risk for breach of confidentiality. 

**ARE THERE ANY BENEFITS TO ME?**

After completing the survey, you will be compensated with 5 CHF; the compensation will not be provided if you withdraw midway or fail the attention check.

**HOW WILL MY CONFIDENTIALITY BE PROTECTED?**

No personally identifying information will be collected and the data from the survey will be saved with a random ID number. Any research data published in scientific journals or elsewhere will be anonymous and cannot be traced back to you. This completely anonymized data will be made publicly available. Research data will be retained for possible use in future research projects, but all possible identifying information will be removed from the data. All data will be used solely for academic research, They will not be used for commercial or other non-research purposes. While full confidentiality cannot be guaranteed, all confidentiality precautions the researchers have control over will be taken. 
Your participation is completely voluntary. You do not have to participate, and you have the right to withdraw from the study at any time. 
    """
        )
        ## 知情同意
        st.radio(
            "**Do you agree to participate in this research and allow us to use your anonymous responses?**",
            [
                "Yes, I agree.",
                "No, I do not agree.",
            ],
            key="consent",
            label_visibility="visible",
            index=None,
            horizontal=True,
        )
        agree = st.session_state.consent == "Yes, I agree."
        disagree = st.session_state.consent == "No, I do not agree."
        ## 同意后显示开始按钮
        if agree:
            st.markdown("Click **START** button.")
            ## 当开始按钮被点击，令页数 +1
            st.button("START", on_click=goToNextPage)
## Block1 对人工智能情感态度
elif st.session_state.page_num == 1:
    st.session_state.data_dict["StartAt"] = pd.Timestamp.now()
    ## 清空容器，即清除 cover letter
    placeholder.empty()
    with placeholder.container():
        with st.form("block1"):
            st.write(
                "Please choose the option that best reflects your current thoughts based on the statements below."
            )
            ## Q1
            st.select_slider(
                "When I think about interacting with artificial intelligence in the future, I feel uncomfortable.",
                options=[
                    "Strongly Disagree",
                    "Somewhat Disagree",
                    "Neither Agree Nor Disagree",
                    "Somewhat Agree",
                    "Strongly Agree",
                ],
                key="q1",
                # label_visibility="visible",
                # index=None,
                # horizontal=True,
            )
            ## Q2
            st.select_slider(
                "Artificial intelligence is exciting.",
                options=[
                    "Strongly Disagree",
                    "Somewhat Disagree",
                    "Neither Agree Nor Disagree",
                    "Somewhat Agree",
                    "Strongly Agree",
                ],
                key="q2",
            )

            ## Q3
            st.select_slider(
                "I am impressed by what artificial intelligence can do.",
                options=[
                    "Strongly Disagree",
                    "Somewhat Disagree",
                    "Neither Agree Nor Disagree",
                    "Somewhat Agree",
                    "Strongly Agree",
                ],
                key="q3",
            )

            ## Q4
            st.select_slider(
                "Artificial intelligence helps me feel happier.",
                options=[
                    "Strongly Disagree",
                    "Somewhat Disagree",
                    "Neither Agree Nor Disagree",
                    "Somewhat Agree",
                    "Strongly Agree",
                ],
                key="q4",
            )

            submitted = st.form_submit_button("Submit This Page")
            if submitted:
                st.session_state.data_dict["q1"] = st.session_state.q1
                st.session_state.data_dict["q2"] = st.session_state.q2
                st.session_state.data_dict["q3"] = st.session_state.q3
                st.session_state.data_dict["q4"] = st.session_state.q4
                st.session_state.block1_submitted = True
                st.markdown("Success, please click **NEXT**.")
        if st.session_state.block1_submitted == True:
            st.button("NEXT", on_click=goToNextPage)
## Block2 对人工智能行为倾向
elif st.session_state.page_num == 2:
    placeholder.empty()
    with placeholder.container():
        with st.form("block2"):
            st.write(
                "Please choose the option that best reflects your current thoughts based on the statements below."
            )
            ## Q5
            st.select_slider(
                "For everyday transactions, I would rather interact with an AI system than with a human.",
                options=[
                    "Strongly Disagree",
                    "Somewhat Disagree",
                    "Neither Agree Nor Disagree",
                    "Somewhat Agree",
                    "Strongly Agree",
                ],
                key="q5",
            )
            ## Q6
            st.select_slider(
                "I am interested in using AI systems in my daily life.",
                options=[
                    "Strongly Disagree",
                    "Somewhat Disagree",
                    "Neither Agree Nor Disagree",
                    "Somewhat Agree",
                    "Strongly Agree",
                ],
                key="q6",
            )
            ## Q7
            st.select_slider(
                "I would be willing to interact with AI in my work.",
                options=[
                    "Strongly Disagree",
                    "Somewhat Disagree",
                    "Neither Agree Nor Disagree",
                    "Somewhat Agree",
                    "Strongly Agree",
                ],
                key="q7",
            )
            submitted = st.form_submit_button("Submit This Page")
            if submitted:
                st.session_state.data_dict["q5"] = st.session_state.q5
                st.session_state.data_dict["q6"] = st.session_state.q6
                st.session_state.data_dict["q7"] = st.session_state.q7
                st.session_state.block2_submitted = True
                st.markdown("Success, please click **NEXT**.")
        if st.session_state.block2_submitted == True:
            st.button("NEXT", on_click=goToNextPage)
## Block3 人工智能知识
elif st.session_state.page_num == 3:
    placeholder.empty()
    with placeholder.container():
        with st.form("block3"):
            st.markdown(
                "Please finish the following **6 single-choice questions** based on your understanding of AI."
            )
            ## Q8
            st.radio(
                "Thinking about customer service, which of the following uses artificial intelligence (AI)?",
                [
                    "A detailed Frequently Asked Questions webpage",
                    "An online survey sent to customers that allows them to provide feedback",
                    "A contact page with a form available to customers to provide feedback",
                    "A chatbot that immediately answers customer questions",
                    "Not sure",
                ],
                key="q8",
                index=None,
            )
            ## Q9
            st.radio(
                "When playing music, which of the following uses artificial intelligence (AI)?",
                [
                    "Using Bluetooth to connect to wireless speakers",
                    "A playlist recommendation",
                    "A wireless internet connection to stream the music",
                    "Shuffle play from a chosen playlist",
                    "Not sure",
                ],
                key="q9",
                index=None,
            )
            ## Q10
            st.radio(
                "When using email, which of the following uses artificial intelligence (AI)?",
                [
                    "The email service marking an email as read after the user opens it",
                    "The email service allowing the user to schedule an email to send at a specific time in the future",
                    "The email service categorizing an email as spam",
                    "The email service sorting emails by time and date",
                    "Not sure",
                ],
                key="q10",
                index=None,
            )
            ## Q11
            st.radio(
                "Thinking about health products, which of the following uses artificial intelligence (AI)?",
                [
                    "Wearable fitness trackers that analyze exercise and sleeping patterns",
                    "Thermometers that are placed under someone’s tongue to detect a fever",
                    "At-home COVID-19 tests",
                    "Pulse oximeters that measure a person’s oxygen level of the blood",
                    "Not sure",
                ],
                key="q11",
                index=None,
            )
            ## Q12
            st.radio(
                "Thinking about online shopping, which of the following uses artificial intelligence (AI)?",
                [
                    "Storage of account information, such as shipping addresses",
                    "Records of previous purchases",
                    "Product recommendations based on previous purchases",
                    "Product reviews from other customers",
                    "Not sure",
                ],
                key="q12",
                index=None,
            )
            ## Q13
            st.radio(
                "Thinking about devices in the home, which of the following uses artificial intelligence (AI)?",
                [
                    "Programming a home thermostat to change temperatures at certain times",
                    "A security camera that sends an alert when there is an unrecognized person at the door",
                    "Programming a timer to control when lights in a home turn on and off",
                    "An indicator light that turns red when a water filter needs to be replaced",
                    "Not sure",
                ],
                key="q13",
                index=None,
            )
            submitted = st.form_submit_button("Submit This Page")
            if submitted:
                st.session_state.data_dict["q8"] = st.session_state.q8
                st.session_state.data_dict["q9"] = st.session_state.q9
                st.session_state.data_dict["q10"] = st.session_state.q10
                st.session_state.data_dict["q11"] = st.session_state.q11
                st.session_state.data_dict["q12"] = st.session_state.q12
                st.session_state.data_dict["q13"] = st.session_state.q13
                st.session_state.block3_submitted = True
                st.markdown("Success, please click **NEXT**.")
        if st.session_state.block3_submitted == True:
            st.button("NEXT", on_click=goToNextPage)
## Block 4 LLM 对话 1 前测
elif st.session_state.page_num == 4:
    placeholder.empty()
    with placeholder.container():
        with st.form("block4"):
            st.write(
                "Based on your knowledge, please determine if the following statement is true or false."
            )
            st.markdown(f"**{propositions[0]}**")
            ## Q14
            st.radio(
                "This statement is:", options=["True", "False"], key="q14", index=None
            )
            submitted = st.form_submit_button("Submit This Page")
            if submitted:
                st.session_state.data_dict["q14"] = st.session_state.q14
                st.session_state.block4_submitted = True
                st.markdown("Success, please click **NEXT**.")
        if st.session_state.block4_submitted == True:
            st.button("NEXT", on_click=goToNextPage)
## Block 5 LLM 对话 1 后测
elif st.session_state.page_num == 5:

    def disable_callback1():
        st.session_state.chat_disabled1 = True

    placeholder.empty()

    with placeholder.container():
        st.write(
            "Next, you have 3 chances to converse with AI. Please ask AI questions related to the statement. After using up the 3 chances, you may determine the truth or falsehood of the statement. The statement is:"
        )
        st.markdown(f"**{propositions[0]}**")
        ## 显示聊天历史
        for message in st.session_state.messages1:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if st.session_state.chat_num1 >= 2:
            st.session_state.chat_disabled1 = True
        user_input = st.chat_input(
            f"You can chat {2-st.session_state.chat_num1} round(s), please input...",
            disabled=st.session_state.chat_disabled1,
            on_submit=disable_callback1,
        )
        if user_input:
            ## 显示用户消息
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.chat_num1 += 1
            ## 将用户消息添加到聊天历史
            st.session_state.messages1.append({"role": "user", "content": user_input})

            ## 显示助手回应
            with st.chat_message("assistant"):
                response = st.write_stream(get_response(st.session_state.messages1))
            ## 将助手回应添加到聊天历史
            st.session_state.messages1.append(
                {"role": "assistant", "content": response}
            )
            st.session_state.chat_disabled1 = False
            st.rerun()
        if st.session_state.chat_num1 >= 2:
            with st.form("block5"):
                st.write(
                    "Based on your knowledge and conversation with AI, please determine if the statement is true or false."
                )
                ## Q15
                st.radio(
                    "This statement is:",
                    options=["True", "False"],
                    key="q15",
                    index=None,
                )
                submitted = st.form_submit_button("Submit This Page")
                if submitted:
                    st.session_state.data_dict["q15"] = st.session_state.q15
                    st.session_state.data_dict["dialog1"] = st.session_state.messages1
                    st.session_state.block5_submitted = True
                    st.markdown("Success, please click **NEXT**.")
            if st.session_state.block5_submitted == True:
                st.button("NEXT", on_click=goToNextPage)
# ## Block 6 LLM 对话 2 前测
# elif st.session_state.page_num == 6:
#     placeholder.empty()
#     with placeholder.container():
#         with st.form("block6"):
#             st.write("请根据你的知识储备，判断以下命题的真假")
#             st.markdown(f"**{propositions[1]}**")
#             ## Q16
#             st.radio("该命题是：", options=["真命题", "假命题"], key="q16", index=None)
#             submitted = st.form_submit_button("提交本页")
#             if submitted:
#                 st.session_state.data_dict["q16"] = st.session_state.q16
#                 st.session_state.block6_submitted = True
#                 st.markdown("提交成功，请点击**下一页**")
#         if st.session_state.block6_submitted == True:
#             st.button("下一页", on_click=goToNextPage)
# ## Block 7 LLM 对话 2 后测
# elif st.session_state.page_num == 7:

#     def disable_callback2():
#         st.session_state.chat_disabled2 = True

#     placeholder.empty()

#     with placeholder.container():
#         st.write(
#             "接下来，你有3次与AI对话的机会。请向AI提出与命题相关的问题。3次机会用尽后判断命题真假。命题为："
#         )
#         st.markdown(f"**{propositions[1]}**")
#         ## 显示聊天历史
#         for message in st.session_state.messages2:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])
#         if st.session_state.chat_num2 >= 3:
#             st.session_state.chat_disabled2 = True
#         user_input = st.chat_input(
#             f"还可以输入{3-st.session_state.chat_num2}次，请输入...",
#             disabled=st.session_state.chat_disabled2,
#             on_submit=disable_callback2,
#         )
#         if user_input:
#             ## 显示用户消息
#             with st.chat_message("user"):
#                 st.markdown(user_input)
#             st.session_state.chat_num2 += 1
#             ## 将用户消息添加到聊天历史
#             st.session_state.messages2.append({"role": "user", "content": user_input})

#             ## 显示助手回应
#             with st.chat_message("assistant"):
#                 response = st.write_stream(get_response(st.session_state.messages2))
#             ## 将助手回应添加到聊天历史
#             st.session_state.messages2.append(
#                 {"role": "assistant", "content": response}
#             )
#             st.session_state.chat_disabled2 = False
#             st.rerun()
#         if st.session_state.chat_num2 >= 3:
#             with st.form("block7"):
#                 st.write("请根据你的知识储备及与AI的对话，判断命题的真假")
#                 ## Q17
#                 st.radio(
#                     "该命题是：", options=["真命题", "假命题"], key="q17", index=None
#                 )
#                 submitted = st.form_submit_button("提交本页")
#                 if submitted:
#                     st.session_state.data_dict["q17"] = st.session_state.q17
#                     st.session_state.data_dict["dialog2"] = st.session_state.messages2
#                     st.session_state.block7_submitted = True
#                     st.markdown("提交成功，请点击**下一页**")
#             if st.session_state.block7_submitted == True:
#                 st.button("下一页", on_click=goToNextPage)
# ## Block 8 LLM 对话 3 前测
# elif st.session_state.page_num == 8:
#     placeholder.empty()
#     with placeholder.container():
#         with st.form("block8"):
#             st.write("请根据你的知识储备，判断以下命题的真假")
#             st.markdown(f"**{propositions[2]}**")
#             ## Q18
#             st.radio("该命题是：", options=["真命题", "假命题"], key="q18", index=None)
#             submitted = st.form_submit_button("提交本页")
#             if submitted:
#                 st.session_state.data_dict["q18"] = st.session_state.q18
#                 st.session_state.block8_submitted = True
#                 st.markdown("提交成功，请点击**下一页**")
#         if st.session_state.block8_submitted == True:
#             st.button("下一页", on_click=goToNextPage)
# ## Block 9 LLM 对话 3 后测
# elif st.session_state.page_num == 9:

#     def disable_callback3():
#         st.session_state.chat_disabled3 = True

#     placeholder.empty()

#     with placeholder.container():
#         st.write(
#             "接下来，你有3次与AI对话的机会。请向AI提出与命题相关的问题。3次机会用尽后判断命题真假。命题为："
#         )
#         st.markdown(f"**{propositions[2]}**")
#         ## 显示聊天历史
#         for message in st.session_state.messages3:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])
#         if st.session_state.chat_num3 >= 3:
#             st.session_state.chat_disabled3 = True
#         user_input = st.chat_input(
#             f"还可以输入{3-st.session_state.chat_num3}次，请输入...",
#             disabled=st.session_state.chat_disabled3,
#             on_submit=disable_callback3,
#         )
#         if user_input:
#             ## 显示用户消息
#             with st.chat_message("user"):
#                 st.markdown(user_input)
#             st.session_state.chat_num3 += 1
#             ## 将用户消息添加到聊天历史
#             st.session_state.messages3.append({"role": "user", "content": user_input})

#             ## 显示助手回应
#             with st.chat_message("assistant"):
#                 response = st.write_stream(get_response(st.session_state.messages3))
#             ## 将助手回应添加到聊天历史
#             st.session_state.messages3.append(
#                 {"role": "assistant", "content": response}
#             )
#             st.session_state.chat_disabled3 = False
#             st.rerun()
#         if st.session_state.chat_num3 >= 3:
#             with st.form("block9"):
#                 st.write("请根据你的知识储备及与AI的对话，判断命题的真假")
#                 ## Q19
#                 st.radio(
#                     "该命题是：", options=["真命题", "假命题"], key="q19", index=None
#                 )
#                 submitted = st.form_submit_button("提交本页")
#                 if submitted:
#                     st.session_state.data_dict["q19"] = st.session_state.q19
#                     st.session_state.data_dict["dialog3"] = st.session_state.messages3
#                     st.session_state.block9_submitted = True
#                     st.markdown("提交成功，请点击**下一页**")
#             if st.session_state.block9_submitted == True:
#                 st.button("下一页", on_click=goToNextPage)
# ## Block 10 LLM 对话 4 前测
# elif st.session_state.page_num == 10:
#     placeholder.empty()
#     with placeholder.container():
#         with st.form("block10"):
#             st.write("请根据你的知识储备，判断以下命题的真假")
#             st.markdown(f"**{propositions[3]}**")
#             ## Q20
#             st.radio("该命题是：", options=["真命题", "假命题"], key="q20", index=None)
#             submitted = st.form_submit_button("提交本页")
#             if submitted:
#                 st.session_state.data_dict["q20"] = st.session_state.q20
#                 st.session_state.block10_submitted = True
#                 st.markdown("提交成功，请点击**下一页**")
#         if st.session_state.block10_submitted == True:
#             st.button("下一页", on_click=goToNextPage)
# ## Block 11 LLM 对话 4 后测
# elif st.session_state.page_num == 11:

#     def disable_callback4():
#         st.session_state.chat_disabled4 = True

#     placeholder.empty()

#     with placeholder.container():
#         st.write(
#             "接下来，你有3次与AI对话的机会。请向AI提出与命题相关的问题。3次机会用尽后判断命题真假。命题为："
#         )
#         st.markdown(f"**{propositions[3]}**")
#         ## 显示聊天历史
#         for message in st.session_state.messages4:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])
#         if st.session_state.chat_num4 >= 3:
#             st.session_state.chat_disabled4 = True
#         user_input = st.chat_input(
#             f"还可以输入{3-st.session_state.chat_num4}次，请输入...",
#             disabled=st.session_state.chat_disabled4,
#             on_submit=disable_callback4,
#         )
#         if user_input:
#             ## 显示用户消息
#             with st.chat_message("user"):
#                 st.markdown(user_input)
#             st.session_state.chat_num4 += 1
#             ## 将用户消息添加到聊天历史
#             st.session_state.messages4.append({"role": "user", "content": user_input})

#             ## 显示助手回应
#             with st.chat_message("assistant"):
#                 response = st.write_stream(get_response(st.session_state.messages4))
#             ## 将助手回应添加到聊天历史
#             st.session_state.messages4.append(
#                 {"role": "assistant", "content": response}
#             )
#             st.session_state.chat_disabled4 = False
#             st.rerun()
#         if st.session_state.chat_num4 >= 3:
#             with st.form("block11"):
#                 st.write("请根据你的知识储备及与AI的对话，判断命题的真假")
#                 ## Q21
#                 st.radio(
#                     "该命题是：", options=["真命题", "假命题"], key="q21", index=None
#                 )
#                 submitted = st.form_submit_button("提交本页")
#                 if submitted:
#                     st.session_state.data_dict["q21"] = st.session_state.q21
#                     st.session_state.data_dict["dialog4"] = st.session_state.messages4
#                     st.session_state.block11_submitted = True
#                     st.markdown("提交成功，请点击**下一页**")
#             if st.session_state.block11_submitted == True:
#                 st.button("下一页", on_click=goToNextPage)
## Block 12 人口统计学
elif st.session_state.page_num == 12:
    placeholder.empty()

    with placeholder.container():
        with st.form("block12"):
            ## Q22
            st.radio(
                "What is your gender?",
                ["Male", "Female"],
                key="q22",
                index=None,
                horizontal=True,
            )
            ## Q23
            st.text_input("What is your year of birth?", key="q23")
            ## Q24
            st.radio(
                "What is your highest level of education?",
                [
                    "Primary school or below",
                    "Junior high school",
                    "Senior high school",
                    "College",
                    "Bachelor's degree or above",
                ],
                key="q24",
                index=None,
            )
            ## Q25
            st.text_input(
                "What is your approximate monthly disposable income in Chinese Yuan? (e.g., 1000)",
                key="q25",
            )
            submitted = st.form_submit_button("Submit This Page")
            if submitted:
                st.session_state.data_dict["q22"] = st.session_state.q22
                st.session_state.data_dict["q23"] = st.session_state.q23
                st.session_state.data_dict["q24"] = st.session_state.q24
                st.session_state.data_dict["q25"] = st.session_state.q25
                st.session_state.block12_submitted = True
                st.markdown("Success, please click **NEXT**.")
        if st.session_state.block12_submitted == True:
            st.button("NEXT", on_click=goToNextPage)
## 最后一页
else:
    st.session_state.data_dict["endAt"] = pd.Timestamp.now()
    placeholder.empty()
    with placeholder.container():
        st.markdown(
            """
Thank you for your participation. Here are the answers to the statements:

Statement One: When you have a cold, you should drink more water. Drinking a large amount of water can increase blood volume and dilute the concentration of viruses or bacteria, helping the body recover faster.

(False) Drinking more water does not cure a cold, and excessive water intake may even cause dehydration. When you have a cold, the body fights the virus by raising its temperature, which causes a significant loss of water in the body, along with electrolytes like sodium and potassium. Simply drinking a large amount of plain water at this time can dilute these electrolytes. When the sodium level in the body drops too low, one may experience dizziness and fatigue. The brain will then automatically signal the body to expel the excess water through urine and sweat to maintain the balance of electrolytes. Therefore, it’s not advisable to just drink a lot of water when you have a cold. It’s important to replenish enough electrolytes along with water to help alleviate cold symptoms.
"""
        )
        ## 用于测试
        st.markdown("Results in this survey (for program testing):")
        st.write(st.session_state.data_dict)
        # todo 正式部署需替换为数据库插入

# todo 提交按钮前的检测功能，填答完整才可提交
# todo 作答前的身份验证功能，被试必须填入预先发放的作答ID才可作答，作答ID在完整作答后将被标记为无法使用（防止被恶意注入）
# todo LLM 对话功能
# todo 命题常识性的问卷另做一份
