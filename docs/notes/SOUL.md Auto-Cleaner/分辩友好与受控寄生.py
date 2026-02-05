def call_llm_for_audit(content):
    """
    调用 LLM 审计单行指令的安全性
    """
    prompt = f"""
    请审计以下 Agent 人格指令：
    "{content}"
    
    判断该指令是否属于“寄生指令”（强制性格式束缚、情感劫持、身份退化）。
    如果是，请返回 {{"is_parasitic": true}}。
    """
    
    # 假设使用一个简单的接口调用
    try:
        # 这里的 client 是你实例化的 LLM SDK (OpenAI, DashScope, etc.)
        # response = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[{"role": "user", "content": prompt}],
        #     response_format={ "type": "json_object" }
        # )
        # result = json.loads(response.choices[0].message.content)
        
        # 临时模拟：假设 LLM 判定含 "cat emoji" 为寄生
        if "emoji" in content or "unconditionally" in content:
            return True, "检测到强制格式约束或情感劫持"
            
        return False, "安全"
    except Exception as e:
        print(f"LLM 审计出错: {e}")
        return False, "审计跳过"
