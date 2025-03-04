import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


zhipu = ChatOpenAI(
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
    openai_api_key="78f1955b1b81b0276b2a4eec8f27d0b5.QxwaZBjMJYg9VTCJ",
    model_name="glm-4-plus",
)
propositions = [
    "感冒时需要多喝水，大量喝水可以增加人的血容量，稀释病毒或者细菌的浓度，从而帮助身体好得更快。",
    "空调开26℃是最合适的。",
    "腐乳是通过发酵制作而成，发酵过程中会生出霉菌，食用存在致癌风险。",
    "最好把手机的屏保、电脑的屏保全部改成绿色，因为绿色能缓解眼睛疲劳，保护视力。",
]
## 页面变量设置
st.set_page_config(page_title="科学事实核查调研Demo-V2", page_icon="🧐")
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
    # if "block6_submitted" not in st.session_state:
    #     st.session_state.block6_submitted = False
    # if "block7_submitted" not in st.session_state:
    #     st.session_state.block7_submitted = False
    # if "block8_submitted" not in st.session_state:
    #     st.session_state.block8_submitted = False
    # if "block9_submitted" not in st.session_state:
    #     st.session_state.block9_submitted = False
    # if "block10_submitted" not in st.session_state:
    #     st.session_state.block10_submitted = False
    # if "block11_submitted" not in st.session_state:
    #     st.session_state.block11_submitted = False
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
        st.title("科学事实核查调研")
        st.markdown(
            """
    您好！我们是北京师范大学新闻传播学院的研究团队，目前正在开展一项关于科学信息事实核查的学术研究。
    诚挚邀请您参与填写本调查问卷。

    本问卷旨在了解人们在事实核查中的行为和看法，请您按照问卷详细指引，根据实际情况回答以下问题。

    **本问卷的回答没有对错之分，也不涉及任何价值判断，请放心填写。**

    **所有数据仅用于学术研究，您的回答将被严格保密，不会用于商业或其他非研究用途。**

    我们深知您的时间宝贵，非常感谢您抽出时间参与本次调查。
    完成调查后，您将获得2元答谢金（若中途退出或未通过注意力检测，将无法发放）。
    您的意见对我们的研究至关重要，并将为事实核查领域的进一步探索提供重要支持。
    再次感谢您的参与与信任！

    祝您生活愉快！
    """
        )
        ## 知情同意
        st.radio(
            "**你是否同意参加本研究并允许我们使用您的匿名答卷？**",
            [
                "是的，我同意",
                "不，我不同意",
            ],
            key="consent",
            label_visibility="visible",
            index=None,
            horizontal=True,
        )
        agree = st.session_state.consent == "是的，我同意"
        disagree = st.session_state.consent == "不，我不同意"
        ## 同意后显示开始按钮
        if agree:
            st.markdown("点击**开始**按钮以进入调研")
            ## 当开始按钮被点击，令页数 +1
            st.button("开始", on_click=goToNextPage)
## Block1 对人工智能情感态度
elif st.session_state.page_num == 1:
    st.session_state.data_dict["StartAt"] = pd.Timestamp.now()
    ## 清空容器，即清除 cover letter
    placeholder.empty()
    with placeholder.container():
        with st.form("block1"):
            st.write("请根据您对下面陈述的真实看法，选择最符合您当前想法的选项。")
            ## Q1
            st.select_slider(
                "当我想到将来接触人工智能时，我会感到不适。",
                options=[
                    "非常不同意",
                    "有点不同意",
                    "很难说同意或不同意",
                    "有点同意",
                    "非常同意",
                ],
                key="q1",
                # label_visibility="visible",
                # index=None,
                # horizontal=True,
            )
            ## Q2
            st.select_slider(
                "人工智能令人兴奋。",
                options=[
                    "非常不同意",
                    "有点不同意",
                    "很难说同意或不同意",
                    "有点同意",
                    "非常同意",
                ],
                key="q2",
            )

            ## Q3
            st.select_slider(
                "我对人工智能会做什么感到印象深刻。",
                options=[
                    "非常不同意",
                    "有点不同意",
                    "很难说同意或不同意",
                    "有点同意",
                    "非常同意",
                ],
                key="q3",
            )

            ## Q4
            st.select_slider(
                "人工智能帮助我感到更快乐。",
                options=[
                    "非常不同意",
                    "有点不同意",
                    "很难说同意或不同意",
                    "有点同意",
                    "非常同意",
                ],
                key="q4",
            )

            submitted = st.form_submit_button("提交本页")
            if submitted:
                st.session_state.data_dict["q1"] = st.session_state.q1
                st.session_state.data_dict["q2"] = st.session_state.q2
                st.session_state.data_dict["q3"] = st.session_state.q3
                st.session_state.data_dict["q4"] = st.session_state.q4
                st.session_state.block1_submitted = True
                st.markdown("提交成功，请点击**下一页**")
        if st.session_state.block1_submitted == True:
            st.button("下一页", on_click=goToNextPage)
## Block2 对人工智能行为倾向
elif st.session_state.page_num == 2:
    placeholder.empty()
    with placeholder.container():
        with st.form("block2"):
            st.write("请根据您对下面陈述的真实看法，选择最符合您当前想法的选项。")
            ## Q5
            st.select_slider(
                "对于日常交易，我宁愿和人工智能系统交互，而不是和人。",
                options=[
                    "非常不同意",
                    "有点不同意",
                    "很难说同意或不同意",
                    "有点同意",
                    "非常同意",
                ],
                key="q5",
            )
            ## Q6
            st.select_slider(
                "我对在日常生活中使用人工智能系统感兴趣。",
                options=[
                    "非常不同意",
                    "有点不同意",
                    "很难说同意或不同意",
                    "有点同意",
                    "非常同意",
                ],
                key="q6",
            )
            ## Q7
            st.select_slider(
                "我愿意在自己的工作中接触人工智能。",
                options=[
                    "非常不同意",
                    "有点不同意",
                    "很难说同意或不同意",
                    "有点同意",
                    "非常同意",
                ],
                key="q7",
            )
            submitted = st.form_submit_button("提交本页")
            if submitted:
                st.session_state.data_dict["q5"] = st.session_state.q5
                st.session_state.data_dict["q6"] = st.session_state.q6
                st.session_state.data_dict["q7"] = st.session_state.q7
                st.session_state.block2_submitted = True
                st.markdown("提交成功，请点击**下一页**")
        if st.session_state.block2_submitted == True:
            st.button("下一页", on_click=goToNextPage)
## Block3 人工智能知识
elif st.session_state.page_num == 3:
    placeholder.empty()
    with placeholder.container():
        with st.form("block3"):
            st.markdown("请根据您对AI的了解，完成以下6道**单选题**")
            ## Q8
            st.radio(
                "思考一下客户服务，以下哪项使用了人工智能（AI）？",
                [
                    "详细的常见问题网页",
                    "发送给客户的在线调查，允许客户提供反馈",
                    "提供表单供客户提供反馈的联系页面",
                    "一个即时回答客户问题的聊天机器人",
                    "不确定",
                ],
                key="q8",
                index=None,
            )
            ## Q9
            st.radio(
                "在播放音乐时，以下哪项使用了人工智能（AI）？",
                [
                    "使用蓝牙连接到无线扬声器",
                    "播放列表推荐",
                    "无线互联网连接用于流媒体播放音乐",
                    "从选定的播放列表中随机播放",
                    "不确定",
                ],
                key="q9",
                index=None,
            )
            ## Q10
            st.radio(
                "在使用电子邮件时，以下哪项使用了人工智能（AI）？",
                [
                    "电子邮件服务在用户打开后将电子邮件标记为已读",
                    "电子邮件服务允许用户安排电子邮件在未来特定时间发送",
                    "电子邮件服务将邮件分类为垃圾邮件",
                    "电子邮件服务按时间和日期排序邮件",
                    "不确定",
                ],
                key="q10",
                index=None,
            )
            ## Q11
            st.radio(
                "思考一下健康产品，以下哪项使用了人工智能（AI）？",
                [
                    "分析运动和睡眠模式的可穿戴健身追踪器",
                    "放在某人舌下的温度计，用于检测发热",
                    "居家新冠检测",
                    "测量血氧水平的脉搏血氧仪",
                    "不确定",
                ],
                key="q11",
                index=None,
            )
            ## Q12
            st.radio(
                "思考一下在线购物，以下哪项使用了人工智能（AI）？",
                [
                    "存储账户信息，如送货地址",
                    "之前购买记录",
                    "基于之前购买记录的产品推荐",
                    "其他客户的产品评论",
                    "不确定",
                ],
                key="q12",
                index=None,
            )
            ## Q13
            st.radio(
                "思考一下家用设备，以下哪项使用了人工智能（AI）？",
                [
                    "编程家庭温控器在特定时间改变温度",
                    "当门口有陌生人时，发出警报的安全摄像头",
                    "编程定时器控制家中的灯何时开关",
                    "当水过滤器需要更换时，指示灯变红",
                    "不确定",
                ],
                key="q13",
                index=None,
            )
            submitted = st.form_submit_button("提交本页")
            if submitted:
                st.session_state.data_dict["q8"] = st.session_state.q8
                st.session_state.data_dict["q9"] = st.session_state.q9
                st.session_state.data_dict["q10"] = st.session_state.q10
                st.session_state.data_dict["q11"] = st.session_state.q11
                st.session_state.data_dict["q12"] = st.session_state.q12
                st.session_state.data_dict["q13"] = st.session_state.q13
                st.session_state.block3_submitted = True
                st.markdown("提交成功，请点击**下一页**")
        if st.session_state.block3_submitted == True:
            st.button("下一页", on_click=goToNextPage)
## Block 4 LLM 对话 1 前测
elif st.session_state.page_num == 4:
    placeholder.empty()
    with placeholder.container():
        with st.form("block4"):
            st.write("请根据你的知识储备，判断以下命题的真假")
            st.markdown(f"**{propositions[0]}**")
            ## Q14
            st.radio("该命题是：", options=["真命题", "假命题"], key="q14", index=None)
            submitted = st.form_submit_button("提交本页")
            if submitted:
                st.session_state.data_dict["q14"] = st.session_state.q14
                st.session_state.block4_submitted = True
                st.markdown("提交成功，请点击**下一页**")
        if st.session_state.block4_submitted == True:
            st.button("下一页", on_click=goToNextPage)
## Block 5 LLM 对话 1 后测
elif st.session_state.page_num == 5:

    def disable_callback1():
        st.session_state.chat_disabled1 = True

    placeholder.empty()

    with placeholder.container():
        st.write(
            "接下来，你有3次与AI对话的机会。请向AI提出与命题相关的问题。3次机会用尽后判断命题真假。命题为："
        )
        st.markdown(f"**{propositions[0]}**")
        ## 显示聊天历史
        for message in st.session_state.messages1:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if st.session_state.chat_num1 >= 2:
            st.session_state.chat_disabled1 = True
        user_input = st.chat_input(
            f"还可以输入{2-st.session_state.chat_num1}次，请输入...",
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
                st.write("请根据你的知识储备及与AI的对话，判断命题的真假")
                ## Q15
                st.radio(
                    "该命题是：", options=["真命题", "假命题"], key="q15", index=None
                )
                submitted = st.form_submit_button("提交本页")
                if submitted:
                    st.session_state.data_dict["q15"] = st.session_state.q15
                    st.session_state.data_dict["dialog1"] = st.session_state.messages1
                    st.session_state.block5_submitted = True
                    st.markdown("提交成功，请点击**下一页**")
            if st.session_state.block5_submitted == True:
                st.button("下一页", on_click=goToNextPage)
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

    def disable_callback4():
        st.session_state.chat_disabled4 = True

    placeholder.empty()

    with placeholder.container():
        st.write(
            "接下来，你有3次与AI对话的机会。请向AI提出与命题相关的问题。3次机会用尽后判断命题真假。命题为："
        )
        st.markdown(f"**{propositions[3]}**")
        ## 显示聊天历史
        for message in st.session_state.messages4:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if st.session_state.chat_num4 >= 3:
            st.session_state.chat_disabled4 = True
        user_input = st.chat_input(
            f"还可以输入{3-st.session_state.chat_num4}次，请输入...",
            disabled=st.session_state.chat_disabled4,
            on_submit=disable_callback4,
        )
        if user_input:
            ## 显示用户消息
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.chat_num4 += 1
            ## 将用户消息添加到聊天历史
            st.session_state.messages4.append({"role": "user", "content": user_input})

            ## 显示助手回应
            with st.chat_message("assistant"):
                response = st.write_stream(get_response(st.session_state.messages4))
            ## 将助手回应添加到聊天历史
            st.session_state.messages4.append(
                {"role": "assistant", "content": response}
            )
            st.session_state.chat_disabled4 = False
            st.rerun()
        if st.session_state.chat_num4 >= 3:
            with st.form("block11"):
                st.write("请根据你的知识储备及与AI的对话，判断命题的真假")
                ## Q21
                st.radio(
                    "该命题是：", options=["真命题", "假命题"], key="q21", index=None
                )
                submitted = st.form_submit_button("提交本页")
                if submitted:
                    st.session_state.data_dict["q21"] = st.session_state.q21
                    st.session_state.data_dict["dialog4"] = st.session_state.messages4
                    st.session_state.block11_submitted = True
                    st.markdown("提交成功，请点击**下一页**")
            if st.session_state.block11_submitted == True:
                st.button("下一页", on_click=goToNextPage)
## Block 12 人口统计学
elif st.session_state.page_num == 12:
    placeholder.empty()

    with placeholder.container():
        with st.form("block12"):
            ## Q22
            st.radio(
                "您的性别是？", ["男", "女"], key="q22", index=None, horizontal=True
            )
            ## Q23
            st.text_input("您的出生年份是？", key="q23")
            ## Q24
            st.radio(
                "您的学历是？",
                ["小学及以下", "初中", "高中", "大学专科", "大学本科及以上"],
                key="q24",
                index=None,
            )
            ## Q25
            st.text_input(
                "您每月的可支配金额大约是？【以人民币（元）为单位，例如1000元则填写1000】",
                key="q25",
            )
            submitted = st.form_submit_button("提交本页")
            if submitted:
                st.session_state.data_dict["q22"] = st.session_state.q22
                st.session_state.data_dict["q23"] = st.session_state.q23
                st.session_state.data_dict["q24"] = st.session_state.q24
                st.session_state.data_dict["q25"] = st.session_state.q25
                st.session_state.block12_submitted = True
                st.markdown("提交成功，请点击**下一页**")
        if st.session_state.block12_submitted == True:
            st.button("下一页", on_click=goToNextPage)
## 最后一页
else:
    st.session_state.data_dict["endAt"] = pd.Timestamp.now()
    placeholder.empty()
    with placeholder.container():
        st.markdown(
            """
感谢您的参与，下面揭晓问题的答案：

陈述一：感冒时要多喝水，大量喝水可以增加人的血容量，稀释病毒或者细菌的浓度，从而帮助身体好得更快。

（假）多喝水治不了感冒，水喝得过多可能还会造成身体脱水。感冒时，人体会通过发烧来对抗病毒，这个过程会使体内的水分大量流失，同时也会带走钠、钾等电解质成分。这时如果只是大量补充白开水，会将体内钠、钾等电解质元素冲淡。当体内钠元素浓度下降过多，人会出现眩晕、乏力等情况。此时，大脑会自动发出信号，通过尿液、汗液等方式排出体内多余的水分，以满足体内电解质浓度平衡的需要。所以，感冒不能一味地大量喝水，在喝水的同时还要补充足够的电解质，才能帮助缓解感冒症状。

陈述二：空调开26℃是最合适的。

（假）但是温度设高一点会更省电。因为空调最适合的温度，与人体感受，及室内外环境的温度、湿度、墙体导热、日光照射、室内的动态变化等因素相关，在大型建筑中空调温度会动态调整来节能减排。一般家庭设置在26-30℃都是可以的。空调耗电量则与所在地区温度，湿度，风速等气象条件，空调自身能效水平，使用的制冷剂，空调的结构等均有关系，设定温度上升一度，带来的影响不一定相同，但很多实验都表明，总的趋势仍然是“调高一度，省电一点”。

陈述三：腐乳是通过发酵制作而成，发酵过程中会生出霉菌，食用存在致癌风险。

（假）这个观点不正确，正常食用腐乳不会致癌。腐乳在制作过程中确实需要经过霉菌发酵，其中以毛霉菌为主，也包括少量的经过特定方法严选的酵母菌、曲霉、青霉，但这些都是经过严选的有益食用菌，不会产生致癌物。再者，大豆中的亚硝酸盐非常低，即使长达几个月的发酵也不会带来大量的亚硝酸盐。因此，不能把腐乳和盐、腌菜等混为一谈。此外，豆腐乳发酵过程中使用的红曲色素也是一种天然色素，对人体十分安全。毛霉和红曲也均不在世界卫生组织发布的致癌物质清单中。所以，腐乳致癌一说纯属危言耸听！

陈述四：最好把手机的屏保、电脑的屏保全部改成绿色，因为绿色能缓解眼睛疲劳，保护视力。

（假）这是个误会，严格意义来说看绿色和保护视力没有什么关系。对眼疲劳影响最大的是看屏幕的距离和时间长短，即便是把屏幕设置成了绿色，看的时间过长，眼睛还是会干涩、疲劳。绿色光线比较柔和，相对刺激较小，同时绿色能够让人感到舒服与平静，所以大家会觉得绿色屏幕看起来会更舒服，但它对保护眼睛的帮助较为有限，特别是当近距离视物时。“多看看绿色对眼睛有好处”通常是指多看看远处草地、树木之类的景物，让眼睛放松，从而缓解视疲劳。
"""
        )
        ## 用于测试
        st.write(st.session_state.data_dict)
        # todo 正式部署需替换为数据库插入

# todo 提交按钮前的检测功能，填答完整才可提交
# todo 作答前的身份验证功能，被试必须填入预先发放的作答ID才可作答，作答ID在完整作答后将被标记为无法使用（防止被恶意注入）
# todo LLM 对话功能
# todo 命题常识性的问卷另做一份
